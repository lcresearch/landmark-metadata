# Acceptance-focused editorial validation

Base: `8005274e9eccbea30fb3189779f03e8d693b3720`.
This task edits the manuscript and screens existing public reports. It performs
no Android/model execution or new raw-evidence audit. The preceding revision’s
[validation](../rerun-paper-revision-20261111/VALIDATION.md) and frozen evidence
index retain their original scope; no earlier result is relabeled as newly run.

## Document build

Built from the new source in `/tmp/landmark-acceptance-paper-20261111/final-v3/`
using the previously extracted pdfTeX 1.40.26 and IEEEtran V1.8b toolchain. Its
[package identity lock](../rerun-paper-revision-20261111/build-toolchain.json) is
unchanged. Actual commands source `/tmp/landmark-paper-tex-20261111/tex-env.sh`,
then run two passes of `pdflatex -interaction=nonstopmode -halt-on-error
-file-line-error paper.tex`, `pdfinfo`, `pdffonts`, `pdftotext -layout`, and
`pdftoppm -scale-to 1400 -png` in that fresh external build directory.

The final source SHA-256 is
`d3876b7d9279528e479807a8ef2d655ac8061b86b28558e3dafea61a3e4a42aa`.
The PDF has four US-letter pages, 16 references, 156,675 bytes and SHA-256
`fd0f1522f75b35de5777303afb59722b0794c9f81264f41d5f7284c19d4e4b74`.
No overfull boxes or undefined references. One underfull paragraph-spacing notice
remains in the P2 paragraph containing the long constructor name. All eleven fonts are embedded Type 1 fonts. All four final pages were visually
checked, including the balanced final bibliography columns; no layout geometry/font-size
reduction or negative spacing was introduced.

## Source and evidence boundaries

The source checker validates current and predecessor manuscript pins, preserved
imports (working tree or Git archive), syntax, navigation and source-only scope.
The source check passed: 354 preserved imports, 16 artifact pins and no failures.
The 18 historical/archived-locator and external-digest warnings remain visible.
All 193 regression tests passed. `git diff --check` also passed. No new tests were
added for these document-only edits.

All earlier manuscript areas, the frozen November evidence index, `experiment/`,
`support/`, archive manifests and source imports remain unchanged. Core counts,
negative findings and the six unsigned author questions are preserved. The four
acceptance decisions are engineering implications of existing observations;
complete-package integrity coverage remains analytical. No measured prevalence,
developer productivity, detector advantage or new natural defect is claimed.

Retained output: `/home/hsz/landmark-evidence/acceptance-paper-20261111/short-paper.pdf`.
Adjacent `build/` records and `delivery.json` bind the copied PDF/source/logs/images
and verification outputs. These files remain outside Git and outside the sealed
November experiment archive.
