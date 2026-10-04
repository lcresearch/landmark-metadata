#!/usr/bin/env bash
set -euo pipefail
# Execute in a new experiment root; do not rerun in sealed evidence.
# Preparation requires SDK links and input provenance setup documented in plan.
PYTHONDONTWRITEBYTECODE=1 python3 scripts/fetch_dependencies.py
PYTHONDONTWRITEBYTECODE=1 /workspace/hand-contract-repro/.venv/bin/python scripts/prepare.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/build.py
PYTHONDONTWRITEBYTECODE=1 /workspace/hand-contract-repro/.venv/bin/python scripts/capture_versions.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/start_emulator.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/run.py
PYTHONDONTWRITEBYTECODE=1 /workspace/hand-contract-repro/.venv/bin/python scripts/analyze.py
# During this execution initial APKs were retained then rebuilt before first run,
# solely to distinguish decoded serialization failures from API failures.
# BUILD_ATTEMPTS.json and commands-executed.sh preserve both actual attempts.
PYTHONDONTWRITEBYTECODE=1 python3 scripts/normalize_results.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/write_report.py
