# Reproduction commands and execution boundaries

Use the repository root as the working directory unless a block says otherwise.
Keep every new report, downloaded input and build outside this checkout. Existing
evidence must remain untouched. These commands distinguish three activities:

| Label | Meaning |
|---|---|
| TODAY | Source checks or finite readback exercised during this handoff; see the handoff status for the exact commands and results |
| HISTORICAL | A command/sequence preserved from a previously reported run; not a fresh execution during this handoff |
| PLANNED | A prospective command after its stated prerequisites; source inspection does not establish successful execution |

The handoff runs no model, build, dependency installation, download or emulator.
A command returning zero is not sufficient evidence of successful model behavior.
Read the stage records and the independent checks. Historical Python assertions
must remain enabled (`PYTHONOPTIMIZE=0`; never `python -O`).

TODAY below is the original handoff's recorded activity label, not a claim that
its excluded evidence is available in the current environment. The
[21 October repair record](../../work/review-fixes-20261021/README.md) identifies
the current maintained tools and their source-only regression validation.

## 1. TODAY: source checks, without experiment dependencies

```sh
PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_source_tree.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
git diff --check
```

These check source scope, imported source identities, syntax, navigation,
manuscript provenance and verifier regressions. They do not authenticate excluded
model/evidence archives or reproduce an experiment. Warnings about historical
locators or unchecked external archive hashes must remain visible.

The following source-copy smoke checks ran during the original handoff and are
retained as a historical command record:

```sh
PYTHONDONTWRITEBYTECODE=1 python \
  sources/repro-audit-20261004/base/prepare_base.py \
  --repo-root /workspace/landmark-reproduction-handoff \
  --hand-root /workspace/landmark-handoff-audit-20261004/source-copy-hand \
  --corpus-root /workspace/landmark-handoff-audit-20261004/source-copy-corpus \
  --copy-only
PYTHONDONTWRITEBYTECODE=1 python \
  sources/repro-audit-20261004/android/initialize_run.py \
  --repo /workspace/landmark-reproduction-handoff \
  --root /workspace/landmark-handoff-audit-20261004/android-source-copy
```

The first copied and hash-checked 37 source files and returned
`SOURCE_COPY_ONLY_NO_ENVIRONMENT`. The second initialized copied/adapted Android
harness sources. Neither installs dependencies, downloads a model, compiles Java,
starts an emulator or executes inference. These temporary parent-copy roots are
not the hardcoded `/workspace` parent layout required by the full workflow.
For new Android source copies use the maintained initializer in section 4; the
historical initializer above contains an unconditional publisher-retrieval claim.
Choose new absent outputs and the actual checkout path; do not reuse completed
directories. The old execution records remain in the handoff's external
`copy-command-records.json`.

## 2. TODAY: finite readback of available historical records

The maintained reader uses only Python's standard library. Both roots below
must contain the actual old device/input/raw/decoded records and P3 comparisons,
not just the source copies in Git. The two roots are adjustable CLI arguments;
the output directory must be new and outside the repository.

```sh
PYTHONDONTWRITEBYTECODE=1 python \
  research/20261004-significance-review/scripts/read_existing_outcomes.py \
  --output-dir /workspace/landmark-handoff-audit-20261004/readback
```

The defaults are `--e2e-root /workspace/metadata-contract-e2e-20261004T030536Z`
and `--p2p3-root /workspace/metadata-contract-p2p3-20261004T073824Z`; use those
options to point to independently recovered copies. This handoff used host
CPython 3.12.14 for the readback, not the experiment's Python environment.

That output path identifies this handoff's attempt. Choose a different, absent
external directory for a subsequent attempt; the reader rejects an existing
one. Missing input files are a blocker, not an invitation to manufacture them
from summary prose.

