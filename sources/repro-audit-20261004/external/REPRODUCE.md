# Reproduce the E4 and E5 static experiments

This source bundle prepares a **new external evidence directory** and runs the
historical E4 checker and E5 `preflight.check()` without changing their source.
Keep these four files together:

- `bootstrap_external.py`
- `run_e4.py`
- `run_e5_incremental.py`
- `REPRODUCE.md`

The repository is source-only. The commands below do not restore a historical
binary evidence archive and do not independently reproduce Android executions.
Use the existing checkout; each cloud task is already isolated, so a Git worktree
is unnecessary. Models, dependencies, generated Java/classes, logs and results
stay outside the checkout.

## Prerequisites and path layout

Prepare these using the main reproduction setup before running the experiments:

1. Python at `/workspace/hand-contract-repro/.venv/bin/python`, with every package
   in `sources/metadata-contract-e2e-20261004T030536Z/E4/protocol/requirements.lock`
   installed at its pinned version. The current replay used Python 3.11.16.
2. Temurin JDK 17.0.12+7 at
   `/workspace/hand-contract-repro/toolchains/jdk-17.0.12+7` and the pinned Support
   0.4.4 / Lite 2.13.0 / Android / annotation / FlatBuffers jars in
   `/workspace/hand-contract-repro/deps`. E4 invokes `javac --release 8`.
3. The restored base corpus and completed `results/static-suite.json` under
   `/workspace/metadata-contract-paper`. E5 requires the actual files named by
   that report; a historical Markdown summary cannot replace them.
4. HTTPS access to the fixed `storage.googleapis.com/mediapipe-models` candidate
   URLs through the configured proxy and CA trust. If policy denies the host,
   request its supported environment-setting addition; do not bypass the proxy,
   disable TLS verification, substitute URLs or invent a successful download.

The historical code has intentional absolute-path assumptions. The new replay
root must be a sibling of `metadata-contract-paper` for E5; the default Android
source of actual outcomes is the sibling `repro-android`. The support/JDK root
remains `/workspace/hand-contract-repro`. These helpers do not install those
prerequisites or claim that arbitrary directory layouts are supported.

## Create a fresh working copy and a current freeze

Choose a root that does not exist. Replace the bundle path with this directory's
location in your source checkout:

```bash
bundle_dir=/path/to/this/source-bundle
replay_root=/workspace/repro-external-new
python "$bundle_dir/bootstrap_external.py" \
  --repo-root /workspace/landmark-metadata \
  --output-root "$replay_root"
```

Bootstrap uses only Python's standard library and Git. It copies the required
protocol, common helper, generator, checker and E5 source from the byte-preserved
`metadata-contract-e2e-20261004T030536Z` snapshot, verifies every copy's SHA-256,
and copies the two new runner scripts. It makes no network requests and runs no
model checks. It refuses an existing output directory or a directory inside the
source checkout. A failure leaves its new partial directory for inspection;
choose another fresh root after correcting the cause.

Before any E4 downloads, bootstrap commits the copied protocol and a new
`REPLAY_CONTEXT.json` in a local Git repository. `FROZEN_FILES.json`,
`prevalidation-freeze.json`, `source-provenance.json` and `bootstrap-context.json`
record the current commit, hashes, repository revision and setup context. This is
**a current repeat with historical results already known**. Its commit must not
be described as the historical freeze or as a new blinded preregistration.
Historical protocol sentences about prior inspection describe the original
experiment; the new context explicitly states the current scope.

## Run E4

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 \
  /workspace/hand-contract-repro/.venv/bin/python "$replay_root/run_e4.py" \
  > "$replay_root/logs/e4.stdout" 2> "$replay_root/logs/e4.stderr"
