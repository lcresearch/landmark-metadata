# P2/P3 follow-up source and evidence index

Read `RESULTS_OVERVIEW.md` for completed findings and their limits,
`MANUSCRIPT_IMPACT.md` for claim changes, and `HUMAN_AUDIT.md` for pending review.
`CURRENT_STATE.md` is the frozen starting-state note and is intentionally not
rewritten to look like a pre-existing result.

- `P2/`: ten same-Android generated-wrapper/Task configurations.
- `P3/`: bounded publisher-reference retrieval and full display-order comparison.
- `review/`: separate raw-record, reference-chain and implementation reviews.
- `manuscript/paper.tex`: current targeted revision, rebuilt by
  `scripts/revise_paper.py` from the sealed prior manuscript.
- `BUILD_REVIEW.md`: nine-page generic build/visual review; no venue-fit claim.
- `EVIDENCE_INDEX.json` and `CLAIM_EVIDENCE_FOLLOWUP.json`: local evidence hashes
  and strengthened-claim links, written at finalization.

The local evidence root is
`/workspace/metadata-contract-p2p3-20261004T073824Z`. Its `SHA256SUMS` incorporates
the P2, P3 and mechanism submanifests plus the final reviews/manuscript. Mutable
SDK/AVD state and unmanifested operational files are excluded according to P2's
seal. Do not write to sealed subpackages or rerun finalization against them.

The corresponding GitHub area is a selected **source/documentation copy only**.
It omits model/dependency binaries, third-party retrieved source, generated Java,
APKs/classes/DEX, raw JSON/tensors/images, logs, PDF/preview and SDK/emulator state.
Relative references to those omitted evidence files remain local provenance
locators, not available downloads. Scripts retain their original path-dependent
prerequisites and are not advertised as a standalone clean-machine reproduction.
Dependency lock text and candidate URL plans are included as source configuration.

Reproduction requires recovering the specified prior inputs and installed pinned
tools, adapting output roots to a new directory, and reviewing the commands before
execution. The manuscript source alone can be built separately with TeX. Human
audit is pending; all recorded reviews this round were performed by agents.
