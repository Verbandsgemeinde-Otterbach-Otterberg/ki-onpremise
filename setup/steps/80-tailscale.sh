#!/usr/bin/env bash
# Schritt 8 (optional): API-Zugriff für Anwendungen über das Tailscale-VPN.
# shellcheck source=../lib.sh
. "$(dirname "$0")/../lib.sh"
require_root
load_conf
log "Schritt 8: Tailscale (optional)"

if [ "${TAILSCALE_ENABLED:-no}" != yes ]; then
  ok "TAILSCALE_ENABLED=no – übersprungen"
  exit 0
fi

command -v tailscale >/dev/null 2>&1 || curl -fsSL https://tailscale.com/install.sh | sh
if ! tailscale ip -4 >/dev/null 2>&1; then
  if [ -n "${TAILSCALE_AUTHKEY:-}" ]; then
    tailscale up --authkey "$TAILSCALE_AUTHKEY"
  else
    tailscale up
  fi
fi
ts_ip=$(tailscale ip -4 | head -1)
set_conf PROXY_BIND "${DOCKER_GATEWAY},${ts_ip}"
systemctl restart llm-proxy
ok "Proxy zusätzlich erreichbar unter ${ts_ip}:${PROXY_PORT} (nur im VPN, nur mit Token)"
