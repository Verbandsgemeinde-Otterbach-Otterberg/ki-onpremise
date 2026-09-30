#!/usr/bin/env bash
# Schritt 2: Ollama als nativen systemd-Dienst installieren und konfigurieren.
# Nativ statt im Container: direkter GPU-Zugriff ohne NVIDIA-Container-Toolkit.
# shellcheck source=../lib.sh
. "$(dirname "$0")/../lib.sh"
require_root
load_conf
log "Schritt 2: Ollama"

nvidia-smi >/dev/null 2>&1 || die "NVIDIA-Treiber nicht aktiv – Schritt 1 ausführen und neu starten."

if ! command -v ollama >/dev/null 2>&1; then
  curl -fsSL https://ollama.com/install.sh | sh
fi

# Nur lokal erreichbar; Zugriff von außen ausschließlich über den Auth-Proxy.
install -d /etc/systemd/system/ollama.service.d
cat > /etc/systemd/system/ollama.service.d/override.conf <<CONF
[Service]
Environment="OLLAMA_HOST=127.0.0.1:11434"
Environment="OLLAMA_CONTEXT_LENGTH=${CONTEXT_LENGTH}"
Environment="OLLAMA_KEEP_ALIVE=${KEEP_ALIVE}"
Environment="OLLAMA_MAX_LOADED_MODELS=2"
CONF

systemctl daemon-reload
systemctl enable ollama >/dev/null
systemctl restart ollama
wait_for http://127.0.0.1:11434/api/version 30 || die "Ollama antwortet nicht (journalctl -u ollama)."
ok "Ollama $(curl -fsS http://127.0.0.1:11434/api/version | jq -r .version) läuft auf 127.0.0.1:11434"