Inspect `readback.json`, including every recorded comparison boolean. This reader
reports comparisons as data; it does not turn every false boolean into a nonzero
process exit. It reads 59 selected old files: E1/E2 primary observations, P2's two
deletion-stage records and P3's stored comparison/bridge/chain reports. It does
not rehash the whole archive, inspect APK assets or generated code, recompute
graph preservation, authenticate the P3 source chain, or execute inference.

The historical comparison targets are 16 E1/E2 input observations: 14 successful
category lists and two caught deletion-getter failures; unchanged raw scores and
999 changed labels for each permutation input; P2 wrapper getter rejection versus
Task construction rejection; P3 display agreement at 1000 original/restored and
one permuted position. A discrepancy must be reported, not normalized away.

## 3. A different reader: reconstructed evidence, currently prerequisite-gated

[The full maintained observation reader](../../work/observation-review-20261004/README.md)
targets `/workspace/repro-task`, `/workspace/repro-hand`,
`/workspace/repro-external` and `/workspace/repro-android`. It does not target the
older roots in section 2. It requires the actual model, build and execution
files, plus the separately pinned 65-artifact E5 identity manifest. Merely
redirecting its output does not redirect those inputs.

Its help path is safe after inspection; invoking the full command is **PLANNED**
until the excluded reconstruction inputs are recovered:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  work/observation-review-20261004/verify_observations.py --help
```

```sh
# PLANNED: only when all four reconstruction roots and the pinned manifest exist.
PYTHONDONTWRITEBYTECODE=1 python3 \
  work/observation-review-20261004/verify_observations.py \
  --output-dir /workspace/reconstruction-readback-new
```

Default E5 manifest digest:
`bf49a475696eec4b38fb17587f6541a8393da14297e5dca1d433a051ba166e79`.
An explicit `--required-manifest`/`--required-manifest-sha256` override must come
from independently preserved provenance, not a digest computed from the candidate
catalog being checked. Its missing prerequisites cannot be replaced by section
2's smaller successful readback. The reader refuses to replace an existing
`observation-readback.json`; choose an external output directory yourself, since
it does not enforce the repository boundary in the same way as the smaller reader.

## 4. E1/E2 clean build: dependency order and historical commands

The closest existing setup route is
[base preparation](../../sources/repro-audit-20261004/base/REPRODUCE.md) followed by
[Android reconstruction](../../sources/repro-audit-20261004/android/REPRODUCE.md).
The helpers have been inspected; installation, build and inference below are
**HISTORICAL sequences / PLANNED executions**, not completed handoff checks.

Before execution, supply all of the following:

1. An existing `uv` and Python **3.11.16**. `prepare_base.py` does not install an
   interpreter; its dependency lock has exact versions but no wheel hashes.
2. Fresh external `/workspace/hand-contract-repro` and
   `/workspace/metadata-contract-paper` roots, or a separately reviewed adaptation
   of the copied scripts' absolute paths. Never remove an occupied old root to
   make setup work. `--hand-root`/`--corpus-root` alone do not adapt downstream
   hardcoded imports, interpreter paths or build dependencies.
3. The exact original, description-control and label-deletion models under
   `metadata-contract-paper/runs/6c7ab0a6e5dc/{original,description_control,label_drop_1}/model.tflite`,
   verified against the input inventory. The original digest must be
   `6c7ab0a6e5dcbf38a8c33b960996a55a3b4300b36a018c4545801de3a3c8bde0`.
   Setup-only does not create these models. Recover them from the evidence owner
   or use a separately reviewed minimal reconstruction. The optional historical
   `--fetch-and-static` mode fetches the whole fixed corpus; it is not a necessary
   minimal E1/E2 step and is not requested by this handoff.
4. A new Android root; enough disk/RAM for SDK, AVD and builds; a free selected
   emulator port; writable Android user configuration. Do not change `HOME` or
   overwrite existing user configuration. Preserve the configured proxy/CA trust.
5. Availability and hash verification of every pinned SDK/JDK/Java archive in
   `android-prerequisites.lock.json`. Current official XML may stop listing an
   old archive; retain that failure instead of silently selecting a newer version.

For a **new machine with the default parent roots absent**, the setup-only form
is (set the two input paths to actual existing locations):

```sh
# PLANNED: not safe to reuse against occupied historical parent roots.
HANDOFF_REPO=/path/to/landmark-metadata
HANDOFF_PY311=/path/to/existing/python3.11
python3 "$HANDOFF_REPO/sources/repro-audit-20261004/base/prepare_base.py" \
  --repo-root "$HANDOFF_REPO" --python "$HANDOFF_PY311"
