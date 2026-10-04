# Research extension: verified outcomes

The principal evidence gap is closed for one pinned generated Android interface: the label-deletion failure is reached through the actual generated public getter after successful model loading and inference. This is a controlled injected failure, not a newly discovered natural EfficientNet defect.

The existing manuscript and preserved evidence remain unchanged. [CURRENT_STATE.md](CURRENT_STATE.md) records the starting state; it is deliberately a **pre-E1 snapshot**, not the final status. [results.json](results.json) indexes the completed phases. Each phase has a plan, results, machine records, exact command logs, source/build/runtime evidence and its own immutable SHA256SUMS.

| Experiment | Observed result | Evidence and boundary |
|---|---|---|
| E1: actual generated interface | Original, description control and label restoration return 1,000 categories. Deletion to 999 labels loads and infers, then the actual generated getter throws `IllegalArgumentException: Label number 999 mismatch the shape on axis 1`. | [E1 results](EXPERIMENT_E1_RESULTS.md), [machine records](E1/results.json). Android API 30 x86_64 software emulator; unmodified Support 0.4.4 generated Java, TFLite 2.13.0. Graph/weights, embedded metadata for deletion/restoration, generated source/classes/DEX and both tested raw outputs are preserved. |
| E2: fixed cyclic label permutation | All stages succeed. Raw outputs, scores and top-k indices stay identical, while 999 of 1,000 exposed label strings change. The inverse permutation restores the original result. | [E2 results](EXPERIMENT_E2_RESULTS.md), [machine records](E2/results.json). Same label multiset and filename. One position retains the same string because adjacent original entries both say `maillot`. No independent class-order reference: this is association change relative to original, not established semantic error. |
| E3: official Task comparison | The identical deletion model is rejected by Task ImageClassifier 0.4.4 at initialization, before inference. Original, description and permutation succeed. | [E3 results](EXPERIMENT_E3_RESULTS.md), [stage matrix](E3/results.json). Actual Python/C++ Task API on Linux versus actual generated Java on Android; both consumer and platform differ. Android Studio was not evaluated. |
| E4: frozen external rules | 20 fixed candidate URLs, 16 downloads, 4 unavailable candidates; after prior-component/graph exclusions, 15 new canonical groups. All 15 structural checks accept; 8 wrappers compile, 7 fail. D reports 4 compatible, 9 incompatible and 2 inapplicable; all 15 semantic checks abstain. | [Protocol](PREVALIDATION_PROTOCOL.md), [E4 results](EXPERIMENT_E4_RESULTS.md). The nine static incompatibilities include five uncompilable detector wrappers and four explicitly unsupported segmentation fallbacks. **No new supported end-to-end natural failure or reference-backed semantic mismatch is established.** No external runtime experiment was performed. |
| E5: scoped pre-flight command | Separates structure, supplied-reference agreement, selected decoder compatibility, preservation and abstention. Flags the actual EfficientNet deletion failure; does not reject the four byte-distinct conditions with successful tested Android getters. | [E5 results](EXPERIMENT_E5_RESULTS.md), [command](scripts/preflight.py). Evaluated on 65 byte-distinct fixtures, not 65 independent models. Abstains on three dynamic-signature Gesture fixtures, including its known isolated deletion failure. No precision/recall estimate. |
| E7: secondary Hand | A source-pinned test component and the focal component have different file hashes but identical graph/weights. The source-backed role comparison supports the focal index mismatch. The official Hand Task returns identical decoded results before and after the metadata exchange on the one fixed image. | [Hand results](EXPERIMENT_HAND_RESULTS.md), [reference chain](E7/REFERENCE_CHAIN.md). One detected hand, 21 landmarks and 21 world landmarks in each condition and replay. Generic repaired-bytecode evidence is separate; swapping metadata is not a complete decoder repair. |

## Primary witness

EfficientNet original SHA-256: `6c7ab0a6e5dcbf38a8c33b960996a55a3b4300b36a018c4545801de3a3c8bde0`.

Deletion SHA-256: `739f08462e831806db6a9bce7ed5b70a037fce593003028e5d6911dbd284fd83`.

Canonical graph SHA-256: `73e57df01115600419abb72de4b2c3257200e12eb205d335bcbfc203a589bee8`.

Actual call chain: `ContractModel.newInstance(...) → process(TensorImage) → Outputs.getProbabilityAsCategoryList()`. The [instrumentation harness](scripts/ContractInstrumentation.java) observes a duplicate output buffer and then invokes the real getter. It does not copy the decoder expression. [Deletion device record](E1/executions/primary/label_deletion/device/result.json) contains the generated-getter frame and exact exception for both inputs. The harness catches the exception; this is not evidence of an uncaught application crash.

For the predetermined RGB-pattern input, E2 preserves output position 904 and score `0.23542051017284393`, while its exposed label changes from `window screen` to `window shade`. These synthetic inputs provide no task-accuracy evidence. Java `Category.getIndex()` is unset by this overload; the tested association is returned-list position, independently matched to every raw score bit.

## Evidence status and counting

- Phase 0 freshly verified hashes, arrays and records from the old study. Its 105 CPU invocations and 23 isolated decoder probes remain historical executions, not new runs.
- E1/E2 freshly generated, compiled, packaged and executed the actual Android interface. Each has four variant/configuration units and two prescribed inputs per unit. They share original/description/restored artifact conditions; the phase counts must not be summed into independent model counts. Replays use the same operator, environment and APKs.
- E3 freshly executed the official Task classifier and reused E1/E2 Android rows for comparison; reused rows are not additional runs. Its public API does not expose raw internal tensors.
- E4 freshly inspected and compiled originals after a local same-session freeze; E5 freshly applied the checker. They do not establish external end-to-end behavior.
- E7 freshly executed the official Hand Task, checked model bytes and source provenance, and disassembled preserved generic classes. Old Hand raw/repaired compiler runs were not rerun. Hand Task outputs are decoded outputs, not internal raw TFLite tensors.

The independent human audit remains pending. Novelty, venue suitability, task accuracy, defect prevalence, general semantic inference and production-user consequences are not established by these results. See [manuscript impact](MANUSCRIPT_IMPACT.md), [audit checklist](HUMAN_AUDIT.md), [reproduction guide](REPRODUCE.md) and [reporting clarifications](REPORTING_CLARIFICATIONS.md).
