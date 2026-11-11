# Two real-report candidates for bounded reproduction

**Decision:** prioritize Support #770, retain Support #319 as a complementary
asset-selection case, and do not select a third candidate. Neither is an
independently reproduced natural defect. This screen adds no paper observations.

The [protocol](PROTOCOL.md) fixed seven previously inspected reports before
fresh retrieval. All seven current bodies and all 69 returned comments were read;
comment counts match the issue metadata. This is a new November read of the same
pool, not recovery of the October response snapshots or a representative search.
Exact response identities and link checks are in [sources.json](sources.json).

## 1. Support #770 — highest relevance; conditional reconstruction

[Issue](https://github.com/tensorflow/tflite-support/issues/770),
[consumer-selection reply](https://github.com/tensorflow/tflite-support/issues/770#issuecomment-1108777779).

The reporter imported a DeepLab metadata model through Android Studio ML Model
Binding. The generated segmentation getter reached TensorLabel and rejected 21
labels against a spatial dimension of 257. The reply directs the reporter to
Task ImageSegmenter and says that generated integration is unsupported. This is
a real reported **consumer/model incompatibility**, not evidence of a defective
published classifier or a supported-path official bug.

Why pursue: it directly tests whether successful model import/generated code is
sufficient acceptance evidence for the application's final output endpoint. It
extends the engineering question to an unmodified reported model and a different
output shape, without pretending to discover the failure category.

Material checked now:

- The old overview URL redirects to the official TensorFlow examples repository.
  Its [Android README](https://github.com/tensorflow/examples/blob/master/lite/examples/image_segmentation/android/README.md)
  links DeepLab `metadata/2`, consistent with the reporter's generated model name.
- The [download script](https://github.com/tensorflow/examples/blob/master/lite/examples/image_segmentation/android/app/download_models.gradle)
  supplies a public `lite-model_deeplabv3_1_metadata_2.tflite` URL. A bounded GET
  returned HTTP 200, advertised 2,780,051 bytes and had `TFL3` at bytes 4–7.
  Only 4,096 bytes were retained; no full model hash/structure was verified.
- The current [Task guide](https://developers.google.com/edge/litert/libraries/task_library/image_segmenter)
  documents segmentation outputs and the Task route. It is later documentation,
  not a snapshot of the reporter's 2022 configuration. Its model example links
  `metadata/1`; do not substitute that for the README's `metadata/2` silently.

Missing: the reporter's model digest, Android Studio/AGP generator and library
versions, source commit and exact input image. Current availability is insufficient
to identify the original bytes or certify exact historical reproduction.

Minimum proposed experiment, after separately authorizing execution:

1. Acquire/pin the complete unmodified `metadata/2` model and record its graph,
   output shape, metadata and labels. Stop if it cannot be linked to the report's
   described shape/resource; never edit it to force the reported error.
2. Freeze one documented ML Model Binding configuration. Exercise its actual
   generated construction, process and category getter; preserve source/classes,
   raw output, cause chain and the public failing stage. A hand-written TensorLabel
   probe or CLI-codegen substitute alone is not a replay of the reported route.
3. With that same model and recorded input, test Task ImageSegmenter in a pinned
   supported configuration. Record whether construction and segmentation return;
   keep output-kind/configuration differences explicit. Do not promise this arm
   will succeed or interpret its mask as an accuracy measurement.

Stopping rule: if original versions cannot be identified, label any runnable
configuration a **new reconstruction of the reported mechanism**. If faithful
generation or the unmodified asset cannot be obtained within the one frozen
setup attempt, retain the failure and stop. Do not version-search until a desired
exception appears. Expected contribution is consumer-selection/acceptance evidence,
with the unsupported-path qualification retained even if reproduced.

## 2. Support #319 — explicit before/after asset-selection report

[Issue](https://github.com/tensorflow/tflite-support/issues/319),
[reporter's resolution](https://github.com/tensorflow/tflite-support/issues/319#issuecomment-772558484).

The reporter supplies the C++ BERT QA demo command, a fixed question/context,
Bazel 3.7.2 and WSL2. The default MobileBERT asset fails with a missing input
process-unit diagnostic; the reporter says replacing `default/1` with `metadata/1`
fixed it. This is a reported **asset-selection error with existing rejection**,
not a new validator failure or an output-label permutation case.

Why pursue: it offers a concrete negative/positive acceptance pair and an explicit
repair. It can show why a valid downloadable model is not enough for a selected
task consumer. Keep it complementary; it cannot establish the prevalence or
generality of the classifier's display-association result.

Material checked now:

- Both exact reported TFHub URLs redirect through Kaggle to binary responses:
  HTTP 200; advertised lengths 100,456,296 (`default/1`) and 100,670,436
  (`metadata/1`) bytes. Both retained 4,096-byte prefixes contain `TFL3`.
  These are availability observations, not complete-file identities.
- The currently retrieved [demo README](https://github.com/tensorflow/tflite-support/blob/master/tensorflow_lite_support/examples/task/text/desktop/README.md)
  uses `metadata/1` in its download command while its named prerequisite link
  still points to `default/1`. That is a current retrieved document observation,
  not proof that the same text caused the 2021 report.

Missing: complete model hashes, model graph/weight equality and the original
Support commit/build environment. Different package names or sizes do not prove
that metadata is the sole difference.

Minimum proposed experiment: pin both complete assets; compare computation,
weights, metadata/process units and resources before any causal claim. Freeze one
C++ Task configuration and replay the same question/context with each asset.
Observe construction/answer stages and diagnostics. A returned answer provides
only a smoke-test outcome. If the graphs/weights differ, retain the asset-selection
comparison and explicitly withhold computation-preserving metadata attribution.

Stopping rule: one pinned configuration for the pair, with both results retained.
Stop if either asset cannot be acquired or the command cannot be built without
unbounded legacy dependency repair. A current API reconstruction must be labeled
as such; exact historical recreation is not presently supported.

## Remaining fixed-pool dispositions

| Report | Decision and concrete reason |
|---|---|
| [TensorFlow #1269](https://github.com/tensorflow/tensorflow/issues/1269) | Defer. The GraphDef Android thread mixes missing operators, node names, preprocessing and later label-filename mistakes across different reporters. The original author reports repair, but no single pinned configuration isolates the focal acceptance question. Legacy reconstruction cost and mechanism drift are high. Linked assets were not newly checked. |
| [MediaPipe #22](https://github.com/google-ai-edge/mediapipe/issues/22) | Exclude from this shortlist. No original custom-model locator; a quantization/configuration alternative was suggested without reporter confirmation. Closing the issue does not establish the cause or repair. |
| [MediaPipe #195](https://github.com/google-ai-edge/mediapipe/issues/195) | Exclude. Documentation/protobuf-field mismatch with only a cross-reference reply, no model or observed runtime consequence. The linked issue was not followed in this bounded screen. |
| [Support #870](https://github.com/tensorflow/tflite-support/issues/870) | Exclude after availability check. The Drive URL in the later graph-editing discussion returned HTTP 404. It is also unclear whether it identifies the original or modified model. Encoded-image versus decoded-tensor inputs and graph changes confound the report; no unmodified pair can presently be bound. Do not reconstruct an artificial substitute and call it the real case. |
| [Support #703](https://github.com/tensorflow/tflite-support/issues/703) | Defer as documented existing rejection. The writer expects four output tensors while the custom YOLO export has one; replies describe unsupported configuration. The original custom asset and precise versions are missing. A newly exported YOLO would be a separate construction, not a recovered report artifact. |

## Evidence retention and boundary

Fresh responses, current documentation and bounded response prefixes are retained
at `/home/hsz/landmark-evidence/case-screening-20261111/`. The source index records
sizes/hashes and public URLs. Signed temporary download query strings stay out of
Git; complete raw responses remain external. No model was fully downloaded or
executed, no generated interface was built, and no reporter was contacted.
**New reproduced natural cases: zero.** The shortlist belongs to future work;
the current paper remains the one-classifier controlled case.
