# Bounded public-report inquiry

The search found a directly related public report of a generated getter failure,
plus examples of existing early rejection and consumer/configuration mistakes.
This strengthens the evidence that developers encounter these integration
boundaries. It does not establish a newly reproduced natural defect, a supported
segmentation-generation failure, prevalence, or production impact.

The strongest report also constrains novelty: the generated-getter/label-axis
failure pattern was already publicly reported in 2022. The paper should explain
what its controlled preservation, reversals, reference comparison and matched
consumer observations add, rather than claim the first discovery that a generated
getter can fail on a decoder contract.

## Scope and denominator

Followed the eight queries in [PROTOCOL.md](PROTOCOL.md), each with
`created:<=2026-10-04`, `sort=created`, `order=asc`, `per_page=5`, `page=1`.
Queries completed without access failure; every `incomplete_results` flag was
false. Only the first page was requested. False incomplete flags do not mean that
this deliberately truncated inquiry is comprehensive.

| Query | GitHub total count | Returned |
|---|---:|---:|
| Q1 — Support, `"Label number"` | 1 | 1 |
| Q2 — TensorFlow, `"Label number"` | 153 | 5 |
| Q3 — MediaPipe, `"label map"` | 25 | 5 |
| Q4 — Support, `"label map"` | 2 | 2 |
| Q5 — TensorFlow, `metadata label order` | 115 | 5 |
| Q6 — Support, `label order` | 3 | 3 |
| Q7 — MediaPipe, `metadata output` | 101 | 5 |
| Q8 — Support, `metadata output` | 15 | 5 |

The 31 returned occurrences contain 30 unique issues; Support #870 occurs in Q4
and Q6. All 30 titles/bodies were triaged in first-occurrence order. Seven were
eligible, including uncertain or adjacent mechanisms, so all seven received
issue-and-comment inspection under the maximum-eight budget. Twenty-three were
excluded with reasons below. All 69 available comments on those seven issues
were retrieved and read, with zero omitted comments. No linked implementation/PR
pages, model assets or issue-provided code were fetched or executed. No candidate
was substituted. **Artifact-reproduced natural cases: 0.**

The sum of query totals is 415 overlapping search hits, not 415 unique reports or
models. GitHub search can match discussion comments while the initial triage was
explicitly title/body based. Ascending creation order strongly favors older
reports and leaves many later hits unexamined. These counts are search accounting,
not estimates of defect frequency or adoption.

## Selected reports and their consequences

