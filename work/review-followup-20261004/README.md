# Repository review follow-up

[manuscript/paper.tex](manuscript/paper.tex) is the current editorial working
draft, derived from the byte-preserved October 4 audit-informed revision.
[The manuscript index](../../docs/CURRENT_MANUSCRIPT.json) records both source
digests. Do not rewrite the imported parent or its import-index entry.

The changes name the supporting diagnostic E5 consistently, expose E4's
18-component denominator flow in its table, clarify payload/behavior restoration
in the abstract, table and conclusion, and disclose the abstract-only use of
Stalnaker and AIBOM. The abstract explicitly identifies Linux Task, and evidence
availability is stated in the manuscript.

See the [review disposition](../../docs/REVIEW_FOLLOWUP.md),
[historical README notes](../../docs/HISTORICAL_README_NOTES.md) and
[English audit summary](../../docs/AUDIT_SUMMARY_EN.md).
No new model experiment or human audit was performed.

Copy `manuscript/paper.tex` into a separate build directory and run `pdflatex`
twice there, or use `latexmk -pdf`. Keep PDFs, logs and rendered pages outside
this repository. The generic draft still requires human verification and
venue-specific formatting. After editing this working source, update its
SHA-256 in `docs/CURRENT_MANUSCRIPT.json`, then run the repository check.
