"""Resume E1/E2 transport collection, preserving interrupted attempts and provenance.

Runs the unchanged external collector for each missing condition. Complete device
records are retained regardless of their scientific outcome; only transport gaps
are retried. A copied analysis view supports the original strict auditor, while
attempt folders and the selection manifest retain the real invocation history.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

REPO = Path(__file__).resolve().parents[2]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, required=True)
    ap.add_argument('--experiment', choices=['E1', 'E2'], required=True)
    ap.add_argument('--run', choices=['primary', 'replay'], required=True)
    args = ap.parse_args()
    root = args.root.resolve()
    if root.is_relative_to(REPO):
        raise ValueError('Expected external run')
    area = root / 'android' / args.experiment
    executions = area / 'executions'
    view = executions / args.run
    view.mkdir(parents=True, exist_ok=True)
    expected = [r['variant'] for r in json.loads((area / 'static-results.json').read_text())]
    results = view / 'results.json'
    rows = json.loads(results.read_text()) if results.exists() else []
    if len({r['variant'] for r in rows}) != len(rows) or any(r['variant'] not in expected for r in rows):
        raise ValueError('Duplicate or unknown collected condition')
    selected = {}
    for row in rows:
        device = view / row['variant'] / 'device/result.json'
        if row.get('observed') is not None and row.get('instrumentation_exit_code') == 0 and device.is_file():
            if json.loads(device.read_text()) != row['observed']:
                raise ValueError('Collected device record differs from controller')
            selected[row['variant']] = row
    attempt = 1
    while (executions / f'{args.run}-continuation-{attempt}-provenance').exists():
        attempt += 1
    run_name = f'{args.run}-continuation-{attempt}'
    # The historical collector creates its own run directory, so auxiliary records
    # live alongside it until the first invocation creates that directory.
    provenance = executions / f'{run_name}-provenance'
    provenance.mkdir(exist_ok=False)
    if results.exists():
        shutil.copyfile(results, provenance / 'previous-results.json')
    record = {'started_utc': datetime.now(timezone.utc).isoformat(),
              'collector_sha256': hashlib.sha256((root / 'android/scripts/run_android.py').read_bytes()).hexdigest(),
              'continuation_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'retained_conditions': list(selected), 'resumed_conditions': [], 'relocated_partial': []}
    def save_record():
        (provenance / 'continuation.json').write_text(json.dumps(record, indent=2) + '\n')
    save_record()
    for variant in expected:
        if variant in selected:
            continue
        old = view / variant
        if old.exists():
            destination = provenance / ('interrupted-' + variant)
            hashes = {str(p.relative_to(old)): hashlib.sha256(p.read_bytes()).hexdigest()
                      for p in old.rglob('*') if p.is_file()}
            old.rename(destination)
            record['relocated_partial'].append({'from': str(old), 'to': str(destination), 'sha256': hashes})
            save_record()
        # One condition per exclusive attempt directory prevents a later transport
        # interruption from invalidating completed earlier conditions.
        variant_run = run_name + '-' + variant
        command = [str(root / 'hand/.venv/bin/python'), str(root / 'android/scripts/run_android.py'),
                   '--experiment', args.experiment, '--run', variant_run, '--variants', variant]
        print('START', args.experiment, args.run, variant, flush=True)
        process = subprocess.run(command)
        source = executions / variant_run
        if process.returncode:
            raise SystemExit(process.returncode)
        observed = json.loads((source / 'results.json').read_text())
        if len(observed) != 1 or observed[0]['variant'] != variant:
            raise ValueError('Wrong collector condition')
        row = observed[0]
        # Failed transport is retained in its attempt, never promoted as complete.
        if row.get('observed') is None or row.get('instrumentation_exit_code') != 0:
            record['failed_transport_attempt'] = str(source)
            save_record()
            raise ValueError('Collector did not retrieve complete device evidence')
        shutil.copytree(source / variant, view / variant)
        copied = {str(p.relative_to(view / variant)): hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in (view / variant).rglob('*') if p.is_file()}
        record['resumed_conditions'].append({'variant': variant, 'source': str(source / variant),
                                             'analysis_view': str(view / variant), 'sha256': copied,
                                             'collector_command': command})
        selected[variant] = row
        results.write_text(json.dumps([selected[v] for v in expected if v in selected], indent=2) + '\n')
        save_record()
        print('RETAINED', args.experiment, args.run, variant, flush=True)
    record['completed_utc'] = datetime.now(timezone.utc).isoformat()
    record['status'] = 'COMPLETE_TRANSPORT_COLLECTION_REQUIRES_SCIENTIFIC_AUDIT'
    save_record()


if __name__ == '__main__':
    main()
