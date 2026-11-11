"""Record the actual fresh Python distribution and host, without credentials."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess

REPO = Path(__file__).resolve().parents[2]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', required=True, type=Path)
    args = ap.parse_args()
    root = args.root.resolve()
    if root.is_relative_to(REPO) or not (root / 'PROTOCOL.md').is_file():
        raise ValueError('Expected initialized external run')
    output = root / 'provenance/fresh-environment.json'
    if output.exists():
        raise ValueError('Preserve prior environment record')
    def sha(path):
        digest = hashlib.sha256()
        with path.open('rb') as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b''):
                digest.update(block)
        return digest.hexdigest()
    python_tree = root / 'python-setup/python'
    files = [{'path': str(p.relative_to(python_tree)), 'bytes': p.stat().st_size, 'sha256': sha(p)}
             for p in sorted(python_tree.rglob('*')) if p.is_file() and not p.is_symlink()]
    python = root / 'hand/.venv/bin/python'
    observed = subprocess.check_output([str(python), '-c',
        'import sys,platform,json; print(json.dumps({"version":sys.version,"executable":sys.executable,"prefix":sys.prefix,"base_prefix":sys.base_prefix,"libc":platform.libc_ver()}))'], text=True)
    data = {'recorded_utc': datetime.now(timezone.utc).isoformat(),
            'platform': platform.platform(), 'machine': platform.machine(),
            'logical_cpu_count': os.cpu_count(), 'kvm_device_present': Path('/dev/kvm').exists(),
            'python': json.loads(observed), 'python_binary_sha256': sha(python.resolve()),
            'uv_binary_sha256': sha(root / 'python-setup/uv'), 'python_distribution_files': files,
            'scope': 'Observed fresh distribution; no assertion of equality to the unpinned historical Python binary. No credentials/environment variables collected.'}
    with output.open('x') as stream:
        json.dump(data, stream, indent=2)
        stream.write('\n')
    print(json.dumps({'output': str(output), 'python_distribution_files': len(files),
                      'python_binary_sha256': data['python_binary_sha256']}))


if __name__ == '__main__':
    main()
