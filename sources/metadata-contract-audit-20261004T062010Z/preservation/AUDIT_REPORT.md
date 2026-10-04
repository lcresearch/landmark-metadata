# E1/E2 preservation and executed-interface artifact audit

**Overall: PASS for the bounded checks of retained artifacts.** No contradictory graph, weight, code, tensor, label, or restoration evidence was found. This is a fresh AI-agent audit of existing local evidence, not a new inference run, independent researcher reproduction, or human audit. The source evidence was read only; no emulator was started and no sealed artifact was changed.

## Scope and reproducible commands

Evidence root: `/workspace/metadata-contract-e2e-20261004T030536Z`.
Audit root: `/workspace/metadata-contract-audit-20261004T062010Z/preservation`.

The new `audit_preservation.py` does not import or invoke the study's checker, canonicalizer, preparation, mutation, or summarization scripts. It directly parses the original model bytes with the generated FlatBuffer schema; reads associated ZIP files and APK entries; hashes Java/classes/DEX; unpacks every saved raw float tensor; and reconstructs labels, score bits, stable top-five positions, and reversals from decoded JSON and the actual label resource. It uses no TensorFlow Lite interpreter.

Final command, executed with the preserved Python environment:

```bash
PYTHONDONTWRITEBYTECODE=1 /workspace/hand-contract-repro/.venv/bin/python /workspace/metadata-contract-audit-20261004T062010Z/preservation/audit_preservation.py > /workspace/metadata-contract-audit-20261004T062010Z/preservation/audit.stdout 2> /workspace/metadata-contract-audit-20261004T062010Z/preservation/audit.stderr
```

The script was rerun after adding the whole-file description-byte check and clarifying record-count terminology; these are artifact-reading passes, not additional model executions. `results.json` records the exact final script hash, interpreter command, schema-module paths/hashes, 180 inspected-file hashes, all checks, per-buffer hashes, ZIP member hashes, APK member hashes, and every observation. Full independent bytecode commands are recorded in `bytecode/commands.json`, with fresh disassembly in that directory.

## Recomputed results

- **PASS — preservation:** all eight phase/variant model paths (five distinct artifact byte sequences) have the same independently normalized computation/weight/schema fields. Each model has 166 buffers; buffer 165 is TFLITE_METADATA, is not referenced by any graph tensor, and the other 165 buffers are byte-identical. The new normalization removes the metadata entry and clears only its payload, without reusing the study's canonicalizer. Its digest is `9bf2f59a285519dd62e62941041ad60925376c4bcd2a88433166d25499e818b8`; this deliberately differs in format from the study's canonical hash.
- **PASS — label interventions:** deletion/permutation/restorations preserve the entire 18571560 byte pre-ZIP prefix, including embedded metadata. Their embedded metadata SHA-256 is `8608ff0e1650d5d7d2d841fb722e91b503730cde0fd7bfa1c2c67acaaa594ecb`. Deletion removes exactly the final label from the interpreted list; permutation is exactly the predetermined left cyclic shift and retains the multiset. Both restorations restore the original associated payload bytes.
- **PASS — description control:** exactly one byte differs in the entire model, and exactly one byte differs in embedded metadata. The association resource remains unchanged. Thus embedded-metadata equality is not incorrectly claimed for this control.
- **PASS — packaging:** every final APK's `assets/model.tflite` equals its working model and staged asset byte for byte; every APK `classes.dex` equals the corresponding build DEX. All eight generated Java files, all four class files per build (including the harness), and DEX are identical across conditions. Pre-dependency-closure builds are excluded from the executed-artifact comparison.
- **PASS — recorded numerical observations:** 16 complete **phase/run/variant records**, including primary and same-environment replay/recovery, supply 32 raw-output observations. These are repeated records, not 16 independent experimental units or models. Every saved RGB input equals its independently reconstructed prescribed bytes. Each output contains 1,000 finite float32 values. Every raw array is byte-identical to the original for the same input; every recorded top-five list reconstructs from raw bits with a stable index tie break.
- **PASS — decoded values:** all 28 successful lists contain 1,000 categories. Every list position is sequential, the Java category index remains -1, and all 28,000 recorded score bit patterns match the corresponding raw positions. JSON numeric scores round-trip to those same float bits. Every label equals the matching position of the actual APK/model label resource.
- **PASS — association change and reversal:** each permutation observation has exactly 999 changed label strings. Position 638 retains `maillot` because original positions 638 and 639 are duplicates. For `rgb_pattern`, position 904 preserves score `0.23542051017284393` (bits 1047597587) while `window screen` becomes `window shade`; for `gray127`, position 649 preserves `0.001122338930144906` (bits 982719346) while `megalith` becomes `microphone`. Every non-permutation successful decoded file, including both restoration kinds, is byte-identical to the original's decoded JSON for that input.
- **PASS — deletion boundary in retained records:** four deletion observations (two inputs in primary/replay) have raw tensors after successful inference, no decoded-list file, and the exact caught `IllegalArgumentException: Label number 999 mismatch the shape on axis 1` with the generated getter on the stack. No claim of an uncaught application crash is made.

