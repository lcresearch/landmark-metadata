# Validation of the label-resource revision

Performed 20 October 2026 (America/Los_Angeles; raw command timestamps are UTC).
This record concerns repository integrity, editorial consistency and document
builds, not new model experiments or human research verification.

## Source and regression checks

Run from `/workspace/landmark-metadata`:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_source_tree.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
git diff --check
```

The initial baseline passed source checks (354 imported files, 12 existing
warnings) and executed all 83 regression tests successfully, with none skipped.
The final revision also passed: 83 tests in 3.000 seconds, zero failures/errors
and no skipped tests; source check PASS with 354 unchanged imported files,
545 inspected files and the same 12 warnings; `git diff --check` passed.
The warnings concern historical README locators and unchecked excluded-evidence
hashes; they do not verify external files. The 48 historical claim-source files
were separately rehashed, all matching their recorded sizes and hashes.

## Build environment and repeatability

Python 3.12.14, pdfTeX 1.40.26 (TeX Live 2025/dev), latexmk 4.86 and Poppler
26.05.0 are available. IEEEtran was initially absent. It was obtained from the
signed Debian trixie package metadata and `texlive-publishers_2024.20250309-2_all.deb`,
whose SHA-256 is
`213656c0c3e6014f99bc3c5da07196501fb9b9bc748d32c92a30c2b8050c1b34`.
The extracted IEEEtran V1.8b class matches the prior recorded class digest
`da751920a317ed318b7b5cd7fa585a6cc7d28502d457856382e9be24b10a3bd7`.
It is retained outside Git at `/workspace/texmf/tex/latex/IEEEtran/IEEEtran.cls`.
TLS, package signatures and artifact hashes were not bypassed.

The install script was exercised for a clean target, a repeated install and the
existing target. The saved startup build block was executed against both the
old and new manuscript pointer. It copies sources into a fresh external directory
and runs two `pdflatex -interaction=nonstopmode -halt-on-error -file-line-error`
passes per target, then pdfinfo, text extraction and PNG rendering.

Activate the retained class in each build shell:

```sh
export TEXINPUTS=/workspace/texmf/tex/latex/IEEEtran:
kpsewhich IEEEtran.cls
```

For an equivalent fresh build of either source, copy its `.tex` file into a new
directory outside the repository, change into that directory, and execute the
two passes there. No PDF, image, log, TeX class or dependency is committed.
The exact dynamic-pointer build instructions and install script are saved in
the cloud configuration draft (`start_skill` and `install_script`); they require
environment-settings review/save and publication before a future snapshot can
be claimed. No future-task restoration has been tested.

## Final document builds and visual inspection

Final clean build root: `/workspace/landmark-builds/current-paper-njansugt/`.
Each target directory contains its copied `.tex`, two pass logs, final `.log`,
PDF, `pdfinfo.txt`, extracted text and rendered pages. Copied source hashes match
the current pointer and checkout.

| Target | Pages including references | References | Overfull boxes | Undefined references/citations |
|---|---:|---:|---:|---:|
| Short | 4 | 16 | 0 | 0 |
| Companion | 8 | 18 | 0 | 0 |

The short source SHA-256 is
`be3367013898a7fe61594b9ad0c8705b6b9d0a10030e3adccd89f6952c71ce2c`;
the companion is
`3ad2458ff34619d7a34a79bc2e439563f960dad0ed03cdef1d62cdcfdadd0adb`.
Final PDFs are respectively
`5b998c10cbee421967d0d5b516ce2b23bf060f7d7bdf7e8bbd3975abfae693c8` and
`a9cf51483891e60c94db13584322df6ab49d291a68782452c5167f7a0affba4b`.
These identify this build, not guaranteed byte-identical future PDFs.

All four final short pages were actually viewed. The title, call chain,
five-condition table, seven-row matrix, body and references are readable without
clipping or table overflow. The source uses unchanged 10pt IEEEtran conference
geometry; tables use `small`. No reduced margins, resized tables or negative
spacing were introduced to force the page count. One underfull vertical-box
warning remains; it produces whitespace, not missing text. The companion's eight
pages were also visually inspected during its separate build of identical source;
13 underfull horizontal-box warnings remain around long identifiers. Its final
rebuild has no overflow or unresolved references. This is provisional formatting,
not certification of a selected venue's requirements.

## Content, identity and scope review

The title/abstract, two RQs, five-condition table, coverage matrix, results,
conclusion and claim crosswalk were checked together against the historical
source/report trail. Review retained one core classifier; description-M versus
resource-F intervention; unchanged tested H/numerics; caught getter exceptions;
unset wrapper Category index; Task atomic classify and unobserved raw tensor;
integration differences; P3 deletion unmeasured; qualified display reference;
analytical hash row; and E5's zero additional core rejections.

The new pointer retains the imported P2/P3 parent identity and records the exact
October 8 editorial predecessor; old sources and audit targets were not rewritten.
No new citation or fresh full-text literature audit was claimed. Agent review
was used to identify concrete consistency/layout issues, not as a vote or author
signature. The final call-chain wrapping and availability wording incorporate
those observations.

External availability checks and their limits are in
[ARTIFACT_HANDOFF.md](ARTIFACT_HANDOFF.md). No raw historical evidence was rehashed,
no Android/model/JVM experiment was run, and no independent reproduction,
anonymous deposit or human author audit was completed. Six author questions remain
PENDING. The current environment supports source/test/TeX work, not the excluded
Android/model reproduction workflow.

## Remote and environment delivery

Read-only Git verified main equals review anchor `65004d4…`; the public PR #14
page reports MERGED and matches the terminal squash on main. The GitHub API was
initially denied by the managed network proxy (CONNECT 403), while native Git
reads and the public PR page worked. An existing GH_TOKEN binding is present;
no value was printed or requested. `api.github.com` was added to the configuration
draft without replacing the package-manager preset. A subsequently approved
escalated execution reached the GitHub API and independently confirmed #14 as
closed/merged with merge commit `65004d4…`; the original failure was therefore
not treated as missing credentials. The draft update itself does not apply
runtime policy or publish a snapshot.

The feature branch was pushed and [PR #15](https://github.com/lcresearch/landmark-metadata/pull/15)
created and checked OPEN/unmerged with auto-merge disabled. Remote main remains
`65004d4ac573118d58eb8c6f3125d67c0b330d62`. The current pointer and TODO link
that PR; its live head identifies the final delivery commit. This task does not authorize
merging, auto-merge, evidence upload or submission.
