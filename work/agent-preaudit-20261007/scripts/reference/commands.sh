#!/usr/bin/env bash
set -eu
# Existing dependency environment, preserved schema imported read-only.
# Writes only this reviewer's output directory. No network or inference.
PYTHONDONTWRITEBYTECODE=1 /workspace/hand-contract-repro/.venv/bin/python -B \
  /workspace/agent-preaudit-20261007T0749Z/reference/audit_reference.py \
  > /workspace/agent-preaudit-20261007T0749Z/reference/audit.stdout \
  2> /workspace/agent-preaudit-20261007T0749Z/reference/audit.stderr
