"""Archive new local evidence, verify every member, and record explicit exclusions.

This makes a local evidence copy, not a remote backup or an offline SDK image.
Stop the emulator and finish all stages before invoking it.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import io
import json
import os
from pathlib import Path
import sys
import tarfile

REPO = Path(__file__).resolve().parents[2]
EXCLUDED_DIRS = {'android/sdk', 'round/P2/sdk', 'hand/.venv', 'hand/toolchains',
                 'python-setup/python', 'python-setup/cache', 'python-setup/bin'}


def digest(stream):
    result = hashlib.sha256()
    for block in iter(lambda: stream.read(1024 * 1024), b''):
        result.update(block)
    return result.hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', required=True, type=Path)
    ap.add_argument('--inputs', required=True, type=Path)
    ap.add_argument('--references', required=True, type=Path)
    ap.add_argument('--archive', required=True, type=Path)
    args = ap.parse_args()
    root, inputs, refs, target = (p.resolve() for p in (args.root, args.inputs, args.references, args.archive))
    partial = target.with_name(target.name + '.partial')
    receipt = target.with_name(target.name + '.json')
    if target.is_relative_to(REPO) or any(target.is_relative_to(p) for p in [root, inputs, refs]):
        raise ValueError('Archive must be outside the repository and selected input trees')
    if any(p.exists() for p in [target, partial, receipt]):
        raise ValueError('Choose fresh archive/receipt names')
    stages = [json.loads(p.read_text()) for p in (root / 'stages').glob('*/command.json')]
    if not stages or any(s.get('status') == 'RUNNING' for s in stages):
        raise ValueError('Stages are absent or still running')
    files, excluded = [], []
    trees = [('run', root), ('recovered-inputs', inputs), ('recovered-references', refs),
             ('rerun-source', Path(__file__).parent)]
    for prefix, tree in trees:
        if not tree.is_dir():
            raise ValueError('Missing input tree: ' + str(tree))
        for current, directories, names in os.walk(tree, followlinks=False):
            parent = Path(current)
            for name in list(directories):
                path = parent / name
                relative = path.relative_to(tree).as_posix()
                if path.is_symlink() or (prefix == 'run' and relative in EXCLUDED_DIRS) or name == '__pycache__':
                    excluded.append({'path': prefix + '/' + relative, 'reason': 'installed runtime/cache, symlink or bytecode'})
                    directories.remove(name)
            for name in names:
                path = parent / name
                relative = path.relative_to(tree).as_posix()
                member = prefix + '/' + relative
                if path.is_symlink() or path.suffix == '.keystore' or name.startswith('adbkey'):
                    excluded.append({'path': member, 'reason': 'symlink or disposable signing/ADB key'})
                    continue
                with path.open('rb') as stream:
                    checksum = digest(stream)
                files.append((path, {'path': member, 'bytes': path.stat().st_size, 'sha256': checksum}))
    files.sort(key=lambda item: item[1]['path'])
    manifest = {'created_utc': datetime.now(timezone.utc).isoformat(),
                'scope': 'New local execution evidence with recovered inputs; not the lost October archive, remote backup, human review, or complete offline environment.',
                'command': sys.argv, 'files': [row for _, row in files], 'excluded': excluded}
    encoded = (json.dumps(manifest, indent=2) + '\n').encode()
    target.parent.mkdir(parents=True, exist_ok=True)
    with partial.open('xb') as output:
        with tarfile.open(fileobj=output, mode='w:gz', compresslevel=1) as archive:
            for path, row in files:
                archive.add(path, arcname=row['path'], recursive=False)
            info = tarfile.TarInfo('MANIFEST.json')
            info.size = len(encoded)
            archive.addfile(info, io.BytesIO(encoded))
    expected = {row['path']: row for _, row in files}
    expected['MANIFEST.json'] = {'bytes': len(encoded), 'sha256': hashlib.sha256(encoded).hexdigest()}
    seen = set()
    with tarfile.open(partial, 'r|gz') as archive:
        for member in archive:
            if not member.isfile() or member.name not in expected or member.name in seen:
                raise ValueError('Unexpected or duplicate archive member: ' + member.name)
            row = expected[member.name]
            with archive.extractfile(member) as stream:
                checksum = digest(stream)
            if member.size != row['bytes'] or checksum != row['sha256']:
                raise ValueError('Archive/member changed during packaging: ' + member.name)
            seen.add(member.name)
    if seen != set(expected):
        raise ValueError('Incomplete archive readback')
    with partial.open('rb') as stream:
        checksum = digest(stream)
    # The destination was absent at preflight; exclusive link also refuses a race.
    os.link(partial, target)
    partial.unlink()
    report = {'status': 'LOCAL_ARCHIVE_MEMBERS_VERIFIED', 'archive': str(target),
              'bytes': target.stat().st_size, 'sha256': checksum,
              'manifest_sha256': hashlib.sha256(encoded).hexdigest(), 'verified_members': len(seen),
              'source_file_count': len(files), 'source_bytes': sum(r['bytes'] for _, r in files),
              'completed_utc': datetime.now(timezone.utc).isoformat(),
              'remote_backup': False, 'historical_evidence_recovered': False}
    with receipt.open('x') as stream:
        json.dump(report, stream, indent=2)
        stream.write('\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
