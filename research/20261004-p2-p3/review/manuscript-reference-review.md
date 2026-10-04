# P3 manuscript reference review

**Result: PASS for the P3 claim scope; no blocking factual correction.** This is an AI evidence-consistency review, not a human audit. The manuscript and sealed reference-audit content were read only; this report is written outside that audit subtree.

Reviewed manuscript: `/workspace/metadata-contract-p2p3-20261004T073824Z/manuscript/paper.tex`.
Full source SHA-256 at review: `81594a27f7653f0df61b96c8cd5fe846e1b56407970feeeb1f366fc0e69124a9`.
Selected P3-related section fingerprint: `72f69068f9cf05ea46d73ecef9f6d6ed0761bd303c07184f186060b5975bfa77`.
P2 edits may occur concurrently; this judgment covers P3 content only and not later unreviewed edits or PDF formatting.

## Checks against the retained P3 audit

- **Abstract:** Correctly upgrades the conclusion to disagreement with a publisher-prescribed **display-label order**, names the graph/weights bridge, and leaves stable class-ID provenance unresolved. It does not claim prediction error or accuracy loss.
- **I definition:** Distinguishes display-string reference agreement from stable identifiers. It retains artifact linkage, human review, and the limit that original embedded labels alone are not an independent reference.
- **P3 chain:** Correctly states 166 buffers / 165 equal non-metadata buffers, metadata buffer 165 not used as tensor data, tensor 163 with `[1,1000]`, and equal computational/output descriptors. The exact Lite fp32/2 card points to **classification/1**, and the parent explicitly provides the background-removal rule. The text does not substitute classification/2, fit an offset, infer byte-identical packages, or claim reconstructed export history.
- **Full comparison:** Original/restored 1,000 matches and mutant 999 disagreements are correct; position 904 and both duplicate-string pairs are accurate. Successful decoding and unchanged score bits come from E2, while P3 adds reference comparison without new inference.
- **Reference provenance limits:** Current catalog snapshot versus original release-time documentation, unversioned external URL, stored reference hash, unresolved stable-synset lineage, and pending human source interpretation are retained.
- **Hand introduction:** Describes a different reference-backed role association; it no longer claims Hand uniquely supplies the independent reference that the classifier still lacks.
- **Historical E5/baseline abstention:** The manuscript explicitly leaves the 65 earlier semantic judgments and baseline runs unchanged because no reference was supplied to those runs. The later P3 comparison is kept separate. No retrospective checker-success claim appears.
- **Validity and conclusion:** Restrict the strengthened result to publisher display-order disagreement and restored agreement. Stable IDs, prediction correctness, and human validation remain unestablished. P stays an intervention-preservation judgment, separate from reference agreement.

## Optional precision edit

In the I definition, replace:

> `$I_{\mathrm{display}}$ compares output positions with prescribed display strings`

with:

> `$I_{\mathrm{display}}$ compares positions within a classification output tensor with prescribed display strings`

Reason: the preceding equation uses `i` for whole output-tensor/metadata-entry roles. The proposed wording makes the distinction from the 1,000 positions inside the classifier's single output tensor explicit. This is a terminology clarification, not an unsupported current result.

## Reference-audit freeze status

The reference-audit subtree is **content-frozen with a hash manifest**. All **13 manifested files** still match their recorded SHA-256 values, including the initial failed-header-assumption attempt. No file in that subtree was changed by this review.

Manifest: `/workspace/metadata-contract-p2p3-20261004T073824Z/review/reference-audit/audit-output-manifest.json`.
Manifest SHA-256: `b0cbee89c97bf2e23e574b5a7b49e76e04d066ba32f4af4b0308f93089a3e334`.

There is no separate filesystem write-protection seal: the directory and files remain owner-writable. Thus “sealed” here means the preserved content/manifest state, not an OS-enforced read-only directory. The manifest itself is excluded from its own inventory, as expected.
