# Human audit — pending

No item below has been independently verified by a human. Checkboxes remain empty until a real reviewer records name, date, inspected evidence and conclusion. An AI-run hash check is not human verification.

- [ ] Confirm the original manuscript, frozen manifest and old evidence archive identities against CURRENT_STATE.md and phase0/results.json.
- [ ] Inspect exact EfficientNet original model provenance and digest; compare associated label deletion/restoration/permutation bytes and filenames.
- [ ] Independently calculate canonical graph, non-metadata buffer, metadata table and pre-ZIP-prefix equality from raw model bytes.
- [ ] Compare generated Java and actual compiled class bytes across variants; inspect package dependency versions and DEX records. Do not use APK inequality as a code-change claim.
- [ ] Inspect the Android instrumentation source and bytecode: loading, inference and decoding must call the real generated interface. Verify raw-output observation does not replace or alter the getter.
- [ ] Inspect original, description, deletion and restoration stage records, device logs and exact stack traces. Confirm the earliest failure stage.
- [ ] Compare saved input and raw output tensors byte-for-byte; check labels and numeric scores by output position for permutation and restoration.
- [ ] Confirm an independently tied class-index reference exists before claiming original or mutant semantic truth. Otherwise require explicit abstention.
- [ ] Check exact Hand SHA-256, graph output order, metadata names, source-reference revision and artifact-version linkage. Distinguish association, scalar handedness representation, decoder suitability and coordinate normalization.
- [ ] Inspect disclosed Hand syntax repair and javap association evidence. Do not infer a complete repair from swapping metadata entries.
- [ ] Check corpus denominators, exclusions, previously inspected candidates, frozen protocol time/hash and natural-versus-seeded findings before interpreting external validation.
- [ ] Verify no claims of prevalence, general detector accuracy, task accuracy or deployed application impact exceed collected evidence.

## Exact inspection route

| Claim to audit | Primary evidence |
|---|---|
| E1 actual generated call and earliest exception | `scripts/ContractInstrumentation.java`; `E1/variants/*/generated/src/main/java/org/example/contract/ContractModel.java`; `E1/executions/primary/label_deletion/device/result.json`; both `primary` and `replay` logs |
| Model, metadata, label payload and compiled-code equality | `E1/static-results.json`, `E1/build-results.json`, `E2/static-results.json`, `E2/build-results.json`; raw models/associated files, generated classes and DEX under each `variants/*` directory |
| Raw output equality and successful permutation | `E1/executions/*/*/device/*-output-0.f32`; `E2/executions/primary/*/device/*-decoded.json`; `E2/results.json`; `phase0/pre-E2-freeze.json` |
| E2 replay completeness | `E2/deviations.json`; three completed `executions/replay` units and the separately identified restoration recovery; do not mark the interrupted attempt successful |
| Official classifier's earlier rejection and shared implementation boundaries | `E3/executions/primary/label_deletion/outputs/result.json`; `E3/sources/`; `E3/implementation.json`; `E3/results.json` |
| Frozen external denominator and abstentions | `E4/prevalidation-freeze.json`; `E4/protocol/candidates.json`; `E4/results.json`; `E4/summary.json`; source warnings and javac failures |
| Pre-flight interpretation and known limits | `E5/preflight.py`; `E5/results.json`; dynamic-signature Gesture abstentions; `EXPERIMENT_E5_RESULTS.md` |
| Hand exact source/graph bridge | `E7/REFERENCE_CHAIN.md`; `E7/sources/external_files.bzl`; `E7/source-pinned-assets.json`; `E7/source-component-equivalence.json`; `E7/sources/immutable-commit-source-verification.json` |
| Hand generic association versus actual Task behavior | `E7/binding-audit.json`; `E7/binding-audit/*/fresh-outputs-javap.stdout`; `E7/results.json`; `E7/executions/{primary,replay}/*/outputs/`; `E7/original-role-reference.json` and `E7/metadata_exchange-role-reference.json` |

- [ ] Verify that source-pinned Hand component `11c272…` and focal `6acda7…` are different files with a documented graph/weight bridge, not an asserted exact-hash source pin.
- [ ] Check the system-image revision discrepancy, vacuous failed-decoder replay field and separately unknown embedded Task runtime versions in `REPORTING_CLARIFICATIONS.md`.
- [ ] Run `bash commands.sh verify` and inspect its output; automated verification alone must not check off any human-review item.

For each completed human item, append reviewer name, UTC date, exact inspected paths/hashes, independent method, conclusion and unresolved objections. No human reviewer has yet supplied such a record.
