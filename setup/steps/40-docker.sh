#!/usr/bin/env bash
# Schritt 4: Docker und ein eigenes Netz mit festem Adressbereich.
# shellcheck source=../lib.sh
. "$(dirname "$0")/../lib.sh"
require_root
load_conf
log "Schritt 4: Docker"

command -v docker >/dev/null 2>&1 || apt-get install -y -q docker.io
systemctl enable --now docker >/dev/null
ok "$(docker --version)"

if ! docker network inspect "$DOCKER_NETWORK" >/dev/null 2>&1; then
  docker network create --driver bridge \
    --subnet "$DOCKER_SUBNET" --gateway "$DOCKER_GATEWAY" "$DOCKER_NETWORK" >/dev/null
fi
ok "Netz $DOCKER_NETWORK ($DOCKER_SUBNET, Gateway $DOCKER_GATEWAY)"
