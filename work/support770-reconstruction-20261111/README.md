# Support #770 bounded reconstruction

This area follows the [fixed screening plan](../case-screening-20261111/SHORTLIST.md)
after the user authorized PR #23 review/squash integration and one #770 execution.
The main base is `fd9ce5d27b5add8c4fe2242450bfaa8db45ed16f`; its sole parent is
`c82253d487b487747de47460b558209518c78949`, and its tree matches reviewed head
`dc367576d2add164ab30521f9ab62899c2b08779`. PR #24's maintenance refactor is preserved.

[PROTOCOL](PROTOCOL.md) was recorded before acquisition. [RUNTIME_PLAN](RUNTIME_PLAN.md)
fixes the actual generated-code build/observation path before compilation and
inference. Both retain the unsupported-consumer and historical-identity limits.
Results, validation and retention identities are recorded alongside this run's
source after collection. This area does not expand the current manuscript sample.

The [PR #25 review fixes](REVIEW_FIXES.md) strengthen output/call validation and
enforce one shared 600-second build deadline per consumer. They preserve all
sealed records and use saved-byte checks/synthetic regressions without new inference.

## Execution entry points

All outputs must be outside Git in a **new, absent** root. The actual root is
`/home/hsz/landmark-evidence/support770-reconstruction-20261111`; never rerun into it.
`record_command.py` stores command, timestamps, exit/timeout and stdout/stderr in
a fresh stage. Each stage below was invoked through that recorder. External
`stages/*/command.json` files preserve the full actual arguments.

1. `acquire.py URL OUTPUT --max-bytes LIMIT`: two bounded transport attempts at
   most, preserving errors/partial bodies. Model bytes are copied unchanged.
2. `inspect_model.py MODEL OUTPUT`: run with the preceding verified Support 0.4.4
   Python environment. Pin metadata, tensor descriptors and associated labels.
3. `prepare_generation.py --root ROOT --previous PREVIOUS`: verify the Gradle
   publisher checksum, copy SDK components, stage/pin the fixed AGP project.
4. Gradle 7.5.1 `--no-daemon --console=plain --stacktrace --info
   :app:generateDebugMlModelClass`: exactly one AGP generation invocation, with
   a new `GRADLE_USER_HOME`, SDK/user directories and recorded JDK 17 path.
5. `build_consumers.py --root ROOT --previous PREVIOUS`: verify/copy the previous
   run's dependency lock, compile unchanged generated source plus first-party
   instrumentation, build two separate APKs once, retain all stages/classes/DEX.
6. `boot_device.py --root ROOT --previous PREVIOUS`: copy emulator/system image,
   boot one fresh software AVD on port 5556, preserve bounded readiness records.
7. `run_consumers.py --root ROOT`: install each new package, invoke it once,
   collect caught exceptions and raw output. Collector success is distinct from
   a successful public call. No failed inference/getter is retried.
8. `verify_results.py --root ROOT --output NEW_JSON`: validate saved identities
   and completion. It does not require either consumer to have a desired result.
9. Stop only this run's owned `emulator-5556`, then retain outputs and verify the
   selected evidence archive. Do not upload evidence through Git, Releases or LFS.

This is not a self-contained offline reproduction: the scripts currently reuse
the preceding local JDK/Python/SDK/dependency material, and generator acquisition
uses public repositories. Original Studio/AGP/library versions and image remain
unknown. Retained hashes bind the reconstructed configuration, not the 2022 run.
