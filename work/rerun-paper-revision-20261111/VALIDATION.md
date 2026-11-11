# Validation of the November short-paper revision

Date: 11 November 2026 (America/Los_Angeles; execution logs use UTC).
Review base: `e9da459f6043684cdecba913c9c711433371909d`.
This record distinguishes **saved-byte checks**, **document builds** and
**source regression tests**. No new Android/model inference or JVM parser probe
was run. Human review remains PENDING.

## Actual saved-byte review

The experiment roots and original records were read, not overwritten. Commands:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 work/rerun-paper-revision-20261111/recheck_core.py \
  --run /home/hsz/landmark-evidence/focal-rerun-20261110 \
  --inputs /home/hsz/landmark-evidence/input-recovery-20261110 \
  --references /home/hsz/landmark-evidence/reference-recovery-20261110 \
  --python /home/hsz/landmark-evidence/focal-rerun-20261110/hand/.venv/bin/python \
  --output /tmp/landmark-paper-review-20261111/core-readback
PYTHONDONTWRITEBYTECODE=1 python3 work/rerun-paper-revision-20261111/verify_new_archive.py \
  --archive /home/hsz/landmark-evidence/focal-rerun-20261110-evidence.tar.gz \
  --output /tmp/landmark-paper-review-20261111/archive
```

Use absent external destinations for a future check. The helper refuses existing
outputs; its Android adaptations are recorded complete patches, redirecting only
ROOT/report paths and the preservation-audit subprocess. Both preserved source
hashes are fixed in the helper; neither scientific checks nor original reports
are edited. Ten receipt-pinned original records still matched after readback.

| Check | Actual result |
|---|---|
| Android actual-file audit | PASS: eight builds, sixteen condition/phase records, 32 input observations; 28 returned lists/four caught getter failures |
| Model/code preservation | PASS: eight aliases, five byte conditions, one canonical graph; 165 non-metadata buffers and the tested code/native family unchanged |
| Maintained P2 reader | PASS in evidence-validity, coverage and historical-outcome sections; 348 checks, ten configurations, 18 observations, 16 lists, ten wrapper tensors and eight shared successful pairs |
| P3 offline core calculation | PASS_WITHIN_CORE_SCOPE; original/permutation/restoration matching counts 1000/1/1000, 165 equal non-metadata buffers, stable IDs ABSTAIN, accuracy NOT_EVALUATED |
| Complete local archive | PASS: 3,321,366,905 bytes, 2,120 members; entire archive SHA-256 and embedded manifest match the published receipt; every member read and matched without extraction |
| Selected live evidence | 1,036 files read and matched to the archive manifest; all 112 files named by the maintained P2 reader are represented |
| Historical 48-source ledger | 47 current files match; S40's changed maintained README resolves to its exact original Git version, with both identities retained |

The first index-building attempt stopped on S40 instead of accepting a changed
file. Its original bytes at `87290c2f7571d1fdf5cc2e56286a0ecff5b984ac` match the
old SHA-256. The old ledger was not changed. This resolves historical document
identity, not old execution provenance. New index construction used:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 work/rerun-paper-revision-20261111/index_evidence.py \
  --readback /home/hsz/landmark-evidence/paper-revision-20261111 \
  --output /path/to/new-evidence-index.json
```

The committed index was produced by the retained script and copied without byte
changes from the final external output. Readbacks are retained in
`/home/hsz/landmark-evidence/paper-revision-20261111/{core-readback,archive}/`.
`editorial-readback-copy.json` records each original `/tmp` path, retained path,
size and hash. Command paths remain the actual original paths. These new review
outputs are not members of the sealed November experiment archive. The new index
contains identities only; raw models, tensors, decoded data and archives stay
outside Git.

## Document build

No TeX engine was initially installed on this host. Nineteen APT-selected Debian
packages were downloaded and extracted under `/tmp/landmark-paper-tex-20261111/`,
without installing system packages or placing toolchain bytes in Git. Their
names, versions, sizes and SHA-256 values are in [build-toolchain.json](build-toolchain.json).
The engine is pdfTeX 1.40.26 (TeX Live 2025/dev/Debian). IEEEtran V1.8b matches the
previous class SHA-256 `da751920a317ed318b7b5cd7fa585a6cc7d28502d457856382e9be24b10a3bd7`.

The extracted TEXMF roots were explicitly configured; the local pdfLaTeX format
was generated with `pdftex -ini -etex -jobname=pdflatex -progname=pdflatex pdflatex.ini`.
A local font map combines the eight installed map sources listed in the lock;
the map's SHA-256 is recorded. The initial format attempt without `-etex` stopped
with “LaTeX requires e-TeX”; the corrected format initialized successfully.
The unchanged October short source also built to four pages as a baseline.

For a normal configured TeX environment, copy the new `.tex` into a **fresh
external build directory** and run:

```sh
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error paper.tex
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error paper.tex
pdfinfo paper.pdf
pdftotext -layout paper.pdf paper.txt
pdftoppm -scale-to 1600 -png paper.pdf page
```

The actual local build additionally sourced
`/tmp/landmark-paper-tex-20261111/tex-env.sh`; that environment text and build
records are retained with the output. This establishes the tested local build,
not universal PDF byte reproducibility or a delivered offline TeX installation.
No font-size/margin reduction, resized table or negative spacing was introduced.
The ordinary IEEE bibliography column trigger balances the final page.

## Final source and layout checks

The final source is 21,351 bytes, SHA-256
`30890778c7264174f9b1ef0e3ee6801d4bdf8b9d15416503d0f76f03880f3ed1`.
Two pdfLaTeX passes produced **four US-letter pages**, 16 bibliography entries
and a 155,365-byte PDF, SHA-256
`ad9d8aae4231636d352f3517c23b287fa311a25ae518c8b58b863b58b1967dd2`.
The build's source copy matches the indexed manuscript exactly. All eleven fonts
are embedded Type 1 fonts. There are no overfull boxes or undefined references.
Two underfull spacing notices remain (one page vbox and one paragraph hbox);
all four final page images were visually inspected, including both tables,
paragraph labels, page transitions and references. No clipping, overlap or
unreadable content was observed. Initial table-column spacing and paragraph-label
punctuation were corrected before this final build.

The retained PDF is
`/home/hsz/landmark-evidence/paper-revision-20261111/short-paper.pdf`.
The adjacent `short-build/` retains source, PDF, logs, extracted text, four page
images, font inspection and environment/lock text. `short-build-copy.json`
records those identities; every copied build file and all nineteen local package
files matched their recorded bytes/hashes. These document-build files are
outside Git and are not experiment-archive members.

Source validation used:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_source_tree.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests
git diff --check
```

The source checker passed: 354 preserved imports, one import-backed memory hash,
13 current/historical artifact pins, Python/shell/JSON syntax and navigation.
Its twelve historical missing-locator/external-manifest warnings remain visible;
there were no failures. **All 180 tests passed**. Four new archive regressions
cover valid readback, tampered payload despite a matching outer digest,
duplicate members/wrong manifest identity, and preservation of existing output.
These synthetic tests do not authenticate the real run; the actual saved-byte
checks above are a separate validation layer.

Protected source imports, the October manuscript/companion and original audit
targets are unchanged. Only first-party source, tests and necessary text are
included in the feature-branch PR; rendered papers, raw evidence, packages and
other generated products remain outside Git. Human author verification and
durable reviewer access remain open.

Delivery: [PR #22](https://github.com/lcresearch/landmark-metadata/pull/22),
`codex/paper-rerun-evidence-20261111` into `main`, open for review and not merged.
