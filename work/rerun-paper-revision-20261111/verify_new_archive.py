"""Verify the November archive and every member against its published receipt.

Read-only: no extraction, experiment execution, or evidence mutation. Save the
verified embedded manifest and a new readback receipt outside the source tree.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import tarfile

REPO = Path(__file__).resolve().parents[2]


class DigestReader:
    def __init__(self, stream):
        self.stream = stream
        self.digest = hashlib.sha256()

    def read(self, size=-1):
        data = self.stream.read(size)
        self.digest.update(data)
        return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    target, output = args.archive.resolve(), args.output.resolve()
    receipt = json.loads((REPO / 'work/focal-rerun-20261110/delivery-record.json').read_text())
    pin = receipt['archive']
    if output.exists() or output.is_relative_to(REPO) or output.is_relative_to(receipt['run_root']):
        raise ValueError('Choose a fresh external readback directory')
    if target.stat().st_size != pin['bytes']:
        raise ValueError('Archive size differs from published receipt')
    observed, manifest_bytes = {}, None
    with target.open('rb') as raw:
        reader = DigestReader(raw)
        with tarfile.open(fileobj=reader, mode='r|gz') as archive:
            for member in archive:
                if not member.isfile() or member.name in observed:
                    raise ValueError('Non-file or duplicate archive member')
                digest = hashlib.sha256()
                with archive.extractfile(member) as stream:
                    if member.name == 'MANIFEST.json':
                        if member.size > 5_000_000:
                            raise ValueError('Unexpected manifest size')
                        manifest_bytes = stream.read()
                        digest.update(manifest_bytes)
                    else:
                        for block in iter(lambda: stream.read(1024 * 1024), b''):
                            digest.update(block)
                observed[member.name] = {'bytes': member.size, 'sha256': digest.hexdigest()}
        while reader.read(1024 * 1024):
            pass
        archive_sha256 = reader.digest.hexdigest()
    if archive_sha256 != pin['sha256']:
        raise ValueError('Archive digest differs from published receipt')
    if manifest_bytes is None or hashlib.sha256(manifest_bytes).hexdigest() != pin['manifest_sha256']:
        raise ValueError('Manifest differs from published receipt')
    manifest = json.loads(manifest_bytes)
    expected = {row['path']: {'bytes': row['bytes'], 'sha256': row['sha256']} for row in manifest['files']}
    if len(expected) != len(manifest['files']):
        raise ValueError('Duplicate manifest entry')
    expected['MANIFEST.json'] = {'bytes': len(manifest_bytes), 'sha256': pin['manifest_sha256']}
    if observed != expected or len(observed) != pin['verified_members']:
        raise ValueError('Archive member inventory or payload digest mismatch')
    output.mkdir(parents=True, exist_ok=False)
    (output / 'archive-manifest.json').write_bytes(manifest_bytes)
    report = {'status': 'PASS', 'archive': str(target), 'sha256': archive_sha256,
              'verified_members': len(observed), 'manifest_sha256': pin['manifest_sha256'],
              'completed_utc': datetime.now(timezone.utc).isoformat(),
              'scope': 'Complete saved-archive byte readback, not new model execution or authenticated history.',
              'human_verification': False, 'remote_backup': False}
    (output / 'archive-readback.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
