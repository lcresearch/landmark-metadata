# P3: Bounded independent class-order reference inquiry

Frozen before new network retrieval on 2026-10-04 UTC. This is automated evidence inquiry, not independent human verification.

## Question and interpretation
Can the exact EfficientNet-Lite0 artifact used in E1/E2 be connected, independently of its embedded metadata and associated label bytes, to an authoritative complete output-index → stable class ID → display-name mapping?

Focal artifact: `/workspace/metadata-contract-e2e-20261004T030536Z/E1/variants/original/model.tflite`, SHA-256 `6c7ab0a6e5dcbf38a8c33b960996a55a3b4300b36a018c4545801de3a3c8bde0`.
Publisher locator: `https://storage.googleapis.com/mediapipe-models/image_classifier/efficientnet_lite0/float32/1/efficientnet_lite0.tflite`.

A mapping match is distinct from an artifact-to-reference provenance chain. The original embedded labels are comparison data, never an independent oracle. A generic ImageNet label list, matching a single index, or a same-named model is insufficient. A byte-identical or carefully documented graph/weights-equivalent model bridge may establish identity; a matching architecture name does not.

## Bounded sources
Only these three official publisher/source families will be examined:
1. Google MediaPipe publisher model object, model documentation and directly linked model cards.
2. TensorFlow Hub official model catalog/cards and explicitly referenced downloadable EfficientNet-Lite0 artifacts.
3. Google AutoML / TensorFlow Models official EfficientNet-Lite training, export, and dataset/class mapping source.

At most 12 initial candidate locators and at most 18 directly linked follow-ups (source revision resolution, explicitly referenced mapping/export code, model files). Network redirects within a request do not create new candidates; all redirects/final URLs and status codes are recorded. HTTP errors count as examined candidates. No broad model collection, natural-bug search, or replacements outside these bounds.

Predeclared initial candidates:
- the exact MediaPipe publisher model URL above;
- `https://ai.google.dev/edge/mediapipe/solutions/vision/image_classifier`;
- `https://raw.githubusercontent.com/tensorflow/tfhub.dev/master/assets/docs/tensorflow/efficientnet/lite0/classification/2.md`;
- `https://raw.githubusercontent.com/tensorflow/tfhub.dev/master/assets/docs/tensorflow/lite-model/efficientnet/lite0/fp32/2.md`;
- `https://raw.githubusercontent.com/tensorflow/tfhub.dev/master/assets/docs/tensorflow/lite-model/efficientnet/lite0/fp32/1.md`;
- `https://tfhub.dev/tensorflow/lite-model/efficientnet/lite0/fp32/2?lite-format=tflite`;
- `https://tfhub.dev/tensorflow/efficientnet/lite0/classification/2`;
- `https://raw.githubusercontent.com/google/automl/master/efficientnet/lite/README.md`;
- `https://raw.githubusercontent.com/google/automl/master/efficientnet/README.md`.

Up to three remaining initial slots may be used for official export/class mapping locators motivated by these pages. Their selection rationale must be recorded before retrieval. Follow-ups must record parent/source relationships.

## Procedure
1. Freeze this plan and hash; verify focal artifact SHA-256; recover existing provenance without rewriting it.
2. Archive network bodies, status, headers, redirects/final URLs, retrieval times and SHA-256. Resolve source revisions where accessible. Preserve failed requests too.
3. Inspect cards and export/training source for the exact artifact bridge, output class count/offset, background handling, stable IDs and label rendering.
4. If a candidate mapping is found, compare the complete mapping to the focal resource. Report positional string matches and stable-ID evidence separately; repeated strings (including maillot) are not unique IDs.
5. If an independently tied mapping exists, evaluate original and predeclared E2 cyclic permutation against it. Otherwise report I = ABSTAIN / provenance chain incomplete; E2 remains an association change relative to the original.

## Stop conditions
Stop at a complete trustworthy chain with full mapping comparison, or when the bounded source set/follow-up allowance has been exhausted, or every discovered plausible official chain terminates at missing/unlinked evidence. Do not broaden source families or infer undocumented conversion lineage. Failure to find an oracle completes this inquiry and does not invalidate E2.

## Deliverables and preservation
`results.json`, `EXPERIMENT_P3_RESULTS.md`, command/retrieval scripts and log, `MANUSCRIPT_IMPACT.md`, `HUMAN_AUDIT.md`, and SHA256SUMS. Raw downloaded artifacts/pages/models stay outside the source-only GitHub repository. Existing evidence is read-only. Versions and all comparisons are recorded. No inference or accuracy experiment is planned.
