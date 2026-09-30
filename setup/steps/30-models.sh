#!/usr/bin/env bash
# Schritt 3: Modelle herunterladen.
# shellcheck source=../lib.sh
. "$(dirname "$0")/../lib.sh"
require_root
load_conf
log "Schritt 3: Modelle"

# shellcheck disable=SC2086
for model in $CHAT_MODELS $EMBED_MODEL; do
  if ollama show "$model" >/dev/null 2>&1; then
    ok "$model bereits vorhanden"
  else
    ollama pull "$model"
    ok "$model geladen"
  fi
done
ollama show "$DEFAULT_MODEL" >/dev/null 2>&1 || die "DEFAULT_MODEL $DEFAULT_MODEL ist nicht installiert."
