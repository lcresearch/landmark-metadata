# HA01–HA02 agent pre-audit: executable path and model attribution

**Agent verdict: SUPPORTED_WITHIN_INSPECTED_SCOPE. Human statuses: PENDING.** No contradiction to C2/C2R/C3/C6 was found in the checked source, final binary, packaging and saved primary-run attribution. This is a fresh static/readback audit, not a new build, inference, human signature, independent operator replication, or authentication of the historical executions.

Target repository head: `24f660cf093c3e52efc0cde0c39e7aea1df48053`. Short manuscript SHA-256: `c79ba7f62a194abd487ec4b8ccedb60428ec4edd1f43e6ee155518ffd8bb416e`. Both were freshly checked. The current short-paper crosswalk and HA01/HA02 checklist were read; historical reports supplied locators and context, not inherited verdicts.

## Exact scope and denominator

All evidence inputs below use the selected package root `/workspace/evidence-recovery-20261005T170453Z/package-v2/payload/`, except the explicitly inventoried installed disassembly tools and some dependency JARs at secondary original paths.

| Family relative to package root | Selected final builds and corresponding primary result records | Recorded input observations |
| --- | ---: | ---: |
| `metadata-contract-e2e-20261004T030536Z/{E1,E2}` | 8 wrapper phase/variant aliases | 16 |
| `metadata-contract-audit-20261004T062010Z/rebuild/{E1,E2}` | 8 separate construction-audit wrapper aliases | 16 |
| `metadata-contract-p2p3-20261004T073824Z/P2` | 5 conditions × 2 consumers = 10 | 18 |

This is 26 final APK paths / 26 primary records, with **20 distinct APK SHA-256 values**, five distinct model byte identities, and one historically specified focal graph. APK aliases, construction audits and input observations do not increase the independent-model denominator. This reviewer did not independently derive graph identity, compare numerical outputs, inspect replay records or inspect the initial unexecuted builds.

E1 aliases: original, description_control, label_deletion, label_restoration. E2 aliases: original, description_control, label_permutation, permutation_restoration. P2 aliases: original, description_control, label_deletion, label_permutation, restoration. Full path expansion and every checked hash are in `raw-checks.json` and `inspected-inputs.json` (510 distinct inspected input paths, including source/record/dependency/tool files). No sealed input was modified.

## Fresh executable inspection (HA01, C3/C2R)

Fresh `javap -c -p -s` inspected **all seven distinct application-class byte identities** present across these units: three generated model classes shared across the 21 wrapper units, three wrapper-harness identities (original, construction audit, P2), and the Task harness. Fresh `dexdump -d` inspected **all four distinct final DEX identities**; each selected APK's embedded DEX was freshly compared with its staged DEX. Disassembler commands and return codes are recorded in `commands.json`; every command returned 0. The full fresh disassemblies and selected class extracts are retained under `disassembly/`.

The generated Java SHA-256 is `60c1fb6022891cc2bd41b5bacdd2194361eb0ca40e37da2eddf6cba963279670`. The three generated class identities across all 21 wrapper builds are:

- `ContractModel.class`: `bbf74b8a5b53e2efa47986a11c99b6c52ef533c7c6f149f7032c09adc5059145`
- `ContractModel$Metadata.class`: `6fd67e5f9d764e833d0e8441850a708676dbd3128c736ffc72234742caf33e4b`
- `ContractModel$Outputs.class`: `947d1073a42002d3aaa070e37a498d9a65a8244c3468bf945116e6cb205fcf44`

The source and fresh class/DEX instructions support the actual path: the harness invokes `ContractModel.newInstance(context, "model.tflite", options)`, then `process(TensorImage)`, then `Outputs.getProbabilityAsCategoryList()`. Generated `process` allocates Outputs, preprocesses the input and calls `Model.run` with output buffer 0. The actual getter uses the stored label list and postprocessed probability TensorBuffer to construct the **list-based TensorLabel**, then calls its `getCategoryList`; the handwritten top-five observation does not provide the returned categories.

Metadata selects output tensor metadata 0, associated file 0, its filename, `MetadataExtractor.getAssociatedFile`, then `FileUtil.loadLabels`. The generated default probability postprocessor contains `DequantizeOp` using the output quantization parameters. Thus the audit retains the real postprocessing/resource selection rather than treating the getter as a bare label-count test. This static review did not independently execute that postprocessor.

The raw observation is nonmutating within the inspected code path. `Outputs.getBuffer` creates a HashMap containing `probability.getBuffer()` at key 0. The exact bundled `TensorBuffer.getBuffer` consists solely of loading its buffer field and returning it in every inspected DEX: no rewind, clear or write occurs before duplication. The harness invokes `duplicate`, applies order/rewind to the duplicate, and reads it into a new byte array. Top-five processing uses a new float array from that copy. The generated getter receives the original TensorBuffer. A duplicate shares backing storage and is not intrinsically read-only; the relevant evidence is the absence of backing writes and original-buffer position changes on this observation path.

