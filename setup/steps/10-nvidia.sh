#!/usr/bin/env bash
# Schritt 1: NVIDIA-Treiber aus den Debian-Paketquellen installieren.
# Ollama bringt die CUDA-Laufzeit selbst mit; auf dem Host wird nur der Treiber benötigt.
# shellcheck source=../lib.sh
. "$(dirname "$0")/../lib.sh"
require_root
log "Schritt 1: NVIDIA-Treiber"

if nvidia-smi >/dev/null 2>&1; then
  ok "Treiber aktiv: $(nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader)"
  exit 0
fi

# Paketquellen um contrib, non-free und non-free-firmware erweitern (Format deb822 und klassisch)
for f in /etc/apt/sources.list.d/*.sources; do
  [ -f "$f" ] || continue
  sed -i -E 's/^Components:.*/Components: main contrib non-free non-free-firmware/' "$f"
done
if [ -f /etc/apt/sources.list ]; then
  sed -i -E '/^deb(-src)? .*debian/ s/^(deb(-src)? +[^ ]+ +[^ ]+) +.*/\1 main contrib non-free non-free-firmware/' \
    /etc/apt/sources.list
fi
ok "Paketquellen: contrib non-free non-free-firmware aktiviert"

apt-get update -q
apt-get install -y -q linux-headers-amd64
apt-get install -y -q nvidia-driver nvidia-smi firmware-misc-nonfree
ok "Treiberpakete installiert"

# Exit-Code 100 signalisiert install.sh, dass ein Neustart nötig ist.
exit 100
