# Fresh focal execution after cloud evidence loss

Date: 10 November 2026 (America/Los_Angeles). This work starts from
`05e6b22ad6dc32c18e340309c40431609651e0a8`, the input-recovery branch in
[PR #18](https://github.com/lcresearch/landmark-metadata/pull/18).
The user explicitly requested rerunning experiments using the repository guide.
The new external run is `/home/hsz/landmark-evidence/focal-rerun-20261110`.
See [observed results and evidence limits](RESULTS.md) for actual completion,
separate from the protocol's comparison targets.
The [delivery receipt](delivery-record.json) pins the new 3.32 GB local archive;
all 2,120 members passed full readback. E1/E2 and P2 automated audits pass, P3 core
is complete within its stated scope, and all 176 source/regression tests pass.

This is a known-outcome rerun of the focal E1/E2/P2 case plus the six-input P3
core analysis. It does not recover or authenticate the lost October execution.
The [protocol](PROTOCOL.md) was copied and hashed before model execution.
One graph, five byte conditions and two inputs remain the experimental scope.
Human verification, the full historical P3 search and broader Hand/E4/E5 histories
are separate. Manuscripts and historical snapshots remain unchanged.

## Source and environment handling

- [initialize.py](initialize.py) checks recovered input pins, creates new external
  working copies using the maintained Android initializer, records absolute-path
  adaptations and freezes their hashes. It does not edit imported sources.
- [bootstrap_python.py](bootstrap_python.py) installs an isolated uv-managed
  Python 3.11.16 and eleven historical wheel bytes verified against
  [toolchain.json](../../docs/reproduction/toolchain.json). uv 0.13.7 is separately
  pinned by wheel SHA-256. The new Python distribution is not claimed to equal an
  unrecorded historical interpreter binary.
- [stage.py](stage.py) gives each invocation an exclusive directory with command,
  time, exit status, stdout and stderr. Python assertions remain enabled. Completed
  means the process ended; scientific success requires actual evidence checks.
- [verify_p2_dependencies.py](verify_p2_dependencies.py) compares the newly fetched
  P2 archives and selected Java/native files with historical hashes and sizes.
- [record_environment.py](record_environment.py) records the actual interpreter
  binary/distribution hashes, host architecture and KVM availability, without
  collecting credentials or the host environment-variable dictionary.
- [continue_android.py](continue_android.py) runs the remaining serial Android
  sequence after a started E1 primary and prepared/frozen P2 builds. It waits for
  that primary, checks completion, and stops at failed stages. It is a foreground
  continuation tool, not a scheduler or cross-session synchronization service.
- [resume_android_phase.py](resume_android_phase.py) invokes the unchanged
  E1/E2 collector one condition at a time. Complete observations are kept even
  when their scientific outcome is FAIL. Only missing transport collections are
  retried. New invocation folders, prior partial folders, hash inventories and
  explicit selection records remain available alongside the audit's copied view.
- [analyze_p3_core.py](analyze_p3_core.py) checks all six reference pins and five
  model pins, recomputes the graph/buffer bridge and compares display order. Its
  normalization follows the preserved P3 method; this is not a new independent
  algorithm. No stable-class-ID or accuracy assertion is made.
- [package_evidence.py](package_evidence.py) creates and fully reads back a local
  evidence archive, with a manifest and explicit exclusions. Installed SDK/JDK/
  Python environments, caches, symlinks and disposable keys are excluded; downloaded
  archives, actual builds, raw observations and command records are retained.
  This is not remote backup, reviewer publication or a complete offline environment.

All SDK, JDK, model, APK, raw-output and archive bytes remain outside Git. The
historical toolchain restore scripts are used without changing their pins.
P2's preserved build script still says dependencies were reused from the old
sealed setup: for this run they were freshly acquired and rehashed, as the new
dependency receipt and mapped paths show. That old sentence is not new provenance.

## Reproduction sequence

Run from this checkout, with already verified input/reference directories from
the [input recovery tools](../input-recovery-20261110/README.md). Choose an absent
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
driver="$repo_root/work/focal-rerun-20261110"
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
  "$repo_root/sources/repro-audit-20261004/android/restore_prerequisites.py" \
  --root "$run_root/android" --hand "$run_root/hand" --repo "$repo_root"
stage android-prerequisite-recheck python3 \
  "$repo_root/sources/repro-audit-20261004/android/restore_prerequisites.py" \
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

## Preserved failures and scope limits

The current official Android XML omitted locked emulator 37.2.12. The
`android-metadata` stage failed and was retained. The guide permits separately
pinned archives; the historical direct archive remained available and matched its
SHA-256. All archive/cache verification passed without upgrading the emulator.

The first new P3 analyzer used E2's name `permutation_restoration` instead of the
input inventory's `restoration`; it stopped with `KeyError` before final results.
Its source and partial outputs remain in external `p3-core/`. After correcting
that identifier, a separate `p3-core-attempt2/` completed. No failed output was
overwritten or counted as a successful comparison.

A chat interruption ended the first E1 host collector after two complete
conditions, during deletion instrumentation collection. The stage is explicitly
marked `INTERRUPTED`, with no invented exit code; its former RUNNING record is
retained. All 51 collected files were hashed and relocated unchanged to
`android/E1/executions/primary-interrupted-attempt1/`; the path mapping is recorded
in `provenance/primary-attempt1-relocation.json`. Residual device evidence was
collected before stopping only the test app. Stage `e1-primary-attempt2` then
completed original, description and deletion before a second chat interruption
during restoration collection. Its state is also explicitly INTERRUPTED.

The new per-condition continuation collector retains those three completed
second-attempt records and runs restoration in a separate invocation. Its source
hash, previous results, interrupted restoration files and copied-view hashes are
recorded under `primary-continuation-1-provenance/`; actual invocation paths remain
in the controller rows. Subsequent E1/E2 phases use the same per-condition approach.
These are explicitly interrupted/resumed collections, not an uninterrupted single
controller run. No first-attempt observations are pooled in, and no unsuccessful
scientific outcome is discarded in favor of a retry.

The P3 core result matches all 1,000 original/restored positions and one permuted
position; the other 999 permuted positions disagree. All 165 non-metadata buffers
and ordered outputs match the bridge. Stable class IDs remain `ABSTAIN`;
the historical 30-request search and auxiliary synset comparison were not rerun.
New execution and local archive retention do not complete human audit or external
evidence distribution, and they do not broaden the paper's empirical population.

The first P2 independent readback found one exact-message mismatch in the reader:
its expected cause omitted the Java `Error occurred when initializing ImageClassifier:`
prefix present in both historical documentation and fresh device bytes. The
maintained reader was corrected to require that full exact text, with an independent
literal fixture and adversarial rejection tests. The original failing report/reader
remain in external `readback/`; `p2-after-message-fix.json` passes all 348 checks
against unchanged evidence. See [results](RESULTS.md) for counts and scope.
