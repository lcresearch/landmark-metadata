#!/usr/bin/env bash
set -euo pipefail
# Command index for completed work. Do not execute against sealed directories.
# This source package depends on pinned old artifacts and installed tools.
# P2/commands-executed.sh retains expanded build/run commands and both builds.
# P2/commands.sh and P3/commands.sh document their respective pipelines.
python review/verify_runtime_records.py
python review/verify_protected_evidence.py
# Run only after the manuscript revision script has completed.
bash build_manuscript.sh
