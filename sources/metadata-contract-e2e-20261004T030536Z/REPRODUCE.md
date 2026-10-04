# Reproduction and inspection

This is a locally preserved extension of two existing workspace projects, not a standalone offline release. Do not execute the original suite writers or the new preparation/build scripts inside their already populated evidence directories. They would either refuse existing destinations or overwrite summary records. Every new execution needs a fresh timestamped root.

## Read-only verification

```bash
cd /workspace/metadata-contract-e2e-20261004T030536Z
bash commands.sh verify
```

This verifies historical manifest entries, the phase-0 inventory, all six sealed experiment manifests, the final global manifest when present, and saved primary/replay tensor, label, bytecode and failure evidence. It runs no generation, compilation or inference. `verification/final-integrity.json` records the final pre-global-manifest audit; the final global verification is reported separately by this command.

`commands-executed.sh` is a historical command log, **not a script to replay in place**. Each `.command.json` records the exact argument vector, working directory and return code, with adjacent stdout/stderr. Model-generation/build/runtime subprocesses use these records. Archived download/source provenance additionally records URLs and hashes; exploratory shell inspection is not claimed to be fully captured by the subprocess logger.

## Required local dependencies and exact identities

- `/workspace/metadata-contract-paper`: original model/control bytes, helper scripts, old contracts and manifests. It remains unchanged.
- `/workspace/hand-contract-repro`: CPython 3.11.16 environment, Temurin 17.0.12+7, original jars, Hand evidence and archived JDK distribution. It remains unchanged.
- `prerequisites/downloads.json`: official SDK platform API 30 r3, build tools 35.0.0, platform tools 37.0.1, emulator 37.2.12/build 16428233, Android 30 x86_64 system-image archive r11, exact archive hashes and original checksums. The image's internal properties report r10; see `REPORTING_CLARIFICATIONS.md`.
- `prerequisites/`: TFLite Java/native 2.13.0; Support, Support API and metadata 0.4.4; FlatBuffers Java 2.0.0; AndroidX annotation 1.3.0; ODML image 1.0.0-beta1; checker-qual 2.5.8; auto-value-annotations 1.6. Every compiled unit records its exact jar hashes. Actual SDK/API 30 is used for the APK harness; historical compile-only stubs were 4.1.1.4.
- `prerequisites/python-wheels/`, `python-wheels.json` and the old `requirements.lock`: archived generator/Task Python dependencies. Installed native files were matched to wheel members. TFLite Runtime 2.14.0 belongs to the historical Python inference phase; Android uses 2.13.0.
- `E7/requirements.lock`, `E7/wheels.json`, `E7/native-implementation.json`: separate MediaPipe 0.10.14 Task environment and pinned native identities. Embedded Task TFLite versions were not separately established.

The selected SDK repository XML is archived; `scripts/setup_android.py` extracts those selected packages and official AARs. Additional declared dependencies, obtained before any Android execution, are separately recorded in `extra-dependencies.json`. Reproduction must include them, not just run the initial setup script and omit the later dependency closure.

## Fresh E1/E2 execution using the preserved local toolchain

The following commands retain the old workspace dependencies and reuse the installed SDK tools read-only. The new AVD, logs, generated code, builds and results live in a new directory. This is same-toolchain reproduction, not independent verification or a newly claimed completed run.

```bash
set -euo pipefail
TASK_SOURCE=/workspace/metadata-contract-e2e-20261004T030536Z
TASK_REPLAY="/workspace/metadata-contract-replay-$(date -u +%Y%m%dT%H%M%SZ)"
test ! -e "$TASK_REPLAY"
mkdir -p "$TASK_REPLAY/scripts" "$TASK_REPLAY/prerequisites" "$TASK_REPLAY/sdk"
cp "$TASK_SOURCE"/scripts/*.py "$TASK_SOURCE"/scripts/*.java "$TASK_REPLAY/scripts/"
cp "$TASK_SOURCE"/EXPERIMENT_E1_PLAN.md "$TASK_SOURCE"/EXPERIMENT_E2_PLAN.md "$TASK_REPLAY/"
cp -a "$TASK_SOURCE/prerequisites/aar" "$TASK_SOURCE/prerequisites/extra-jars" "$TASK_REPLAY/prerequisites/"
for TASK_PART in emulator platform-tools build-tools platforms system-images; do
  ln -s "$TASK_SOURCE/sdk/$TASK_PART" "$TASK_REPLAY/sdk/$TASK_PART"
done
cd "$TASK_REPLAY"
export PYTHONDONTWRITEBYTECODE=1
TASK_PY=/workspace/hand-contract-repro/.venv/bin/python
"$TASK_PY" scripts/prepare_e1.py
python3 scripts/start_emulator.py
"$TASK_PY" scripts/build_android.py --experiment E1
python3 scripts/run_android.py --experiment E1 --run primary
python3 scripts/run_android.py --experiment E1 --run replay
python3 scripts/summarize_android.py --experiment E1
"$TASK_PY" scripts/prepare_e2.py
"$TASK_PY" scripts/build_android.py --experiment E2
python3 scripts/run_android.py --experiment E2 --run primary
python3 scripts/run_android.py --experiment E2 --run replay
python3 scripts/summarize_android.py --experiment E2
sdk/platform-tools/adb -s emulator-5554 emu kill
```

