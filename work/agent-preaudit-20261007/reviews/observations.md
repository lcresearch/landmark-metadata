# HA04–HA06 agent pre-audit of saved observations

**Agent review only. All human statuses remain PENDING.** HA04 and HA06 saved-observation checks are **SUPPORTED_WITHIN_INSPECTED_SCOPE**. HA05 full permutation/reversal observations are **SUPPORTED_WITHIN_INSPECTED_SCOPE**; independent historical predeclaration chronology is **PARTIAL**. No contradiction was found in the inspected experiment observations. This is fresh readback/computation over saved evidence, with no model generation, build, emulator, or inference execution.

Target: `/workspace/landmark-agent-preaudit/work/workshop-convergence-20261007/manuscript/paper.tex`, SHA-256 `c79ba7f62a194abd487ec4b8ccedb60428ec4edd1f43e6ee155518ffd8bb416e`; protocol frozen head `24f660cf093c3e52efc0cde0c39e7aea1df48053`. HA04–HA06 and the current crosswalk were read. Claims inspected: C2 numerical portion, C2R saved observation comparison, C3, C4, C6. APK/model attribution and compiled-call verification are separate reviewers' scopes.

## Exact scope and denominator

All primary observations below were independently enumerated, read, hashed and parsed. Preserved summary booleans were not used as replacements for these computations. There is one graph, with five model byte conditions; phase aliases and repeated inputs are not additional models.

| Family | Phase/consumer configurations | Actual input observations | Raw wrapper tensors | Successful lists | Categories read |
| --- | ---: | ---: | ---: | ---: | ---: |
| Original E1/E2 primary | 8 | 16 | 16 | 14 | 14,000 |
| Separate historical construction audit primary | 8 | 16 | 16 | 14 | 14,000 |
| P2 primary, wrapper + Task | 10 | 18 | 10 | 16 | 16,000 |

Root `B` is `/workspace/evidence-recovery-20261005T170453Z/package-v2/payload/`.

- `E = B/metadata-contract-e2e-20261004T030536Z/`
- `A = B/metadata-contract-audit-20261004T062010Z/rebuild/`
- `P = B/metadata-contract-p2p3-20261004T073824Z/P2/`

Original/rebuild units are `{E,A}/{E1,E2}/executions/primary/<variant>/`. E1 variants: `original`, `description_control`, `label_deletion`, `label_restoration`; E2: `original`, `description_control`, `label_permutation`, `permutation_restoration`. P2 units are `P/executions/primary/{wrapper,task}/<variant>/`, with `original`, `description_control`, `label_deletion`, `label_permutation`, `restoration`.

For each unit, inspected `device/result.json` and `logs/{instrumentation.command.json,instrumentation.stdout,logcat.stdout}`. For each actual input, inspected `device/<input>-input.rgb`, each available `*-output-0.f32`, and complete successful `*-decoded.json`. Inputs are exactly `gray127` and `rgb_pattern`; Task deletion has neither. `findings.json` lists all 26 exact unit paths, every comparison, observed stages, commands, log attribution and 260 freshly hashed objects, including the four extracted E2 resource members. It distinguishes 256 files from four member-byte identities; this is not full-package authentication.

## Newly computed comparisons

The new standard-library helper reconstructs all 150,528 bytes of each 224×224×3 RGB input from the documented formulas, then compares bytes and independently computed SHA-256 with saved input bytes and recorded hashes. Gray is byte 127; pattern byte `i` is `(37*i+17)&255`.

| Object (same across inspected matching inputs) | SHA-256 |
| --- | --- |
| gray127 RGB | `0748107f4221d0bb4ed8bada6a865b9348fb3b2a4c83b46f8e5eee704078b0ca` |
| rgb_pattern RGB | `fb23d2aecf5083dd57637ecebd7e80993a33af2561208c4cdd732cfe9249052f` |
| gray127 raw 4,000 bytes | `ac9f6cf6bee6c65a3aad87075a805662ae607af58f04f06fc64aff5dd4c36784` |
| rgb_pattern raw 4,000 bytes | `940add8f7e0f1da3ed8e699296a53e1fcba6b7f974a393b2ee4f137a24da7cc5` |

All 42 saved wrapper raw tensors are exactly 1,000 little-endian float32 values, all finite. Full bytes match their own family/phase baseline, including deletion. The 16 construction-audit observations match corresponding original primary input bytes, raw bytes and complete decoded values/absence. Every successful wrapper list has exactly positions 0–999 and Category index `-1`; all 36,000 wrapper returned score bits and serialized scores match raw floats at list position. No absent deletion list was counted as a decoded success.

Top five were recomputed from all raw floats: gray `[649,979,977,445,984]`; pattern `[904,556,318,632,753]`. Recorded indices, float scores and bits agree throughout. Across all successful conditions, all 1,000 strings and bits were compared to their own baseline. Controls/restorations match; permutation equals the exact one-position left rotation. Exactly 999 strings differ, with only index 638 unchanged (`maillot`). Pattern index 904 retains score `0.23542051017284393` / bits `1047597587` while `window screen` changes to `window shade`. This witness supplements full comparison; it does not replace it.

