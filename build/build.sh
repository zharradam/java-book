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

# Sanity check: extract plain text back out of the EPUB so it can be
# diffed against the source. AI never touches the prose; this proves it.
pandoc "$OUT/$SLUG.epub" -t plain -o "$OUT/$SLUG-extracted.txt"
echo "Wrote $OUT/$SLUG-extracted.txt (for verification diffs)"
