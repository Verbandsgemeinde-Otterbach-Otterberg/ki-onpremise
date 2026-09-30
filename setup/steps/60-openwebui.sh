#!/usr/bin/env bash
# Schritt 6: Open WebUI als Container starten.
# shellcheck source=../lib.sh
. "$(dirname "$0")/../lib.sh"
require_root
load_conf
log "Schritt 6: Open WebUI"

install -m 755 "$SETUP_DIR/bin/llm-webui-run" /usr/local/sbin/llm-webui-run
install -m 755 "$SETUP_DIR/bin/llm-webui-update" /usr/local/sbin/llm-webui-update

if docker inspect open-webui >/dev/null 2>&1; then
  ok "Container open-webui existiert bereits (Aktualisierung: sudo llm-webui-update)"
else
  docker pull -q "$OPENWEBUI_IMAGE" >/dev/null
  /usr/local/sbin/llm-webui-run
fi
wait_for "http://127.0.0.1:${OPENWEBUI_PORT}/health" 90 || die "Open WebUI startet nicht (docker logs open-webui)."
ok "Open WebUI läuft auf 127.0.0.1:${OPENWEBUI_PORT}"
