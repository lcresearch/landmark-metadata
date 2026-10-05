# Editorial build and review disposition

Scope: manuscript rewrite, source/provenance checks and document compilation.
No model generator, model-code compiler, Android package, emulator, interpreter
or inference experiment was run. Earlier recorded experiments remain distinct
from this editorial work. All reviews described below are agent reviews;
human verification remains pending.

## Manuscript identity and build

| Object | Identity / observation |
|---|---|
| Current source | `manuscript/paper.tex`, SHA-256 `43b92dbb0230fc1232093be6a33fca435188dc2f43ae499ac6bfa8e362f37bb2` |
| Preserved editorial predecessor | `work/review-followup-20261004/manuscript/paper.tex`, SHA-256 `6e77175d25ff0834978463bdb2359ab82e6cf62bc8e2d611960c23dcf8b48537` |
| Preserved imported ancestor | `research/20261004-p2-p3/manuscript/paper.tex`, SHA-256 `118ccc9820454f8ac1d3b0416ba456401e5ef3f9e9d0199ba1c59991103ec5a9` |
| Build tool | `pdfTeX 3.141592653-2.6-1.40.26 (TeX Live 2025/dev/Debian)` |
| Text/render tools | Poppler 25.03.0 |
| Final external directory | `/workspace/landmark-paper-rewrite-build-20261004/final/` |
| Final PDF | `paper.pdf`, SHA-256 `0f28dfd6d9390aed16e7c8cef144fcbcb6457a0cd29541d984fcece1ca75f973` |
| Compilation | Two passes, both exit 0; no undefined citations/references, LaTeX warnings or overfull boxes |
| Underfull boxes | Ten nonfatal paragraph-spacing notices; pages inspected rather than treating these notices as a clean-layout proof |
| Layout | Eight pages including references, generic two-column letter-paper draft; all pages visually inspected, no clipping or overlap observed |

The final external directory retains exact command arrays and exit codes in
`commands.json`, TeX stdout/log/auxiliary files, PDF metadata, extracted text
and rendered page images. The [README recipe](README.md#build-the-reading-draft-outside-the-repository)
uses equivalent commands in a new external directory. The PDF hash identifies
this build; TeX timestamps mean future PDF-byte equality is not promised.
Rendered files and raw build logs are not committed.

The first successful build is retained in the parent external directory. The
final source changes the hash-defense wording from “detects” to “would detect”.
Only rendered page 6 differs; it was inspected again. The other seven final
page images match the already inspected images byte for byte. No venue template,
anonymization rule or page budget has yet been selected or validated.

## Review and corrections

| Review | Finding and disposition |
|---|---|
| Evidence/scope review | Corrected E2's preservation sentence: description control changes embedded metadata; permutation and inverse preserve it. Graph/weights/code/raw comparisons remain as recorded. |
| Evidence/scope review | Narrowed P2 source equality to generated wrapper Java. Classes/DEX agree within each consumer, not between the two consumers. |
| Exact diagnostics | Moved punctuation outside the E1 and Task outer-message quotations; retained the complete Task inner cause. |
| Direct provenance | Added reconstruction, development-corpus and E5 reports to the ledger instead of relying only on predecessor prose. Source IDs S43–S48 and subclaims C2R/C8D/C9E preserve their different verification levels. |
| Contribution/related-work review | Confirmed the scoped mechanisms and citation records against the retained review sources. All 21 bibliography keys are unique and cited; #770 is both motivation and antecedent, with its unsupported-route qualification. |
| Significance | Changed “detects” to “would detect” for trusted whole-package pinning, marking the coverage argument separately from a newly run defense evaluation. E5 remains auxiliary with zero measured core-set rejection increment. |
| Presentation | Retained qualified P3 display-order agreement, same-Android native-integration limits, one-image Hand boundary and honest external/preflight denominators. Compressed internal review history. |

No blocking factual or positioning issue remained in the reviewed text after
these corrections. That is a source/report consistency judgment, not archive
authentication, a publication decision or an independent human audit.

## Repository checks

`python scripts/check_source_tree.py` returned PASS with zero failures: all 354
imported files remain byte-identical; 232 Python and 14 shell sources passed
syntax checks, 38 JSON files parsed, and 226 navigation targets were checked.
The current and imported-parent manuscript hashes and the historical memory
digest matched. The 12 warnings concern unavailable historical evidence locators
and unchecked excluded-manifest identities; they do not authenticate those files.
The check runs no model experiment. `git diff --check` also passed.

A separate editorial check recomputed all 48 ledger source hashes/sizes, found
no mismatches, and checked all 21 citations and both table references without
duplicates or unresolved targets. Both earlier manuscript hashes still match.
The final external directory holds `source-check.stdout`, `source-check.stderr`
and `editorial-checks.json`. These outputs are retained outside Git; this note
records only the bounded verification summary.

## PR #9 merge review

The user requested review and Squash and merge. Separate read-only agent reviews
of the manuscript claims and repository/provenance found no blocking issue in
the submitted source. E1/E2/P2 input denominators, P3 display-reference limits,
Hand's single-image boundary, E4/E5 counts and #770 attribution were checked
against the preserved reports. All 48 repository-source hashes and 13 inherited
external-digest provenance entries match their respective sources; excluded
external bytes were not rehashed.

The repository review passed all 40 existing regression tests, source/import
checks and manuscript identities. The root agent also verified the existing
successful TeX build/PDF against the unchanged current manuscript; this review
did not rerun TeX or model experiments. The submitted head had no GitHub check
runs or commit statuses, so no CI success is claimed. Final policy/status edits
record the user's squash preference and the completed review, with a final
source check before merging the verified head.

## Remaining delivery and research gates

GitHub authentication initially returned HTTP 401, and the user requested local
completion first. On resumed delivery, API access recovered and PR #8's merge
was verified at remote main `ccf1a98eca39d49f06e54f4c3def675a90c10540`. That
revision was merged into the feature branch without manuscript changes.
[PR #9](https://github.com/lcresearch/landmark-metadata/pull/9) records delivery,
review and the live merge state. Direct Git push returned 401 during delivery;
authenticated API publication preserved matching Git trees and commits. The
user subsequently authorized Squash and merge after review. No direct main push
or new model experiment is part of this handoff.

Human audit, recovery/delivery of the external evidence package, fresh-workspace
reproduction and venue-specific formatting remain open. See the active
[TODO](../../TODO.md) and [evidence ledger](CLAIM_EVIDENCE.md).
