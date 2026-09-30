#!/usr/bin/env bash
# Schritt 5: Auth-Proxy vor Ollama (Token, Modellfreigabe, Schreibschutz) und Umschaltwerkzeug.
# shellcheck source=../lib.sh
. "$(dirname "$0")/../lib.sh"
require_root
load_conf
log "Schritt 5: Auth-Proxy"

install -d -m 755 /opt/llm
install -m 755 "$SETUP_DIR/files/llm-proxy.py" /opt/llm/llm-proxy.py
[ -f /opt/llm/active_model ] || echo "$DEFAULT_MODEL" > /opt/llm/active_model
chmod 644 /opt/llm/active_model
install -m 644 "$SETUP_DIR/files/llm-proxy.service" /etc/systemd/system/llm-proxy.service
install -m 755 "$SETUP_DIR/bin/llm-model-switch" /usr/local/sbin/llm-model-switch

systemctl daemon-reload
systemctl enable llm-proxy >/dev/null
systemctl restart llm-proxy
wait_http "http://${DOCKER_GATEWAY}:${PROXY_PORT}/" 15 || die "Proxy antwortet nicht (journalctl -u llm-proxy)."
ok "Proxy läuft auf ${PROXY_BIND} Port ${PROXY_PORT}, freigegeben: $(cat /opt/llm/active_model)"
