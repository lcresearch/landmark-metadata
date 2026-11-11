"""Install isolated Python 3.11.16 and the exact eleven pinned wheel bytes."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import urllib.request
import zipfile

REPO = Path(__file__).resolve().parents[2]
UV_URL = 'https://files.pythonhosted.org/packages/b9/93/0e053a2ca4523ee9825ccbedeb7121470d0a188933f11688b6d90d7f5c08/uv-0.13.7-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl'
UV_SHA256 = '2c9bdc4a872b60a93c5f26c0791089ea11585a4f9d3b3c017d78eb8487505e25'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', required=True, type=Path)
    args = ap.parse_args()
    root = args.root.resolve()
    if root.is_relative_to(REPO) or not (root / 'PROTOCOL.md').is_file():
        raise ValueError('Expected initialized external run')
    tooling = root / 'python-setup'
    tooling.mkdir(exist_ok=False)
    records = []
    def download(url, path, expected):
        with urllib.request.urlopen(url, timeout=180) as response:
            data = response.read()
        with path.open('xb') as out:
            out.write(data)
        actual = sha(data)
        records.append({'url': url, 'path': str(path), 'expected_sha256': expected,
                        'actual_sha256': actual, 'bytes': len(data), 'matches': actual == expected})
        (tooling / 'downloads.json').write_text(json.dumps(records, indent=2) + '\n')
        if actual != expected:
            raise ValueError('Downloaded bytes differ: ' + path.name)
        return data
    wheel = tooling / 'uv.whl'
    download(UV_URL, wheel, UV_SHA256)
    with zipfile.ZipFile(wheel) as archive:
        names = [name for name in archive.namelist() if name.endswith('.data/scripts/uv')]
        if len(names) != 1:
            raise ValueError('Unexpected uv wheel executable inventory')
        uv = tooling / 'uv'
        uv.write_bytes(archive.read(names[0]))
        uv.chmod(0o755)
    env = dict(os.environ, UV_PYTHON_INSTALL_DIR=str(tooling / 'python'),
               UV_PYTHON_BIN_DIR=str(tooling / 'bin'), UV_CACHE_DIR=str(tooling / 'cache'),
               UV_NO_MODIFY_PATH='1', PYTHONDONTWRITEBYTECODE='1', PYTHONOPTIMIZE='0')
    calls = []
    def run(label, command):
        process = subprocess.run(command, env=env, capture_output=True, text=True)
        (tooling / (label + '.stdout')).write_text(process.stdout)
        (tooling / (label + '.stderr')).write_text(process.stderr)
        calls.append({'label': label, 'command': command, 'exit_code': process.returncode})
        (tooling / 'commands.json').write_text(json.dumps(calls, indent=2) + '\n')
        process.check_returncode()
        return process.stdout.strip()
    run('install-python', [str(uv), '--no-config', 'python', 'install', '3.11.16'])
    python = run('find-python', [str(uv), '--no-config', 'python', 'find', '--managed-python', '3.11.16'])
    if run('python-version', [python, '-c', 'import platform; print(platform.python_version())']) != '3.11.16':
        raise ValueError('Wrong Python version')
    run('venv', [str(uv), '--no-config', 'venv', '--python', python, str(root / 'hand/.venv')])
    wheels = tooling / 'wheels'
    wheels.mkdir()
    lock = json.loads((REPO / 'docs/reproduction/toolchain.json').read_text())
    requirements = []
    for row in lock['python_wheels']:
        filename = row['filename']
        package, version = filename.split('-')[:2]
        url = f'https://pypi.org/pypi/{package}/{version}/json'
        with urllib.request.urlopen(url, timeout=60) as response:
            metadata = response.read()
        (tooling / (package + '-pypi.json')).write_bytes(metadata)
        candidates = [item for item in json.loads(metadata)['urls'] if item['filename'] == filename]
        expected = row['local']['expected_sha256']
        if len(candidates) != 1 or candidates[0]['digests']['sha256'] != expected:
            raise ValueError('Pinned wheel unavailable or changed: ' + filename)
        download(candidates[0]['url'], wheels / filename, expected)
        requirements.append(f'{package}=={version} --hash=sha256:{expected}')
    required = tooling / 'requirements-hashed.txt'
    required.write_text('\n'.join(requirements) + '\n')
    executable = str(root / 'hand/.venv/bin/python')
    run('install-wheels', [str(uv), '--no-config', 'pip', 'install', '--python', executable,
        '--no-index', '--find-links', str(wheels), '--no-deps', '--require-hashes', '-r', str(required)])
    run('pip-check', [str(uv), '--no-config', 'pip', 'check', '--python', executable])
    run('imports', [executable, '-c', 'import numpy, flatbuffers, tflite_support; from tensorflow_lite_support.metadata import schema_py_generated; print("imports OK")'])
    run('versions', [executable, '-c', 'import importlib.metadata as m,json,sys; print(json.dumps({"python":sys.version,"packages":{d.metadata["Name"]:d.version for d in m.distributions()}},indent=2))'])
    print('Verified Python 3.11.16 and installed 11 exact historical wheels; imports pass')


if __name__ == '__main__':
    main()
