#!/usr/bin/env bash
# Read-only evidence audit. Derivative outputs go to a NEW directory.
set -euo pipefail
if [[ $# -ne 1 ]]; then
  echo 'Usage: bash commands.sh /absolute/path/to/new-claims-audit-directory' >&2
  exit 2
fi
claims_new_output="$1"
if [[ "$claims_new_output" != /* || -e "$claims_new_output" ]]; then
  echo 'Output must be an absolute path that does not yet exist.' >&2
  exit 2
fi
claims_script_directory="$(cd -- "$(dirname -- "$0")" && pwd)"
mkdir -p -- "$claims_new_output"
cp -- "$claims_script_directory/recompute.py" "$claims_script_directory/supplement.py" "$claims_script_directory/write_report.py" "$claims_new_output/"
PYTHONDONTWRITEBYTECODE=1 /workspace/hand-contract-repro/.venv/bin/python "$claims_new_output/recompute.py" > "$claims_new_output/recompute.stdout" 2> "$claims_new_output/recompute.stderr"
PYTHONDONTWRITEBYTECODE=1 /workspace/hand-contract-repro/.venv/bin/python "$claims_new_output/supplement.py" > "$claims_new_output/supplement.stdout" 2> "$claims_new_output/supplement.stderr"
PYTHONDONTWRITEBYTECODE=1 /workspace/hand-contract-repro/.venv/bin/python "$claims_new_output/write_report.py" > "$claims_new_output/report.stdout" 2> "$claims_new_output/report.stderr"
