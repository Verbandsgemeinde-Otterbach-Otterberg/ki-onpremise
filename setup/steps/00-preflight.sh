#!/usr/bin/env bash
# Schritt 0: Voraussetzungen prüfen, Grundpakete installieren, Geheimnisse erzeugen.
# shellcheck source=../lib.sh
. "$(dirname "$0")/../lib.sh"
require_root
load_conf
log "Schritt 0: Vorprüfung"

# shellcheck disable=SC1091
. /etc/os-release
[ "${ID:-}" = debian ] && [ "${VERSION_ID:-}" = 13 ] \
  || die "Die Skripte sind für Debian 13 (trixie) geschrieben, gefunden: ${PRETTY_NAME:-unbekannt}."
ok "$PRETTY_NAME"

[ -n "${DOMAIN:-}" ] || die "DOMAIN ist in $CONF nicht gesetzt."
[ -n "${LETSENCRYPT_EMAIL:-}" ] || die "LETSENCRYPT_EMAIL ist in $CONF nicht gesetzt."

apt-get update -q
apt-get install -y -q curl ca-certificates openssl jq python3 pciutils iproute2
lspci | grep -qi nvidia || die "Keine NVIDIA-GPU gefunden."
ok "GPU: $(lspci | grep -i nvidia | head -1 | cut -d: -f3- | sed 's/^ *//')"

ensure_secret PROXY_TOKEN
ensure_secret WEBUI_SECRET_KEY
chmod 600 "$CONF"
ok "Konfiguration $CONF geprüft"
