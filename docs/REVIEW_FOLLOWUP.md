# Disposition of the repository review

Date: October 4, 2026 UTC. Initial review base: `a341d8b`.
Integration base after PR review: `da97450`.
The initial follow-up read the complete then-current manuscript and the relevant
repository records, then ran source-only checks. It did not inspect the excluded
raw experiment archive, run inference, perform P2 or complete human review.

The review is broadly sound as a consistency and repository-usability check.
Its favorable assessment does not establish publication readiness: novelty,
generalization and practical research significance remain unresolved. The
existing comparison reports zero extra E5 rejections over its matched baseline.
Removing platform confounding would strengthen attribution without by itself
creating a new constraint or detection method.

| Review item | Finding and disposition |
|---|---|
| 1. Historical README references | Confirmed. PDFs, root audit machine results/manifests and SDK/AVD state are excluded by the authorized source-only scope. The root audit `commands.sh` is present, but its inputs are not. Added [availability notes](HISTORICAL_README_NOTES.md), linked from current entry points. Historical READMEs remain immutable; file-like locators now warn rather than silently disappear. Missing current document targets fail. |
| 2. Chinese audit report | Added an [English summary](AUDIT_SUMMARY_EN.md) with the audit's measured bounds and pending items. The original report remains unchanged. |
| 3. E5 naming | The [new working manuscript](../work/review-followup-20261004/manuscript/paper.tex) consistently calls the supporting diagnostic E5; D continues to name the selected-decoder judgment. |
| 4. E4 denominators | The review's proposed one-file exclusion is incorrect. The preserved report and manuscript text say 16 successful downloads produce 18 component occurrences; one prior component and two prior-graph occurrences are excluded, leaving 15 new canonical graph groups. Added those rows and the flow to the table caption. This is Table 3 (`tab:external`) in the compiled draft; Table 4 is the baseline comparison. The underlying excluded execution records remain outside this repository. |
| 5. Citations | Both queried identities are real and consistent with the bibliography; see checks below. The Stalnaker entry cites a 2026 journal article, rather than just a preprint. All 14 bibliography keys are cited and no cited key is undefined. Both Stalnaker and AIBOM are now explicitly abstract-based background, outside the four full-text method comparisons. |
| 6. Restoration | Clarified the abstract, combined E1/E2 table, intervention description and conclusion: label payloads and observed behavior recover; original publisher ZIP container bytes do not. The incomplete initial replay is still disclosed. |
| 7. Hash locators | The original checker already compared imported files with `docs/SOURCE_IMPORT.json`. The preserved manuscript also matches the digest in MEMORY: `390445a494c24cf9e9069ca3d5ab62e4d0174587f631856b764846d54908782d`. Added an explicit MEMORY/import/source cross-check and a [current/parent digest index](CURRENT_MANUSCRIPT.json). External evidence-manifest digests are reported as unchecked, not verified. |
| 8. Same-Android P2 | Pending at the initial review base; subsequently completed on main and now retained in the editorial manuscript. It is an important validity improvement. Identical platform/API/ABI and input bytes reduce confounding; decoder paths, preprocessing, native interpreter versions and packaging can still differ. The integrated abstract retains the same-Android comparison and qualified P3 reference. The original review environment limitations are recorded below. |
| 9. Script tests and language | Added seven regression tests for changed checker behavior and existing source-only rejection. Imported historical Java is preserved. No Kotlin/Compose mandate was found in the inspected AGENTS policy; Kotlin is a reasonable choice for new P2 harness code. Compose is unnecessary for an instrumentation-only consumer comparison. No P2 implementation is claimed. |

The editorial working copy and preserved parent are indexed separately. The
historical 281-file import and its index have not been rewritten. The four
full-text comparisons remain historical audit records; this follow-up did not
re-read all four full texts or rerun their tools.

## Initial publication identity checks

Checked on October 4, 2026 UTC:

