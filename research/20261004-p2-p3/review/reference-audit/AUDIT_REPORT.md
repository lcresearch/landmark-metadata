# Independent P3 reference-chain audit

**Decision: PASS for a qualified publisher-documented display-order reference. The protocol's complete stable-class-ID chain remains UNVERIFIABLE / ABSTAIN.** This is an AI-agent audit, not a completed human audit. No network retrieval, model inference, or modification of P3/older evidence was performed. All new files are under this review directory.

## Link-by-link judgment

| Link | Status | Basis and limit |
|---|---|---|
| Focal -> exact publisher object | PASS | Fresh retrieved version-1 model bytes equal exact focal SHA-256. |
| Publisher/versioned TFHub artifact provenance | PASS | Saved successful official TFHub versioned request, publisher redirects and remote-url metadata; artifact bytes/hash and storage generation retained. This is publisher provenance, not a verified build attestation. |
| TFHub artifact -> focal computational identity | PASS | All 165 non-metadata buffers, complete parsed computation fields, output tensor indices/order and tensor fields agree. Whole files and metadata differ. |
| Version-pinned Lite card -> exact parent card | PASS | Immutable-commit raw Markdown matches resolved commit tree blob hashes; Lite fp32/2 explicitly declares classification/1. |
| Parent card -> external display mapping and offset | PASS | Exact parent card states 1000 classes, points to separate external ImageNetLabels object, and explicitly says ignore leading background; no fitted offset. |
| External mapping -> full original/mutant display agreement | PASS | All 1000 original positions match; cyclic permutation mismatches 999 positions, with duplicate maillot at 638/639. |
| Output index -> stable synset/class ID -> display name | UNVERIFIABLE | The graph-linked mapping retrieved here contains display strings, not unique stable IDs; duplicate names prevent recovering a unique ID chain from those strings alone. Ancillary generic dataset resources need their own model-specific bridge. |
| Prediction correctness or task accuracy | UNVERIFIABLE | Reference agreement is an output-association property. No independently ground-truthed image accuracy test is supplied. |
| Independent human audit | UNVERIFIABLE | This is an AI-agent read-only evidence audit. |

These statuses evaluate whether each evidence link supports its stated scope. The mutant's 999 reference disagreements are an expected finding, not an audit failure.

## Independent recomputation

`audit_candidate.py` reads saved bodies and model bytes directly. It does not import the P3 analysis script or old checker/canonicalizer. Its final run reports **38 PASS checks and no FAIL checks**; full results and 1,000 comparison rows are in `results.json`.

- Focal model SHA-256: `6c7ab0a6e5dcbf38a8c33b960996a55a3b4300b36a018c4545801de3a3c8bde0`.
- TFHub model SHA-256: `7276a936443685daae8612fc3cb9370247cb1f4966286cd95e02c44e1183f0dd`. The whole files differ.
- Both contain 166 buffers. Only metadata buffer 165 differs; all other 165 buffers match byte for byte. The metadata buffer is not referenced by any graph tensor. Complete independently serialized non-metadata model fields and weights match; ordered output tensor 163 is the same float32 `[1,1000]` tensor backed by buffer 164. This establishes graph/weight/output-order equivalence, without reconstructing undocumented conversion history.
- The parent card is **classification/1**, as explicitly declared by the exact **lite0/fp32/2** card. Classification/2 is not substituted merely because its mapping text is similar.
- The exact parent card states 1,000 classes, explicitly links the standalone ImageNetLabels object, and says to ignore the first background entry so output index 0 is `tench`. The offset is fixed by this text, not chosen by matching focal labels.
- After that documented offset, original and restored resources match **1,000/1,000** reference strings. The fixed permutation mismatches **999/1,000**. Position 904 is `window screen` in the reference/original/restoration and `window shade` in the permutation; the independently recorded E2 score remains unchanged.
- Display names are not unique IDs: `crane` occurs at positions 134/517 and `maillot` at 638/639. Only the adjacent maillot pair leaves position 638's displayed string unchanged under the one-position cyclic shift.

The external label bytes are a separately retrieved object expressly prescribed by publisher documentation, rather than labels extracted from the focal model and renamed ground truth. This is source separation from the mutated package, not statistical independence, independent training verification, or a human accuracy oracle.

