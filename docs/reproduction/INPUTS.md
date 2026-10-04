# Inputs and evidence availability

This is a finite, read-only inventory made on **2026-10-04 UTC**, based on repository
revision `052a839cdc64ec43ce362dde0cd3e410926e107d`.
[inputs.json](inputs.json) contains the exact checked paths, expected and observed
digests, source-file digests and observation timestamp. No model was downloaded,
generated, compiled or executed for this inventory. A matching manifest-file
digest does **not** authenticate all files listed inside that manifest.

## Primary EfficientNet model conditions

The starting object is the direct `.tflite` download
[`efficientnet_lite0/float32/1/efficientnet_lite0.tflite`](https://storage.googleapis.com/mediapipe-models/image_classifier/efficientnet_lite0/float32/1/efficientnet_lite0.tflite).
There is no enclosing task-bundle member to select. Its appended ZIP resource is
`labels_without_background.txt`. The URL is a retrieval locator; require the exact
digest below even when the path contains a version. Network availability was not
retested in this handoff.

All five selected local model files were read and their complete bytes rehashed;
each matches its historical recorded digest. The selected resource member was
also read from each model's ZIP and rehashed. Exact local paths are in the JSON.

| Condition | Model SHA-256 | Input preparation |
|---|---|---|
| Original | `6c7ab0a6e5dcbf38a8c33b960996a55a3b4300b36a018c4545801de3a3c8bde0` | Publisher bytes |
| Description control | `ed16d9573d8fe3e489c27637036a4e5c8476d15f013b7116f89864d55432f51d` | Same-length case change in one description byte |
| Label deletion | `739f08462e831806db6a9bce7ed5b70a037fce593003028e5d6911dbd284fd83` | Delete the final label line; deterministically rebuild appended ZIP |
| Label permutation | `455a04a2c6193ea81bef8fbc47e193aee0449b8cebdc9cc487c7e9e85fe42da7` | One-position cyclic left shift, declared before prediction inspection |
| Restoration | `0a605ed10a38fc6f92fc4e266f5560756d2809e2669c45aa3b5a631cd88cea72` | Restore original associated payload; container bytes differ from publisher package |

The E1 restoration file was rehashed. The E2 inverse-permutation restoration
alias and five P2 copied model files were checked for existence only in this
inventory; their historical expected digests are separately labeled. Do not
read those existence checks as another APK, preload or native-buffer identity
audit. Inputs are one computational graph under five model-byte conditions,
not five independent models.

For P2, `/workspace/metadata-contract-p2p3-20261004T073824Z/INPUTS.json` is
**present locally but excluded from Git**. Its freshly measured SHA-256 is
`61b1fa22db4562586d6294bd6919bf6d4591efab03dde20745ea5212da4a6ce7`.
[P2 preparation](../../research/20261004-p2-p3/P2/scripts/prepare.py) reads
`ROOT.parent/INPUTS.json`: the necessary field is an `input_models` array of
objects containing `variant`, absolute `path`, and expected `sha256`.
Use exactly `original`, `description_control`, `label_deletion`,
`label_permutation`, and `restoration`; the historical restoration maps to
E1 `label_restoration`. For a new run, create a separately reviewed configuration
under its new parent directory using the hashes above and actual new model paths.
Do not edit the old configuration or reuse its absolute paths without checking
the corresponding bytes. The JSON inventory records this schema and availability.

The exact historical mutation definitions are in
[prepare_e1.py](../../sources/metadata-contract-e2e-20261004T030536Z/scripts/prepare_e1.py),
[prepare_e2.py](../../sources/metadata-contract-e2e-20261004T030536Z/scripts/prepare_e2.py)
and [suite_static.py](../../sources/metadata-contract-paper/scripts/suite_static.py).
These scripts require their documented sibling files and external workspace;
copying one script alone is insufficient. The first description byte in
`Probabilities of the 1000 labels respectively.` is XORed with 32. Restoration
uses the original member bytes; it is not a copy of the whole original model.

| Resource payload | SHA-256 of `labels_without_background.txt` |
|---|---|
| Original, description control, restoration | `e697a491aa735cc6c2aaf982f8e86e8fc7b0a1ea7750a2cc6a2bdfc1e109012f` |
| Deletion | `7da978074d861c47f650a000db04db008aaecafcc1ae3e58eb71718e36c5ff4a` |
| Permutation | `334152d1cce3445fc73c27c32001b5a6e8b7e548a37cc0e050ea363ebde18d3a` |

The recorded canonical graph digest is
`73e57df01115600419abb72de4b2c3257200e12eb205d335bcbfc203a589bee8`.
Canonicalization removes the `TFLITE_METADATA` entry, clears its buffer and
repacks the graph; the digest is not a whole-package digest and omits appended
resources. This turn did **not** rerun canonicalization, compare graph fields or
rehash individual FlatBuffer buffers. The JSON marks canonical and embedded
metadata digests as recorded values. Their preservation analysis must be rerun
with the pinned schema/library implementation when reproducing P.

## Deterministic RGB inputs

Both inputs are 224 × 224 × 3 bytes, row-major RGB (`150528` bytes). The harness
constructs an `ARGB_8888` bitmap with alpha 255, then loads `TensorImage(UINT8)`;
the generated wrapper performs its own preprocessing. These hashes identify
the RGB source bytes, not an inferred normalized interpreter-input tensor.

| Input | Definition | RGB SHA-256 |
|---|---|---|
| `gray127` | Every channel is 127 | `0748107f4221d0bb4ed8bada6a865b9348fb3b2a4c83b46f8e5eee704078b0ca` |
| `rgb_pattern` | Byte at zero-based offset `j` is `(37*j + 17) & 255` | `fb23d2aecf5083dd57637ecebd7e80993a33af2561208c4cdd732cfe9249052f` |

This handoff recomputed both formulas without inference and rehashed both
saved input files in each of three selected locations: E1 original, P2 wrapper
original and P2 Task original. All six files match the expected digests.
Other condition/input files were not exhaustively checked. Task deletion has
no reached input execution in the historical P2 record; do not manufacture it
from these definitions.

Construction source:
[E1/E2 instrumentation](../../sources/metadata-contract-e2e-20261004T030536Z/scripts/ContractInstrumentation.java),
[P2 wrapper instrumentation](../../research/20261004-p2-p3/P2/scripts/ContractInstrumentation.java)
and [P2 Task instrumentation](../../research/20261004-p2-p3/P2/scripts/TaskInstrumentation.java).
No image dataset or image-class ground truth is required for these observations.

## P3 reference prerequisites

P3 is a reference/graph comparison, not an inference run. The following six
preserved response bodies are present and were rehashed against their historical
retrieval records. Original request URLs, local body paths and retrieval-record
hashes are in `inputs.json`; no new HTTP request was made.

| Object | Exact identity / role |
|---|---|
| Publisher version-1 model (`I01`) | Same `6c7ab0…` model digest above |
| [TFHub Lite0 fp32/2](https://tfhub.dev/tensorflow/lite-model/efficientnet/lite0/fp32/2?lite-format=tflite) (`I06`) | Package SHA-256 `7276a936443685daae8612fc3cb9370247cb1f4966286cd95e02c44e1183f0dd` |
| [Pinned Lite card](https://raw.githubusercontent.com/tensorflow/tfhub.dev/81fdea8ffa53b5acbd66a012d17fb8f9602c714b/assets/docs/tensorflow/models/efficientnet/lite0/fp32/lite/2.md) (`F07`) | SHA-256 `77300c8c37140316900b5712ad4c73f9dd2e87d0701c5804cdccf185b2b8bfae`; names classification/1 parent |
| [Pinned parent card](https://raw.githubusercontent.com/tensorflow/tfhub.dev/81fdea8ffa53b5acbd66a012d17fb8f9602c714b/assets/docs/tensorflow/models/efficientnet/lite0/classification/1.md) (`F10`) | SHA-256 `2b94894d016a0b9a6edcb09d19d3e4b9a3d22ab5393c1af85c70d34a75511f58`; prescribes external labels and background offset |
| [ImageNetLabels.txt](https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt) (`F11`) | SHA-256 `536feacc519de3d418de26b2effb4d75694a8c4c0063e36499a46fa8061e2da9` |
| [Publisher label-list URL](https://storage.googleapis.com/mediapipe-tasks/image_classifier/labels.txt) (`F01`) | Same `536fea…` bytes as F11 |

The TFHub logical URL historically redirected through Kaggle to a signed,
expiring download URL. Obtain a new redirect from the logical URL and require
the digest; the old signed URL is not a portable acquisition address. The label
URLs are unversioned, so a matching future response must not be presumed.

For a fresh P3 analysis, follow the complete graph/weights/ordered-output bridge,
then the exact parent-card instruction to remove the first background line.
Do not compare only position 904 or silently use a generic ImageNet label list.
The preserved [P3 report](../../research/20261004-p2-p3/P3/EXPERIMENT_P3_RESULTS.md)
links its analysis and records the narrower display-order result. This input
inventory rehashes source objects and analysis records; it does not redo the
bridge or independently derive the full mapping. The separate finite reader
recounts agreements in the already stored 1000-position table. Stable class-ID
lineage remains unresolved, and matching duplicate display strings cannot
establish it.

## Original evidence versus later reconstruction

The original E1/E2, construction-audit and P2/P3 directories are present on this
machine. Six manifest **files** were rehashed successfully; entries inside them
were not all reopened. These are local provenance locators, not download links:

| Manifest path under `/workspace/` | SHA-256 of manifest file |
|---|---|
| `metadata-contract-e2e-20261004T030536Z/SHA256SUMS` | `aba0739ac893ee69795556d43384029d20cc096a584156d0f0c37638fdc8751d` |
| `metadata-contract-audit-20261004T062010Z/SHA256SUMS` | `b73388bf6ce263d9fff7659a90166d80ae56544d540a12620768a1bc8a8af89d` |
| `metadata-contract-paper-revision-20261004T065132Z/SHA256SUMS` | `daa981d200c058a8a958ee20c8fdfd1dee0b0bfa560f543d14540e73cd23c13a` |
| `metadata-contract-p2p3-20261004T073824Z/P2/SHA256SUMS` | `d903826e8d6f666921ba9e6e9247fe541cb3b7c6b8170113c4b5c572f82f58d5` |
| `metadata-contract-p2p3-20261004T073824Z/P3/SHA256SUMS` | `77345fcadf085095d23722ac7a16ef7c4d5d34c202e4f32b7046750cad919de3` |
| `metadata-contract-p2p3-20261004T073824Z/SHA256SUMS` | `aed26d18de158a3eebf5dcd7a3996356da99419779b689addd1f083a6a0cec27` |

The separately reported [fresh reconstruction](../../sources/repro-audit-20261004/REPORT.md)
used `/workspace/repro-android`, `repro-task`, `repro-hand`, `repro-external`,
`repro-claims`, `repro-audit` and `repro-control`. **All seven paths and
`/workspace/reproduction-evidence-index-20261004.json` are absent at their
recorded locations in this handoff.** That is an exact-path check, not a search
of every disk. Historical E1/E2 records cannot authenticate that later run.
The current [maintained readback](../../work/observation-review-20261004/README.md)
needs those distinct records and the original 65-fixture E5 catalog, expected
SHA-256 `bf49a475696eec4b38fb17587f6541a8393da14297e5dca1d433a051ba166e79`;
that catalog is also missing at the checked path.

Two old ZIP archive paths are present (`hand-contract-evidence.zip` and
`metadata-contract-paper-sources.zip`). This inventory checked their existence
and size only; expected historical digests are labeled separately in the JSON.
It did not authenticate their bytes, inspect their entries or identify them as
the complete later E1/E2/P2/P3 package.

## Remaining handoff gaps

- No portable evidence-deposit/download locator is recorded for the full
  original or reconstruction raw package. Local presence does not make the
  source-only repository a complete archive or promise future availability.
- Generated Java, classes/DEX, APK assets, raw outputs and logs are excluded
  from Git. This inventory rehashed one original generated Java example
  (`60c1fb6022891cc2bd41b5bacdd2194361eb0ca40e37da2eddf6cba963279670`),
  not every build or APK. A fresh run must create and audit its own artifacts.
- Secondary Gesture/Hand/Linux Task/E4/E5 recovery is not made complete by
  this focal inventory. Use their preserved source protocols and require their
  own models, bundles/members, inputs, dependency locks and frozen catalogs;
  do not substitute another model/version when any are unavailable.
- Human verification, clean-machine reconstruction, network retrieval and
  installed SDK/runtime readiness were not performed by this input inventory.
  Stop on a missing or mismatched prerequisite rather than reporting a partial
  inventory as an experimental PASS.
