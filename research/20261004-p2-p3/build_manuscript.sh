#!/usr/bin/env bash
set -euo pipefail
TASK_DRAFT_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$TASK_DRAFT_ROOT/manuscript"
pdflatex -interaction=nonstopmode -halt-on-error paper.tex > build-pass1.stdout 2>&1
pdflatex -interaction=nonstopmode -halt-on-error paper.tex > build-pass2.stdout 2>&1
pdftotext -layout paper.pdf paper-text.txt
pdftotext paper.pdf paper-reading.txt
mkdir -p preview
pdftoppm -r 100 -png paper.pdf preview/page > preview-render.stdout 2> preview-render.stderr
pdfinfo paper.pdf > paper-pdfinfo.txt
if rg 'Overfull|undefined references|undefined on input' paper.log; then
  echo 'Review the LaTeX diagnostics before treating the build as complete.' >&2
  exit 1
fi