Use emulator port 5554 only when free. Hardware acceleration was absent; the preserved command uses `-accel off` and software graphics. Initial boot took approximately five minutes. The actual run command is `adb -s emulator-5554 shell am instrument -w -e variant <variant> org.example.contract.consumer/org.example.contract.ContractInstrumentation`, preceded by installation of the corresponding APK. The source calls the generated `newInstance`, `process`, and public category getter. No generated-source repair is permitted.

The build uses javac `--release 8`, D8, aapt2, zipalign and apksigner, with exact expanded arguments in each build log. A new disposable debug key changes APK bytes; APK equality is not a preservation criterion. Generated source, generated classes, DEX and raw outputs are compared separately. The harness records and catches decoder errors, so an instrumentation-process exit code alone does not describe decoder success.

For an interrupted replay, retain the partial directory and run only the uncompleted variant under a **new** `--run replay-recovery-<timestamp>` directory using `--variants <name>`. Do not replace completed records. The summary merges nonoverlapping replay records explicitly. This is the disclosed E2 recovery procedure, not permission to discard experimental failures.

## Other phases and standalone checks

After E1/E2 in the new root, `"$TASK_PY" scripts/task_consumer.py --run primary` and `--run replay` execute E3 against the same variants and saved RGB inputs. `python3 scripts/summarize_e3.py` prepares its comparison; archived official source/provenance must also be retained for implementation interpretation.

The E4 rule/candidate freeze already occurred at commit `a1adde5e2e77b6f30a77a689b5e1025a887a58bd`. Reapplying its rules to archived artifacts is a replay; it cannot constitute another previously unseen sample. See `E4/protocol/`, `scripts/external_validation.py` and the preserved command log. Do not replace failed candidates or silently revise the frozen rules. E5's evaluated implementation is preserved at `E5/preflight.py`; its evaluation script is `scripts/evaluate_preflight.py` with E1/E2/E4 as inputs.

Run the pre-flight command with a new output directory:

```bash
cd /workspace/metadata-contract-e2e-20261004T030536Z
PYTHONDONTWRITEBYTECODE=1 /workspace/hand-contract-repro/.venv/bin/python scripts/preflight.py \
  E1/variants/label_deletion/model.tflite \
  --evidence-dir "/workspace/preflight-evidence-$(date -u +%Y%m%dT%H%M%SZ)"
```

The demonstrated deletion returns exit 2 for its specific incompatibility. Exit 0 may include explicit semantic/dynamic-shape abstention; it is not universal correctness. No compile/inference occurs in this command.

Hand uses a separate environment: `scripts/setup_hand_task.py` records its setup, `scripts/prepare_hand.py` preserves bundle variants and audits old bindings, and `scripts/run_hand_task.py --run <new-name>` invokes the actual Task. Source-pinned assets, references and model-bridge records must be copied into a **fresh E7 destination** first, as identified in `EXPERIMENT_HAND_PLAN.md` and `E7/REFERENCE_CHAIN.md`. The original setup selected versions before execution; for future replay install the exact archived `E7/requirements.lock` from `E7/wheels` rather than resolving current transitive versions. E7 is not an unmodified generic Hand-wrapper runtime experiment.

## Preservation scope

The root `SHA256SUMS` covers evidence, scripts, documents, archived SDK downloads, dependency wheels, model bytes and phase manifests. It excludes installed `sdk/` state (including the writable AVD), installed virtual environments, Python caches and itself. Phase manifests retain their original scope; E4 includes its frozen local Git records. Do not mutate sealed directories, including their Git index.

The original manuscript is unchanged; manuscript updates are proposed in `MANUSCRIPT_IMPACT.md`. A public deposit, independent reproduction and human audit are still pending.