- Stalnaker et al.: [Crossref DOI record](https://api.crossref.org/works/10.1145/3776739)
  identifies the manuscript's exact title, Trevor Stalnaker as first author,
  *ACM Transactions on Software Engineering and Methodology* 35(8), published
  online July 16, 2026. [ACM](https://dl.acm.org/doi/10.1145/3776739) exists but
  direct retrieval returned HTTP 403. The [arXiv abstract](https://arxiv.org/abs/2502.04484)
  confirms the same current title/authors and the background scope used here;
  its v2 is dated September 29, 2025. No journal/preprint byte equivalence or
  fresh full-text method comparison is claimed.
- AIBOM: [arXiv record](https://arxiv.org/abs/2607.17242) confirms the exact title,
  Md Erfan, Ahmed Ryan and Md Rayhanur Rahman, and v1 submitted July 19, 2026.
  Its abstract concerns completeness of machine-readable supply-chain
  documentation. The identifier and abstract-level use are verified; full-text
  comparison is not claimed. The version-suffixed browser fetch failed, but the
  accessible unversioned record identifies v1 as its sole/current version.

## Initial review environment and submission boundaries

The three original `/workspace/metadata-contract-*` package roots identified
in MEMORY were absent from this follow-up environment. `adb` and an Android
execution toolchain were not available on PATH. Model/RGB evidence and SDKs are
intentionally absent from this source-only checkout. A fresh source checkout
therefore cannot perform the proposed matched comparison without recovering
and verifying those inputs and tools.

The initial P2 recommendation was to freeze exact model/input hashes, Android API/ABI/device,
wrapper and Android Task dependency versions, CPU/thread settings and remaining
integration differences. Preserve original, description control, deletion,
permutation and payload-restoration conditions. Observe public load/init,
input preparation, inference and output stages; record stages not exposed by a
public API or not reached. Identical RGB bytes do not guarantee identical
internally preprocessed tensors. Retain unexpected or disappearing differences.
Do not select replacement versions merely to obtain the expected stage result.

P2 and the bounded P3 inquiry are now complete. Actual human verification, a
separately planned evidence deposit and a credible explanation of the research
contribution remain open in
[TODO.md](../TODO.md). The source check and TeX build verify repository and
manuscript construction, not the numerical claims or publication novelty.

## Initial validation (before main integration)

- Original `python scripts/check_source_tree.py`: PASS, 291 files and 281
  imported-file digests; no model execution.
- Extended check: PASS, 298 files, all 281 imported hashes/sizes, 65 local
  navigation targets, one MEMORY/import/source digest and two indexed manuscript
  source digests. Nine warnings disclose seven unavailable historical README
  locators and two unchecked external evidence-manifest digests.
- `PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -v`: seven
  passing regression tests for navigation, warning scope, stale provenance,
  working-manuscript digest changes and source-only exclusions.
- All 14 bibliography entries are cited; no duplicate keys, undefined citations
  or undefined local LaTeX references were found.
- Two `pdflatex` passes in a separate build directory: eight pages, no overfull
  boxes or undefined-reference diagnostics. All eight rendered pages were
  visually inspected, including the expanded E4 table and restoration caption.
  Ordinary underfull-box diagnostics remain; no clipping or overlapping table
  content was observed. This is still a generic reading draft.
- `git diff --check`: PASS. Imported `sources/` bytes and `SOURCE_IMPORT.json`
  are unchanged. No models, logs, rendered pages, PDFs or installed tools are
  included in the source changes.

## PR review repair and integration

Merged main `da97450` and applied the editorial changes to its completed P2/P3
manuscript in the separate working area. Both imported source sets remain
byte-preserved. The current/parent index now names the P2/P3 manuscript parent,
and README, MEMORY and TODO agree on completed P2/P3 and pending human review.
The checker validates both import manifests (354 files), tolerates external
protocol-relative URLs, and requires README to point to the indexed current
manuscript. Nine regression tests pass, including corruption of a P2/P3 import
and stale current-manuscript navigation. The integrated paper has 17 cited
bibliography entries; the older 14-entry and eight-page counts above describe
the initial draft only. No new model execution, evidence recovery or human
audit is claimed by these source fixes.