```

`run_e4.py` runs the unchanged historical controller with download concurrency
capped at two. Checker, candidate order, exclusion rules and compile commands
are unchanged. No failed candidate is replaced. It writes `E4/results.json`,
per-download records, and per-component raw checker and compiler evidence.
This run is not an Android or model-inference experiment. After a completed run,
use a new replay root for another E4 attempt; the download directories are
intentionally created exclusively.

Read counts from `E4/results.json`, preserving unavailable candidates, exclusions,
compile failures, warnings and abstentions. Do not infer successful runtime
execution from compilation or decoder preconditions. The original copied
`summarize_e4.py` and `summarize_e5.py` are preserved for audit; their Markdown
contains hardcoded historical conclusions and must not certify a new run.

## Run E5 and add core evidence incrementally

E5 can first evaluate the completed base suite and E4 originals:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 \
  /workspace/hand-contract-repro/.venv/bin/python \
  "$replay_root/run_e5_incremental.py" \
  > "$replay_root/logs/e5.stdout" 2> "$replay_root/logs/e5.stderr"
```

To include the five real core model conditions prepared for the Linux Task
replay, pass their directory. It must contain `original.tflite`,
`description_control.tflite`, `label_deletion.tflite`, `label_permutation.tflite`
and `label_restoration.tflite`:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 \
  /workspace/hand-contract-repro/.venv/bin/python \
  "$replay_root/run_e5_incremental.py" \
  --core-models /workspace/repro-task/models \
  > "$replay_root/logs/e5-with-core.stdout" 2> "$replay_root/logs/e5-with-core.stderr"
```

This catalog source is explicitly labeled `core_reconstructed_for_Task`; Task
outcomes never become Android outcomes. Once the **formal E1 and E2 variant
directories** exist, `--include-core` adds their real aliases. Actual Android
outcomes are added only when the new E1/E2 `results.json` files also exist:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 \
  /workspace/hand-contract-repro/.venv/bin/python \
  "$replay_root/run_e5_incremental.py" --include-core \
  --core-models /workspace/repro-task/models \
  > "$replay_root/logs/e5-with-android.stdout" \
  2> "$replay_root/logs/e5-with-android.stderr"
```

The new controller catalogs actual files, deduplicates by artifact SHA-256,
retains phase aliases and reuses completed checker reports after verifying the
model digest. It evaluates newly seen model bytes with the unchanged historical
checker. Run each catalog refresh with all previously supplied source flags to
retain those aliases and fixtures. No completed per-model checker directory is
overwritten. Aggregate catalog/results files are refreshed only in this new
working replay directory; use another root when preserving a sealed report.

Inspect `E5/results.json` and the computed `E5/replay-summary.json`.
`known_failure_detection: null` means no actual failing Android observation has
been supplied; it must not be reported as successful failure detection. Inspect
`controller_errors`, structural and decoder statuses, and fixture completeness;
a controller's exit 0 alone does not certify the experiment. The checker can
also return exit 0 with explicit semantic or metadata abstentions.

## Interpretation and recorded comparison

The October 4, 2026 replay observed E4: 20 candidate URLs, 16 downloads, four 404s,
18 component occurrences and 15 included canonical groups. All 15 passed S;
Java compilation passed for eight and failed for seven. D returned four
compatible, nine incompatible and two inapplicable results. Five incompatible
detector wrappers failed compilation; four incompatible segmentation wrappers
compiled with explicit unsupported-output warnings. All semantic checks
abstained. These observations establish no supported external runtime defect.

The full E5 catalog contained 65 byte-distinct fixtures, not 65 independent
models: S accepted 52, rejected 11 and abstained on two; D returned 27
incompatible, eight compatible, 14 inapplicable, three dynamic abstentions, two
no-metadata abstentions and 11 not reached. All 65 semantic checks abstained.
The five core conditions produced zero additional E5 rejections over the matched
simple baseline or Task initialization. These are comparison observations, not
hardcoded acceptance requirements: retain and investigate any new deviations.

Independent semantic-reference validation, supported end-to-end external
failures, population defect rates and independent human replication are not
established by this static replay.

The completed replay also linked all five exact core artifact hashes to the new
Android E1/E2 primary and replay summaries: four successful getter conditions
and one failing condition. E5 flagged that failing condition and rejected none
of the four successful conditions. Adding those observed associations preserved
all 65 existing static reports and all 481 static evidence files unchanged.
