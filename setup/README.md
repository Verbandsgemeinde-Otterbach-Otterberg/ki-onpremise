# Nachbau: LLM-Stack auf eigenem GPU-Server

Diese Skripte bauen den Stack der Verbandsgemeinde Otterbach-Otterberg auf einem frischen Server nach:

```
Browser ──HTTPS──► Nginx ──► Open WebUI (Docker) ──► Auth-Proxy ──► Ollama ──► NVIDIA-GPU
                                                        ▲
                             API-Clients (optional über Tailscale-VPN, mit Token)
```

## Voraussetzungen

| Punkt | Anforderung |
|---|---|
| Server | Dedizierter Server mit NVIDIA-GPU; erprobt mit Hetzner GEX44 (RTX 4000 SFF Ada, 20 GB) |
| Betriebssystem | Debian 13 „trixie“, Minimalinstallation |
| Zugang | SSH mit sudo- bzw. root-Rechten |
| Domain | DNS-A-Eintrag der gewünschten Domain zeigt auf die Server-IP |
| Datenschutz | Auftragsverarbeitungsvertrag (AVV) mit dem Hoster, bevor personenbezogene Daten verarbeitet werden |

## Installation

```bash
git clone https://github.com/Verbandsgemeinde-Otterbach-Otterberg/ki-onpremise.git
cd ki-onpremise/setup

sudo ./install.sh                          # legt /etc/llm-stack/llm-stack.env an
sudo nano /etc/llm-stack/llm-stack.env     # DOMAIN und LETSENCRYPT_EMAIL eintragen
sudo ./install.sh                          # installiert den NVIDIA-Treiber
sudo reboot

cd ki-onpremise/setup
sudo ./install.sh                          # installiert den Rest und prüft alles
```

`install.sh` kann beliebig oft ausgeführt werden; erledigte Schritte werden erkannt und übersprungen.
Meldet die Shell „Permission denied“, fehlt das Ausführungsrecht (etwa nach einem Download über die
Weboberfläche); dann `sudo bash install.sh` verwenden.
Der letzte Schritt prüft den gesamten Stack automatisch (Token-Pflicht, Modellfreigabe, HTTPS,
keine unerwünscht offenen Ports).

| Schritt | Skript | Ergebnis |
|---|---|---|
| 0 | `steps/00-preflight.sh` | Debian 13 und GPU geprüft, Grundpakete, Geheimnisse erzeugt |
| 1 | `steps/10-nvidia.sh` | NVIDIA-Treiber aus den Debian-Paketquellen, danach Neustart |
| 2 | `steps/20-ollama.sh` | Ollama als systemd-Dienst, nur lokal erreichbar, 16.384 Token Kontext |
| 3 | `steps/30-models.sh` | Chat- und Embedding-Modelle geladen |
| 4 | `steps/40-docker.sh` | Docker und eigenes Netz mit festen Adressen |
| 5 | `steps/50-proxy.sh` | Auth-Proxy vor Ollama, Umschaltwerkzeug |
| 6 | `steps/60-openwebui.sh` | Open WebUI als Container |
| 7 | `steps/70-nginx-tls.sh` | Nginx mit Let's-Encrypt-Zertifikat |
| 8 | `steps/80-tailscale.sh` | optional: API-Zugriff über Tailscale-VPN |
| 9 | `steps/90-verify.sh` | Funktions- und Sicherheitsprüfung |

## Nach der Installation

**Erstes Konto:** Die erste Registrierung unter `https://<domain>` wird Administrator. Alle weiteren
Konten landen im Status „ausstehend“ und müssen im Adminbereich freigeschaltet werden.

**Modell wechseln:** Auf einer 20-GB-Karte ist immer ein Chat-Modell freigegeben.

```bash
sudo llm-model-switch llama3.2:3b          # freigeben, andere entladen, vorwärmen
sudo llm-model-switch                      # zeigt freigegebenes und installierte Modelle
```

