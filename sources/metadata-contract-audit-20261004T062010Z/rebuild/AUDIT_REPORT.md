# E1/E2 fresh construction audit

This agent audit freshly regenerated and built the same eight phase/variant execution records, then executed the actual generated Android interface on two predetermined synthetic inputs per record. The SDK/JDK/Python installation was reused; the output directories, debug signing key and Android AVD were new. This is not an independent human reproduction or SDK-from-archive reconstruction.

## Observed phase/variant records

| Experiment | Variant | Structure | Generation | Compile/package | Load | Inference | Actual getter |
|---|---|---|---|---|---|---|---|
| E1 | original | PASS | PASS | PASS/PASS | PASS | PASS | PASS |
| E1 | description_control | PASS | PASS | PASS/PASS | PASS | PASS | PASS |
| E1 | label_deletion | PASS | PASS | PASS/PASS | PASS | PASS | FAIL |
| E1 | label_restoration | PASS | PASS | PASS/PASS | PASS | PASS | PASS |
| E2 | original | PASS | PASS | PASS/PASS | PASS | PASS | PASS |
| E2 | description_control | PASS | PASS | PASS/PASS | PASS | PASS | PASS |
| E2 | label_permutation | PASS | PASS | PASS/PASS | PASS | PASS | PASS |
| E2 | permutation_restoration | PASS | PASS | PASS/PASS | PASS | PASS | PASS |

## Audit checks

{'PASS': 180, 'FAIL': 0, 'UNVERIFIABLE': 0}

Denominators: {'phase_variant_execution_records': 8, 'unique_artifact_consumer_configurations': 5, 'byte_distinct_models': 5, 'canonical_graphs': 1, 'input_observations': 16}

These are correlated software assertions over five artifact-by-consumer configurations, not 180 independent experiments or an accuracy metric. Unverified semantic/human claims are listed separately in results.json. Per-check results and exact hashes: `results.json`. Source snapshots and patches preserve the sole instrumentation addition (asset identity) and orchestration gate change (fresh primary sufficient before E2). Every subprocess command and stdout/stderr are preserved under each unit and `commands-executed.sh`.

