#!/usr/bin/env bash
# Schritt 9: Funktions- und Sicherheitsprüfung des gesamten Stacks.
# shellcheck source=../lib.sh
. "$(dirname "$0")/../lib.sh"
require_root
load_conf
log "Schritt 9: Prüfung"

fail=0
check() { if eval "$2"; then ok "$1"; else warn "$1 – FEHLGESCHLAGEN"; fail=1; fi; }
# shellcheck disable=SC2034  # in check() per eval verwendet
proxy="http://${DOCKER_GATEWAY}:${PROXY_PORT}"
# shellcheck disable=SC2034
auth=(-H "Authorization: Bearer ${PROXY_TOKEN}")
code() { curl -s -o /dev/null -w '%{http_code}' "$@"; }

check "GPU mit Treiber verfügbar"            'nvidia-smi >/dev/null 2>&1'
check "Ollama nur lokal (127.0.0.1:11434)"   'ss -tln | grep -q "127.0.0.1:11434"'
check "Proxy lehnt Anfragen ohne Token ab"   '[ "$(code "$proxy/api/tags")" = 401 ]'
check "Proxy akzeptiert gültiges Token"      '[ "$(code "${auth[@]}" "$proxy/api/tags")" = 200 ]'
check "Proxy zeigt nur freigegebene Modelle" \
  '[ "$(curl -fsS "${auth[@]}" "$proxy/api/tags" | jq -r ".models[].name" | grep -vc -e "^${EMBED_MODEL}" -e "^$(cat /opt/llm/active_model)")" = 0 ]'
check "Proxy sperrt Modell-Downloads"        '[ "$(code "${auth[@]}" -X POST -d "{\"model\":\"x\"}" "$proxy/api/pull")" = 403 ]'
check "Open WebUI erreicht Proxy ohne Token" \
  'docker exec open-webui python3 -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen(\"http://host.docker.internal:${PROXY_PORT}/api/tags\").status==200 else 1)"'
check "Open WebUI gesund"                    'curl -fsS "http://127.0.0.1:${OPENWEBUI_PORT}/health" | grep -q true'
check "HTTPS unter ${DOMAIN} erreichbar"     '[ "$(code "https://${DOMAIN}/health")" = 200 ]'

# Öffentlich dürfen nur SSH, HTTP und HTTPS lauschen.
public=$(ss -tlnH | awk '{print $4}' | grep -E '^(0\.0\.0\.0|\[::\]|\*):' | sed -E 's/.*:([0-9]+)$/\1/' | sort -u | grep -vxE '22|80|443' || true)
check "Keine weiteren öffentlichen Ports"    '[ -z "$public" ]'
[ -z "$public" ] || warn "Öffentlich erreichbar: $(echo "$public" | tr '\n' ' ')"

[ "$fail" -eq 0 ] || die "Mindestens eine Prüfung ist fehlgeschlagen."
