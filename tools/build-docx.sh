#!/usr/bin/env bash
# Erzeugt die Word-Fassung des Zwischenberichts aus den Markdown-Kapiteln.
# Voraussetzungen: pandoc, python3 mit python-docx (nur zum Neuerzeugen der Formatvorlage).
set -euo pipefail
cd "$(dirname "$0")/.."

SRC=docs/zwischenbericht-2026-09
OUT=build/Zwischenbericht_VG-Otterbach-Otterberg_2026-09.docx
mkdir -p build

# 1. Architekturbild erzeugen
python3 tools/make-diagram.py >/dev/null

# 2. Formatvorlage bei Bedarf erzeugen
[ -f tools/docx/reference.docx ] || python3 tools/docx/make-reference.py

# 3. Navigationszeilen (nur für GitHub) entfernen
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
for f in "$SRC"/0*.md; do
  sed -e '/^---$/,$d' "$f" > "$tmp/$(basename "$f")"
done

# 4. Word-Datei erzeugen
pandoc tools/docx/cover.md "$tmp"/0*.md \
  --from markdown+pipe_tables+raw_attribute+fenced_divs-auto_identifiers \
  --to docx \
  --reference-doc tools/docx/reference.docx \
  --resource-path "tools/docx:$SRC" \
  --metadata lang=de-DE \
  -o "$OUT"
python3 tools/docx/postprocess.py "$OUT"
echo "Erstellt: $OUT"
