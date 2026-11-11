# Current focal runbook

Run from this checkout, with already verified input/reference directories from
the [input recovery tools](inputs/README.md). Choose an absent
run directory. The paths below identify the actual November run; do not execute
them over its retained outputs. Set `run_root` to a different absent location.
The example assumes a Linux x86_64 host, network access and no other emulator on
port 5554. Initial sandbox inspection did not expose `/dev/kvm`; the later
execution-host record does see the device. Device presence alone does not establish
usable acceleration. The frozen run explicitly uses `-accel off`; software boot
took about 334 seconds. Do not describe KVM as unavailable on the whole host.

```sh
set -eu
repo_root="$PWD"
run_root=/path/outside/repository/new-focal-run
input_root=/home/hsz/landmark-evidence/input-recovery-20261110
reference_root=/home/hsz/landmark-evidence/reference-recovery-20261110
driver="$repo_root/experiment/run"
python3 "$driver/initialize.py" --root "$run_root" \
  --inputs "$input_root" --references "$reference_root"
stage() {
  stage_label="$1"
  shift
  python3 "$driver/stage.py" --root "$run_root" --label "$stage_label" -- "$@"
}
stage python-bootstrap python3 "$driver/bootstrap_python.py" --root "$run_root"
stage record-environment python3 "$driver/record_environment.py" --root "$run_root"
run_python="$run_root/hand/.venv/bin/python"
android_scripts="$run_root/android/scripts"
p2_scripts="$run_root/round/P2/scripts"
stage android-prerequisites python3 \
  "$repo_root/experiment/toolchain/restore_prerequisites.py" \
  --root "$run_root/android" --hand "$run_root/hand" --repo "$repo_root"
stage android-prerequisite-recheck python3 \
  "$repo_root/experiment/toolchain/restore_prerequisites.py" \
  --root "$run_root/android" --hand "$run_root/hand" --repo "$repo_root" --verify-cache
stage e1-prepare "$run_python" "$android_scripts/prepare_e1.py"
stage e1-build "$run_python" "$android_scripts/build_android.py" --experiment E1
stage android-boot python3 "$android_scripts/start_emulator.py"
stage e1-primary python3 "$driver/resume_android_phase.py" --root "$run_root" --experiment E1 --run primary
stage e1-replay python3 "$driver/resume_android_phase.py" --root "$run_root" --experiment E1 --run replay
stage e1-summary "$run_python" "$android_scripts/summarize_android.py" --experiment E1
stage e2-prepare "$run_python" "$android_scripts/prepare_e2.py"
stage e2-build "$run_python" "$android_scripts/build_android.py" --experiment E2
stage e2-primary python3 "$driver/resume_android_phase.py" --root "$run_root" --experiment E2 --run primary
stage e2-replay python3 "$driver/resume_android_phase.py" --root "$run_root" --experiment E2 --run replay
stage e2-summary "$run_python" "$android_scripts/summarize_android.py" --experiment E2
stage android-audit "$run_python" "$android_scripts/audit_android_results.py"
stage p2-fetch python3 "$p2_scripts/fetch_dependencies.py"
stage p2-dependency-pins python3 "$driver/verify_p2_dependencies.py" --root "$run_root"
stage p2-prepare "$run_python" "$p2_scripts/prepare.py"
stage p2-build "$run_python" "$p2_scripts/build.py"
stage p2-versions "$run_python" "$p2_scripts/capture_versions.py"
stage p2-freeze "$run_python" "$p2_scripts/freeze_execution_inputs.py"
```

Inspect all ten P2 build records for successful compile/package before execution;
the historical builder can exit zero while recording failed configurations.
Reuse the existing new AVD rather than invoking P2's separate startup script.
Uninstall only this run's E1/E2 test package before P2: P2 signs the same wrapper
package name with its own disposable key, so an in-place update would conflict.
Preserve the uninstall command and result.

```sh
run_adb="$run_root/android/sdk/platform-tools/adb"
stage p2-remove-e1-app "$run_adb" -s emulator-5554 uninstall org.example.contract.consumer
stage p2-readiness python3 "$android_scripts/check_android_ready.py" \
  --adb "$run_adb" --serial emulator-5554 \
  --evidence "$run_root/round/P2/prerequisites/functional-readiness.json" --timeout 90
stage p2-primary "$run_python" "$p2_scripts/run.py"
stage p2-analysis "$run_python" "$p2_scripts/analyze.py"
stage p2-normalize "$run_python" "$p2_scripts/normalize_results.py"
stage p2-readback python3 "$repo_root/work/review-fixes-20261021/verify_p2_records.py" \
  --round-root "$run_root/round" --output "$run_root/readback/p2.json"
stage p3-core "$run_python" "$driver/analyze_p3_core.py" \
  --inputs "$input_root" --references "$reference_root" --output "$run_root/p3-core"
```

Inspect the independent audit/readback details, not just exit codes. Stop only
the emulator owned by this run after collection, preserve that command, and then
invoke the archive helper directly (outside a still-running stage):

```sh
python3 "$driver/package_evidence.py" --root "$run_root" \
  --inputs "$input_root" --references "$reference_root" \
  --archive /path/outside/repository/new-focal-evidence.tar.gz
```

The actual commands/timestamps are in external `stages/*/command.json`, per-build
and per-execution command records and `commands-executed.sh`. Preparation of P2
and P3 was done while the new AVD booted; device instrumentation is serial.
