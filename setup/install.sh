#!/usr/bin/env bash
# Installiert den kompletten LLM-Stack auf einem frischen Debian-13-Server mit NVIDIA-GPU.
# Aufruf: sudo ./install.sh   (mehrfach ausführbar; erledigte Schritte werden übersprungen)
set -Eeuo pipefail
cd "$(dirname "$0")"
# shellcheck source=lib.sh
. ./lib.sh
require_root

if [ ! -f "$CONF" ]; then
  install -d -m 700 "$(dirname "$CONF")"
  install -m 600 llm-stack.env.example "$CONF"
  log "Konfiguration angelegt: $CONF"
  echo "    Bitte DOMAIN und LETSENCRYPT_EMAIL eintragen und install.sh erneut starten."
  exit 0
fi

for step in steps/[0-9][0-9]-*.sh; do
  set +e
  bash "$step"
  rc=$?
  set -e
  if [ "$rc" -eq 100 ]; then
    log "Neustart erforderlich"
    echo "    Der NVIDIA-Treiber wurde installiert. Bitte 'sudo reboot' ausführen und danach"
    echo "    'sudo ./install.sh' erneut starten. Erledigte Schritte werden übersprungen."
    exit 0
  fi
  [ "$rc" -eq 0 ] || die "Schritt $step fehlgeschlagen (Exit-Code $rc)."
done

load_conf
log "Installation abgeschlossen"
echo "    Open WebUI:   https://${DOMAIN}"
echo "    Die erste Registrierung wird Administrator; weitere Konten müssen freigeschaltet werden."
echo "    Modell wechseln: sudo llm-model-switch <modell>"
