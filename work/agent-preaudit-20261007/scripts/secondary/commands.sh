#!/usr/bin/env bash
# Decisive read-only checks. Run from any directory; outputs confined to reviewer folder.
# Preliminary investigation used cat/sed/rg and Python JSON-key inspection on paths indexed below.
set -eu
TASK_AUDIT_ROOT=/workspace/agent-preaudit-20261007T0749Z/secondary
PYTHONDONTWRITEBYTECODE=1 /workspace/hand-contract-repro/.venv/bin/python -B "$TASK_AUDIT_ROOT/readback.py" > "$TASK_AUDIT_ROOT/readback.stdout" 2> "$TASK_AUDIT_ROOT/readback.stderr"
PYTHONDONTWRITEBYTECODE=1 /workspace/hand-contract-repro/.venv/bin/python -B "$TASK_AUDIT_ROOT/supplement.py" > "$TASK_AUDIT_ROOT/supplement.stdout" 2> "$TASK_AUDIT_ROOT/supplement.stderr"
python -B "$TASK_AUDIT_ROOT/finalize.py"
