#!/usr/bin/env bash
# Build the EPUB and PDF from the manuscript.
# Works locally (needs pandoc + typst on PATH) and in CI.
set -euo pipefail
cd "$(dirname "$0")/.."

OUT=dist
SLUG=the-java
mkdir -p "$OUT"

# Chapters build in filename order: 00-…, 01-…, 02-…
CHAPTERS=(manuscript/*.md)
echo "Building from ${#CHAPTERS[@]} chapter file(s)..."

COMMON_ARGS=(
  --metadata-file=build/metadata.yaml
  --resource-path=.:manuscript
  --toc
  --wrap=none
  --lua-filter=build/extracts.lua
)

# EPUB — include the cover only if the file exists
EPUB_ARGS=()
if [[ -f images/cover.jpg ]]; then
  EPUB_ARGS+=(--epub-cover-image=images/cover.jpg)
fi
pandoc "${CHAPTERS[@]}" "${COMMON_ARGS[@]}" "${EPUB_ARGS[@]}" \
  --css=build/epub.css \
  -o "$OUT/$SLUG.epub"
echo "Wrote $OUT/$SLUG.epub"

# PDF via Typst (fast, no LaTeX install needed).
# The template gives a real title page, a Contents page, and starts
# every chapter on a fresh page.
pandoc "${CHAPTERS[@]}" "${COMMON_ARGS[@]}" \
  --pdf-engine=typst \
  --template=build/template.typ \
  -o "$OUT/$SLUG.pdf"
echo "Wrote $OUT/$SLUG.pdf"

# Narration script for the audiobook (VoiceStudio → Audiobook → import).
# Leaves out the lists and reference sections; no metadata file, so extracts
# keep their italics and narration.lua can give them a voice of their own.
NARRATED=()
for f in "${CHAPTERS[@]}"; do
  case "$f" in
    */11-crew-list-*|*/14-appendix-b-passenger-list*|*/16-bibliography*|*/18-java-masters-and-owners*) ;;
    *) NARRATED+=("$f") ;;
  esac
done
pandoc "${NARRATED[@]}" --wrap=none \
  --lua-filter=build/extracts.lua --lua-filter=build/narration.lua \
  -t plain -o "$OUT/$SLUG-narration.txt"
echo "Wrote $OUT/$SLUG-narration.txt"

# Read-online web pages, one per chapter, published at theshipjava.uk/read/
# so search engines can find the text (and every passenger's name).
rm -rf "$OUT/read"
pandoc "${CHAPTERS[@]}" "${COMMON_ARGS[@]}" \
  -t chunkedhtml --split-level=1 --chunk-template='%i.html' \
  --template=build/web.html -o "$OUT/read"
echo "Wrote $OUT/read/"

# Sanity check: extract plain text back out of the EPUB so it can be
# diffed against the source. AI never touches the prose; this proves it.
pandoc "$OUT/$SLUG.epub" -t plain -o "$OUT/$SLUG-extracted.txt"
echo "Wrote $OUT/$SLUG-extracted.txt (for verification diffs)"
