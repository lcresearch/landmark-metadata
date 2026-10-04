# P3 Results: external display-label order established; stable IDs remain unresolved

The bounded inquiry obtained an **external publisher-prescribed output-index → display-label reference** tied to the focal computational graph through an official graph/weights-equivalent TFHub model. It did not establish a complete artifact-specific output-index → stable synset ID provenance chain. These are separate results.

No inference was performed for P3. E1/E2 original, cyclic permutation and restoration model bytes were recovered read-only; network retrievals and comparisons below were fresh. This is automated agent verification, not human verification.

## Observations

| Check | Observation |
|---|---|
| Focal / publisher version 1 / documentation-linked latest | Byte-identical SHA-256 `6c7ab0a6e5dcbf38a8c33b960996a55a3b4300b36a018c4545801de3a3c8bde0` |
| TFHub lite0/fp32/2 artifact | Package SHA differs; all 165 nonmetadata buffers identical out of 166; only metadata buffer 165 differs |
| Graph and output ordering | All nonbuffer/nonmetadata ModelT fields equal, including operator codes, subgraphs, tensor descriptors, output order and signature definitions; metadata buffer 165 is not referenced by any graph tensor |
| Canonical model SHA-256 | `73e57df01115600419abb72de4b2c3257200e12eb205d335bcbfc203a589bee8` for both models |
| Exact output | One subgraph output, position 0, tensor 163, shape [1,1000] |
| Publisher card lineage | Pinned lite0/fp32/2 card explicitly names classification/1 as its parent |
| Parent card rule | The 1000 output indices use external ImageNetLabels.txt; ignore its first background entry, so index 0 means tench |
| Reference object | 1001 lines, beginning background; SHA-256 `536feacc519de3d418de26b2effb4d75694a8c4c0063e36499a46fa8061e2da9` |
| Original / restoration | 1000/1000 display labels agree with prescribed external order |
| Cyclic permutation | 999/1000 display labels disagree; unchanged display at position 638 only |
| Position 904 | Reference/original/restoration: window screen; permutation: window shade |
| Stable IDs | ABSTAIN: candidate generic synset order and separately linked checkpoint full names agree at 1000 positions, but exact artifact-to-synset training lineage was not established |

The background removal follows the explicit parent-card instruction; it was not fitted to maximize agreement. The complete 1000-position comparison is saved, not only the position 904 witness. There are two duplicate display strings: crane at 134/517, maillot at 638/639. String equality cannot establish stable class identity; the adjacent maillot pair explains the sole unchanged display under the predetermined one-position cyclic shift.

## Evidence chain

1. MediaPipe's documented latest float32 download and its version 1 download reproduce the focal artifact hash.
2. TFHub's exact logical model `tensorflow/efficientnet/lite0/fp32/2` downloads a distinct package whose computational graph, ordered outputs and every nonmetadata buffer match the focal model. The embedded metadata buffer differs and is not used as a graph tensor buffer. The bridge is independently recomputed without importing the old checker or mutation implementation.
3. The catalog card at repository commit `81fdea8ffa53b5acbd66a012d17fb8f9602c714b` explicitly describes that exact Lite model as deployment of `tensorflow/efficientnet/lite0/classification/1`.
4. That exact parent card, at the same commit, explicitly prescribes `https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt`, its background offset and zero-based output index 0. The label object is outside the mutated model package. MediaPipe's own full-label-list URL returns identical reference bytes.
5. The complete original, permutation and restoration associated resources are compared against that independent external reference.

This ties a **display-order specification** to the exact focal graph. It is not a re-executed export or proof of the original undocumented conversion history. The pinned catalog commit preserves the publisher statement retrieved now; we do not assert it was the model's original release-time documentation. The external file URL is unversioned, so the preserved bytes/hash are the reference snapshot.

## Exact publisher statements

