#!/usr/bin/env python3
"""Prepare a fresh external E4/E5 replay directory without running experiments."""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

SNAPSHOT = 'sources/metadata-contract-e2e-20261004T030536Z'
ROOT_SCRIPTS = (
    'common.py', 'external_validation.py', 'summarize_e4.py',
    'summarize_e5.py', 'codegen_one.py',
)
E5_SCRIPTS = ('preflight.py', 'evaluate_preflight.py')
RUNNERS = ('run_e4.py', 'run_e5_incremental.py')


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo-root', required=True, type=Path)
    parser.add_argument('--output-root', required=True, type=Path,
                        help='New directory outside the source checkout; must not exist.')
    args = parser.parse_args()
    repo = args.repo_root.resolve()
    output = args.output_root.resolve()
    source = repo / SNAPSHOT
    bundle = Path(__file__).resolve().parent
    if output == repo or repo in output.parents:
        parser.error('--output-root must be outside the source checkout')
    if output.exists():
        parser.error('--output-root already exists; use a fresh directory')
    required = ([source / 'scripts' / name for name in ROOT_SCRIPTS]
                + [source / 'E5' / name for name in E5_SCRIPTS]
                + [bundle / name for name in RUNNERS]
                + [source / 'E4/protocol' / name for name in (
                    'candidates.json', 'prior-exclusions.json', 'contracts.json',
                    'requirements.lock', 'PREVALIDATION_PROTOCOL.md',
                    'scripts/check_model.py', 'scripts/inspect_suite.py',
                    'scripts/suite_static.py', 'scripts/codegen_one.py')])
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        parser.error('Required source files are missing: ' + ', '.join(missing))
    if shutil.which('git') is None:
        parser.error('git is required for the current local protocol freeze')
    commit = subprocess.run(['git', '-C', str(repo), 'rev-parse', 'HEAD'],
                            capture_output=True, text=True, check=True).stdout.strip()

    # Creating this directory is exclusive. Existing experiment evidence is never reused.
    output.mkdir(parents=True, exist_ok=False)
    (output / 'scripts').mkdir()
    (output / 'logs').mkdir()
    provenance = []

    def copy_file(origin: Path, target: Path) -> None:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(origin, target)
        if digest(origin) != digest(target):
            raise RuntimeError(f'Copy integrity failure: {origin}')
        provenance.append({'file': str(target.relative_to(output)),
                           'source': str(origin), 'sha256': digest(target),
                           'byte_identical': True})

    for name in ROOT_SCRIPTS:
        copy_file(source / 'scripts' / name, output / 'scripts' / name)
    for name in E5_SCRIPTS:
        copy_file(source / 'E5' / name, output / 'scripts' / name)
    for name in RUNNERS:
        copy_file(bundle / name, output / name)
    protocol = output / 'E4/protocol'
    for origin in sorted((source / 'E4/protocol').rglob('*')):
        relative = origin.relative_to(source / 'E4/protocol')
        if '.git' in relative.parts or '__pycache__' in relative.parts:
            continue
        if origin.is_file():
            copy_file(origin, protocol / relative)
    for reserved in ('FROZEN_FILES.json', 'REPLAY_CONTEXT.json'):
        if (protocol / reserved).exists():
            raise RuntimeError(f'Snapshot unexpectedly includes reserved generated file: {reserved}')
    created = datetime.datetime.now(datetime.timezone.utc).isoformat()
    save(protocol / 'REPLAY_CONTEXT.json', {
        'created_utc': created,
        'purpose': 'Fresh repeat of historical candidate list and checker source',
        'historical_candidate_results_already_known': True,
        'new_blinded_external_validation': False,
        'historical_freeze_commit_recreated': False,
        'source_repository_commit': commit,
        'source_protocol': str(source / 'E4/protocol'),
        'protocol_interpretation': (
            'Historical no-prior-inspection statements describe the original experiment. '
            'This is a current repeat after publication of the results.'),
    })
    (protocol / '.gitignore').write_text('checks/\n__pycache__/\n*.pyc\n', encoding='utf-8')
    hashes = {str(path.relative_to(protocol)): digest(path)
              for path in sorted(protocol.rglob('*')) if path.is_file()}
    save(protocol / 'FROZEN_FILES.json', hashes)
    commands = [
        ['git', 'init'], ['git', 'add', '.'],
        ['git', '-c', 'user.name=Reproduction audit',
         '-c', 'user.email=repro@local.invalid', '-c', 'commit.gpgsign=false',
         'commit', '-m', 'Freeze current repeat inputs; historical results already known'],
    ]
    for index, command in enumerate(commands):
        result = subprocess.run(command, cwd=protocol, capture_output=True, text=True)
        prefix = output / 'E4/freeze-logs' / str(index)
        prefix.parent.mkdir(parents=True, exist_ok=True)
        prefix.with_suffix('.stdout').write_text(result.stdout, encoding='utf-8')
        prefix.with_suffix('.stderr').write_text(result.stderr, encoding='utf-8')
        save(prefix.with_suffix('.command.json'), {
            'command': command, 'cwd': str(protocol), 'exit_code': result.returncode})
        if result.returncode:
            raise RuntimeError(f'Protocol freeze failed; inspect {prefix}.stderr')
    frozen_commit = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=protocol,
                                   capture_output=True, text=True, check=True).stdout.strip()
    freeze = {
        'git_commit': frozen_commit,
        'created_utc': created,
        'frozen_files_sha256': digest(protocol / 'FROZEN_FILES.json'),
        'protocol_sha256': digest(protocol / 'PREVALIDATION_PROTOCOL.md'),
        'candidate_sha256': digest(protocol / 'candidates.json'),
        'external_downloads_started': False,
        'status': 'CURRENT_REPRODUCTION_FREEZE_HISTORICAL_RESULTS_KNOWN',
        'historical_freeze_commit_recreated': False,
    }
    save(output / 'E4/prevalidation-freeze.json', freeze)
    save(output / 'source-provenance.json', provenance)
    save(output / 'bootstrap-context.json', {
        'source_repository': str(repo), 'source_repository_commit': commit,
        'snapshot': SNAPSHOT, 'output_root': str(output),
        'bootstrap_sha256': digest(Path(__file__).resolve()),
        'setup_only': True, 'network_requests_issued': 0,
        'download_concurrency': 2,
        'required_shared_support_root': '/workspace/hand-contract-repro',
        'required_base_suite_root': str(output.parent / 'metadata-contract-paper'),
        'default_Android_root': str(output.parent / 'repro-android'),
    })
    print(json.dumps({'output_root': str(output), 'protocol_commit': frozen_commit,
                      'copied_source_files': len(provenance), 'setup_only': True}, indent=2))


if __name__ == '__main__':
    main()