| ID / public source | What was actually reported or explained | Evidence qualification and remaining gap |
|---|---|---|
| R1 — [Support #770](https://github.com/tensorflow/tflite-support/issues/770) | Android Studio's generated `getSegmentationMasksAsCategoryList()` reaches `TensorLabel` and raises `Label number 21 mismatch the shape on axis 1`. Reporter gives shape `[1,257,257,21]` and first-non-unit-axis explanation. | Direct related report. A [repository-member reply](https://github.com/tensorflow/tflite-support/issues/770#issuecomment-1108777779) explicitly says this segmentation model cannot use the drag-and-drop path, the generated API will not work, and recommends Task ImageSegmenter. This is an **unsupported consumer/model combination according to that reply**, not the required evidence of an unmodified supported-path natural failure. No exact model hash, generator/library version or local reproduction. |
| R2 — [TensorFlow #1269](https://github.com/tensorflow/tensorflow/issues/1269) | Replacing an Android demo's Inception model produces a missing output node and then unsupported operations. Contributor replies explain compiled operator inclusion and changed input/output names. A [later user](https://github.com/tensorflow/tensorflow/issues/1269#issuecomment-240426133) reports placeholder labels caused by a wrong label filename. | Adjacent manual TensorFlow GraphDef integration, not embedded TFLite metadata or generated model binding. Mixed causes and configurations; no shared controlled artifact or preservation evidence. Shows troubleshooting occurred, not that all comments are one bug or that this study's decoder caused them. |
| R3 — [MediaPipe #22](https://github.com/google-ai-edge/mediapipe/issues/22) | Custom SSD replacement changes class/box counts and label-map configuration, then yields no boxes. [Reply](https://github.com/google-ai-edge/mediapipe/issues/22#issuecomment-523149861) suggests `use_quantized_tensors:true`; another asks for newer quantized-model support. | Retained uncertain candidate with an alternative input/configuration explanation. No reporter confirmation, label-association diagnosis, pinned custom model or reproduced fix. Closing the issue does not prove resolution. |
| R4 — [MediaPipe #195](https://github.com/google-ai-edge/mediapipe/issues/195) | Classification calculator example uses `num_classes` absent from the shown protobuf options; only reply refers to #172. | Adjacent documentation/configuration mismatch. Linked page was not inspected; no verified code fix or runtime consequence, source revision or model. |
| R5 — [Support #870](https://github.com/tensorflow/tflite-support/issues/870) | Reporter cannot import a model into Android Studio's ML folder, then hits image decoding failure with a manual interpreter. [Repository-member explanation](https://github.com/tensorflow/tflite-support/issues/870#issuecomment-1208629590) points to encoded JPEG versus already decoded bitmap input. | Uncertain binding candidate resolves toward an input-side contract, not output-label drift. A later Google Drive locator exists but availability/bytes/hash were not checked. Reported accuracy loss after graph editing is unverified and is not evidence for this paper's metadata-preserving mechanism. |
| R6 — [Support #703](https://github.com/tensorflow/tflite-support/issues/703) | One-output YOLOv5 model given to four-output object-detector metadata writer is rejected with an explicit tensor/metadata-count `ValueError`. [Repository-member reply](https://github.com/tensorflow/tflite-support/issues/703#issuecomment-930339523) says this configuration is unsupported. | Useful existing-check counterexample: population rejects the incompatibility before the desired Android import. Do not generalize the reply into a schema prohibition on every single-output model or call the model universally invalid. Exact model and dependency versions are absent. |
| R7 — [Support #319](https://github.com/tensorflow/tflite-support/issues/319) | Task BERT consumer reports missing input process unit. [Reporter](https://github.com/tensorflow/tflite-support/issues/319#issuecomment-772558484) says switching the model URL from `default/1` to `metadata/1` fixed it. | Adjacent input metadata/resource prerequisite with a reporter-resolved selection mistake. No independent reproduction, exact model-byte identity or output association failure. Demonstrates that choosing the intended asset may already solve a reported problem. |

GitHub `author_association=MEMBER` is recorded for the relevant Support replies.
This is a repository-organization relationship supplied by GitHub, not separately
verified employment or authorship. TensorFlow `CONTRIBUTOR` and other `NONE`
respondents are not silently promoted to maintainers. The source index keeps the
precise distinction, comment URLs, reported environment details and absent model
identities for every selected item.

The issue creation cutoff does not create a historical snapshot: bodies and
comments are the versions retrieved in this task. The selected comments all
predate the cutoff. Some records are closed with GitHub state reason `completed`;
that field is not treated as a reproduced correction. R1 and R5 were open at
retrieval.

## Complete title/body disposition

Eligibility was assigned before reading the selected issue comments. It is
intentionally permissive for mechanism-relevant uncertainty; retaining a report
for inspection does not mean counting it as a defect. In particular R5 and R7 are
adjacent input-side cases, and R2 predates the focal TFLite stack.

| Order | Issue | Disposition | Reason |
|---|---|---|---|
| 1 | [tensorflow/tflite-support#770](https://github.com/tensorflow/tflite-support/issues/770) | Inspect | Generated segmentation getter stack trace and label-axis mismatch; directly relevant. |
| 2 | [tensorflow/tensorflow#97](https://github.com/tensorflow/tensorflow/issues/97) | Exclude | General request for extracting trained-model predictions; no association/resource contract mechanism in title/body. |
| 3 | [tensorflow/tensorflow#504](https://github.com/tensorflow/tensorflow/issues/504) | Exclude | Transfer-learning tutorial request; no deployment association mechanism in title/body. |
| 4 | [tensorflow/tensorflow#1269](https://github.com/tensorflow/tensorflow/issues/1269) | Inspect | Manual Android output-name binding changes from output:0 to softmax:0, followed by unsupported operation; adjacent binding report, uncertain metadata relevance. |
| 5 | [tensorflow/tensorflow#2072](https://github.com/tensorflow/tensorflow/issues/2072) | Exclude | Training category-list division by zero; no deployed output/metadata contract. |
| 6 | [tensorflow/tensorflow#2084](https://github.com/tensorflow/tensorflow/issues/2084) | Exclude | GraphDef parse failure after replacing Android assets; no explicit label/resource/binding mismatch mechanism. |
| 7 | [google-ai-edge/mediapipe#9](https://github.com/google-ai-edge/mediapipe/issues/9) | Exclude | Face-detection quality/screenshot report; no contract mechanism described. |
| 8 | [google-ai-edge/mediapipe#22](https://github.com/google-ai-edge/mediapipe/issues/22) | Inspect | Model replacement explicitly adjusts label map, num class and num boxes, then no detections; uncertain downstream compatibility mechanism. |
| 9 | [google-ai-edge/mediapipe#195](https://github.com/google-ai-edge/mediapipe/issues/195) | Inspect | Classification calculator example specifies num_classes absent from options schema; adjacent documented cardinality/configuration discrepancy. |
| 10 | [google-ai-edge/mediapipe#199](https://github.com/google-ai-edge/mediapipe/issues/199) | Exclude | Generic model replacement stops preview while outputs are explicitly ignored; no label/output-metadata mechanism in title/body. |
| 11 | [google-ai-edge/mediapipe#204](https://github.com/google-ai-edge/mediapipe/issues/204) | Exclude | Queue/deadlock and memory/rendering complaint; label map appears in pasted graph but no label-contract mechanism is alleged. |
| 12 | [tensorflow/tflite-support#624](https://github.com/tensorflow/tflite-support/issues/624) | Exclude | Training data-loader image resize question, not label-map association or output contract. |
| 13 | [tensorflow/tflite-support#870](https://github.com/tensorflow/tflite-support/issues/870) | Inspect | Reports inability to import model in Android ML folder then image-byte decoding failure; retained as uncertain generated-binding compatibility, though primary symptom is input-side. |
| 14 | [tensorflow/tensorflow#492](https://github.com/tensorflow/tensorflow/issues/492) | Exclude | GPU memory allocator issue during RNN training. |
| 15 | [tensorflow/tensorflow#1045](https://github.com/tensorflow/tensorflow/issues/1045) | Exclude | Training input queue epochs variable initialization failure. |
| 16 | [tensorflow/tensorflow#1824](https://github.com/tensorflow/tensorflow/issues/1824) | Exclude | Generic computational-graph profiling feature request. |
| 17 | [tensorflow/tensorflow#1990](https://github.com/tensorflow/tensorflow/issues/1990) | Exclude | Python wheel/platform installation mismatch. |
| 18 | [tensorflow/tensorflow#2386](https://github.com/tensorflow/tensorflow/issues/2386) | Exclude | Distributed training synchronization hang. |
| 19 | [tensorflow/tflite-support#269](https://github.com/tensorflow/tflite-support/issues/269) | Exclude | Repeated inference memory/thread exhaustion; labels are read but no label-contract failure alleged. |
| 20 | [tensorflow/tflite-support#703](https://github.com/tensorflow/tflite-support/issues/703) | Inspect | Object-detector writer produces four output metadata entries for one-output YOLOv5; explicit cardinality rejection while preparing Android import. |
| 21 | [google-ai-edge/mediapipe#194](https://github.com/google-ai-edge/mediapipe/issues/194) | Exclude | Serialized media SequenceExample/TFRecord format complaint, not model-associated resource parsing. |
| 22 | [google-ai-edge/mediapipe#197](https://github.com/google-ai-edge/mediapipe/issues/197) | Exclude | Video input file cannot be opened; unrelated media-path error. |
| 23 | [google-ai-edge/mediapipe#266](https://github.com/google-ai-edge/mediapipe/issues/266) | Exclude | Request for source to export detected hand coordinates; metadata means runtime result, not embedded model metadata. |
| 24 | [google-ai-edge/mediapipe#289](https://github.com/google-ai-edge/mediapipe/issues/289) | Exclude | Feature extraction ends at error writing an output file; no output-metadata contract diagnostic. |
| 25 | [google-ai-edge/mediapipe#362](https://github.com/google-ai-edge/mediapipe/issues/362) | Exclude | Missing FFmpeg header during build; unrelated dependency error. |
| 26 | [tensorflow/tflite-support#181](https://github.com/tensorflow/tflite-support/issues/181) | Exclude | C++ header/unique_ptr API usage question, unrelated binding generator or model output association. |
| 27 | [tensorflow/tflite-support#278](https://github.com/tensorflow/tflite-support/issues/278) | Exclude | Undefined Python writer variable NameError; no model/resource validation reached. |
| 28 | [tensorflow/tflite-support#319](https://github.com/tensorflow/tflite-support/issues/319) | Inspect | Task BERT API reports missing metadata process unit; retained as adjacent resource/precondition compatibility, input-side rather than focal output association. |
| 29 | [tensorflow/tflite-support#395](https://github.com/tensorflow/tflite-support/issues/395) | Exclude | C++ unique_ptr/StatusOr compilation error; unrelated metadata compatibility. |
| 30 | [tensorflow/tflite-support#450](https://github.com/tensorflow/tflite-support/issues/450) | Exclude | Question about interpreting non-probability score; no association/order/resource or generated-binding failure specified. |

## Permissible paper use

- **Supported motivation:** at least one publicly reported generated segmentation
  getter failure has a concrete stack trace and a member explanation directing
  developers to a different official consumer. Consumer selection and its support
  boundary matter to integration, including when code is generated.
- **Supported counterweight:** public reports also show existing structural
  rejection, wrong asset selection, unsupported operations and input-decoding
  assumptions. They do not support a blanket claim that official checks are
  missing or that metadata explains every cross-platform discrepancy.
- **Unresolved significance:** how often these situations occur, their current
  supported configurations, diagnosis time, avoided incidents, production exposure
  and downstream user costs remain unmeasured. Public issues are not an
  independently labeled natural-defect corpus.
- **Novelty implication:** do not cite R1 only as favorable motivation. Its prior
  report limits firstness claims about generated getter failure. The remaining
  distinction must rest on the study's verified controlled characterization,
  not discovery of this failure category.

## Provenance and repeat command

[public-report-sources.json](public-report-sources.json) preserves all query
strings, returned order/IDs, fetch commands, UTC retrieval timestamps, raw response
SHA-256 digests, disposition reasons and selected-report judgments. Full responses,
comments and stderr remain outside Git under
`/workspace/significance-review-20261004/public-reports/`. No uploaded model or
third-party full text is included in this repository.

The [collector](scripts/search_public_reports.py) writes new files exclusively.
For another inquiry, use a new external directory; rerunning live search is not
guaranteed to reproduce this historical result order or content. The commands
actually used were:

```sh
python research/20261004-significance-review/scripts/search_public_reports.py search \
  --output /workspace/significance-review-20261004/public-reports
# After title/body triage, eligible.json lists seven URLs in fixed return order.
python research/20261004-significance-review/scripts/search_public_reports.py inspect \
  --output /workspace/significance-review-20261004/public-reports \
  --eligible /workspace/significance-review-20261004/public-reports/eligible.json
```

Both command outputs were redirected to `search.stdout` / `inspect.stdout` in the
same external directory. The committed JSON preserves the selected URL list and
selection reasons; manual triage is not presented as an automatic detector or a
human-annotator study.