Four saved E2 `variants/<variant>/model.tflite` ZIP members were independently read. The filename is `labels_without_background.txt`; each has 1,000 strings. Complete members agree with returned lists. Permutation preserves full multiset and exact left shift; restoration recovers original labels. Model/ZIP preservation beyond the selected resource belongs to HA03.

P2 has eight successful shared condition/input pairs. Each Task result contains exactly one head with a bijection of class indices 0–999. Sorting Task entries by `category_index_field` and pairing with wrapper list positions gives equality for every label, score bit and serialized score (8,000 aligned categories). Task display names are empty. Task's returned first five class indices match recomputed wrapper raw top five for all eight pairs. This does **not** observe or establish equality of native Task raw tensors.

## Preserved stage records and their corroboration

The stage narrative is historical recorded evidence, not a new execution. Each of the three wrapper deletion configurations (original E1, rebuild E1, P2) has two actual inputs, successful load/process/raw observation records and a 4,000-byte raw file, followed by the actual getter exception:

`java.lang.IllegalArgumentException: Label number 999 mismatch the shape on axis 1`

All six failure stacks include `SupportPreconditions.checkArgument`, `TensorLabel.<init>`, `ContractModel$Outputs.getProbabilityAsCategoryList` and harness frames. The getter is the earliest recorded failing stage. No decoded file or category count exists for those failures. Instrumentation commands exited zero because the harness catches errors and calls `finish(0, ...)`; this is not an application-crash observation.

Cumulative logcat was filtered to the command's recorded start time and matching `ContractEvidence` failures. Original deletion: command 03:26:48 UTC, PID 2995, errors 03:27:19 and 03:27:44. Rebuild: command 06:34:11, PID 2883. P2 wrapper: command 07:56:56, PID 3130. Each has two attributed getter errors. This attributes available timestamp/PID records; it is not independent runtime authentication or device clock attestation.

Task deletion fails at `ImageClassifier.createFromFileAndOptions`, before the input loop, with the complete recorded public cause chain:

1. `IllegalStateException: Error getting native address of native library: task_vision_jni`
2. Cause `IllegalArgumentException: Error occurred when initializing ImageClassifier: Got 1000 class(es) for output index 0, expected 999 according to the label map.`

Its stack includes the Java constructor boundary and `initJniWithModelFdAndOptions`. P2 Task command starts 08:02:28 UTC; logcat at 08:02:35, PID 3431, corroborates the complete chain. There are zero Task deletion input files, raw files, decoded lists or actual observations: 18 actual P2 inputs out of 20 planned, rather than 20 observed inputs.

All P2 records identify API 30 and the same Android x86_64 build fingerprint; command selectors use emulator-5554. Saved emulator configuration identifies `research30`, port 5554, API-30 x86_64 system image; source sets one CPU thread, Task maxResults 1000. The timestamped execution freeze precedes all ten recorded instrumentations; selected source/dependency/plan freeze identities were freshly checked. These are same-environment record/source checks. They do not isolate differing native integrations, identify Task's bundled interpreter version, or decompose Task's atomic `classify` boundary. Working/APK/preload model identity is outside this review and must be reconciled with HA02.

## Chronology, limitations and audit-helper correction

See `chronology.md` for the separately delegated read-only agent chronology subcheck with exact hashes. Plan bytes match `phase0/pre-E2-freeze.json`; the plan prescribes a fixed left shift. However the freeze JSON contains a hash and an assertion, **no timestamp**. Original-root mtime precedes E1 instrumentation, but mutable local metadata and deterministic source do not independently prove historical predeclaration. Chronology remains PARTIAL. The later runner differs only by the disclosed recovery-selection filter. The interrupted E2 replay restoration remains incomplete; separate recovery is not substituted into its status. Replay numerics were not included in this primary-only audit.

The first version of this new helper incorrectly expected ZIP filename `labels.txt`, producing four check failures despite successfully parsing the actual sole member. Inspection showed the preserved name `labels_without_background.txt`; the helper expectation was corrected. The initial stdout is retained as `check-initial-helper-assumption.stdout`. The initial detailed JSON was overwritten during rerun; `initial-helper-reexecution/` contains the reconstructed original helper and its separately rerun JSON/stdout, explicitly not the initial saved JSON. No preserved input was changed. The final helper reports **784 checks, zero failures**; check count is not a reliability statistic or independent replication count.

No old aggregate PASS, later reconstructed `/workspace/repro-*` record, or missing Task raw output was substituted for required data. Historical provenance/authenticity beyond inspected bytes is not newly established. This review neither changes human verdicts nor validates source authority, stable IDs, task accuracy, natural defects, prevalence or production crashes.

## Next human action

Inspect the exact source calls/compiled path and APK attribution through HA01–HA03, then independently open the enumerated deletion stacks and command/time/PID records, repeat or review full-byte/list comparisons and Task index alignment, and assess whether available local chronology supports the intended predeclaration wording. Inspect HA07 before interpreting E2 as reference-disagreeing display association. Sign only the human template after personal review; all human fields remain PENDING.
