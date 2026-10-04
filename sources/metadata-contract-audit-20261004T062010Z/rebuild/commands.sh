#!/usr/bin/env bash
# Reproducible equivalent top-level command sequence. Expanded executed subprocess arguments are in commands-executed.sh.
# Do not run in the populated evidence directory.
set -euo pipefail
cd /workspace/metadata-contract-audit-20261004T062010Z/rebuild
python3 setup.py
PYTHONDONTWRITEBYTECODE=1 /workspace/hand-contract-repro/.venv/bin/python scripts/prepare_e1.py > logs/prepare_e1.stdout 2> logs/prepare_e1.stderr
# start_emulator ran concurrently with E1 build; readiness was awaited before run_android.
PYTHONDONTWRITEBYTECODE=1 python3 scripts/start_emulator.py > logs/start_emulator.stdout 2> logs/start_emulator.stderr &
AUDIT_BOOT_PID=$!
PYTHONDONTWRITEBYTECODE=1 /workspace/hand-contract-repro/.venv/bin/python scripts/build_android.py --experiment E1 > logs/build_e1.stdout 2> logs/build_e1.stderr
PYTHONDONTWRITEBYTECODE=1 /workspace/hand-contract-repro/.venv/bin/python scripts/capture_versions.py > logs/capture_versions.stdout 2> logs/capture_versions.stderr
PYTHONDONTWRITEBYTECODE=1 python3 scripts/capture_build_evidence.py
wait "$AUDIT_BOOT_PID"
PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_android.py --experiment E1 --run primary > logs/run_e1.stdout 2> logs/run_e1.stderr
PYTHONDONTWRITEBYTECODE=1 /workspace/hand-contract-repro/.venv/bin/python scripts/prepare_e2.py > logs/prepare_e2.stdout 2> logs/prepare_e2.stderr
PYTHONDONTWRITEBYTECODE=1 /workspace/hand-contract-repro/.venv/bin/python scripts/build_android.py --experiment E2 > logs/build_e2.stdout 2> logs/build_e2.stderr
PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_android.py --experiment E2 --run primary > logs/run_e2.stdout 2> logs/run_e2.stderr
PYTHONDONTWRITEBYTECODE=1 python3 scripts/audit_results.py > logs/audit_results.stdout 2> logs/audit_results.stderr
# Shutdown after root agent confirms no supplemental audit needed:
sdk/platform-tools/adb -s emulator-5554 emu kill

# Seal after final report, scope notes and emulator shutdown records exist:
python3 scripts/seal_audit.py
