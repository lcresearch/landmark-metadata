# Prepare the base Python environment and corpus

`prepare_base.py` supplies the two prerequisites used by the Android and E4/E5
helpers: a fresh `hand-contract-repro` source copy with its pinned Python venv,
and a fresh `metadata-contract-paper` source copy. It reads the repository's
historical snapshots without modifying them. All installed packages, models,
generated code, logs and execution results remain outside Git.

The default operation is **setup only**: copy and hash-check source files,
create a venv using an already installed Python, install exactly the dependency
lock with `uv --no-deps`, check package dependencies, and verify installed
versions. It does not download models or execute experiments. Existing output
roots are rejected before copying; the two roots must be outside the checkout,
distinct and nonnested. No existing evidence directory is cleaned or overwritten.
Use the existing checkout; an isolated cloud task does not need a Git worktree.

## Existing Python and uv

The script requires an existing `uv` executable and existing Python **3.11.16**.
It does not install either tool or silently download another interpreter. The
actual replay installed Python with uv's installation directory under
`/workspace/repro-control/python`. If preparing a new machine, install the
interpreter separately through the normal verified download path:

```bash
UV_PYTHON_INSTALL_DIR=/workspace/repro-control/python \
  uv python install 3.11.16
```

Use the exact returned executable path. In the recorded run it was:
`/workspace/repro-control/python/cpython-3.11.16-linux-x86_64-gnu/bin/python3.11`.
Network access to the package repositories and Python release host must be
allowed by the environment policy. Preserve configured proxies and CA trust;
do not disable artifact or TLS verification. No additional secrets are required
for these public packages and model URLs.

## Setup only

On a fresh machine where both default roots do not exist:

```bash
python /path/to/prepare_base.py \
  --repo-root /workspace/landmark-metadata \
  --python /workspace/repro-control/python/cpython-3.11.16-linux-x86_64-gnu/bin/python3.11
```

By default the roots are `/workspace/hand-contract-repro` and
`/workspace/metadata-contract-paper`. `--hand-root`, `--corpus-root` and `--uv`
accept explicit paths. The later E4/E5 and Android helpers retain documented
historical path assumptions; use their standard layout for the full replay.
For copy-only validation in temporary directories, `--copy-only` skips uv,
Python version checks and dependency installation. This mode explicitly reports
that no environment was created; it is not evidence of successful installation.

Source provenance, every executed command, installation logs, the observed
package versions and final status are saved under
`HAND_ROOT/setup-base/`. Both copied roots receive `results/` and `logs/`.
The two historical requirements locks must agree. The shared venv uses the Hand
lock's 11 exact pins, including Support 0.4.4, Lite Runtime 2.14.0, NumPy 1.26.4
and protobuf 3.20.3. It is separate from the MediaPipe 0.10.14 Hand Task venv,
which has different protobuf requirements.

## Explicitly fetch and run the static corpus

To perform model downloads and static checking as part of a **fresh** setup,
add `--fetch-and-static` to the same invocation. Choose this flag on the initial
run; invoking the preparer against roots already created by setup is rejected.

```bash
python /path/to/prepare_base.py \
  --repo-root /workspace/landmark-metadata \
  --python /workspace/repro-control/python/cpython-3.11.16-linux-x86_64-gnu/bin/python3.11 \
  --fetch-and-static
```

This runs the unchanged historical `fetch_suite.py`, validates its actual output,
then runs `inspect_suite.py` and `suite_static.py` with the pinned venv. The script
checks that download records are nonempty, cover every fixed target, have real
successful component files, and match their recorded lengths/hashes. A zero-exit
fetch script with zero usable downloads is rejected.

The precise historical MobileNet V2 URL's HTTP 404 is recorded as a known
unavailable target. Other 404s, 403s, TLS/transport errors and incomplete archives
remain unexpected failures; they are not replaced, relabeled as the known 404,
or silently ignored. The component SHA-256 set must equal the historical base
identities recorded in the repository's E4 `prior-exclusions.json`. Any changed
or missing artifact stops processing with a retained diagnostic in
`results/fetch-validation.json`; inspect the change before claiming the same
corpus. The current recovered set has 13 byte-distinct components.

If setup fails, its new directories and logs remain available for diagnosis.
Correct the cause and choose fresh roots for another preparer invocation. Do
not remove an existing evidence run merely to satisfy the fresh-root guard.

## Continue runtime, Java and decoder validation

`--fetch-and-static` does not install Java dependencies or run inference. Restore
Temurin 17.0.12+7 and the pinned Java jars using the Android preparation helper
before Java compilation/decoder checks. The historical `restore_toolchain.py`
expects an excluded download record, so it is not a stand-alone SDK bootstrap.
Do not claim Java readiness merely because the Python setup completed.

On the new working corpus, run the remaining original stages after the Java
prerequisites exist. These commands generate evidence inside that working copy:

```bash
cd /workspace/metadata-contract-paper
export HAND_REPRO_ROOT=/workspace/hand-contract-repro
export PYTHONDONTWRITEBYTECODE=1
export PYTHONOPTIMIZE=0
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=1
/workspace/hand-contract-repro/.venv/bin/python scripts/suite_runtime.py
/workspace/hand-contract-repro/.venv/bin/python scripts/suite_compile.py
/workspace/hand-contract-repro/.venv/bin/python scripts/suite_decoder.py
/workspace/hand-contract-repro/.venv/bin/python scripts/suite_index.py
/workspace/hand-contract-repro/.venv/bin/python scripts/summarize.py
```

If setup-only was chosen initially, the equivalent model preparation commands
in that fresh working copy are `fetch_suite.py`, `inspect_suite.py` and
`suite_static.py`, in that order. Independently validate the fetch records as
described above before proceeding; alternatively choose fresh roots and use the
opt-in preparer, which enforces that validation automatically.

Preserve expected structural and decoder rejections, compiler failures, missing
metadata and semantic abstentions. The legacy summary script contains fixed
historical counts and some permissive aggregate checks; its exit status is not
independent verification. Inspect raw arrays, actual result records and the
separate audit probes. Do not use optimized Python execution to bypass its
assertions. This corpus workflow does not replace Android getter execution,
independent human audit or evidence-based semantic reference verification.

## Validation already performed in this session

The existing actual setup at `/workspace/hand-contract-repro` matched all 11
historical dependency versions under Python 3.11.16. The already executed base
suite recovered 13 components, 35 structurally accepted variants and 11 rejected
controls. The independent corpus verifier checked 105 CPU observations, 243 raw
arrays and 23 decoder probes: **594 checks passed, zero failed**.

Those observations come from the existing runtime evidence at
`/workspace/repro-external/runtime-environment.json` and
`/workspace/repro-control/corpus-verification.json`. They are local evidence
locators, not files included in the source-only PR. The new preparer's validation
uses fresh temporary directories for source copying and argument guards only;
no extra model run or dependency reinstall is represented as completed.
