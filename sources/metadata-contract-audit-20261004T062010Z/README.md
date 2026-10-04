# Agent technical audit package

This directory contains a new automated audit of the preserved metadata-contract study. It is separate from the immutable experiment and manuscript directories. No item here constitutes independent human verification.

Start with `AUDIT_REPORT.md`, then use `results.json` for the bounded assertions and `MANUSCRIPT_IMPACT.md` for proposed text changes. `TODO.before.md` and `TODO.after.md` preserve the planning change; the current editable planning document is `/workspace/metadata-contract-next/TODO.md`.

| Directory | Evidence |
|---|---|
| `preservation/` | Independent model/ZIP/APK/raw-array calculations and actual APK bytecode inspection over historical executions |
| `rebuild/` | Fresh generation, compilation, packaging and Android execution using new output directories and AVD; installed fixed tools are reused |
| `baseline/` | Fresh official-reader/populator, exact-path simple baseline, E5 and Linux Task-initialization comparison; implementation and used-jar checks |
| `claims/` | Per-claim manuscript audit, E3/E4/E5 counting, Hand source/graph bridge and saved decoded-result verification |
| `literature/` | Four bounded full-text technical comparisons, preserved PDFs, fixed versions and retrieval provenance |
| `verification/` | Root cross-checks and before/after checks of the old evidence manifests |

`AUDIT_PLAN.md` records scope and interpretation before the new runs. Each subtask preserves its own source/scripts, exact commands and diagnostics. The root `commands.sh verify` performs read-only verification of this audit manifest. It does not run generation, installation or inference. The root cross-check script reads completed fresh files; it does not replace the experimental scripts.

The root SHA256SUMS excludes installed/writable emulator state under `rebuild/sdk/`, Python caches, symlinks and itself. Exact AVD configuration, emulator commands, tool versions and dependencies are preserved outside that excluded tree. The tools referenced through SDK symlinks and the historical workspace roots are still dependencies; this is not yet a standalone offline release.

Rebuild commands are recorded for inspection and reconstruction into a **new** destination. Do not rerun experimental writers in this populated audit directory. New executions need a new directory and must preserve negative results and any changes to the harness. The generated Java was not modified; the harness asset-hash addition and orchestration adjustment are disclosed separately.
