# Repository review follow-up

[manuscript/paper.tex](manuscript/paper.tex) is the current editorial working
draft, derived from the byte-preserved completed P2/P3 revision on main (`da97450`).
[The manuscript index](../../docs/CURRENT_MANUSCRIPT.json) records both source
digests. Do not rewrite the imported parent or its import-index entry.

The changes name the supporting diagnostic E5 consistently, expose E4's
18-component denominator flow in its table, clarify payload/behavior restoration
in the abstract, table and conclusion, and disclose the abstract-only use of
Stalnaker and AIBOM. The same-Android P2 comparison and qualified P3 publisher display-order
reference remain in the abstract and body. Historical Linux E3 remains context;
evidence availability is stated in the manuscript.

The current draft also incorporates the fresh audit's
[label-parser correction](../../sources/repro-audit-20261004/reports/CHECKER_AUDIT.md):
the evaluated E5 checker and simple baseline disagree with Java on VT and U+2028
label payloads. It separates those injected, isolated decoder/Task-initialization
probes from Android inference, preserves all historical 65-fixture decisions,
and identifies the maintained valid-UTF-8 parser and malformed-input abstention.
The [maintained implementation](../../sources/repro-audit-20261004/maintained/java_labels.py)
and [fresh reconstruction report](../../sources/repro-audit-20261004/REPORT.md)
remain distinct from the frozen historical evaluation and the P2/P3 parent.

See the [review disposition](../../docs/REVIEW_FOLLOWUP.md),
[historical README notes](../../docs/HISTORICAL_README_NOTES.md) and
[English audit summary](../../docs/AUDIT_SUMMARY_EN.md).
This manuscript update performs no new model experiment or human audit.

Copy `manuscript/paper.tex` into a separate build directory and run `pdflatex`
twice there, or use `latexmk -pdf`. Keep PDFs, logs and rendered pages outside
this repository. The generic draft still requires human verification and
venue-specific formatting. After editing this working source, update its
SHA-256 in `docs/CURRENT_MANUSCRIPT.json`, then run the repository check.