DEX identities are deliberately distinct across families:

| Scope | Final DEX SHA-256 |
| --- | --- |
| Original eight builds | `82ae7e4dafaeba6a1dcc4be479693cd1eb9cfc02ff04f661e801ac0466c5ee99` |
| Construction-audit eight builds | `b5ce8404d0d7b197c1532003e934d7cb32d381aed47c7af2201044e89a50c821` |
| P2 five wrapper builds | `4b8c5a96fcdb8c4f61c1007bf35f267fb629e9d21b8f2a41734d5de3b75467d3` |
| P2 five Task builds | `f46fd408e94d6b85eb3ba38c0fefcb01195312e38f88ad2caddf954fc3f58782` |

Original/rebuild full-DEX equality is not asserted. The original compiled-path evidence does not substitute for the separate construction audit: its own harness classes, DEX, APKs, records and preload reads were examined.

## Fresh model and install attribution (HA02, C2/C2R/C3/C6)

For all **26/26** final units, freshly read working `model.tflite`, staged `assets/model.tflite`, and the APK's ZIP member `assets/model.tflite` are byte-identical. The distinct condition identities are:

| Condition | SHA-256 |
| --- | --- |
| Original | `6c7ab0a6e5dcbf38a8c33b960996a55a3b4300b36a018c4545801de3a3c8bde0` |
| Description | `ed16d9573d8fe3e489c27637036a4e5c8476d15f013b7116f89864d55432f51d` |
| Deletion | `739f08462e831806db6a9bce7ed5b70a037fce593003028e5d6911dbd284fd83` |
| Permutation | `455a04a2c6193ea81bef8fbc47e193aee0449b8cebdc9cc487c7e9e85fe42da7` |
| All restoration aliases | `0a605ed10a38fc6f92fc4e266f5560756d2809e2669c45aa3b5a631cd88cea72` |

Each saved install command names the corresponding selected final APK, exits 0 and has `Success` in saved stdout. Each instrumentation command uses the expected variant and package/instrumentation component. Fresh `aapt dump xmltree` parsed the **actual binary manifest in all 26 APKs** and confirmed its package, instrumentation class and targetPackage match the saved command (26/26). These manifest commands and outputs are in `commands-manifest.json` and `disassembly/manifest-*.txt`; this is stronger than matching only a staged XML source.

All selected compile/dex/package/sign/verify command records report exit 0. Historical final-build identities for original/P2 and the construction-audit `results.json` match the freshly read identities for all 26 units. P2 static model hashes also match all ten consumer/condition units. This tests consistency with saved records; it does not independently attest that those commands ran at their recorded times.

All **18/18 later records** (eight construction-audit, ten P2) report an AssetManager read whose hash equals the working/staged/APK model hash. Source and fresh harness class/DEX inspection show that the read occurs before construction and uses the same context and asset name subsequently passed to the real consumer. **All eight original records lack this preload observation**, consistently with the original harness. The later read is not an intercepted native-interpreter buffer.

Seventeen dependency JAR paths referenced by the final DEX command records were freshly hashed, using the selected package when present and explicit secondary original absolute paths otherwise; none was missing at those checked paths. `record-comparisons.json` records each path and provenance. This does not independently identify the Task library's embedded native interpreter or validate the full dependency supply chain.

## Limits and precise human continuation

- This audit supports saved-byte/code-path/record consistency. No separately device-pulled installed APK, device state, native model buffer, new APK build, emulator or inference was inspected or produced. No authentication of the historical installation beyond saved commands/results is claimed.
- Source and binary agreement here is static inspection plus archived command linkage, not an independent source-to-binary rebuild. Detailed raw-score/list comparisons and graph/resource preservation belong to the other checklist items.
- No new discrepancy or manuscript correction was identified within this scope. Replay and interrupted attempts were excluded explicitly, rather than silently counted as success. Human statuses remain PENDING.
- The human should select and record the original E1 deletion unit and its separate construction-audit counterpart, open their generated getter plus the appropriate fresh class/DEX extracts, and trace the observations through each unit's own `device/result.json` and saved install/instrumentation commands. Review the 26-row identity table and all three restoration aliases explicitly. Then decide whether saved-record attribution is sufficient for the intended claim; direct installed-APK/native-buffer evidence is outside this audit and must not be implied. Record the frozen manuscript digest above and a separate human conclusion.

Reproduce this read-only audit with the two commands in `commands-reproduce.sh`. These scripts write only under this reviewer directory. They do not execute model code.
