# P2 evidence navigation

Primary question: whether generated wrapper and official Task classifier expose different public rejection stages on the same Android API/ABI.

- `EXPERIMENT_P2_PLAN.md`, `PLAN_FREEZE.json`: pre-execution design and hash.
- `EXECUTION_INPUT_FREEZE.json`: final harness/source/build/plan hashes before first model execution.
- `EXPERIMENT_P2_RESULTS.md`, `results.json`: final human-readable and machine-readable results (once run completes).
- `static-results.json`: pinned source fixtures, graph/buffer/metadata preservation, structural population and code generation.
- `build-results.json`: final builds; `build-results-attempt-1.json`, `BUILD_ATTEMPTS.json` preserve the earlier successful builds and reason for pre-execution harness refinement.
- `execution-results.json`, `executions/primary/*/*/device`: unnormalized collector records, exact returned JSON/RGB/raw float outputs and full exception stacks.
- `dependencies/resolved-lock.json`, `downloads.json`: exact separate classpaths/native libraries and downloaded Maven records; complete dependency hashes, not an assertion of identical native interpreters.
- `versions/versions.json`, `prerequisites/android-getprop.stdout`: toolchain and AVD environment.
- `scripts/*.py`, `scripts/*Instrumentation.java`, `commands.sh`, `commands-executed.sh`: actual harness/build/run/analysis sources and expanded commands.
- `../review/mechanism`: separate pinned source and actual-bytecode mechanism review; does not substitute for device observations.

The Task public `classify` method combines inference and decoding. Results keep that granularity separate from whether a call was reached. The standalone generated API exposes a separate `process` return and category getter.

SDK symlinks, emulator state, downloaded model/library binaries, APKs, classes/DEX and raw execution outputs are local evidence only. They must not be uploaded to the source-only GitHub repository. Agent execution/audit does not satisfy pending human verification.
