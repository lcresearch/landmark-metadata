"""Read-only verification of pinned historical packages after P2/P3."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def main():
    destination = ROOT / 'verification/protected-evidence-review.json'
    if destination.exists():
        raise SystemExit('Refusing to overwrite a prior verification')
    inputs = json.loads((ROOT / 'INPUTS.json').read_text())
    results = []
    for record in inputs['protected_manifests']:
        manifest = Path(record['path'])
        failures = []
        if digest(manifest) != record['sha256']:
            failures.append('manifest bytes changed')
        count = 0
        for line in manifest.read_text().splitlines():
            if not line.strip():
                continue
            expected, name = line.split(maxsplit=1)
            path = manifest.parent / name.lstrip('*')
            count += 1
            if not path.is_file() or digest(path) != expected:
                failures.append(str(path))
        results.append({'manifest': str(manifest), 'sha256': record['sha256'],
                        'entries_checked': count, 'failures': failures,
                        'status': 'FAIL' if failures else 'PASS'})
    for record in inputs['input_models']:
        matched = digest(Path(record['path'])) == record['sha256']
        results.append({'variant': record['variant'], 'path': record['path'],
                        'sha256': record['sha256'], 'status': 'PASS' if matched else 'FAIL'})
    status = 'PASS' if all(row['status'] == 'PASS' for row in results) else 'FAIL'
    report = {'status': status, 'scope': 'Pinned historical manifest entries and five inputs; no new inference.',
              'results': results}
    destination.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    raise SystemExit(status != 'PASS')


if __name__ == '__main__':
    main()
