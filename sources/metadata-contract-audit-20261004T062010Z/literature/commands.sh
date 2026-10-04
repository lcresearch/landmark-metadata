#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
# Read-only final evidence verification.
sha256sum --check SHA256SUMS

# Executed acquisition/processing commands are preserved below for replay into
# a NEW audit directory. Do not uncomment them in this sealed directory.
# python scripts/fetch.py
# python scripts/pin_versions.py
# python scripts/finalize.py
# fetch.py records exact URLs, copy source, pdftotext commands and their results
# in retrieval-results.json; pin_versions.py records explicit version requests.

# Full-text inspection used the *-reading.txt and *-layout.txt files, with rg
# section searches and selected sed ranges. The report identifies the exact
# PDF pages/sections supporting each claim. These are human-readable audit
# interpretations, not automated tests proving novelty.
