"""Index fresh external evidence without copying binary artifacts into Git."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path

EXCLUDED_DIRS = {'.git', '.venv', 'venv', 'sdk', 'toolchains', 'uv-cache',
                 '__pycache__', 'cache', 'wheels', 'android-user'}
EXCLUDED_SUFFIXES = {'.keystore', '.jks', '.pem', '.key', '.p12', '.pfx'}

def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', action='append', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[3]
    output = args.output.resolve()
    if output.is_relative_to(repo) or output.exists():
        raise ValueError('Use a new evidence-index path outside the repository')
    files = []; links = []
    roots = [p.resolve() for p in args.root]
    for root in roots:
        if not root.is_dir() or not root.is_relative_to(Path('/workspace')):
            raise ValueError('Required external /workspace evidence root unavailable: ' + str(root))
        for current, dirs, names in os.walk(root, followlinks=False):
            current = Path(current)
            dirs[:] = sorted(d for d in dirs if d not in EXCLUDED_DIRS)
            if current.name == 'prerequisites' and 'downloads' in dirs:
                dirs.remove('downloads')  # Large tool archives have separately verified lock digests.
            for name in list(dirs):
                path = current / name
                if path.is_symlink():
                    links.append({'path': str(path), 'target': os.readlink(path)})
                    dirs.remove(name)
            for name in sorted(names):
                path = current / name
                if (path.resolve() == output or path.suffix in EXCLUDED_SUFFIXES
                        or name.startswith('.env') or name.startswith('adbkey')
                        or name.startswith('.emulator_console_auth')):
                    continue
                if path.is_symlink():
                    links.append({'path': str(path), 'target': os.readlink(path)})
                elif path.is_file():
                    files.append({'path': str(path), 'bytes': path.stat().st_size, 'sha256': sha(path)})
    if not files:
        raise ValueError('No evidence files were indexed')
    document = {'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                'scope': 'Fresh local evidence inventory; not publication or validation of historical archives.',
                'roots': list(map(str, roots)), 'excluded_directories': sorted(EXCLUDED_DIRS),
                'excluded_key_suffixes': sorted(EXCLUDED_SUFFIXES),
                'other_exclusions': ['prerequisites/downloads tool caches', '.env*', 'adbkey*', '.emulator_console_auth*'],
                'files': files, 'symlinks_not_followed': links}
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('x') as stream:
        json.dump(document, stream, indent=2)
        stream.write('\n')
    print(json.dumps({'files': len(files), 'bytes': sum(f['bytes'] for f in files),
                      'index': str(output), 'index_sha256': sha(output)}, indent=2))

if __name__ == '__main__':
    main()
