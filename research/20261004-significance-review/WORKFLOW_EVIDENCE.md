# Official workflows and their significance limits

The focal integration is an officially documented workflow: a developer supplies
a model and label resource, packages metadata/resources, generates an Android
interface or initializes a Task classifier, and consumes labeled output. This
establishes an engineering setting for the experiments. It does **not** establish
how widely the workflow is used, that real users encountered the injected faults,
or that the proposed checks save time or prevent incidents.

Six declared official guides were retrieved successfully. Five legacy TensorFlow
URLs redirected to `developers.google.com`; the Android Studio 4.1 release-notes
URL remained accessible. No additional clarification links were followed, and no
models, libraries or consumer programs were executed. The source/version/digest
index is [workflow-sources.json](workflow-sources.json). Full HTML, response
headers, curl diagnostics and extracted article bodies remain outside Git under
`/workspace/significance-review-20261004/workflows/`.

The Google developer pages display a 2026-05-28 update date; the Android release
page displays 2026-10-01 but describes Studio 4.1. These are current retrievals of
mutable documentation, not archived documentation for Support 0.4.4. Several
examples use nightly or unpinned dependencies; the codegen guide even shows an
older `createInputs` / `run` / `getProbability` API. Its sample is not evidence
that the focal `process` / `getProbabilityAsCategoryList` code compiles. Exact
implementation explanations reuse the prior [official source comparison](../20261004-contribution-review/OFFICIAL_BASELINES.md)
at Support tag `v0.4.4`, commit
`133228616ca14e1b64c03f6a0ea8610f41a60783`. Ten relevant local source-file digests
were freshly checked against that index; they were not downloaded again.

## Documented integration and the developer decisions it informs

