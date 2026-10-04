#!/usr/bin/env bash
# Safe entry point: verify preserved evidence without overwriting old records.
# Exact historical subprocesses: commands-executed.sh and **/*.command.json.
# Fresh execution instructions: REPRODUCE.md (always use a new directory).
set -euo pipefail
TASK_EVIDENCE_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
case "${1:-verify}" in
  verify)
    exec python3 "$TASK_EVIDENCE_ROOT/scripts/verify_delivery.py"
    ;;
  log)
    cat "$TASK_EVIDENCE_ROOT/commands-executed.sh"
    ;;
  *)
    echo 'Usage: bash commands.sh [verify|log]; see REPRODUCE.md for fresh runs.' >&2
    exit 2
    ;;
esac
