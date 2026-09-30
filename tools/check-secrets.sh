#!/usr/bin/env bash
# Prüft das Repository vor jedem Push auf versehentlich enthaltene Geheimnisse
# und personenbezogene Daten. Aufruf aus dem Repo-Stammverzeichnis: ./tools/check-secrets.sh
set -u
cd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)" || exit 1

PATTERNS=(
  'sk-[A-Za-z0-9_-]{16,}'                 # API-Keys (OpenAI-Format, Open WebUI)
  'eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]+' # JWT
  '-----BEGIN [A-Z ]*PRIVATE KEY-----'
  '(password|passwd|secret|token|api_key|apikey)[[:space:]]*[:=][[:space:]]*[^[:space:]<$]{6,}'
  'WEBUI_SECRET_KEY[[:space:]]*[:=][[:space:]]*"?[^[:space:]<$"]+'
  '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' # E-Mail-Adressen
  '\b([0-9]{1,3}\.){3}[0-9]{1,3}\b'        # IPv4-Adressen (private Docker-Netze sind ausgenommen)
)

found=0
for p in "${PATTERNS[@]}"; do
  hits=$(git ls-files -z 2>/dev/null | xargs -0 grep -nIE -- "$p" 2>/dev/null \
         | grep -vE '127\.0\.0\.1|0\.0\.0\.0|<REDACTED>|<SERVER_IP>|example\.(org|com)' \
         | grep -vE '(^|[^0-9])(10\.|172\.(1[6-9]|2[0-9]|3[01])\.|192\.168\.)[0-9]' || true)
  if [ -n "$hits" ]; then
    echo "Treffer für Muster: $p"
    echo "$hits"
    echo
    found=1
  fi
done

if [ "$found" -eq 1 ]; then
  echo "Bitte Treffer prüfen und bereinigen, bevor gepusht wird."
  exit 1
fi
echo "Keine Auffälligkeiten gefunden."
