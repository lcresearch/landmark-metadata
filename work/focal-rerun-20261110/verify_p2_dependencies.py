"""Compare freshly downloaded P2 archives and selected binaries with old pins."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', required=True, type=Path)
    args = ap.parse_args()
    root = args.root.resolve()
    if root.is_relative_to(REPO):
        raise ValueError('Evidence must stay outside the source repository')
    lock = json.loads((REPO / 'docs/reproduction/toolchain.json').read_text())
    rows = [r for r in lock['archive_objects'] if r['source'] == 'p2_downloads']
    rows += lock['selected_java_native_objects']
    mapping = {
        '/workspace/metadata-contract-p2p3-20261004T073824Z': root / 'round',
        '/workspace/metadata-contract-e2e-20261004T030536Z': root / 'android',
        '/workspace/hand-contract-repro': root / 'hand',
    }
    observations = []
    for row in rows:
        old = row['local']
        path = next((new / old['path'][len(prefix) + 1:] for prefix, new in mapping.items()
                     if old['path'].startswith(prefix + '/')), None)
        if path is None:
            raise ValueError('Unmapped dependency: ' + old['path'])
        data = path.read_bytes()
        actual = hashlib.sha256(data).hexdigest()
        observations.append({'path': str(path), 'expected_sha256': old['expected_sha256'],
                             'sha256': actual, 'bytes': len(data),
                             'matches': actual == old['expected_sha256'] and len(data) == old['bytes']})
    report = {'created_utc': datetime.now(timezone.utc).isoformat(),
              'status': 'PASS' if observations and all(r['matches'] for r in observations) else 'FAIL',
              'objects': observations}
    output = root / 'round/P2/prerequisites/dependency-pin-verification.json'
    with output.open('x') as stream:
        json.dump(report, stream, indent=2)
        stream.write('\n')
    print(json.dumps({'status': report['status'], 'objects': len(observations)}))
    if report['status'] != 'PASS':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
