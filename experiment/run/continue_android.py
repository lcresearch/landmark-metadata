"""Finish serial focal execution after an already-started E1 primary stage.

P2 preparation/build/freeze must already be complete. All stages have exclusive
logs; failures stop the sequence. This foreground driver does not schedule work.
"""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
import time

REPO = Path(__file__).resolve().parents[2]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, required=True)
    ap.add_argument('--primary-stage', required=True)
    args = ap.parse_args()
    root = args.root.resolve()
    if root.is_relative_to(REPO):
        raise ValueError('Expected external evidence root')
    stage_record = root / 'stages' / args.primary_stage / 'command.json'
    if not stage_record.is_file():
        raise ValueError('Missing primary stage')
    deadline = time.monotonic() + 2400
    while True:
        try:
            primary = json.loads(stage_record.read_text())
        except json.JSONDecodeError:
            primary = {'status': 'RUNNING'}
        if primary['status'] != 'RUNNING':
            break
        if time.monotonic() > deadline:
            raise TimeoutError('Pending E1 primary did not complete')
        time.sleep(5)
    if primary.get('exit_code') != 0:
        raise ValueError('E1 primary stage did not finish successfully')
    p = root / 'hand/.venv/bin/python'
    android = root / 'android/scripts'
    p2 = root / 'round/P2/scripts'
    adb = root / 'android/sdk/platform-tools/adb'
    resume = Path(__file__).with_name('resume_android_phase.py')
    def stage(label, *command):
        print(datetime.now(timezone.utc).isoformat(), 'START', label, flush=True)
        process = subprocess.run([sys.executable, str(Path(__file__).with_name('stage.py')),
                                  '--root', str(root), '--label', label, '--timeout', '5400',
                                  '--', *map(str, command)], capture_output=True, text=True)
        print(datetime.now(timezone.utc).isoformat(), 'END', label, 'exit', process.returncode, flush=True)
        if process.returncode:
            print(process.stdout, process.stderr, flush=True)
            raise SystemExit(process.returncode)
    def require_e1_complete():
        rows = json.loads((root / 'android/E1/executions/primary/results.json').read_text())
        expected = {'original', 'description_control', 'label_deletion', 'label_restoration'}
        if len(rows) != 4 or {r['variant'] for r in rows} != expected:
            raise ValueError('Incomplete E1 primary')
        for row in rows:
            if row.get('load_status') != 'PASS' or row.get('inference_status') != 'PASS':
                raise ValueError('E1 did not reach inference: ' + row['variant'])
            wanted = 'FAIL' if row['variant'] == 'label_deletion' else 'PASS'
            if row.get('decoder_status') != wanted:
                raise ValueError('E1 decoder differs from target: ' + row['variant'])
    require_e1_complete()
    stage('e1-replay', sys.executable, resume, '--root', root, '--experiment', 'E1', '--run', 'replay')
    stage('e1-summary', p, android / 'summarize_android.py', '--experiment', 'E1')
    stage('e2-prepare', p, android / 'prepare_e2.py')
    stage('e2-build', p, android / 'build_android.py', '--experiment', 'E2')
    for phase in ['primary', 'replay']:
        stage('e2-' + phase, sys.executable, resume, '--root', root, '--experiment', 'E2', '--run', phase)
    stage('e2-summary', p, android / 'summarize_android.py', '--experiment', 'E2')
    stage('android-audit', p, android / 'audit_android_results.py')
    builds = json.loads((root / 'round/P2/build-results.json').read_text())
    expected = {(c, v) for c in ['wrapper', 'task'] for v in
                ['original', 'description_control', 'label_deletion', 'label_permutation', 'restoration']}
    if (len(builds) != 10 or {(r['consumer'], r['variant']) for r in builds} != expected
            or any(r.get('package_status') != 'PASS' for r in builds)):
        raise ValueError('P2 requires ten successful builds')
    if not (root / 'round/P2/EXECUTION_INPUT_FREEZE.json').is_file():
        raise ValueError('P2 requires pre-execution freeze')
    stage('p2-remove-e1-app', adb, '-s', 'emulator-5554', 'uninstall', 'org.example.contract.consumer')
    stage('p2-readiness', sys.executable, android / 'check_android_ready.py', '--adb', adb,
          '--serial', 'emulator-5554', '--evidence', root / 'round/P2/prerequisites/functional-readiness.json', '--timeout', '90')
    stage('p2-primary', p, p2 / 'run.py')
    stage('p2-analysis', p, p2 / 'analyze.py')
    stage('p2-normalize', p, p2 / 'normalize_results.py')
    stage('p2-readback', sys.executable, REPO / 'work/review-fixes-20261021/verify_p2_records.py',
          '--round-root', root / 'round', '--output', root / 'readback/p2.json')
    print('Serial E1/E2/P2 sequence finished; inspect audit reports before claiming success.', flush=True)


if __name__ == '__main__':
    main()
