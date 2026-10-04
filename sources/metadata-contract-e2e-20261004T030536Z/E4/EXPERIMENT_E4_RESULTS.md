# E4 results

The fixed 20 candidate URLs yielded 16 successful downloads and 4 unavailable candidates. Recursive extraction produced 18 component occurrences. One prior component and two prior-graph occurrences were excluded, leaving 15 new canonical groups. No failed candidate was replaced.

All 15 were structurally accepted. Raw generated Java compiled for 8 and failed for 7. The frozen D rule reports 4 compatible category paths, 9 incompatible category paths, and 2 without that category path. All semantic checks abstain for lack of an independently supplied artifact-tied reference.

| Candidate | Component | S | Raw javac | Frozen D | Existing warning |
|---|---|---|---|---|---|
| C01 | `bc2ffe19c111` | PASS | PASS | PASS | None recorded |
| C03 | `94b6c84a5d6d` | PASS | PASS | PASS | None recorded |
| C04 | `7fc3a7dbc1cd` | PASS | PASS | PASS | None recorded |
| C06 | `0720bf247bd7` | PASS | FAIL | FAIL | None recorded |
| C07 | `ad2abbf2b4e1` | PASS | FAIL | FAIL | None recorded |
| C08 | `b3f50554cb0e` | PASS | FAIL | FAIL | None recorded |
| C09 | `5d4ebec1029b` | PASS | FAIL | FAIL | None recorded |
| C10 | `b8ccb1a25d45` | PASS | FAIL | FAIL | None recorded |
| C14 | `191ac9529ae5` | PASS | PASS | FAIL | Non-RGB unsupported fallback |
| C15 | `490e9ea73431` | PASS | PASS | FAIL | Non-RGB unsupported fallback |
| C16 | `2628cf3ce5f6` | PASS | PASS | FAIL | Non-RGB unsupported fallback |
| C17 | `c6748b1253a9` | PASS | PASS | FAIL | Non-RGB unsupported fallback |
| C18 | `82be6d591b9d` | PASS | FAIL | INAPPLICABLE_NO_GENERATED_CATEGORY_PATH | None recorded |
| C19 | `a0fe0e6cbaeb` | PASS | FAIL | INAPPLICABLE_NO_GENERATED_CATEGORY_PATH | None recorded |
| C20 | `4d8b4a53282d` | PASS | PASS | PASS | None recorded |

## Negative and scoped outcomes

Five D-incompatible detector wrappers fail raw javac before a generated runtime path can be exercised. Four D-incompatible segmentation wrappers compile, but each generator explicitly warns that its non-RGB output is unsupported and is treated as a numeric tensor. They are preserved as static consumer-compatibility findings, not silently accepted supported-interface defects. Two Pose wrappers have no applicable generated category getter and fail javac.

No new reference-backed semantic mismatch or supported end-to-end natural failure is established. No runtime execution was performed on the external originals; compatible D results are static precondition checks, not confirmations of end-to-end execution or semantic correctness. No precision/recall or prevalence estimate is reported.

Unavailable candidate addresses (all retained):

- C02: HTTP 404; `https://storage.googleapis.com/mediapipe-models/image_classifier/efficientnet_lite0/float16/1/efficientnet_lite0.tflite`
- C05: HTTP 404; `https://storage.googleapis.com/mediapipe-models/image_classifier/efficientnet_lite2/float16/1/efficientnet_lite2.tflite`
- C11: HTTP 404; `https://storage.googleapis.com/mediapipe-models/object_detector/ssd_mobilenet_v2/int8/1/ssd_mobilenet_v2.tflite`
- C13: HTTP 404; `https://storage.googleapis.com/mediapipe-models/face_detector/blaze_face_full_range_sparse/float16/1/blaze_face_full_range_sparse.tflite`

Frozen protocol commit: `a1adde5e2e77b6f30a77a689b5e1025a887a58bd`. Tracked frozen rule/protocol files remain unchanged after execution. The collected data uses the local same-session freeze, not a third-party registration or independent human review. Candidate URL construction was not verification of publisher-catalog existence.

Exact models, source URLs, shapes/signatures, raw checker output, emitted Java, javac logs/classes and exclusions are in E4/results.json and its artifact paths. The raw checker reports are preserved even when a scope filter would abstain. Dynamic-output abstentions and absent-metadata counts happen to be zero in the included set; that is not a rule to omit them from future studies.