| Check | Status |
|---|---|
| E1/original workspace/APK/runtime asset identity | PASS |
| E1/original unmodified generated source matches historical | PASS |
| E1/original class and DEX records recomputed from actual files | PASS |
| E1/original generated classes match historical actual files | PASS |
| E1/original generated source/classes/DEX equal fresh original | PASS |
| E1/original canonical/nonmetadata preservation | PASS |
| E1/original embedded metadata/preZIP preservation | PASS |
| E1/original/gray127 input equal original | PASS |
| E1/original/gray127 all raw output bytes equal original | PASS |
| E1/original/gray127 all raw output bytes equal historical | PASS |
| E1/original/gray127 independently recomputed top5 matches logged | PASS |
| E1/original/gray127 all returned score bits match raw positions | PASS |
| E1/original/gray127 all returned score bits match original | PASS |
| E1/original/gray127 decoded result matches historical | PASS |
| E1/original/gray127 decoded association unchanged/restored | PASS |
| E1/original/rgb_pattern input equal original | PASS |
| E1/original/rgb_pattern all raw output bytes equal original | PASS |
| E1/original/rgb_pattern all raw output bytes equal historical | PASS |
| E1/original/rgb_pattern independently recomputed top5 matches logged | PASS |
| E1/original/rgb_pattern all returned score bits match raw positions | PASS |
| E1/original/rgb_pattern all returned score bits match original | PASS |
| E1/original/rgb_pattern decoded result matches historical | PASS |
| E1/original/rgb_pattern decoded association unchanged/restored | PASS |
| E1/description_control workspace/APK/runtime asset identity | PASS |
| E1/description_control unmodified generated source matches historical | PASS |
| E1/description_control class and DEX records recomputed from actual files | PASS |
| E1/description_control generated classes match historical actual files | PASS |
| E1/description_control generated source/classes/DEX equal fresh original | PASS |
| E1/description_control canonical/nonmetadata preservation | PASS |
| E1/description_control/gray127 input equal original | PASS |
| E1/description_control/gray127 all raw output bytes equal original | PASS |
| E1/description_control/gray127 all raw output bytes equal historical | PASS |
| E1/description_control/gray127 independently recomputed top5 matches logged | PASS |
| E1/description_control/gray127 all returned score bits match raw positions | PASS |
| E1/description_control/gray127 all returned score bits match original | PASS |
| E1/description_control/gray127 decoded result matches historical | PASS |
| E1/description_control/gray127 decoded association unchanged/restored | PASS |
| E1/description_control/rgb_pattern input equal original | PASS |
| E1/description_control/rgb_pattern all raw output bytes equal original | PASS |
| E1/description_control/rgb_pattern all raw output bytes equal historical | PASS |
| E1/description_control/rgb_pattern independently recomputed top5 matches logged | PASS |
| E1/description_control/rgb_pattern all returned score bits match raw positions | PASS |
| E1/description_control/rgb_pattern all returned score bits match original | PASS |
| E1/description_control/rgb_pattern decoded result matches historical | PASS |
| E1/description_control/rgb_pattern decoded association unchanged/restored | PASS |
| E1/label_deletion workspace/APK/runtime asset identity | PASS |
| E1/label_deletion unmodified generated source matches historical | PASS |
| E1/label_deletion class and DEX records recomputed from actual files | PASS |
| E1/label_deletion generated classes match historical actual files | PASS |
| E1/label_deletion generated source/classes/DEX equal fresh original | PASS |
| E1/label_deletion canonical/nonmetadata preservation | PASS |
| E1/label_deletion embedded metadata/preZIP preservation | PASS |
| E1/label_deletion/gray127 input equal original | PASS |
| E1/label_deletion/gray127 all raw output bytes equal original | PASS |
| E1/label_deletion/gray127 all raw output bytes equal historical | PASS |
| E1/label_deletion/gray127 independently recomputed top5 matches logged | PASS |
| E1/label_deletion/gray127 expected deletion failure at real getter | PASS |
| E1/label_deletion/rgb_pattern input equal original | PASS |
| E1/label_deletion/rgb_pattern all raw output bytes equal original | PASS |
| E1/label_deletion/rgb_pattern all raw output bytes equal historical | PASS |
| E1/label_deletion/rgb_pattern independently recomputed top5 matches logged | PASS |
| E1/label_deletion/rgb_pattern expected deletion failure at real getter | PASS |
| E1/label_restoration workspace/APK/runtime asset identity | PASS |
| E1/label_restoration unmodified generated source matches historical | PASS |
| E1/label_restoration class and DEX records recomputed from actual files | PASS |
| E1/label_restoration generated classes match historical actual files | PASS |
| E1/label_restoration generated source/classes/DEX equal fresh original | PASS |
| E1/label_restoration canonical/nonmetadata preservation | PASS |
| E1/label_restoration embedded metadata/preZIP preservation | PASS |
| E1/label_restoration/gray127 input equal original | PASS |
| E1/label_restoration/gray127 all raw output bytes equal original | PASS |
| E1/label_restoration/gray127 all raw output bytes equal historical | PASS |
| E1/label_restoration/gray127 independently recomputed top5 matches logged | PASS |
| E1/label_restoration/gray127 all returned score bits match raw positions | PASS |
| E1/label_restoration/gray127 all returned score bits match original | PASS |
| E1/label_restoration/gray127 decoded result matches historical | PASS |
| E1/label_restoration/gray127 decoded association unchanged/restored | PASS |
| E1/label_restoration/rgb_pattern input equal original | PASS |
| E1/label_restoration/rgb_pattern all raw output bytes equal original | PASS |
| E1/label_restoration/rgb_pattern all raw output bytes equal historical | PASS |
| E1/label_restoration/rgb_pattern independently recomputed top5 matches logged | PASS |
| E1/label_restoration/rgb_pattern all returned score bits match raw positions | PASS |
| E1/label_restoration/rgb_pattern all returned score bits match original | PASS |
| E1/label_restoration/rgb_pattern decoded result matches historical | PASS |
| E1/label_restoration/rgb_pattern decoded association unchanged/restored | PASS |
| E2/original workspace/APK/runtime asset identity | PASS |
| E2/original unmodified generated source matches historical | PASS |
| E2/original class and DEX records recomputed from actual files | PASS |
| E2/original generated classes match historical actual files | PASS |
| E2/original generated source/classes/DEX equal fresh original | PASS |
| E2/original canonical/nonmetadata preservation | PASS |
| E2/original embedded metadata/preZIP preservation | PASS |
| E2/original/gray127 input equal original | PASS |
| E2/original/gray127 all raw output bytes equal original | PASS |
| E2/original/gray127 all raw output bytes equal historical | PASS |
| E2/original/gray127 independently recomputed top5 matches logged | PASS |
| E2/original/gray127 all returned score bits match raw positions | PASS |
| E2/original/gray127 all returned score bits match original | PASS |
| E2/original/gray127 decoded result matches historical | PASS |
| E2/original/gray127 decoded association unchanged/restored | PASS |
| E2/original/rgb_pattern input equal original | PASS |
| E2/original/rgb_pattern all raw output bytes equal original | PASS |
| E2/original/rgb_pattern all raw output bytes equal historical | PASS |
| E2/original/rgb_pattern independently recomputed top5 matches logged | PASS |
| E2/original/rgb_pattern all returned score bits match raw positions | PASS |
| E2/original/rgb_pattern all returned score bits match original | PASS |
| E2/original/rgb_pattern decoded result matches historical | PASS |
| E2/original/rgb_pattern decoded association unchanged/restored | PASS |
| E2/description_control workspace/APK/runtime asset identity | PASS |
| E2/description_control unmodified generated source matches historical | PASS |
| E2/description_control class and DEX records recomputed from actual files | PASS |
| E2/description_control generated classes match historical actual files | PASS |
| E2/description_control generated source/classes/DEX equal fresh original | PASS |
| E2/description_control canonical/nonmetadata preservation | PASS |
| E2/description_control/gray127 input equal original | PASS |
| E2/description_control/gray127 all raw output bytes equal original | PASS |
| E2/description_control/gray127 all raw output bytes equal historical | PASS |
| E2/description_control/gray127 independently recomputed top5 matches logged | PASS |
| E2/description_control/gray127 all returned score bits match raw positions | PASS |
| E2/description_control/gray127 all returned score bits match original | PASS |
| E2/description_control/gray127 decoded result matches historical | PASS |
| E2/description_control/gray127 decoded association unchanged/restored | PASS |
| E2/description_control/rgb_pattern input equal original | PASS |
| E2/description_control/rgb_pattern all raw output bytes equal original | PASS |
| E2/description_control/rgb_pattern all raw output bytes equal historical | PASS |
| E2/description_control/rgb_pattern independently recomputed top5 matches logged | PASS |
| E2/description_control/rgb_pattern all returned score bits match raw positions | PASS |
| E2/description_control/rgb_pattern all returned score bits match original | PASS |
| E2/description_control/rgb_pattern decoded result matches historical | PASS |
| E2/description_control/rgb_pattern decoded association unchanged/restored | PASS |
| E2/label_permutation workspace/APK/runtime asset identity | PASS |
| E2/label_permutation unmodified generated source matches historical | PASS |
| E2/label_permutation class and DEX records recomputed from actual files | PASS |
| E2/label_permutation generated classes match historical actual files | PASS |
| E2/label_permutation generated source/classes/DEX equal fresh original | PASS |
| E2/label_permutation canonical/nonmetadata preservation | PASS |
| E2/label_permutation embedded metadata/preZIP preservation | PASS |
| E2/label_permutation/gray127 input equal original | PASS |
| E2/label_permutation/gray127 all raw output bytes equal original | PASS |
| E2/label_permutation/gray127 all raw output bytes equal historical | PASS |
| E2/label_permutation/gray127 independently recomputed top5 matches logged | PASS |
| E2/label_permutation/gray127 all returned score bits match raw positions | PASS |
| E2/label_permutation/gray127 all returned score bits match original | PASS |
| E2/label_permutation/gray127 decoded result matches historical | PASS |
| E2/label_permutation/gray127 cyclic shift association | PASS |
| E2/label_permutation/gray127 historical label change count 999 independently recovered | PASS |
| E2/label_permutation/rgb_pattern input equal original | PASS |
| E2/label_permutation/rgb_pattern all raw output bytes equal original | PASS |
| E2/label_permutation/rgb_pattern all raw output bytes equal historical | PASS |
| E2/label_permutation/rgb_pattern independently recomputed top5 matches logged | PASS |
| E2/label_permutation/rgb_pattern all returned score bits match raw positions | PASS |
| E2/label_permutation/rgb_pattern all returned score bits match original | PASS |
| E2/label_permutation/rgb_pattern decoded result matches historical | PASS |
| E2/label_permutation/rgb_pattern cyclic shift association | PASS |
| E2/label_permutation/rgb_pattern historical label change count 999 independently recovered | PASS |
| E2/permutation_restoration workspace/APK/runtime asset identity | PASS |
| E2/permutation_restoration unmodified generated source matches historical | PASS |
| E2/permutation_restoration class and DEX records recomputed from actual files | PASS |
| E2/permutation_restoration generated classes match historical actual files | PASS |
| E2/permutation_restoration generated source/classes/DEX equal fresh original | PASS |
| E2/permutation_restoration canonical/nonmetadata preservation | PASS |
| E2/permutation_restoration embedded metadata/preZIP preservation | PASS |
| E2/permutation_restoration/gray127 input equal original | PASS |
| E2/permutation_restoration/gray127 all raw output bytes equal original | PASS |
| E2/permutation_restoration/gray127 all raw output bytes equal historical | PASS |
| E2/permutation_restoration/gray127 independently recomputed top5 matches logged | PASS |
| E2/permutation_restoration/gray127 all returned score bits match raw positions | PASS |
| E2/permutation_restoration/gray127 all returned score bits match original | PASS |
| E2/permutation_restoration/gray127 decoded result matches historical | PASS |
| E2/permutation_restoration/gray127 decoded association unchanged/restored | PASS |
| E2/permutation_restoration/rgb_pattern input equal original | PASS |
| E2/permutation_restoration/rgb_pattern all raw output bytes equal original | PASS |
| E2/permutation_restoration/rgb_pattern all raw output bytes equal historical | PASS |
| E2/permutation_restoration/rgb_pattern independently recomputed top5 matches logged | PASS |
| E2/permutation_restoration/rgb_pattern all returned score bits match raw positions | PASS |
| E2/permutation_restoration/rgb_pattern all returned score bits match original | PASS |
| E2/permutation_restoration/rgb_pattern decoded result matches historical | PASS |
| E2/permutation_restoration/rgb_pattern decoded association unchanged/restored | PASS |
| eight phase/variant execution records completed | PASS |
| all fresh generated source/classes/DEX identical across phase records | PASS |

