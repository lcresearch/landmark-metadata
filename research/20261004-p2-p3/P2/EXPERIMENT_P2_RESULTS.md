# P2 same-Android consumer comparison: results

Fresh execution; same API 30 default x86_64 AVD, separate generated-wrapper and official Task 0.4.4 APK configurations. Frozen plan/input hashes and all build attempts retained. No generated Java modification.

Experimental denominator: 10 component × variant × consumer units; 1 canonical graph; 5 model byte conditions; 2 consumer configurations. 18 input observations are repeated observations, not models.

| Consumer | Variant | Build | Constructor | Input | Public process / classify | Getter | Earliest rejection |
|---|---|---|---|---|---|---|---|
| wrapper | original | PASS | PASS | PASS | PASS | PASS | none |
| wrapper | description_control | PASS | PASS | PASS | PASS | PASS | none |
| wrapper | label_deletion | PASS | PASS | PASS | PASS | FAIL | generated_getter |
| wrapper | label_permutation | PASS | PASS | PASS | PASS | PASS | none |
| wrapper | restoration | PASS | PASS | PASS | PASS | PASS | none |
| task | original | PASS | PASS | PASS | PASS | INAPPLICABLE | none |
| task | description_control | PASS | PASS | PASS | PASS | INAPPLICABLE | none |
| task | label_deletion | PASS | FAIL | NOT_REACHED | NOT_REACHED | INAPPLICABLE | model_initialization |
| task | label_permutation | PASS | PASS | PASS | PASS | INAPPLICABLE | none |
| task | restoration | PASS | PASS | PASS | PASS | INAPPLICABLE | none |

Task constructor is public loading+initialization. Task classify is atomic inference+decoding; no separate internal runtime stage is instrumented. NOT_REACHED remains distinct from an atomic granularity marker. Exact observational-stage normalization is disclosed in results.json; execution-results.json is unchanged.

## Exact failures

- wrapper/label_deletion/gray127: `java.lang.IllegalArgumentException` at `generated_getter`: Label number 999 mismatch the shape on axis 1
- wrapper/label_deletion/rgb_pattern: `java.lang.IllegalArgumentException` at `generated_getter`: Label number 999 mismatch the shape on axis 1
  Full stack and cause chain: `executions/primary/wrapper/label_deletion/device/result.json`.
- task/label_deletion/constructor: `java.lang.IllegalStateException` at `model_initialization`: Error getting native address of native library: task_vision_jni
  Underlying cause: `java.lang.IllegalArgumentException`: Error occurred when initializing ImageClassifier: Got 1000 class(es) for output index 0, expected 999 according to the label map.
  Full stack and cause chain: `executions/primary/task/label_deletion/device/result.json`.

The Task outer native-address message is a generic wrapping exception. Its recorded underlying cause identifies the label-cardinality check; it is not a missing-native-library result.

## Preservation, identity and returned values

All generated Java equal across variants: True; per-consumer compiled classes equal: True; per-consumer DEX equal: True.
All copied/APK/preload model hashes equal: True. Preload AssetManager read uses same model asset name and context as actual public constructor, but does not intercept native interpreter bytes.

| Consumer | Variant | Input | Raw equal original | Score bits equal original | Changed labels |
|---|---|---|---|---|---|
| wrapper | original | gray127 | True | True | 0 |
| wrapper | original | rgb_pattern | True | True | 0 |
| wrapper | description_control | gray127 | True | True | 0 |
| wrapper | description_control | rgb_pattern | True | True | 0 |
| wrapper | label_deletion | gray127 | True | not reached | not reached |
| wrapper | label_deletion | rgb_pattern | True | not reached | not reached |
| wrapper | label_permutation | gray127 | True | True | 999 |
| wrapper | label_permutation | rgb_pattern | True | True | 999 |
| wrapper | restoration | gray127 | True | True | 0 |
| wrapper | restoration | rgb_pattern | True | True | 0 |
| task | original | gray127 | NOT_OBSERVED (Task API) | True | 0 |
| task | original | rgb_pattern | NOT_OBSERVED (Task API) | True | 0 |
| task | description_control | gray127 | NOT_OBSERVED (Task API) | True | 0 |
| task | description_control | rgb_pattern | NOT_OBSERVED (Task API) | True | 0 |
| task | label_deletion | gray127 | NOT_REACHED | not reached | not reached |
| task | label_deletion | rgb_pattern | NOT_REACHED | not reached | not reached |
| task | label_permutation | gray127 | NOT_OBSERVED (Task API) | True | 999 |
| task | label_permutation | rgb_pattern | NOT_OBSERVED (Task API) | True | 999 |
| task | restoration | gray127 | NOT_OBSERVED (Task API) | True | 0 |
| task | restoration | rgb_pattern | NOT_OBSERVED (Task API) | True | 0 |

The numeric table includes two planned Task deletion inputs that were not reached; they are not counted among the 18 actual input observations. Cross-consumer score comparison aligns Task Category index with wrapper output position; Task ranked-list position is not used. Native Task raw tensors are not observed. All per-index comparison counts and maximum returned-score differences are in results.json.

## Build/dependency and operational record

Two build attempts: initial 10 APKs all compiled/package successfully; before execution, review separated successful public API return from subsequent serialization/IO, then all 10 were rebuilt. Both attempts preserved; generated sources and fixtures unchanged. Only final attempt executed. No version fishing or source repair.

Exact Java/native classpaths and SHA256: `dependencies/resolved-lock.json`. Published Maven POM/AAR/JAR downloads: `dependencies/downloads.json`; exact host/compiler/SDK: `versions/versions.json`; expanded commands/stdout/stderr: `commands-executed.sh`, build and execution logs. Separate Task native library is not asserted identical to standalone TFLite 2.13.0.

Fresh AVD configuration/state is under sdk/avd; installed SDK/JDK/Python are reused read-only, not rebuilt from archived inputs. SDK paths are symlinks to prior installation. Global adb server/default Android preferences are host state; this is not a hermetic host installation.

## Interpretation boundaries

A reproduced stage contrast on the same Android API/ABI reduces the earlier OS/language contrast. The two official consumer configurations still differ in native integration and published libraries; do not infer isolated interpreter-version causality or independent implementations. Full source/javap mechanism audit is preserved separately under ../review/mechanism.

All failures are caught by instrumentation. No application crash, latency improvement, task accuracy, natural EfficientNet defect, or prevalence result is inferred. Label permutation compares exposed association relative to original; independent reference investigation belongs to P3. Agent execution is not human verification.