| Official source and inspected passage | What the developer actually supplies or calls | Existing checks / study relevance | Limit on significance |
|---|---|---|---|
| **WF01:** [Generate model interfaces using metadata](https://developers.google.com/edge/litert/android/metadata/codegen), sections on Studio import, CLI generation and using generated code; extracted lines 1–28, 75–94, 104–140 | Import `.tflite` into Studio or run `tflite_codegen` with model/package/class/destination; initialize the generated model, supply input, run it, then retrieve labeled output. | The documentation deliberately separates running the model from retrieving its public result. E1 tests both operations on an actual, fixed-version generated interface. The inspected generator loads labels at construction and checks the selected decoder at the getter; the file is not first read at the getter. | Successful import, generation, or inference is insufficient evidence for the narrower property that the selected getter returns. This is a test-design implication; this review measures no developer omissions or debugging benefit. Studio itself was not freshly exercised. |
| **WF02:** [Android Studio 4.1 release notes](https://developer.android.com/studio/releases/past-releases/as-4-1-0-release-notes#tensorflow-lite-models), “Use TensorFlow Lite models”; lines 36–76 | Import a supported model into `ml/`; inspect the model/tensor information and generated usage sample; use the generated class in an application. | The release notes distinguish friendly typed outputs for supported metadata-bearing models from `TensorBuffer` outputs for other cases and identify data-type limitations. They establish that generated integration is a product feature rather than a custom research-only decoder. | This is a historical feature description. It neither proves current Studio shares an identical generator nor supports treating Studio and CLI as independent implementations. |
| **WF03:** [Process input and output data with the Support Library](https://developers.google.com/edge/litert/android/metadata/lite_support), “Optional: Mapping results to labels”; lines 110–137 | Place labels in application assets, use `FileUtil.loadLabels`, and feed the list plus the processed probability buffer to `TensorLabel`; this example returns `getMapWithFloatValue()`. | Labels are supplied separately from tensor computation. The pinned `FileUtil` defines line parsing; `TensorLabel` defines compatibility. The project's VT/U+2028 probes show why a preflight approximating that parser can disagree with the modeled library. | This guide's map-returning expression is not the focal generated Category-list getter. The probes identify the project's former approximation defect, not a newly established official-library defect or deployed incident. |
| **WF04:** [Integrate image classifiers](https://developers.google.com/edge/litert/libraries/task_library/image_classifier), Java setup and “Model compatibility requirements”; lines 31–67, 180–204 | Package the model asset; call `ImageClassifier.createFromFileAndOptions`, then `classify`. Supply mandatory metadata, allowed tensor shapes/types, and optional axis-label files. The first axis-label file supplies class names; a locale-matching file supplies display names. | This is an existing alternative consumer with declared compatibility requirements. The pinned `ImageClassifier::Init` → `CheckAndSetOutputs` implementation already checks supported output shapes and nonempty label-map count. P2 records constructor-time versus generated-getter-time rejection on the same Android AVD. | A different enforcement stage is not a demonstrated performance or reliability benefit. Native integrations still differ. A missing optional label map must not be confused with a present, nonempty map of the wrong length. |
| **WF05:** [Adding metadata to LiteRT models](https://developers.google.com/edge/litert/conversion/tensorflow/metadata), format, associated files, image-classifier population and inspection; lines 13–30, 71–90, 201–219, 275–332, 429–445 | Supply the model and label file separately, associate the filename with output tensor metadata, then call `load_metadata_buffer`, `load_associated_files`, and `populate`. Inspect metadata as JSON or read associated-file bytes. | The guide explains that associated files are appended as ZIP resources and consumed alongside an otherwise interpretable model. P therefore compares graph/weights, metadata and associated resources separately. Pinned Populator checks structural cardinality and resource presence; it does not provide an independent class-order oracle. | The documented packaging mechanism makes resource changes technically relevant; it does not establish that conversion actually loses contracts or that resource drift occurs frequently. Label order must remain tied to the intended output positions, not inferred from arbitrary replacement text. |
| **WF06:** [Metadata Writer API](https://developers.google.com/edge/litert/conversion/tensorflow/metadata_writer_tutorial), image-classifier example; lines 30–60, plus richer descriptions at 173–220 | Obtain a model and labels, provide normalization parameters and the label path to `ImageClassifierWriter.create_for_inference`, inspect `get_metadata_json`, then save `writer.populate()`. The descriptive API also attaches label files to classification tensor metadata. | The example explicitly treats labels as a caller-supplied packaging input. E1/E2 explore controlled changes to this association while computation is preserved; they are not tests of retraining or model conversion. | The notebook installs a nightly package and downloads example assets from `master`. This review did not inspect or execute every writer's implementation and does not assign all higher-level writer checks to `MetadataPopulator`. |

## What the selected guides ask developers to verify

The image-classifier writer example labels printing `writer.get_metadata_json()`
as metadata verification (WF06, lines 57–58). The metadata guide recommends JSON
or visual inspection (WF05, lines 319–332). The Task guide points to a CLI demo
with the developer's own model and test data (WF04, lines 177–179). The codegen
guide demonstrates input preparation, model execution and result retrieval.
These passages do **not** prescribe a systematic class-order comparison against
an independent reference, byte-preservation controls, label-parser differential
tests, or mutation/restoration testing. That is a scoped observation about these
six guides, not a claim that official tests are absent or that developers skip
end-to-end testing. No repository-wide official test-suite audit occurred here.

The implementation checks already cover substantial parts of the problem:

- Structural tensor-metadata count and required resource presence are checked
  in the inspected population path. Neither reading nor population establishes
  the semantics of every label position.
- The Task ImageClassifier and generated TensorLabel path already reject the
  focal nonempty 999-label/1000-position condition, at their respective checked
  boundaries. The project does not introduce that rule.
- A count-preserving permutation satisfies those cardinality checks. Disagreement
  with a publisher-prescribed display order needs the separate, artifact-linked
  P3 reference; neither a count check nor a successful inference supplies it.
- A preflight for one decoder needs that decoder's actual parser, resource
  selection, axis and postprocessor assumptions. The project's previous Python
  parser counterexamples establish a limitation of that approximation. They do
  not show an error in the official API's own specified behavior.

## Supported engineering implications and unmeasured benefit

The study can inform **what an integration test asserts**: exercise the public
output getter; check class-index/display association against a supplied reference
when available; and identify which consumer stage rejects a given incompatible
resource. Raw tensor equality and successful source compilation do not settle
those interface properties in the recorded cases.

The study can also inform **what a preflight models**: use the selected consumer's
resource and parsing rules, and retain an explicit unknown judgment when a
reference or runtime shape is missing. The audited core comparison provides no
extra E5 rejection over the implementation-faithful simple baseline or Task
initialization. The evidence therefore supports configuration-specific diagnosis
and testing lessons, not an established stronger validator.

Time saved, earlier failure reducing cost, fewer production incidents, developer
adoption, prediction-accuracy loss and user harm remain unmeasured hypotheses.
Current guide text is not evidence of any of those outcomes. The bounded public
report review is a separate evidence source and must retain its own confirmation
and reproduction status.

## Rechecking these document inputs

Use a new external destination; retrieval never intentionally replaces existing
evidence. The extraction step needs `lxml` (the indexed run used 6.1.1) and verifies
an existing text extraction instead of overwriting it.

```sh
python research/20261004-significance-review/scripts/retrieve_workflows.py \
  --directory /workspace/significance-review-NEW/workflows
python research/20261004-significance-review/scripts/extract_workflows.py \
  --directory /workspace/significance-review-NEW/workflows \
  --index /workspace/significance-review-NEW/workflows/extraction-index.json
```

A later retrieval may differ because the pages are mutable. Keep its new hashes
and observations separate; it does not retroactively authenticate the bytes used
for this assessment.
