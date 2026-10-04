#!/usr/bin/env bash
# Editorial commands used for this revision, in order. Run rebuilds in a COPY
# of this directory; never overwrite a sealed package or historical evidence.
set -euo pipefail
cd /workspace/metadata-contract-paper-revision-20261004T065132Z
python scripts/revise_manuscript.py
bash build.sh
# The first map creation wrote CLAIM_EVIDENCE.json then stopped at an overly
# strict PDF contiguous-text assertion. CHECK_NOTES.md records the correction.
# Initial invocation: python scripts/verify_revision.py --write-map --record verification/revision-check.json
python scripts/verify_revision.py --record verification/revision-check.json
# The following one-time finalizer also updates the editable project TODO.
python scripts/finalize_revision.py
# Seal with a sorted SHA-256 manifest, then verify it (see scripts/seal_revision.py).
python scripts/seal_revision.py
