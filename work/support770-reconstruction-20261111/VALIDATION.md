# Validation and interpretation

The actual scientific outcomes are wrapper **FAIL at category_getter** and Task
**PASS through mask access**. Collection completed for both. These labels are
separate from saved-byte verification PASS; the failure is neither discarded nor
converted into a scientific success because it matched a known report.

At initial PR #25 delivery, `verify_results.py` passed 66 identity/completion checks over the complete model,
actual AGP command, generated source, frozen build sources, classes, DEX, native
payloads, dependencies, APKs, device model/input hashes and returned raw files.
It checks complete failure details without requiring the reported exception to
occur. Four in-memory adverse substitutions (raw output, Task APK, shared input,
generated source hash) were all rejected. Retained evidence files were not changed.
This is consistency verification, not independent provenance or human verification.

The raw wrapper is `[1,257,257,21]` float32 and its caught exception stack reaches
the actual generated getter. Task returns one `[257,257]` category mask and 21
labels. The same model/input hashes are checked on-device in both arms. Task raw
scores are unobserved; neither model accuracy nor cross-consumer score equality
is assessed. Original reporter model/library/input identities remain unavailable.

All 199 existing repository regressions passed after integration. Two additional
synthetic controller regressions verify that a host transport timeout stops the
owned device package, preserves partial evidence without replay, and prevents
the next consumer if stopping cannot be confirmed. They are not model experiments.
The initial complete suite passed **201 tests**. Source/import/manuscript and diff
checks passed; the 18 historical-locator warnings remain visible.

The subsequent [review fixes](REVIEW_FIXES.md) close three gaps in required-output,
invocation-binding and build-deadline enforcement. The current reader passes 111
checks on unchanged evidence and the expanded suite passes 222 tests. Original
readbacks/snapshots are preserved; this follow-up performs no model execution.

## Executed sources and post-run robustness review

External `initial-source/`, `generation-source/`, `runtime-source/` and
`execution-source/` preserve successive actual source snapshots. The protocol was
recorded before acquisition and the runtime plan/harness before compilation and
inference. Source copies and the per-stage command records preserve their identities;
the final PR tree is not retroactively claimed to have executed in full.

Post-run source review tightened two unused failure paths: acquisition now stops
immediately on its own byte/time bound, and the controller explicitly stops a
device package and collects partial evidence after a transport failure. Killing
host adb alone need not stop device inference. The real invocations completed
within 300 seconds, so neither path was exercised or rerun; original executed
controller/download sources remain retained. The two synthetic tests cover the
controller correction. A later offline read adds the complete graph descriptor
and each buffer's digest; it does not alter the original linkage inspection or
execute the model again.

## Retention and boundaries

The emulator was stopped after both collections; its owned PID had no live command
and port 5556 was closed. Selected raw evidence is archived and every selected
member is read back against its size/hash. The receipt identifies that archive and
manifest: 270 verified members, 65,231,419 compressed bytes. The archive SHA-256
is `cc0e3f43117099b8ba1c2a9327cfa5fca5cac6e09eca5aeb93d5bbc0e071d9f1`.
The receipt and final navigation/validation text postdate sealing; the archive
is not a snapshot of the final PR tree. SDK/AVD, Gradle distribution/cache and disposable signing key are excluded
from the selected archive and remain local; toolchain/generator identities are
recorded separately. This is local retention, not a complete offline package,
remote backup, anonymous reviewer access or human signoff.

No source import, prior execution record, sealed focal archive, manuscript source
or manuscript evidence pin was changed. #319, other inputs/configurations and a
LiteRT version comparison were not executed. The shortlist's one-configuration
scope is closed by these two observations; further execution requires a new plan.
