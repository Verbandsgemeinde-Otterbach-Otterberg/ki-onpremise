#!/usr/bin/env python3
"""Auth-Proxy vor Ollama.

Aufgaben:
  * verlangt ein Bearer-Token; ausgenommen ist nur die feste Adresse des Open-WebUI-Containers
  * lässt nur lesende und Inferenz-Endpunkte durch (kein pull, push, create, copy, delete)
  * gibt nur das aktuell freigegebene Chat-Modell und das Embedding-Modell frei
  * reicht Antworten ungepuffert durch, damit Token-Streaming erhalten bleibt
  * protokolliert Methode, Pfad, Modell und Status – niemals Inhalte von Anfragen

Konfiguration über Umgebungsvariablen (siehe /etc/llm-stack/llm-stack.env).
Nur Python-Standardbibliothek, keine zusätzlichen Pakete.
"""
import http.client
import ipaddress
import json
import os
import secrets
import socket
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit

UPSTREAM = urlsplit(os.environ.get("PROXY_UPSTREAM", "http://127.0.0.1:11434"))
TOKEN = os.environ.get("PROXY_TOKEN", "")
PORT = int(os.environ.get("PROXY_PORT", "11435"))
BIND = [a.strip() for a in os.environ.get("PROXY_BIND", "127.0.0.1").split(",") if a.strip()]
TRUSTED = [
    ipaddress.ip_network(a.strip())
    for a in os.environ.get("WEBUI_CONTAINER_IP", "").split(",")
    if a.strip()
]
ACTIVE_FILE = os.environ.get("ACTIVE_MODEL_FILE", "/opt/llm/active_model")
EMBED_MODELS = [m.strip() for m in os.environ.get("EMBED_MODEL", "").split(",") if m.strip()]
MAX_BODY = 32 * 1024 * 1024

# Endpunkte ohne Modellbezug, die gelesen werden dürfen
READ_ONLY = {("GET", "/"), ("HEAD", "/"), ("GET", "/api/version"), ("GET", "/api/ps")}
# Endpunkte, deren Modelliste gefiltert wird
MODEL_LISTS = {("GET", "/api/tags"): "models", ("GET", "/v1/models"): "data"}
# Endpunkte mit Modellangabe im JSON-Body
MODEL_CALLS = {
    "/api/chat", "/api/generate", "/api/embed", "/api/embeddings", "/api/show",
    "/v1/chat/completions", "/v1/completions", "/v1/embeddings",
}
HOP_BY_HOP = {"connection", "keep-alive", "transfer-encoding", "content-length",
              "proxy-authenticate", "proxy-authorization", "te", "trailers", "upgrade"}


def norm(name):
    """Vereinheitlicht Modellnamen: 'nomic-embed-text' entspricht 'nomic-embed-text:latest'."""
    name = (name or "").strip()
    return name if ":" in name else name + ":latest"


def allowed_models():
    try:
        with open(ACTIVE_FILE, encoding="utf-8") as f:
            active = [f.read().strip()]
    except OSError:
        active = []
    return {norm(m) for m in active + EMBED_MODELS if m}


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.0"  # Antwortende = Verbindungsende, ideal für Streaming
    server_version = "llm-proxy"
    sys_version = ""

    def log_message(self, fmt, *args):  # Standard-Log unterdrücken, eigenes Log in audit()
        pass

    def audit(self, status, model=""):
        print(f'{self.client_address[0]} {self.command} {self.path} {model or "-"} {status}',
              flush=True)

    def reply(self, status, payload):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def authorized(self):
        client = ipaddress.ip_address(self.client_address[0])
        if any(client in net for net in TRUSTED):
            return True
        header = self.headers.get("Authorization", "")
        return header.startswith("Bearer ") and secrets.compare_digest(header[7:], TOKEN)

    def upstream(self, body=None):
        headers = {k: v for k, v in self.headers.items()
                   if k.lower() not in HOP_BY_HOP | {"host", "authorization"}}
        conn = http.client.HTTPConnection(UPSTREAM.hostname, UPSTREAM.port or 80, timeout=900)
        conn.request(self.command, self.path, body=body, headers=headers)
        return conn, conn.getresponse()

    def handle_any(self):
        path = urlsplit(self.path).path.rstrip("/") or "/"
        key = (self.command, path)

        if not self.authorized():
            self.audit(401)
            return self.reply(401, {"error": "Token fehlt oder ist ungültig"})

        body, model = None, ""
        if key in READ_ONLY or key in MODEL_LISTS:
            pass
        elif self.command == "POST" and path in MODEL_CALLS:
            length = int(self.headers.get("Content-Length") or 0)
            if length <= 0 or length > MAX_BODY:
                self.audit(400)
                return self.reply(400, {"error": "Anfrage ohne gültigen Inhalt"})
            body = self.rfile.read(length)
            try:
                payload = json.loads(body)
                model = payload.get("model") or payload.get("name") or ""
            except (ValueError, AttributeError):
                self.audit(400)
                return self.reply(400, {"error": "Ungültiges JSON"})
            if norm(model) not in allowed_models():
                self.audit(403, model)
                return self.reply(403, {"error": f"Modell '{model}' ist nicht freigegeben"})
        else:
            self.audit(403)
            return self.reply(403, {"error": "Endpunkt über den Proxy nicht erlaubt"})

        try:
            conn, resp = self.upstream(body)
        except OSError as exc:
            self.audit(502, model)
            return self.reply(502, {"error": f"Ollama nicht erreichbar: {exc}"})

        try:
            if key in MODEL_LISTS and resp.status == 200:
                data = json.loads(resp.read())
                field = MODEL_LISTS[key]
                name_key = "name" if field == "models" else "id"
                allowed = allowed_models()
                data[field] = [m for m in data.get(field, []) if norm(m.get(name_key)) in allowed]
                self.audit(200)
                return self.reply(200, data)

            # Streaming: Antwort blockweise und ohne Pufferung weiterreichen
            self.send_response(resp.status)
            for k, v in resp.getheaders():
                if k.lower() not in HOP_BY_HOP:
                    self.send_header(k, v)
            self.send_header("Connection", "close")
            self.end_headers()
            self.connection.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            if self.command != "HEAD":
                while True:
                    chunk = resp.read1(65536)
                    if not chunk:
                        break
                    self.wfile.write(chunk)
                    self.wfile.flush()
            self.audit(resp.status, model)
        except (BrokenPipeError, ConnectionResetError):
            self.audit("abgebrochen", model)
        finally:
            conn.close()

    do_GET = do_POST = do_HEAD = do_PUT = do_DELETE = do_PATCH = handle_any


def main():
    if len(TOKEN) < 32:
        sys.exit("PROXY_TOKEN fehlt oder ist zu kurz (mindestens 32 Zeichen).")
    servers = []
    for addr in BIND:
        srv = ThreadingHTTPServer((addr, PORT), Handler)
        srv.daemon_threads = True
        servers.append(srv)
        print(f"llm-proxy lauscht auf {addr}:{PORT} -> {UPSTREAM.geturl()}", flush=True)
    threads = [threading.Thread(target=s.serve_forever, daemon=True) for s in servers]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
