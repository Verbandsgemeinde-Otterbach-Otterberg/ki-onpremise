#!/usr/bin/env bash
# Schritt 7: Nginx als Reverse Proxy mit Let's-Encrypt-Zertifikat.
# shellcheck source=../lib.sh
. "$(dirname "$0")/../lib.sh"
require_root
load_conf
log "Schritt 7: Nginx und HTTPS"

apt-get install -y -q nginx certbot python3-certbot-nginx
sed -e "s|__DOMAIN__|${DOMAIN}|g" -e "s|__PORT__|${OPENWEBUI_PORT}|g" \
  "$SETUP_DIR/files/nginx-site.conf" > /etc/nginx/sites-available/llm-stack.conf
ln -sf /etc/nginx/sites-available/llm-stack.conf /etc/nginx/sites-enabled/llm-stack.conf
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl reload nginx
ok "Nginx leitet ${DOMAIN} an Open WebUI weiter"

if [ -d "/etc/letsencrypt/live/${DOMAIN}" ]; then
  ok "Zertifikat für ${DOMAIN} vorhanden"
else
  certbot --nginx -d "$DOMAIN" -m "$LETSENCRYPT_EMAIL" --agree-tos --non-interactive --redirect \
    || die "Zertifikat konnte nicht ausgestellt werden. Zeigt der DNS-Eintrag von ${DOMAIN} auf diesen Server?"
  ok "Zertifikat ausgestellt, HTTP wird auf HTTPS umgeleitet"
fi
