#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
python3 scripts/retrieve.py initial-candidates.json
python3 scripts/retrieve.py followups-1.json
python3 scripts/retrieve.py followups-2.json
python3 scripts/retrieve.py followups-3.json
python3 scripts/retrieve.py followups-4.json
python3 scripts/retrieve.py additional-initial-candidates.json
python3 scripts/retrieve.py followups-5.json
python3 scripts/retrieve.py followups-6.json
PYTHONDONTWRITEBYTECODE=1 /workspace/hand-contract-repro/.venv/bin/python scripts/analyze_reference.py > analysis/analyze.stdout 2> analysis/analyze.stderr
python3 scripts/write_report.py
python3 scripts/seal.py
sha256sum -c SHA256SUMS
