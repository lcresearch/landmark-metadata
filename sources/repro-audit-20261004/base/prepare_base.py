#!/usr/bin/env python3
"""Prepare fresh base source copies and their pinned Python environment.

By default this installs dependencies only. Model downloads and static execution
require --fetch-and-static. --copy-only validates the source-copy setup offline.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

PYTHON_VERSION = '3.11.16'
KNOWN_UNAVAILABLE = {
    'mobilenet': 'https://storage.googleapis.com/mediapipe-models/image_classifier/mobilenet_v2/float32/1/mobilenet_v2.tflite',
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')


def parse_lock(path: Path) -> dict[str, str]:
    packages = {}
    for line in path.read_text(encoding='utf-8').splitlines():
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        match = re.fullmatch(r'([A-Za-z0-9_.-]+)==([^;\s]+)', line.strip())
        if not match:
            raise ValueError(f'Expected an exact package==version pin in {path}: {line!r}')
        package, version = match.groups()
        if any(character in version for character in '*<>=@'):
            raise ValueError(f'Dependency is not pinned to one exact version: {line!r}')
        canonical = re.sub(r'[-_.]+', '-', package).lower()
        if canonical in packages:
            raise ValueError(f'Duplicate dependency in {path}: {package}')
        packages[canonical] = version
    if not packages:
        raise ValueError(f'Empty dependency lock: {path}')
    return packages


def validate_downloads(corpus: Path, expected_hashes: set[str]) -> dict:
    downloads = json.loads((corpus / 'results/downloads.json').read_text())
    components = json.loads((corpus / 'results/components.json').read_text())
    targets = json.loads((corpus / 'protocol.json').read_text())['targets']
    if not isinstance(downloads, list) or not downloads:
        raise RuntimeError('Download records are empty; static processing is blocked')
    expected_targets = {(row['id'], row['url']) for row in targets}
    observed_targets = {(row.get('id'), row.get('url')) for row in downloads}
    errors = []
    known_404 = []
    successes = []
    if observed_targets != expected_targets or len(downloads) != len(targets):
        errors.append({'error': 'Downloaded target identities/count do not match the fixed protocol'})
    for row in downloads:
        if 'error' in row:
            known = (KNOWN_UNAVAILABLE.get(row.get('id')) == row.get('url')
                     and re.search(r'\bHTTPError 404\b', str(row['error'])) is not None)
            (known_404 if known else errors).append({
                'id': row.get('id'), 'url': row.get('url'), 'error': row['error']})
            continue
        if row.get('status') != 200 or not row.get('components'):
            errors.append({'id': row.get('id'), 'error': 'No HTTP 200 model components'})
            continue
        try:
            path = (corpus / row['path']).resolve()
            if not path.is_relative_to(corpus):
                raise RuntimeError('Artifact path escapes corpus root')
            if path.stat().st_size != row['bytes'] or sha(path) != row['sha256']:
                raise RuntimeError('Downloaded artifact length/hash mismatch')
            successes.append(row['id'])
        except (OSError, KeyError, RuntimeError) as error:
            errors.append({'id': row.get('id'), 'error': str(error)})
    component_hashes = set()
    for component in components:
        try:
            path = (corpus / component['path']).resolve()
            if not path.is_relative_to(corpus):
                raise RuntimeError('Component path escapes corpus root')
            if path.stat().st_size != component['bytes'] or sha(path) != component['sha256']:
                raise RuntimeError('Component length/hash mismatch')
            component_hashes.add(component['sha256'])
        except (OSError, KeyError, RuntimeError) as error:
            errors.append({'component': component.get('sha256'), 'error': str(error)})
    comparison = component_hashes == expected_hashes
    report = {
        'target_count': len(downloads), 'successful_targets': successes,
        'known_fixed_URL_404s': known_404, 'unexpected_failures': errors,
        'verified_component_count': len(component_hashes),
        'historical_component_hash_set_matches': comparison,
        'missing_historical_hashes': sorted(expected_hashes - component_hashes),
        'new_component_hashes': sorted(component_hashes - expected_hashes),
        'ready_for_static': bool(successes and components and not errors and comparison),
    }
    save(corpus / 'results/fetch-validation.json', report)
    if not report['ready_for_static']:
        raise RuntimeError('Fetch is incomplete, blocked or differs from historical artifact identities; inspect results/fetch-validation.json')
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo-root', required=True, type=Path)
    parser.add_argument('--hand-root', type=Path, default=Path('/workspace/hand-contract-repro'))
    parser.add_argument('--corpus-root', type=Path, default=Path('/workspace/metadata-contract-paper'))
    parser.add_argument('--python', dest='python_executable', type=Path,
                        help='Existing Python 3.11.16 executable; no interpreter download is performed')
    parser.add_argument('--uv', default=shutil.which('uv'), help='Existing uv executable')
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--copy-only', action='store_true', help='Offline source-copy validation only; do not create a venv')
    mode.add_argument('--fetch-and-static', action='store_true', help='After installation, fetch fixed targets, inspect and run suite_static')
    args = parser.parse_args()
    repo, hand, corpus = (path.resolve() for path in (args.repo_root, args.hand_root, args.corpus_root))
    sources = [(repo / 'sources/hand-contract-repro', hand),
               (repo / 'sources/metadata-contract-paper', corpus)]
    for target in (hand, corpus):
        if target == repo or repo in target.parents:
            parser.error('Output roots must be outside the source checkout')
        if target.exists():
            parser.error(f'Output root already exists; choose fresh roots: {target}')
    if hand == corpus or hand in corpus.parents or corpus in hand.parents:
        parser.error('Output roots must be distinct and must not contain each other')
    for source, _ in sources:
        if not (source / 'requirements.lock').is_file() or not (source / 'scripts').is_dir():
            parser.error(f'Source snapshot unavailable: {source}')
        if any(path.is_symlink() for path in source.rglob('*')):
            parser.error(f'Source snapshot contains a symlink: {source}')
    hand_lock = parse_lock(sources[0][0] / 'requirements.lock')
    if hand_lock != parse_lock(sources[1][0] / 'requirements.lock'):
        parser.error('The two snapshots require different locks; one shared environment is not justified')
    exclusion_source = repo / 'sources/metadata-contract-e2e-20261004T030536Z/E4/protocol/prior-exclusions.json'
    if args.fetch_and_static and not exclusion_source.is_file():
        parser.error('Historical component identity record is required for --fetch-and-static')
    interpreter_version = None
    if not args.copy_only:
        if not args.python_executable or not args.python_executable.is_file():
            parser.error('--python must name an existing Python 3.11.16 executable')
        if not args.uv or not Path(args.uv).is_file():
            parser.error('--uv must name an existing uv executable')
        args.python_executable = args.python_executable.resolve()
        interpreter_version = subprocess.check_output(
            [str(args.python_executable), '-I', '-c', 'import platform; print(platform.python_version())'],
            text=True).strip()
        if interpreter_version != PYTHON_VERSION:
            parser.error(f'Expected Python {PYTHON_VERSION}, found {interpreter_version}')

    # All guards run before either output root is created.
    hand.mkdir(parents=True, exist_ok=False)
    corpus.mkdir(parents=True, exist_ok=False)
    provenance = []
    for source, target in sources:
        for origin in sorted(source.rglob('*')):
            relative = origin.relative_to(source)
            if '.git' in relative.parts or '__pycache__' in relative.parts or not origin.is_file():
                continue
            destination = target / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(origin, destination)
            if sha(origin) != sha(destination):
                raise RuntimeError(f'Source copy hash mismatch: {origin}')
            provenance.append({'source': str(origin), 'destination': str(destination), 'sha256': sha(destination)})
        for name in ('results', 'logs'):
            (target / name).mkdir(exist_ok=True)
    record_dir = hand / 'setup-base'
    record = {
        'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'source_repo': str(repo), 'hand_root': str(hand), 'corpus_root': str(corpus),
        'mode': 'copy-only' if args.copy_only else 'fetch-and-static' if args.fetch_and_static else 'setup-only',
        'python_executable': str(args.python_executable) if args.python_executable else None,
        'python_version': interpreter_version, 'exact_locked_packages': hand_lock,
        'source_files': provenance, 'commands': [], 'status': 'SOURCE_COPIED',
    }
    save(record_dir / 'setup.json', record)
    if args.copy_only:
        record['status'] = 'SOURCE_COPY_ONLY_NO_ENVIRONMENT'
        save(record_dir / 'setup.json', record)
        print(json.dumps({'status': record['status'], 'source_files': len(provenance), 'record': str(record_dir / 'setup.json')}, indent=2))
        return

    env = os.environ.copy()
    env.update(UV_CACHE_DIR=str(record_dir / 'uv-cache'), UV_PYTHON_DOWNLOADS='never',
               PYTHONDONTWRITEBYTECODE='1', PYTHONOPTIMIZE='0',
               OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', HAND_REPRO_ROOT=str(hand))

    def run(label: str, command: list[str], cwd: Path = hand) -> subprocess.CompletedProcess:
        result = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True)
        (record_dir / f'{label}.stdout').write_text(result.stdout, encoding='utf-8')
        (record_dir / f'{label}.stderr').write_text(result.stderr, encoding='utf-8')
        record['commands'].append({'label': label, 'command': command, 'cwd': str(cwd), 'exit_code': result.returncode})
        save(record_dir / 'setup.json', record)
        if result.returncode:
            raise RuntimeError(f'{label} failed with exit {result.returncode}; see {record_dir}/{label}.stderr')
        return result

    try:
        run('venv', [str(args.uv), 'venv', '--python', str(args.python_executable), str(hand / '.venv')])
        python = str(hand / '.venv/bin/python')
        run('install-lock', [str(args.uv), 'pip', 'install', '--python', python, '--no-deps', '--requirement', str(hand / 'requirements.lock')])
        run('pip-check', [str(args.uv), 'pip', 'check', '--python', python])
        installed = run('verify-lock', [python, '-c',
            'import importlib.metadata as m,json,sys; p=json.loads(sys.argv[1]); print(json.dumps({n:m.version(n) for n in p}))', json.dumps(hand_lock)])
        observed = json.loads(installed.stdout)
        if observed != hand_lock:
            raise RuntimeError('Installed versions differ from exact dependency lock')
        record['observed_packages'] = observed
        record['status'] = 'PYTHON_ENVIRONMENT_READY'
        save(record_dir / 'setup.json', record)
        if args.fetch_and_static:
            run('fetch-suite', [python, str(corpus / 'scripts/fetch_suite.py')], cwd=corpus)
            expected = {row['component_sha256'] for row in json.loads(exclusion_source.read_text())}
            record['fetch_validation'] = validate_downloads(corpus, expected)
            for name in ('inspect_suite', 'suite_static'):
                run(name, [python, str(corpus / 'scripts' / (name + '.py'))], cwd=corpus)
            static = json.loads((corpus / 'results/static-suite.json').read_text())
            if not static or len(static) != len(expected):
                raise RuntimeError('Static report is empty or does not cover recovered components')
            record['status'] = 'FETCH_AND_STATIC_COMPLETED'
        save(record_dir / 'setup.json', record)
    except Exception as error:
        record['status'] = 'FAILED'
        record['error'] = str(error)
        save(record_dir / 'setup.json', record)
        raise
    print(json.dumps({'status': record['status'], 'record': str(record_dir / 'setup.json')}, indent=2))


if __name__ == '__main__':
    main()