## Fachanwendungen anbinden

Es gibt zwei Wege. Welcher passt, hängt davon ab, ob die Anwendung Wissen aus den Wissenssammlungen braucht.

**Mit Wissen: über Open WebUI und ein Dienstkonto.** Die Anwendung erhält dieselben Rechte wie eine
Person in ihrer Gruppe.

1. Im Adminbereich eine Gruppe für die Anwendung anlegen (z. B. `app-schadensmelder`) und ihr die
   benötigten Modellprofile und Wissenssammlungen freigeben.
2. Ein Dienstkonto anlegen (z. B. `svc-schadensmelder`), freischalten und dieser Gruppe zuordnen.
3. In den Admin-Einstellungen API-Schlüssel aktivieren und das Erzeugen von Schlüsseln nur dieser
   Gruppe erlauben; bei Bedarf die mit Schlüsseln erreichbaren Endpunkte einschränken.
4. Als Dienstkonto anmelden und in den Kontoeinstellungen einen API-Schlüssel erzeugen.
5. Die Anwendung nutzt die OpenAI-kompatible Schnittstelle von Open WebUI mit dem Namen des Modellprofils:

```bash
curl https://<domain>/api/chat/completions \
  -H "Authorization: Bearer <api-schluessel-des-dienstkontos>" \
  -H "Content-Type: application/json" \
  -d '{"model": "<modellprofil>", "messages": [{"role": "user", "content": "..."}]}'
```

Wird die Anwendung abgeschaltet oder ein Schlüssel bekannt, wird nur dieser Schlüssel bzw. dieses
Konto gesperrt.

**Ohne Wissen: direkt über den Auth-Proxy.** Für Anwendungen, die nur das Modell brauchen. Der Proxy
verlangt das Token aus `PROXY_TOKEN` und ist nur über das VPN erreichbar (Schritt 8).

```bash
curl -H "Authorization: Bearer $PROXY_TOKEN" http://<tailscale-adresse>:11435/api/tags
```

Der Proxy kennt keine Personen und keine Wissenssammlungen. Anwendungen, die auf Wissen zugreifen,
deshalb immer über Open WebUI anbinden.

**Open WebUI aktualisieren:** `sudo llm-webui-update` sichert zuerst die Datenbank nach
`/var/backups/llm-stack/`, lädt dann das Image und startet den Container neu.

**Wissenssammlungen und Modellprofile je Zielgruppe:** In Open WebUI unter *Arbeitsbereich → Wissen*
Sammlungen anlegen, unter *Arbeitsbereich → Modelle* je Zielgruppe ein Profil mit Basismodell,
System-Prompt und zugeordneter Wissenssammlung erstellen und den Zugriff auf eine Benutzergruppe
beschränken.

## Sicherheit

Öffentlich erreichbar sind nur SSH (22), HTTP (80, Umleitung) und HTTPS (443). Ollama lauscht nur auf
`127.0.0.1`, der Proxy nur am Docker-Gateway und optional an der Tailscale-Adresse, Open WebUI nur
auf `127.0.0.1`. Ohne Token darf ausschließlich die feste Adresse des Open-WebUI-Containers den
Proxy nutzen. Zusätzlich empfiehlt sich die Firewall des Hosters (z. B. Hetzner Firewall).

Docker-Ports nie auf `0.0.0.0` veröffentlichen: Docker leitet solchen Verkehr an der INPUT-Kette
der Host-Firewall vorbei.

## Hinweise

- Einstellungen wie `DEFAULT_USER_ROLE` übernimmt Open WebUI nur beim ersten Start in seine
  Datenbank; spätere Änderungen erfolgen im Adminbereich.
- Für reproduzierbare Installationen in `OPENWEBUI_IMAGE` eine feste Version eintragen.
- Die Skripte wurden für Debian 13 geschrieben. Auf anderen Distributionen bricht Schritt 0 bewusst ab.