```

This creates and installs the locked environment but does not download models or
run static checks. After recovering and checking the three corpus model inputs:

```sh
# PLANNED: HANDOFF_RUN must not exist before initialize_android_run.py.
HANDOFF_RUN=/workspace/android-rebuild-new
python3 "$HANDOFF_REPO/scripts/initialize_android_run.py" \
  --repo "$HANDOFF_REPO" --root "$HANDOFF_RUN"
python3 "$HANDOFF_REPO/sources/repro-audit-20261004/android/select_official_android_xml.py" \
  --root "$HANDOFF_RUN"
python3 "$HANDOFF_REPO/sources/repro-audit-20261004/android/restore_prerequisites.py" \
  --root "$HANDOFF_RUN" --hand /workspace/hand-contract-repro --repo "$HANDOFF_REPO"
python3 "$HANDOFF_REPO/sources/repro-audit-20261004/android/restore_prerequisites.py" \
  --root "$HANDOFF_RUN" --hand /workspace/hand-contract-repro --repo "$HANDOFF_REPO" \
  --verify-cache
```

`restore_prerequisites.py` installs into its supplied hand root; it is not a
read-only inspector. Even `--verify-cache` writes an integrity report. Both must
operate on the newly prepared run, not a sealed package. The maintained
[`initialize_android_run.py`](../../scripts/initialize_android_run.py) copies
preserved code and records adaptations, including the audit harness and functional
readiness check; generated model Java is not repaired. It records local input
bytes without claiming to have observed publisher retrieval. Keep actual
acquisition records separately. The preserved historical initializer rewrites
this text to “fresh HTTPS publisher download”; it is not the current setup entry.

Then use the existing documented sequence, one stage at a time, retaining logs
and checking actual outputs before advancing:

```sh
# HISTORICAL sequence; PLANNED for the newly prepared directory.
cd "$HANDOFF_RUN"
export PYTHONDONTWRITEBYTECODE=1
export PYTHONOPTIMIZE=0
HANDOFF_PY=/workspace/hand-contract-repro/.venv/bin/python
"$HANDOFF_PY" scripts/prepare_e1.py
python3 scripts/start_emulator.py
"$HANDOFF_PY" scripts/build_android.py --experiment E1
python3 scripts/run_android.py --experiment E1 --run primary
python3 scripts/run_android.py --experiment E1 --run replay
python3 scripts/summarize_android.py --experiment E1
"$HANDOFF_PY" scripts/prepare_e2.py
"$HANDOFF_PY" scripts/build_android.py --experiment E2
python3 scripts/run_android.py --experiment E2 --run primary
python3 scripts/run_android.py --experiment E2 --run replay
python3 scripts/summarize_android.py --experiment E2
"$HANDOFF_PY" scripts/audit_android_results.py
```

The audit writes fresh reports and invokes `audit_model_preservation.py`; do not
invoke either against preserved evidence or use their `--help` as a safety probe
(they execute top-level code). The independent audit recomputes working/APK/
AssetManager identity, graph/buffers/resources, actual generated source/classes/
DEX, inputs/raw scores/decoded values, stage completeness and replay. APK byte
differences across model variants are not a preservation failure.

Expected historical result: five model-byte conditions, one graph, eight
phase/variant builds, 16 primary/replay configuration records and 32 inputs;
28 successful category lists and four caught deletion getter exceptions. E1
must call the unmodified generated getter. E2 must compare all scores/positions
and restore the association; it does not measure prediction accuracy. Preserve
deviations, early rejection and incomplete service readiness. Stop only the
emulator started for this run. This sequence does not establish a new P2 run.

## 5. P2 same-Android comparison: copied working tree required

[P2's plan](../../research/20261004-p2-p3/P2/EXPERIMENT_P2_PLAN.md) and
[command history](../../research/20261004-p2-p3/P2/commands.sh) identify the exact
stages, but do not bootstrap their prerequisites. Before a future run, prepare
a new external round containing a source copy of `P2/` and its review scripts:

- Copy the preserved [`INPUTS.json`](../../research/20261004-p2-p3/INPUTS.json)
  into the round parent. It already records the five exact model digests and P2
  variant names (including `restoration`). Adapt paths only to independently
  recovered matching model bytes, and record each path adaptation as new provenance.
- Provide fresh `P2/prerequisites`, SDK links and writable AVD state. The pinned
  reusable tool bytes may be shared read-only; old AVD state may not.
- Resolve `/workspace/hand-contract-repro` in `common.py` and the corpus import in
  `prepare.py`. `build.py` additionally reads wrapper native libraries and extra
  jars from `/workspace/metadata-contract-e2e-20261004T030536Z/prerequisites`.
  Adapt those references in the new copy if using a newly reconstructed toolset;
  record and review the exact patch before execution.
- Check `fetch_dependencies.py` downloads against the separately recorded Maven
  hashes before building. It records hashes but does not enforce an independent
  expected-hash lock. Inspect resolved Java/native classpaths, rather than claiming
  both consumers use identical embedded interpreters.
- Freeze the new plan/input provenance before generation and execution. Create a
  new `PLAN_FREEZE.json`; do not reuse a historical timestamp to imply blinding.
  The default startup and runner target port 5554; both need the same adaptation
  if another port is selected. Use functional package/activity readiness checks,
  since P2's original startup checks only `sys.boot_completed`.

Only after those preparations, run this **HISTORICAL sequence / PLANNED execution**
from the new `P2` directory:

```sh
export PYTHONDONTWRITEBYTECODE=1
export PYTHONOPTIMIZE=0
HANDOFF_PY=/workspace/hand-contract-repro/.venv/bin/python
python3 scripts/fetch_dependencies.py
"$HANDOFF_PY" scripts/prepare.py
python3 scripts/build.py
"$HANDOFF_PY" scripts/capture_versions.py
python3 scripts/freeze_execution_inputs.py
python3 scripts/start_emulator.py
python3 scripts/run.py
"$HANDOFF_PY" scripts/analyze.py
python3 scripts/normalize_results.py
```

Check the frozen inputs and raw records independently before generating prose.
Use the [maintained P2 reader](../../work/review-fixes-20261021/verify_p2_records.py)
against the recovered or newly created round:

```sh
# PLANNED: requires actual APKs, device records, models and frozen inputs.
PYTHONDONTWRITEBYTECODE=1 python3 \
  work/review-fixes-20261021/verify_p2_records.py \
  --round-root /path/to/p2-round \
  --output /path/outside/round-and-repository/new-p2-readback.json
