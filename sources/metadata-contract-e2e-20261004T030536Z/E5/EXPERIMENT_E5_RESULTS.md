# E5 results

The pre-flight command was applied to 65 byte-distinct fixtures; aliases to development, E1/E2 and external phases are retained. These are not independent models.

| Condition group (first alias) | Fixtures | Structural results | Decoder results |
|---|---:|---|---|
| prior/original | 11 | {'ACCEPTED_BY_METADATA_POPULATOR_0_4_4': 11} | {'INCOMPATIBLE': 5, 'INAPPLICABLE_NO_SELECTED_GETTER': 4, 'ABSTAIN': 1, 'COMPATIBLE_PRECONDITIONS': 1} |
| prior/description_control | 11 | {'ACCEPTED_BY_METADATA_POPULATOR_0_4_4': 11} | {'INCOMPATIBLE': 5, 'INAPPLICABLE_NO_SELECTED_GETTER': 4, 'ABSTAIN': 1, 'COMPATIBLE_PRECONDITIONS': 1} |
| prior/count_minus_one | 11 | {'REJECTED_BY_METADATA_POPULATOR_0_4_4': 11} | {'NOT_REACHED': 11} |
| prior/swap_first_different_shape | 8 | {'ACCEPTED_BY_METADATA_POPULATOR_0_4_4': 8} | {'INCOMPATIBLE': 4, 'INAPPLICABLE_NO_SELECTED_GETTER': 4} |
| prior/label_drop_1 | 5 | {'ACCEPTED_BY_METADATA_POPULATOR_0_4_4': 5} | {'INCOMPATIBLE': 4, 'ABSTAIN': 1} |
| prior/no_metadata_original | 2 | {'ABSTAIN_NO_METADATA': 2} | {'ABSTAIN_NO_METADATA': 2} |
| E1/label_restoration | 1 | {'ACCEPTED_BY_METADATA_POPULATOR_0_4_4': 1} | {'COMPATIBLE_PRECONDITIONS': 1} |
| E2/label_permutation | 1 | {'ACCEPTED_BY_METADATA_POPULATOR_0_4_4': 1} | {'COMPATIBLE_PRECONDITIONS': 1} |
| E4_external/original | 15 | {'ACCEPTED_BY_METADATA_POPULATOR_0_4_4': 15} | {'COMPATIBLE_PRECONDITIONS': 4, 'INCOMPATIBLE': 9, 'INAPPLICABLE_NO_SELECTED_GETTER': 2} |

## Detection and abstention

S accepts 52 fixtures, rejects the 11 count-reduction controls using the existing official population check, and abstains on two no-metadata originals. D flags 27 selected category paths, finds eight compatible under its stated static preconditions, marks 14 inapplicable, and abstains on three dynamic-signature Gesture fixtures. Eleven structurally rejected fixtures do not reach D. All 65 semantic judgments abstain because no independently supplied artifact-tied semantic reference is provided.

The dynamic-signature abstention is deliberately more conservative than the earlier isolated Gesture probes at concrete shape [1,8]. It includes the 7-label mutant whose isolated decoder already failed. This is a disclosed limit; the pre-flight command does not claim to detect every previously observed failure. The 15 external scope-filtered outcomes agree with the frozen E4 results; this is implementation agreement, not detector accuracy.

Among 4 distinct artifact conditions with actual successful E1/E2 Android getters, the command makes 0 incompatible/structural-rejection judgments. The real EfficientNet 999-label getter failure is flagged after generation and before compilation/loading/inference. Permutation is compatible under D, with semantic abstention.

Exact diagnostic: “Generated category getter getProbabilityAsCategoryList for output 0 is incompatible with the selected TensorLabel path because selected axis 1 has size 1000, which differs from label count 999.”

## Existing checks and earliest failures

The official MetadataPopulator already rejects count reductions. TensorLabel already throws at the failing generated getter; Task ImageClassifier already rejects the same deletion during initialization. E5 collects and moves the selected Java path precondition to pre-flight. For uncompilable wrappers, javac is already the first observed rejection; a D finding does not establish a prevented runtime failure there. Unsupported non-RGB fallback warnings remain visible.

The command emits separate STRUCTURAL, REFERENCE_BACKED_SEMANTIC, DECODER_COMPATIBILITY, PRESERVATION and UNKNOWN_ABSTAIN sections. It parses actual tensor and associated-file bindings and the understood default postprocessor. It makes no “model invalid” statement. Optional reference comparison verifies supplied bytes/digests and compares a supplied contract; source interpretation and artifact linkage require human verification, and this feature has no independently labeled semantic evaluation here.

CLI exits 2 for a demonstrated selected-contract incompatibility or official structural rejection, 3 for tool/generation errors, and otherwise 0 while retaining explicit abstentions. Exit 0 is not universal correctness. Compilation and inference are not performed by this static command.

## Usage

```bash
PYTHONDONTWRITEBYTECODE=1 /workspace/hand-contract-repro/.venv/bin/python scripts/preflight.py E1/variants/label_deletion/model.tflite --evidence-dir /tmp/new-preflight-evidence
```

The evidence directory must be new; old results are never overwritten. Exact code, generated sources, logs, aliases and machine results are under E5/.
