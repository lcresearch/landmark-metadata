#!/usr/bin/env bash
set -euo pipefail
python /workspace/agent-preaudit-20261007T0749Z/executable/scripts/audit_executable.py
python /workspace/agent-preaudit-20261007T0749Z/executable/scripts/compare_records.py
