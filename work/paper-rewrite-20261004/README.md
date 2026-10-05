# Controlled executable-contract manuscript rewrite

This source area contains the revised reading draft and its claim–evidence
ledger. It integrates the completed contribution and significance assessments.
It runs no new model experiment and leaves earlier manuscripts and imported
evidence snapshots unchanged.

- [Manuscript source](manuscript/paper.tex)
- [Claim–evidence ledger](CLAIM_EVIDENCE.md): 16 claims/subclaims in narrative order
- [Source identities](claim-sources.json): 48 repository files rehashed here;
  13 external provenance locators inherited from prior indexes, not rehashed
- [Related-work integration notes](RELATED_WORK_NOTES.md)
- [Build and review disposition](BUILD_REVIEW.md)
- [Current manuscript and predecessor identities](../../docs/CURRENT_MANUSCRIPT.json)
- [Reproduction prerequisites and evidence availability](../../docs/reproduction/README.md)

## Argument and contribution

The paper follows contracts → E1 actual getter failure → E2 successful but
changed display association → same-Android enforcement stages → Hand boundary
→ external checks and preflight limits. The P3 reference supports display-order
disagreement with a qualified publisher specification, leaving stable class-ID
lineage unresolved.

The contributions are controlled public-interface execution evidence and a
configured enforcement-stage comparison. E5 remains supporting diagnostics:
the core comparison adds no rejection beyond the matched simple baseline or
Task initialization. Support #770 is both engineering context and an earlier
generated-getter failure report; its member reply calls that segmentation
generation route unsupported. It is not a new reproduced natural defect.

The [claim ledger](CLAIM_EVIDENCE.md) distinguishes recorded executions, earlier
selected readback, source interpretation and remaining unknowns. The new paper
does not turn source/report consistency into fresh inference or human review.
Rendered pages are a generic reading draft, not evidence of venue-length fit.

## Build the reading draft outside the repository

The current source uses a conventional TeX Live installation. The following
two-pass recipe was exercised with pdfTeX 1.40.26 / TeX Live 2025/dev/Debian; Poppler tools
extract text and render pages for inspection. It does not execute model code.

```sh
repository="$(git rev-parse --show-toplevel)"
build_dir="$(mktemp -d /tmp/landmark-paper-rewrite.XXXXXX)"
paper_source="$repository/work/paper-rewrite-20261004/manuscript/paper.tex"
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error \
  -output-directory="$build_dir" "$paper_source" >"$build_dir/pass-1.stdout" 2>&1
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error \
  -output-directory="$build_dir" "$paper_source" >"$build_dir/pass-2.stdout" 2>&1
pdfinfo "$build_dir/paper.pdf"
pdftotext -layout "$build_dir/paper.pdf" "$build_dir/paper.txt"
pdftoppm -r 105 -png "$build_dir/paper.pdf" "$build_dir/page"
python scripts/check_source_tree.py
git diff --check
```

PDF, page images, TeX intermediates and raw build logs stay outside Git. The
source checker covers imports, navigation, syntax and indexed manuscript hashes;
it does not verify the excluded experiment archive. Inspect its failure and
warning lists as well as the exit code.

## PR delivery state

The feature branch is `paper/executable-contract-rewrite`, based on saved PR #8
head `87290c2f7571d1fdf5cc2e56286a0ecff5b984ac`. The initial authentication
failure led to local completion first. After API access recovered, PR #8's merge
was verified at main `ccf1a98eca39d49f06e54f4c3def675a90c10540` and incorporated
into the feature branch; the merge changed no manuscript bytes.

[PR #9](https://github.com/lcresearch/landmark-metadata/pull/9) records delivery,
completed agent review and live merge state. Direct Git push returned HTTP 401
during delivery; authenticated API publication preserved the exact local Git
trees and commits. The user subsequently authorized Squash and merge after
review, and this is the default for future authorized merges. Human audit,
external evidence delivery and venue formatting remain on the active
[TODO](../../TODO.md).