```

The round contains `INPUTS.json`, `P2/EXECUTION_INPUT_FREEZE.json`, build results,
APKs and device files. The output must be new and outside both the evidence round
and checkout. The report separates evidence validity, observation coverage and
historical-outcome comparisons; overall PASS/exit 0 requires all three to pass.
Differences remain failures to inspect, not reasons to alter evidence.
The preserved `review/verify_runtime_records.py` remains a historical source:
its old total PASS omitted score/raw invariance and required coverage. It is not
the maintained acceptance gate. Neither reader executes a model or independently
authenticates historical execution.

Historical targets: ten configurations, 18 actual input observations, 16 decoded
lists and ten wrapper raw tensors. Wrapper deletion rejects at the getter after
process; Task deletion rejects during construction. Task `classify` combines
inference and decoding, so do not invent an independently observed internal
inference stage. The eight successful shared variant/input pairs compare returned
score bits and labels, not unobserved native Task raw tensors. These are comparison
targets, not conditions to force by changing dependencies or fixtures.

## 6. P3 reference inquiry: retrieval and offline analysis are separate

P3 does not run inference. A replay of its network requests is a new retrieval
with historical findings already known; mutable responses may differ. First copy
the P3 source and eight request-plan JSON files to a new external `P3` directory.
Create its absent `retrieved/` and `analysis/` directories. Keep the same bounded
30-request sequence; do not replace failed requests with additional candidates.

From that new copy, this is the **HISTORICAL retrieval sequence / PLANNED execution**:

```sh
export PYTHONDONTWRITEBYTECODE=1
python3 scripts/retrieve.py initial-candidates.json
python3 scripts/retrieve.py followups-1.json
python3 scripts/retrieve.py followups-2.json
python3 scripts/retrieve.py followups-3.json
python3 scripts/retrieve.py followups-4.json
python3 scripts/retrieve.py additional-initial-candidates.json
python3 scripts/retrieve.py followups-5.json
python3 scripts/retrieve.py followups-6.json
```

The retriever preserves HTTP failures and refuses existing per-request folders.
It expects a positional JSON plan, not `--help`. Inspect each retrieval record
and source digest before analysis. To analyze recovered old bytes instead, copy
verified `retrieved/` objects into a fresh working copy and record that activity
as recovery, not fresh retrieval. Never refetch over a recovered directory.

`analyze_reference.py` requires the pinned Support/FlatBuffers/NumPy environment,
exact original/E2 permutation/restoration model bytes, and the retrieval IDs
specified in its source. Its `OLD` constant points at
`/workspace/metadata-contract-e2e-20261004T030536Z`; re-root only the new copy when
necessary and record the patch. It executes and writes on import; no help mode.

```sh
# PLANNED: after sources/model identities and any re-rooting patch are reviewed.
PYTHONOPTIMIZE=0 PYTHONDONTWRITEBYTECODE=1 \
  /workspace/hand-contract-repro/.venv/bin/python scripts/analyze_reference.py \
  > analysis/analyze.stdout 2> analysis/analyze.stderr