## Interpretation and remaining boundaries

The fresh E1 deletion reproduces java.lang.IllegalArgumentException: Label number 999 mismatch the shape on axis 1, reached through the actual unmodified generated getter after successful inference on both tested inputs. Original, description and restoration complete successfully. The fresh E2 permutation completes successfully, preserves all raw/returned score bits and changes 999 displayed labels on each input; inverse restoration recovers the original decoded lists. At RGB position 904, score 0.23542051017284393 remains fixed while window screen changes to window shade. Raw outputs are compared byte-for-byte on the tested inputs; no inference accuracy or universal-input numerical claim is made. E2 label permutation changes exposed association relative to the original, without an independently tied class-order reference. A successful decoder is not semantic validation.

A new harness hashes the installed AssetManager resource immediately before generated newInstance uses the identical asset name and Context. It does not intercept or replace the native interpreter buffer. Generated-source inspection and library tracing therefore remain part of the load-identity chain. Whole APK byte equality is intentionally not assessed; the embedded model and signing key differ. Generated classes are compared against historical classes, whereas full DEX is compared across fresh variants only because the harness changed.

The build compiles unmodified generated Java inside the disclosed custom minimal instrumentation harness; it does not claim that the untouched generated Gradle project builds. Fresh results are compared to preserved historical primary outputs. No new independent model or blinded held-out validation is implied. New same-APK replay was not required by this construction audit. Human verification, standalone archived-toolchain installation and independent class-order reference remain pending.