The raw-artifact runner reports **655 PASS checks, zero FAIL checks**. These are assertions over retained records, not independent statistical samples.

| Model path | Labels | Recomputed SHA-256 |
|---|---:|---|
| E1 / description_control | 1000 | `ed16d9573d8fe3e489c27637036a4e5c8476d15f013b7116f89864d55432f51d` |
| E1 / label_deletion | 999 | `739f08462e831806db6a9bce7ed5b70a037fce593003028e5d6911dbd284fd83` |
| E1 / label_restoration | 1000 | `0a605ed10a38fc6f92fc4e266f5560756d2809e2669c45aa3b5a631cd88cea72` |
| E1 / original | 1000 | `6c7ab0a6e5dcbf38a8c33b960996a55a3b4300b36a018c4545801de3a3c8bde0` |
| E2 / description_control | 1000 | `ed16d9573d8fe3e489c27637036a4e5c8476d15f013b7116f89864d55432f51d` |
| E2 / label_permutation | 1000 | `455a04a2c6193ea81bef8fbc47e193aee0449b8cebdc9cc487c7e9e85fe42da7` |
| E2 / original | 1000 | `6c7ab0a6e5dcbf38a8c33b960996a55a3b4300b36a018c4545801de3a3c8bde0` |
| E2 / permutation_restoration | 1000 | `0a605ed10a38fc6f92fc4e266f5560756d2809e2669c45aa3b5a631cd88cea72` |

## Independent source and APK-bytecode checks

See `bytecode/report.md`, `bytecode/results.json`, and preserved `javap`/`dexdump` outputs for the separate source/bytecode audit.

**PASS — raw-output observation is non-mutating at the inspected APK-bytecode boundary.** The actual harness invokes `ContractModel.newInstance`, `process(TensorImage)`, and `Outputs.getProbabilityAsCategoryList`. `Outputs.getBuffer()` allocates a map and retrieves the tensor's buffer. The exact APK implementation of `TensorBuffer.getBuffer()` only returns that field: it does not rewind or change its position. The harness then duplicates the returned ByteBuffer and changes order/position and reads bytes only on that duplicate; it does not write tensor bytes. The generated getter constructs the actual library `TensorLabel` and calls `getCategoryList`; it does not substitute a handwritten decoder. The separate bytecode report records method instructions and source/DEX paths.

## Counterevidence searched and reporting hazards

1. **Whole-file restoration equality is false.** Both restorations have digest `0a605ed10a38fc6f92fc4e266f5560756d2809e2669c45aa3b5a631cd88cea72`, different from the publisher original, although associated payloads, the entire pre-ZIP prefix, computation, code, and observed decoded behavior are restored. The container bytes must not be described as restored wholesale.
2. **The original E2 replay restoration attempt is incomplete and unclassified.** It has no recovered device result. The separately retained recovery supplies the complete restoration record; the partial attempt is neither a consumer pass nor fail. `results.json` explicitly records it as UNVERIFIABLE / UNCLASSIFIED_INCOMPLETE_ATTEMPT.
3. **Logcat files are cumulative dumps.** Later successful runs can contain earlier deletion exception text. Presence of that text in a dump is not evidence that the current variant failed. The bytecode/log audit uses the recorded instrumentation-to-logcat time window (and process information where present) to attribute current exceptions, together with the per-run device record. Current-window exceptions occur only in deletion primary/replay. The time-window limitations are documented by that audit.
4. **Deletion has no decoded value.** A generic earlier summary's true decoded-equality flag is vacuous for deletion. This audit never compares absent deletion decoded lists and records that field as not applicable due to exception.

## What remains unverifiable here

- Historical execution provenance cannot be independently established by rereading local files. The APK assets and retained install commands can be checked, but no independently device-pulled installed APK was used as a second source of installed-byte identity.
- No independent class-order reference is established. The association change is relative to the retained original labels; correctness, accuracy degradation, or harmful classification is not inferred.
- Two synthetic inputs and one retained runtime configuration do not establish invariance for all inputs or environments. Replays are same-environment observations.
- The generated schema package is a shared parser dependency, with its path/hash recorded; this is not an independently implemented FlatBuffer parser. Exact prefix equality for associated-file interventions and the one-byte whole-file description diff independently restrict the mutation surface.
- This audit does not rerun structural MetadataPopulator acceptance, perform new model inference, build a new APK, or complete the pending independent human audit.