```

This computes the graph bridge and full display comparison, but does not recreate
all supplemental chain-authentication evidence by itself. The separate
`review/reference-audit/audit_candidate.py` also has fixed `BASE` and model paths;
it must be reviewed and re-rooted in a new copy with its raw retrieval inputs
before it can certify that portion of the reproduction. Treat report/sealing
scripts as historical publishing steps, not validators.

Historical targets: identical computation fields, ordered outputs and 165
non-metadata buffers across the model bridge; 1000 original/restored matches and
999 permutation disagreements with the qualified publisher display reference.
The background offset must come from the pinned publisher card. Stable-class-ID
lineage remains ABSTAIN; display agreement does not establish task accuracy.

## 7. Commands deliberately not offered as a one-click replay

Do not run a repository-wide `commands.sh`, `seal*.py`, `finalize*.py`, or a
historical manuscript-revision script against preserved paths. Several scripts
write on import, replace summary files, depend on old absolute roots, or contain
fixed historical conclusions. Historical `commands-executed.sh` records exact
past actions, including failed/replaced attempts; replaying all lines is not a
clean build procedure. Never probe such scripts with `--help` without reading
their top-level code first.

E4/E5, Hand and broad corpus re-execution are not required to hand off the focal
E1/E2/P2/P3 paths. Their [existing entry points](../../sources/repro-audit-20261004/README.md)
remain available for separately scoped work. No command in this document upgrades
agent execution to human audit or turns historical hashes into an available
evidence deposit.
