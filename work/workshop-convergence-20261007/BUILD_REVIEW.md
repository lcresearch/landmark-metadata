# Build and editorial review

This task compiled documents and inspected source/report consistency. It ran no
model generation, Android build, emulator, inference or human audit. Binary
evidence, dependencies and rendered output remain outside Git.

## Final document builds

| Object | Result |
|---|---|
| Current short source | `manuscript/paper.tex`, SHA-256 `c79ba7f62a194abd487ec4b8ccedb60428ec4edd1f43e6ee155518ffd8bb416e` |
| Longer companion | `manuscript/paper-full.tex`, SHA-256 `facd0688073d66353e2b0ab2c3f5d08e64d292e1f7efdfd7bac7a69f80e8a39b` |
| Template | IEEEtran `2015/08/26 V1.8b`, `[10pt,conference]`; unchanged external class fetched from CTAN |
| Class SHA-256 | `da751920a317ed318b7b5cd7fa585a6cc7d28502d457856382e9be24b10a3bd7` |
| Toolchain | pdfTeX 1.40.26 / TeX Live 2025/dev/Debian; Poppler 25.03.0 |
| Output | Short: **4 pages including 18 references**. Full: **7 pages including 18 references**. Letter paper, normal conference margins; no geometry override. |
| Short PDF SHA-256 | `943097f8204c4fd7f5f0b11dd8acd6da67542dba3e47dc88211b8d74e65b6315` |
| Full PDF SHA-256 | `191406a7bec07d1c56b65982cee9ddf097773ad766fa1598ca5f6e39779b38db` |

Both sources compiled twice successfully. The final logs contain no undefined
citations/references or overfull boxes. Nonfatal underfull spacing notices are
not treated as a clean-layout proof. The four-page short draft is the active
submission candidate; the full companion is explanatory source, not automatically
an allowed venue supplement. These page counts meet the corresponding numerical
caps of the provisional SQA4AI format, not every submission requirement.

Final commands, exit codes, stdout/stderr, logs, PDFs, extracted text and page
images are retained at `/workspace/workshop-convergence-build-20261007/final/`.
The exact executed command arrays are in `commands.json` there. The external
`final-build.py` records orchestration. These local paths are not a public deposit.
PDF bytes include build timestamps; future byte-identical PDFs are not promised.

## Rebuild in a new external directory

Prerequisites: TeX Live with the packages used in the source, IEEEtran V1.8b,
and Poppler. The environment lacked IEEEtran, so this task fetched the unchanged
class from the pinned CTAN locator below and verified the recorded digest. The
class is not committed. With that class installed, omit the `TEXINPUTS` override.

```sh
repository="$(git rev-parse --show-toplevel)"
build_dir="$(mktemp -d /tmp/landmark-workshop.XXXXXX)"
mkdir -p "$build_dir/tex" "$build_dir/short" "$build_dir/full"
curl -fL https://mirrors.ctan.org/macros/latex/contrib/IEEEtran/IEEEtran.cls \
  -o "$build_dir/tex/IEEEtran.cls"
sha256sum "$build_dir/tex/IEEEtran.cls"
# Require the class digest recorded above; do not silently accept a changed class.
for variant in short full; do
  if [ "$variant" = short ]; then source_name=paper; else source_name=paper-full; fi
  for pass in 1 2; do
    TEXINPUTS="$build_dir/tex:" pdflatex -interaction=nonstopmode \
      -halt-on-error -file-line-error -output-directory="$build_dir/$variant" \
      "$repository/work/workshop-convergence-20261007/manuscript/$source_name.tex" \
      >"$build_dir/$variant/pass-$pass.stdout" 2>&1
  done
  pdfinfo "$build_dir/$variant/$source_name.pdf"
  pdftotext -layout "$build_dir/$variant/$source_name.pdf" "$build_dir/$variant/paper.txt"
  pdftoppm -scale-to 1300 -png "$build_dir/$variant/$source_name.pdf" "$build_dir/$variant/page"
done
python scripts/check_source_tree.py
git diff --check
```

## Review disposition

Separate agent reviews checked manuscript focus, evidence availability and official
CFPs. The shortened paper retained the core results and qualifications. Corrections:

- Replaced an unsupported implication of official support with “tested path.”
- Distinguished output positions from the unset wrapper Category index field.
- Specified that decoder **axis size**, not axis number, matches label count.
- Clarified model-byte identity **between consumers**, not between variants.
- Distinguished omitted secondary payloads from unrecovered later raw records.
- Removed bibliography language implying excluded dependency binaries were in
  the recovered focal package.
- Moved table captions above tables for IEEE presentation; kept references intact.

No main-contribution upgrade, new experiment, semantic-accuracy claim or author
verdict resulted from editorial review. The preceding 48 source records were
rehashed successfully; the old ledger and earlier manuscript are unchanged.

## Remaining checks

Human audit, anonymous durable evidence access and author/venue decisions remain
pending. The official CFP includes novelty and significance criteria; neither
four-page layout nor workshop status guarantees acceptance. The final source
integrity and visual checks are recorded in the completion note below.


## Completion checks

The root agent inspected all four final short-paper page images: no clipping or
text/table overlap was observed. The longer companion compiled and rendered but
was not given a separate all-page visual audit. Final source checking passed
with zero failures: 354 imported files unchanged, 238 Python and 14 shell syntax
checks, 42 parsed JSON documents, 311 navigation targets and both current/imported
manuscript identities. Twelve existing warnings identify historical absent
locators or unchecked excluded digests; they are not suppressed or called passes.

All 48 preceding ledger source records and the new revision-map repository
identities match. Both drafts have 18 unique, cited bibliography entries and no
unresolved citation/table references. `git diff --check` passed. Exact check
outputs remain alongside the external build under `final/`; no model tests were
run for this text-only change. Repository regression tests were not rerun because
no executable source changed.
