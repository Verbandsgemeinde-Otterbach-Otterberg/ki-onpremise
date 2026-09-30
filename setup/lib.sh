#!/usr/bin/env bash
# Gemeinsame Hilfsfunktionen für alle Installationsschritte.
set -Eeuo pipefail

# shellcheck disable=SC2034  # wird von den Schritt-Skripten genutzt
SETUP_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
CONF=${LLM_STACK_CONF:-/etc/llm-stack/llm-stack.env}
export DEBIAN_FRONTEND=noninteractive

log()  { printf '\n\033[1;34m==> %s\033[0m\n' "$*"; }
ok()   { printf '    \033[1;32m✓\033[0m %s\n' "$*"; }
warn() { printf '    \033[1;33m!\033[0m %s\n' "$*"; }
die()  { printf '\033[1;31mFEHLER:\033[0m %s\n' "$*" >&2; exit 1; }

require_root() { [ "$(id -u)" -eq 0 ] || die "Bitte mit sudo bzw. als root ausführen."; }

load_conf() {
  [ -f "$CONF" ] || die "Konfiguration $CONF fehlt (Vorlage: setup/llm-stack.env.example)."
  set -a
  # shellcheck disable=SC1090
  . "$CONF"
  set +a
}

# Setzt oder ersetzt einen Wert in der Konfigurationsdatei.
set_conf() {
  local name=$1 value=$2
  if grep -q "^${name}=" "$CONF"; then
    sed -i "s|^${name}=.*|${name}=${value}|" "$CONF"
  else
    printf '%s=%s\n' "$name" "$value" >> "$CONF"
  fi
  export "${name}=${value}"
}

# Erzeugt ein Geheimnis, falls der Wert in der Konfiguration leer ist.
ensure_secret() {
  local name=$1
  if [ -z "${!name:-}" ]; then
    set_conf "$name" "$(openssl rand -hex 32)"
    ok "$name erzeugt"
  fi
}

# Wartet, bis eine URL erreichbar ist.
wait_for() {
  local url=$1 tries=${2:-60}
  for _ in $(seq "$tries"); do
    curl -fsS -o /dev/null "$url" && return 0
    sleep 2
  done
  return 1
}

# Wartet, bis ein Dienst überhaupt per HTTP antwortet (auch 401/403 zählen).
wait_http() {
  local url=$1 tries=${2:-30}
  for _ in $(seq "$tries"); do
    [ "$(curl -s -o /dev/null -w '%{http_code}' "$url")" != 000 ] && return 0
    sleep 1
  done
  return 1
}