Pinned [Lite model card](https://github.com/tensorflow/tfhub.dev/blob/81fdea8ffa53b5acbd66a012d17fb8f9602c714b/assets/docs/tensorflow/models/efficientnet/lite0/fp32/lite/2.md):
> TF Lite deployment of tensorflow/efficientnet/lite0/classification/1.

Pinned [exact parent card](https://github.com/tensorflow/tfhub.dev/blob/81fdea8ffa53b5acbd66a012d17fb8f9602c714b/assets/docs/tensorflow/models/efficientnet/lite0/classification/1.md), lines 77–83:
> The indices into logits are the `num_classes` = 1000 classes of the classification from the original training (see above). The mapping from indices to class labels can be found in the file at [download.tensorflow.org/data/ImageNetLabels.txt](https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt) and please ignore the first background class, ie. index 0 corresponds to "tench".

The full protocol question asked for output index → stable class ID → display name. That chain remains incomplete. The completed result is a narrower qualified success for **I_display**; stable-ID I remains **ABSTAIN**. This later reference result does not retroactively change frozen E5 semantic abstentions, nor imply that the existing checker consumed this reference.

## Bounded search and negative outcomes

The frozen plan allowed three official source families, 12 initial candidates and 18 follow-ups. Exactly those bounds were reached: 25 HTTP 200 responses and 5 HTTP 404 responses. The initial legacy TFHub raw paths were 404; a pinned repository tree resolved their moved paths. Two assumed Google AutoML README paths were 404 and their path-history query was empty. The parent card's TPU tutorial URL now redirects to a general PyTorch TPU guide, not a preserved EfficientNet export recipe. Those outcomes remain in the records.

The official TensorFlow TPU EfficientNet-Lite README separately links checkpoint evaluation names. The candidate official TensorFlow Models synset order yields 1000/1000 full-name matches against that checkpoint map and 1000/1000 first-name matches against the display reference. This corroborates a conventional ImageNet ordering but does not independently bind stable synset IDs to the exact downloaded artifact's training lineage. No more sources were sought after the budget. Stable-ID agreement remains ABSTAIN.

## Interpretation and limits

P3 strengthens E2 from a change relative to the embedded baseline to a **violation of an independently supplied publisher display-order specification** for 999 positions, with restoration agreement. It does not establish prediction accuracy, an incorrect classification of an input image, a natural EfficientNet defect, stable class identities for duplicate labels, or external defect prevalence. The immutable E2 execution evidence supplies successful getter behavior; P3 adds the reference comparison rather than a new runtime execution.

## Tool versions and exact artifact records

Analysis Python: `3.11.16 (main, Sep 24 2026, 17:56:40) [Clang 22.1.3 ]`; tflite-support `0.4.4`; FlatBuffers `25.12.19`; NumPy `1.26.4`. Requests use Python urllib and retain status, headers, redirects, raw body SHA and UTC retrieval timestamps. Source requests/commands are in the JSON request plans and `commands.sh`.

| Preserved source | SHA-256 |
|---|---|
| I01-publisher-model | `6c7ab0a6e5dcbf38a8c33b960996a55a3b4300b36a018c4545801de3a3c8bde0` |
| F02-publisher-latest-model | `6c7ab0a6e5dcbf38a8c33b960996a55a3b4300b36a018c4545801de3a3c8bde0` |
| I06-tfhub-lite-model | `7276a936443685daae8612fc3cb9370247cb1f4966286cd95e02c44e1183f0dd` |
| F07-pinned-lite-card | `77300c8c37140316900b5712ad4c73f9dd2e87d0701c5804cdccf185b2b8bfae` |
| F10-pinned-parent-card | `2b94894d016a0b9a6edcb09d19d3e4b9a3d22ab5393c1af85c70d34a75511f58` |
| F11-explicit-class-order | `536feacc519de3d418de26b2effb4d75694a8c4c0063e36499a46fa8061e2da9` |
| F01-publisher-labels | `536feacc519de3d418de26b2effb4d75694a8c4c0063e36499a46fa8061e2da9` |
| F15-tpu-labelmap | `be557fc1338e7892f9845fe785a678e211256e6948a26482b8345ba1d213cc88` |
| F17-synset-order | `70002b0ff5de60a3a17a82dbfcff291931f96225ddf941ad2e182fc39e183d15` |
| F18-synset-names | `5b8db22d2e2b0ad28b55c9c502eb45e018bc0c907524b8782958cca4805689ea` |

See `analysis/reference-chain.json`, `analysis/artifact-bridge.json`, `analysis/full-display-order-comparison.json`, `analysis/candidate-synset-comparison.json`, `SOURCE_EXCERPTS.md`, and `results.json`. Raw sources, models and network responses remain outside the source-only GitHub repository.
