# Fresh Android E1/E2 reconstruction and audit

Completed UTC: 2026-10-04T08:23:25.990386+00:00. Status: strict verification PASS. This is an agent reconstruction from public downloads, not independent human verification.

All 16 planned variant/run records completed: 16 successful model initializations and 32 successful input/inference observations, 28 successful 1,000-category lists, and 4 caught expected label-deletion getter exceptions. There are eight phase/variant configurations repeated once, five distinct model byte conditions, and one independently recomputed canonical graph. Do not count phases, mutations, inputs or replay as independent models.

| Phase | Variant | Primary load/inference/getter | Replay load/inference/getter |
|---|---|---|---|
| E1 | original | PASS/PASS/PASS | PASS/PASS/PASS |
| E1 | description_control | PASS/PASS/PASS | PASS/PASS/PASS |
| E1 | label_deletion | PASS/PASS/FAIL | PASS/PASS/FAIL |
| E1 | label_restoration | PASS/PASS/PASS | PASS/PASS/PASS |
| E2 | original | PASS/PASS/PASS | PASS/PASS/PASS |
| E2 | description_control | PASS/PASS/PASS | PASS/PASS/PASS |
| E2 | label_permutation | PASS/PASS/PASS | PASS/PASS/PASS |
| E2 | permutation_restoration | PASS/PASS/PASS | PASS/PASS/PASS |

## Actual findings

- E1 deletion loads 999 labels and completes both inputs; the real generated `getProbabilityAsCategoryList()` throws `java.lang.IllegalArgumentException: Label number 999 mismatch the shape on axis 1`. The stack includes the generated getter. The instrumentation catches it; this is not an application-crash observation.
- E2 permutation returns 1,000 categories successfully. Both primary and replay preserve all raw outputs and score bits and change exactly 999 displayed labels under the declared cyclic mapping; restoration returns the original lists. No independent class-order reference was added, so this remains an exposed association change rather than an accuracy/error claim.
- Across all 32 observations, raw tensors match the original corresponding input byte-for-byte. Working models, packaged APK assets and pre-initialization AssetManager reads agree. The native interpreter buffer was not intercepted.
- All 165 non-metadata buffers match; label conditions preserve embedded metadata and the pre-ZIP prefix. The description control changes exactly one case bit in the parsed output-tensor description. Normalizing only TFLITE_METADATA yields canonical graph SHA-256 `73e57df01115600419abb72de4b2c3257200e12eb205d335bcbfc203a589bee8`.
- The strict auditor rereads all generated Java, generated/harness classes, DEX, APK DEX and native libraries. Code matches across all eight fresh builds; execution build snapshots and successful install-command targets match those audited APKs. No equality to unavailable historical binaries is claimed.

| Input | Top index | Exact original score | Float bits | Original label | Permuted label |
|---|---:|---:|---:|---|---|
| gray127 | 649 | 0.001122338930144906 | 982719346 | megalith | microphone |
| rgb_pattern | 904 | 0.23542051017284393 | 1047597587 | window screen | window shade |

## Toolchain and setup outcomes

Freshly recovered exact versions: Temurin 17.0.12+7; Support/generator 0.4.4; Java/native TFLite 2.13.0; SDK platform API 30 r3; build tools 35.0.0; platform tools 37.0.1; emulator 37.2.12/build 16428233; x86_64 default system-image archive r11 (internal properties r10). SDK official SHA-1/size plus pinned SHA-256 and JDK official SHA-256 were checked. All 17 SDK/JDK/Java archives and extracted jars passed an explicit-exception integrity recheck.

The primary software AVD booted in 537.7 seconds and ran all successful primary/replay records. A second cold-boot AVD reported `sys.boot_completed=1` after 723.9 seconds but suffered SystemUI ANR/system_server restarts. Four APK installs failed because the package service was absent. No model stage ran in those attempts. Its complete failed evidence remains at `/workspace/repro-android-replay`, and the AVD was stopped. All required replay was then executed in the stable primary AVD; these four setup failures are excluded from model observation counts.

The historical runner exits 0 even after installation/harness failures; stage JSON and the strict auditor determine outcome. Startup property alone also proved insufficient. The new source helper checks package/activity responses and three stable system_server observations. It passed on the primary AVD and failed on an absent serial. The updated startup composition was generated/compiled but was not retrospectively claimed to have governed the earlier boots.

E2 used the preserved audit `prepare_e2.py`, which gates on completed E1 primary, enabling overlap with the attempted second-device replay. The mutation and generation code was unchanged, and all required replay was subsequently completed. Details: `E2_PROTOCOL_ADAPTATION.json`.

The source-only restoration helpers were tested with fresh official XML selection, complete second extraction into an independent smoke directory, version execution for JDK/ADB/D8/aapt2, cache integrity, repository-output guards including symlinks, and stale-PASS invalidation. Evidence: `prerequisites/helper-validation.json`.

## Evidence and boundaries

- Strict audit: `audit-results.json`; model preservation: `model-preservation-audit.json`.
- Phase summaries: `E1/results.json`, `E2/results.json`; original stage data: `E1|E2/executions/{primary,replay}/<variant>/device/`.
- Build data: `E1|E2/build-results.json`, actual generated sources/classes/DEX/APKs under `variants/<variant>/`.
- Public package provenance: `prerequisites/downloads.json`, `java-dependency-restoration.json`, selected XML, and `source-export/android-prerequisites.lock.json`.
- Secondary-AVD setup failure: `/workspace/repro-android-replay/FAILURE_REPORT.md` and `SETUP_FAILURE_SUMMARY.json`.

P2 Android Task comparison was only prepared and not executed in this branch of work; no new P2 result is claimed. Cross-platform E3 limitations, absent artifact-tied semantic reference, one controlled graph/two fixed inputs, and pending human audit remain. Full binaries and execution evidence stay outside the source-only repository. The owned primary emulator was stopped after verification; `prerequisites/emulator-termination.json` records cleanup.
