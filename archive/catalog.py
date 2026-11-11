"""Verify and restore historical source bytes from the fixed pre-cleanup Git tree."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess

ARCHIVE_COMMIT = 'e9da459f6043684cdecba913c9c711433371909d'


def safe_path(value):
    path = PurePosixPath(value)
    if not value or path.is_absolute() or '..' in path.parts or str(path) != value:
        raise ValueError('Unsafe archive path: ' + value)
    return path


def read_archive(root):
    """Read all catalogued Git blobs; missing history or altered pins fails closed."""
    root = Path(root).resolve()
    manifest = root / 'archive/manifest.json'
    if not manifest.exists():
        return {}
    index = json.loads(manifest.read_text())
    if index['commit'] != ARCHIVE_COMMIT:
        raise ValueError('Unexpected historical archive commit')
    rows = index['files']
    names = [str(safe_path(row['path'])) for row in rows]
    if any((root / name).exists() or (root / name).is_symlink() for name in names):
        raise ValueError('Archived path reintroduced into the working tree')
    if len(names) != len(set(names)):
        raise ValueError('Duplicate archive path')
    historical_paths = subprocess.check_output(
        ['git', '-C', str(root), 'ls-tree', '-r', '--name-only', '-z', ARCHIVE_COMMIT]
    ).decode().split('\0')
    missing = {p for p in historical_paths if p and not (root / p).exists()} - set(names)
    if missing:
        raise ValueError('Uncatalogued historical removals: ' + ', '.join(sorted(missing)))
    requests = ''.join(ARCHIVE_COMMIT + ':' + name + '\n' for name in names)
    result = subprocess.run(['git', '-C', str(root), 'cat-file', '--batch'],
                            input=requests.encode(), capture_output=True, check=True)
    raw, offset, records = result.stdout, 0, {}
    for row in rows:
        end = raw.find(b'\n', offset)
        header = raw[offset:end].split()
        if end < 0 or len(header) != 3 or header[1] != b'blob':
            raise ValueError('Archive Git objects unavailable; use a full clone including ' + ARCHIVE_COMMIT)
        size = int(header[2])
        start = end + 1
        data = raw[start:start + size]
        if (len(data) != size or raw[start + size:start + size + 1] != b'\n'
                or size != row['bytes'] or hashlib.sha256(data).hexdigest() != row['sha256']):
            raise ValueError('Archived bytes differ: ' + row['path'])
        if row.get('replacement'):
            safe_path(row['replacement'])
            if not (root / row['replacement']).is_file():
                raise ValueError('Current replacement is missing: ' + row['replacement'])
        records[row['path']] = data
        offset = start + size + 1
    if offset != len(raw):
        raise ValueError('Unexpected trailing Git data')
    return records


def preserved_bytes(root, relative, records):
    path = Path(root) / relative
    # An archived path must not silently reappear and shadow its recorded bytes.
    if relative in records:
        if path.exists() or path.is_symlink():
            raise ValueError('Archived path reintroduced: ' + relative)
        return records[relative]
    return path.read_bytes()


def restore(root, output):
    """Restore the complete old tree, with original paths, to an absent external folder."""
    import io
    import tarfile
    root, output = Path(root).resolve(), Path(output).resolve()
    if output.exists() or output.is_relative_to(root) or root.is_relative_to(output):
        raise ValueError('Choose an absent external directory')
    read_archive(root)
    payload = subprocess.check_output(['git', '-C', str(root), 'archive', ARCHIVE_COMMIT])
    with tarfile.open(fileobj=io.BytesIO(payload)) as archive:
        for member in archive.getmembers():
            safe_path(member.name.rstrip('/'))
            if not (member.isfile() or member.isdir()):
                raise ValueError('Unexpected archive member type')
        output.mkdir(parents=True)
        archive.extractall(output, filter='data')
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--restore', type=Path, help='Restore the full historical source tree outside this checkout')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    records = read_archive(root)
    if args.restore:
        print(restore(root, args.restore))
    else:
        print(json.dumps({'status': 'PASS', 'archived_files_verified': len(records),
                          'commit': ARCHIVE_COMMIT, 'external_evidence_verified': False}))


if __name__ == '__main__':
    main()
