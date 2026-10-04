# P3 independent display-order reference inquiry

Read `EXPERIMENT_P3_RESULTS.md`, `analysis/reference-chain.json` and `results.json`.

The plan was frozen before retrieval (`PLAN_SHA256SUMS`). All 30 retrieval units are preserved with bytes, hashes, headers, statuses, redirects and timestamps. Request plans and `commands.sh` specify the bounded sequence. Retrieval creates new directories and refuses to overwrite evidence; use a fresh P3 directory to replay network requests. The focal original and E2 mutant/restoration paths are explicit in `scripts/analyze_reference.py`; its analysis is offline and does not import the historical checker.

Positive result: an externally prescribed display-label order is tied to the exact graph; original/restoration agree at 1000 positions, the cyclic permutation disagrees at 999. Stable class-ID lineage remains ABSTAIN.

Raw `retrieved/` bodies and model binaries are local evidence and excluded from source-only GitHub synchronization. `analysis/` and `results.json` are generated reports; repository publication policy is controlled by the parent project. No SDK, emulator, APK, class or DEX is part of this subtask.
