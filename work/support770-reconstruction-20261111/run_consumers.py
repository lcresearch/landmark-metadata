"""Collect one invocation per built consumer; scientific FAIL is never retried."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile

SOURCE = Path(__file__).resolve().parent


def extract_device(archive_path, destination):
    destination.mkdir()
    with tarfile.open(archive_path) as archive:
        for member in archive.getmembers():
            if member.isdir(): continue
            relative = Path(member.name.removeprefix('./'))
            if not member.isfile() or relative.is_absolute() or '..' in relative.parts:
                raise ValueError('Unexpected device archive member')
            path = destination / relative; path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(archive.extractfile(member).read())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    destination = root / 'executions'; destination.mkdir(exist_ok=False)
    shutil.copytree(SOURCE, root / 'execution-source')
    if json.loads((root / 'boot/readiness.json').read_text())['status'] != 'PASS':
        raise ValueError('Device not ready')
    builds = json.loads((root / 'build-results.json').read_text())
    adb = root / 'sdk/platform-tools/adb'
    prefix = [str(adb), '-s', 'emulator-5556']
    results = []
    for build in builds:
        consumer = build['consumer']
        folder = destination / consumer; folder.mkdir()
        record = {'consumer': consumer, 'build': build, 'scientific_status': 'NOT_REACHED'}
        package = build['package']
        stop_remaining = False

        def command(name, arguments, timeout=90):
            output = folder / name
            result = subprocess.run([sys.executable, '-B', str(SOURCE / 'record_command.py'),
                '--output', str(output), '--cwd', str(root), '--timeout', str(timeout),
                '--', *map(str, arguments)])
            if result.returncode:
                raise RuntimeError(f'{name} transport failed; retained without inference retry')
            return output

        try:
            apk = root / 'build' / consumer / 'consumer.apk'
            if build['status'] != 'PASS' or hashlib.sha256(apk.read_bytes()).hexdigest() != build['apk_sha256']:
                raise ValueError('Build/APK identity invalid')
            installed = command('install', [*prefix, 'install', apk], 180)
            if b'Success' not in (installed / 'stdout').read_bytes():
                raise RuntimeError('Installation did not report Success')
            command('instrumentation', [*prefix, 'shell', 'am', 'instrument', '-w',
                package + '/org.example.support770.' + build['instrument']], 300)
            command('logcat', [*prefix, 'logcat', '-d', '-v', 'threadtime', 'tflite:I', 'AndroidRuntime:E', '*:S'])
            archive_dir = command('collect', [*prefix, 'exec-out', 'run-as', package,
                'tar', '-C', 'files/evidence', '-cf', '-', '.'])
            device = folder / 'device'
            extract_device(archive_dir / 'stdout', device)
            observed = json.loads((device / 'result.json').read_text())
            record.update(collection_status='PASS', scientific_status=observed.get('scientific_status'),
                          observed=observed)
        except Exception as exc:
            record.update(collection_status='FAIL', error=repr(exc))
            # Killing a timed-out host adb process does not stop device inference.
            # Stop this owned package before another consumer can start; never rerun it.
            try:
                command('stop-incomplete', [*prefix, 'shell', 'am', 'force-stop', package], 30)
                record['incomplete_package_stopped'] = True
            except Exception as stop_error:
                record['stop_error'] = repr(stop_error)
                stop_remaining = True
            try:
                partial = command('collect-incomplete', [*prefix, 'exec-out', 'run-as', package,
                    'tar', '-C', 'files/evidence', '-cf', '-', '.'])
                extract_device(partial / 'stdout', folder / 'partial-device')
                record['partial_observed'] = json.loads((folder / 'partial-device/result.json').read_text())
            except Exception as partial_error:
                record['partial_collection_error'] = repr(partial_error)
        results.append(record)
        (root / 'runtime-results.json').write_text(json.dumps(results, indent=2) + '\n')
        print(json.dumps({k: record.get(k) for k in ('consumer','collection_status','scientific_status','error')}), flush=True)
        if stop_remaining:
            break
    raise SystemExit(0 if all(r['collection_status'] == 'PASS' for r in results) else 1)


if __name__ == '__main__':
    main()