## Source pinning and the preserved first audit failure

The cards were retrieved by immutable TFHub catalog commit `81fdea8ffa53b5acbd66a012d17fb8f9602c714b`. Their raw bytes independently reproduce the Git blob hashes stored in the recursive tree. The commit names root tree `1dade93cc8973a65e45373a0fdbc2cc2d99088f7`.

The first audit used the condition `tree_response.sha == commit.commit.tree.sha`. It failed: the saved GitTrees response to a **commit-addressed request** reports the requested commit SHA in its header, while the saved commit correctly records a different root-tree object SHA. The complete initial script, results, stdout and stderr are retained in `attempt-1-header-assumption/`; no source evidence was edited.

The revised audit does not accept either SHA by fiat. It reconstructs Git's tree-object byte encoding from the saved entry names, modes and child hashes. The root reconstructs exactly to the commit's declared tree SHA, and **all 3,411 directory tree objects** reconstruct to their declared hashes. Both card bodies then match their committed blob hashes. This resolves the audit-condition issue through stronger object-level checking. It does not constitute an independent cryptographic authentication of the original network source.

The catalog commit preserves the publisher statement available in the retrieved snapshot; it is not asserted to be the original model-release-time documentation. The external label URL is unversioned. Its retained SHA-256 is `536feacc519de3d418de26b2effb4d75694a8c4c0063e36499a46fa8061e2da9`, with recorded storage generation `1542242075395516`; do not infer historical lifetime immutability from this snapshot.

## Stable IDs and protocol completion

The saved generic TensorFlow synset order has 1,000 entries. Independently recomputing its names finds 1,000 matches with the separately linked checkpoint full-name list and 1,000 first-synonym matches with the display reference (`ancillary-stable-id-review.json`). This corroboration does not supply the missing exact-artifact-to-training-synset lineage. In particular, duplicate display strings cannot resolve which stable synset belongs to each duplicate position from display agreement alone.

The original P3 question asked for **output index → stable class ID → display name**. That complete chain is **not established**. The narrower **output index → publisher-prescribed display string** chain is supported. It is legitimate to strengthen the manuscript to reference-consistent original/restoration and reference-inconsistent permutation display associations; it is not legitimate to claim stable-ID semantic correctness, incorrect prediction of an input, accuracy degradation, or a natural EfficientNet defect.

The bounded request inventory is 12 initial candidates and 18 follow-ups (25 HTTP 200, five HTTP 404), matching the frozen limits. This audit issued no additional request. P3's distinction between qualified display success and stable-ID abstention is appropriate; no required wording correction was found in its completed results/impact documents. Earlier E5 abstentions must remain historical outputs from a run without this supplied reference.

## Strongest defensible manuscript wording

> A publisher-prescribed external reference now supports display-label order for the focal classifier. A versioned TFHub Lite0 fp32/2 artifact has identical computational fields, ordered outputs, and all 165 non-metadata buffers to the focal model. Its commit-pinned card identifies classification/1 as parent; that card explicitly prescribes an external 1,001-line label file with the background line omitted. Original and restored associations agree at all 1,000 output positions, while the predetermined cyclic permutation disagrees at 999 despite successful E2 decoding. This establishes disagreement with the documented display-order specification. The complete artifact-to-stable-synset provenance chain and prediction correctness remain unverified; human review is pending.

## Reproduction and remaining review

```bash
PYTHONDONTWRITEBYTECODE=1 /workspace/hand-contract-repro/.venv/bin/python /workspace/metadata-contract-p2p3-20261004T073824Z/review/reference-audit/audit_candidate.py > /workspace/metadata-contract-p2p3-20261004T073824Z/review/reference-audit/audit.stdout 2> /workspace/metadata-contract-p2p3-20261004T073824Z/review/reference-audit/audit.stderr
```

`results.json` records input paths/hashes, generated-schema path/hash, the script hash/command, per-buffer comparison, complete output descriptors, all Git tree/blob checks, and the complete display-order comparison. Schema parsing remains a shared dependency and no new inference validates the publisher's training assertions. The source cards' deployment relationship is a publisher statement; this audit did not recreate the classification/1-to-TFLite export. Independent human review of that documentary and artifact chain remains pending.
