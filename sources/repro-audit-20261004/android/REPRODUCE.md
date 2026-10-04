# Fresh Android reconstruction

These text/source files reconstruct the Android prerequisites and copy preserved experiment scripts into a new external directory. Models, SDKs, JDKs, AVDs, dependency archives/jars, generated wrappers, APKs, keys and runtime evidence stay outside Git. Keep existing checkouts; a Git worktree is unnecessary.

The parent restoration must first prepare `/workspace/hand-contract-repro/.venv/bin/python` (CPython 3.11.16, recorded Python lock) and `/workspace/metadata-contract-paper/runs/6c7ab0a6e5dc/{original,description_control,label_drop_1}/model.tflite`, plus its `scripts/` directory. The original publisher model must have SHA-256 `6c7ab0a6e5dcbf38a8c33b960996a55a3b4300b36a018c4545801de3a3c8bde0`. This Android helper does not claim to restore those independent prerequisites.

## Installation

Run from this source directory; use a new external output directory, never a sealed run or `sources/` import. Set `REPRO_ROOT` below to an unused path. The scripts intentionally retain the two parent dependency paths above.

```bash
set -euo pipefail
REPRO_ROOT=/workspace/android-fresh-reconstruction
python3 initialize_run.py --repo /workspace/landmark-metadata --root "$REPRO_ROOT"
python3 select_official_android_xml.py --root "$REPRO_ROOT"
python3 restore_prerequisites.py --root "$REPRO_ROOT" --hand /workspace/hand-contract-repro
python3 restore_prerequisites.py --root "$REPRO_ROOT" --hand /workspace/hand-contract-repro --verify-cache
```

`android-prerequisites.lock.json` fixes the 5 SDK archives, Temurin 17.0.12+7, and 11 Java archives. SHA-256, official SHA-1 where available, SDK size and extracted Java jar digests are checked with explicit exceptions, including under optimized Python. The lock records the official XML/checksum sources used to establish these identities. TLS verification stays enabled. The separate XML selector verifies the exact package versions against current official metadata; if future metadata stops listing a pinned version, report that difference instead of silently selecting a new version. Pinned archives remain identifiable independently of mutable XML.

The tested versions are API 30 platform r3, build tools 35.0.0, platform tools 37.0.1, emulator 37.2.12/build 16428233, and x86_64 API-30 default system-image archive r11. The image's internal properties say r10; its archive SHA-256 is `8d591034a4244a920d7a3ec274bb1734dd6474a3d8c11d0fce902010db3a13aa`. This publisher packaging discrepancy is preserved.

ADB 37 writes local configuration to `~/.android`; it ignores `ANDROID_USER_HOME` and `ANDROID_SDK_HOME` in the checked binary. In this cloud instance, a scoped filesystem escalation created `/home/agent/.android` as a symlink to `/workspace/repro-android/android-user`. Use an existing writable Android configuration directory, or obtain write access for this local setup if a new instance has a read-only home. Do not overwrite existing user files or change `HOME` to work around this.

## Execute the actual generated getter

From the fresh root, run the unchanged generated Java through the preserved instrumentation harness. The imported audit harness adds a pre-initialization AssetManager hash measurement. The generated wrapper is not repaired or changed. The copied audit `prepare_e2.py` requires completed E1 primary; all replays are still required for the final audit.

```bash
cd "$REPRO_ROOT"
export PYTHONDONTWRITEBYTECODE=1
REPRO_PY=/workspace/hand-contract-repro/.venv/bin/python
"$REPRO_PY" scripts/prepare_e1.py
python3 scripts/start_emulator.py
"$REPRO_PY" scripts/build_android.py --experiment E1
python3 scripts/run_android.py --experiment E1 --run primary
python3 scripts/run_android.py --experiment E1 --run replay
python3 scripts/summarize_android.py --experiment E1
"$REPRO_PY" scripts/prepare_e2.py
"$REPRO_PY" scripts/build_android.py --experiment E2
python3 scripts/run_android.py --experiment E2 --run primary
python3 scripts/run_android.py --experiment E2 --run replay
python3 scripts/summarize_android.py --experiment E2
"$REPRO_PY" scripts/audit_android_results.py
```

Keep Python assertions enabled for the historical experiment scripts; no optimized-mode execution is validated. The default emulator uses port 5554, a newly created AVD, `-accel off`, software graphics, 2 GiB RAM and two virtual cores. No KVM device was available in the reconstruction environment. First boot took 537.7 seconds. Allow the readiness script's 900-second deadline and inspect real readiness; an ADB connection by itself is insufficient.

The runner catches experiment and harness errors; its exit 0 alone is insufficient. `audit_android_results.py` requires complete variants and observations, verifies actual getter stages/stack traces, model identity across working file/APK/AssetManager, both input constructions, raw outputs, returned score bits, permutation, restoration, replay, and actual Java source/class/DEX/native equality across all eight fresh builds. It rereads class and DEX files, compares APK DEX bytes, recomputes five distinct model identities and one canonical graph from the actual models, and checks recorded input hashes against input bytes. It never equates fresh binaries to excluded historical binaries. A failed assertion in this independent checker is a failed evidence check, not automatically a model defect.

## Failed parallel-AVD attempt and successful strategy

The reconstruction attempted a second cold-boot AVD at port 5556, sharing verified tools and exact APKs read-only. Its boot property became 1 after 723.9 seconds, but SystemUI ANR and system_server restarts left the package service unavailable. All four E1 replay installation attempts failed with `Can't find service: package`; model loading, inference and decoding were NOT_REACHED. Evidence remains under `/workspace/repro-android-replay`; it is excluded from successful model observation counts.

The second AVD was stopped. Required E1/E2 replay was resumed in the stable primary AVD using new replay directories and the same APKs. The failure is a secondary virtual-device setup failure, not a model defect. No parallel replay success or independent human replication is claimed.

`initialize_run.py` now adds a functional readiness helper to copied startup instructions: boot property, real package lookup, activity configuration response, and three consecutive observations of the same system_server PID must pass. `check_android_ready.py` was exercised against the stable primary AVD. These checks describe observed service readiness; they cannot guarantee future process stability. The original experiment startup and failed second-AVD logs are preserved rather than rewritten to claim these additional checks ran earlier.

If execution is interrupted, preserve the partial attempt and its logs. Do not replace evidence or treat an incomplete record as a pass. Stop only emulator processes started by this workflow; the emulator PID is recorded in `prerequisites/emulator-command.json`. The cloud sandbox's read-only home prevented the emulator console token, so process termination was used for cleanup rather than claiming `adb emu kill` was available.

## What was tested for these source helpers

- `select_official_android_xml.py`: freshly downloaded both official XML files and matched all 5 exact archive identities.
- `restore_prerequisites.py --verify-cache`: validated all 17 archived prerequisites.
- `restore_prerequisites.py`: performed a second complete extraction into `/workspace/repro-android-restore-smoke`; the resulting JDK, ADB, D8 and aapt2 executables ran with the expected versions. The active experiment SDK was untouched.
- `check_android_ready.py`: verified package/activity service responses and stable system_server observations on the primary AVD; the added startup path was not retrospectively attributed to the earlier boot.
- `initialize_run.py`: initialized `/workspace/repro-android-initialize-smoke`; all copied Python sources compiled. The actual primary/replay model execution results are reported separately from this helper installation smoke test.
