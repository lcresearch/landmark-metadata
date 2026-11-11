"""Read back saved focal evidence into a fresh external directory; no inference.

The preserved Android audits write beside their inputs. Exact, pinned source
copies below redirect only their root/report locations and preservation subprocess.
Both original/adapted source identities and the complete patches are retained.
"""
import argparse
from datetime import datetime, timezone
import difflib
import hashlib
import json
import os
from pathlib import Path
import subprocess

REPO = Path(__file__).resolve().parents[2]
PINS = {
    'audit_android_results.py': 'b78a7a2084fd87b7dd53311028e7577dc2e07d10185b6e7b8f2551e9b7f7f107',
    'audit_model_preservation.py': 'bd8d22a979c429d147ad2d7e0ddbd91bf879a57087cef2289d6c87011ee00808',
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ['run', 'inputs', 'references', 'python', 'output']:
        parser.add_argument('--' + name, type=Path, required=True)
    args = parser.parse_args()
    run, inputs, refs, output = [p.resolve() for p in
                                [args.run, args.inputs, args.references, args.output]]
    if output.exists() or any(output.is_relative_to(p) for p in [REPO, run, inputs, refs]):
        raise ValueError('Choose a fresh output outside the checkout and all evidence inputs')
    sources = {}
    for name, pin in PINS.items():
        source = (REPO / 'sources/repro-audit-20261004/android' / name).read_bytes()
        if sha(source) != pin:
            raise ValueError('Preserved audit source differs: ' + name)
        sources[name] = source.decode()
    receipt = json.loads((REPO / 'work/focal-rerun-20261110/delivery-record.json').read_text())
    # Bind the supplied saved records to the already published receipt.
    records = {}
    for row in receipt['selected_external_records']:
        relative = Path(row['path']).relative_to(receipt['run_root'])
        path = run / relative
        if path.stat().st_size != row['bytes'] or sha(path.read_bytes()) != row['sha256']:
            raise ValueError('Saved record differs from receipt: ' + str(relative))
        records[str(path)] = row['sha256']
    output.mkdir(parents=True, exist_ok=False)
    report = {'started_utc': datetime.now(timezone.utc).isoformat(),
              'kind': 'SAVED_BYTE_RECHECK_NO_NEW_INFERENCE', 'adaptations': [],
              'commands': [], 'human_verification': False}
    for name, before in sources.items():
        after = before.replace('ROOT=pathlib.Path(__file__).resolve().parents[1]',
                               'ROOT=pathlib.Path(' + repr(str(run / 'android')) + ')')
        for target in ['audit-results.json', 'model-preservation-audit.json']:
            after = after.replace("ROOT/'" + target + "'",
                                  'pathlib.Path(' + repr(str(output / target)) + ')')
        after = after.replace("ROOT/'scripts/audit_model_preservation.py'",
                              'pathlib.Path(' + repr(str(output / 'audit_model_preservation.py')) + ')')
        if after == before:
            raise ValueError('Audit redirection was not applied')
        (output / name).write_text(after)
        (output / (name + '.patch')).write_text(''.join(difflib.unified_diff(
            before.splitlines(True), after.splitlines(True), fromfile='preserved/' + name,
            tofile='readback/' + name)))
        report['adaptations'].append({'name': name, 'before_sha256': sha(before.encode()),
                                       'after_sha256': sha(after.encode())})
    commands = [
        ('android', [str(args.python), str(output / 'audit_android_results.py')]),
        ('p2', [str(args.python), str(REPO / 'work/review-fixes-20261021/verify_p2_records.py'),
                '--round-root', str(run / 'round'), '--output', str(output / 'p2.json')]),
        ('p3', [str(args.python), str(REPO / 'work/focal-rerun-20261110/analyze_p3_core.py'),
                '--inputs', str(inputs), '--references', str(refs), '--output', str(output / 'p3')]),
    ]
    for label, command in commands:
        result = subprocess.run(command, capture_output=True,
                                env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONOPTIMIZE='0'))
        (output / (label + '.stdout')).write_bytes(result.stdout)
        (output / (label + '.stderr')).write_bytes(result.stderr)
        report['commands'].append({'label': label, 'command': command, 'exit_code': result.returncode})
        (output / 'recheck.json').write_text(json.dumps(report, indent=2) + '\n')
        result.check_returncode()
    for path, pin in records.items():
        if sha(Path(path).read_bytes()) != pin:
            raise ValueError('Original saved record changed during readback: ' + path)
    report.update(status='PASS', completed_utc=datetime.now(timezone.utc).isoformat(),
                  original_selected_records_unchanged=len(records))
    (output / 'recheck.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
