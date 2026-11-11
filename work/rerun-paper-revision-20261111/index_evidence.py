"""Index claim-supporting saved bytes; write text identities, never raw payloads.

The embedded manifest must match the published November receipt. Every selected
live file is then independently read and matched to that manifest. Use the
separate archive verifier first to establish the complete archive inventory.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from functools import lru_cache

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from archive.catalog import read_archive

REPO = Path(__file__).resolve().parents[2]
AREA = Path(__file__).resolve().parent
GROUPS = {
    'N0': 'Reported old-material loss, bounded availability search and fresh input recovery',
    'N1': 'Initial protocol, input/source freeze, environment and dependency identities',
    'N2': 'Model/code preservation, actual build artifacts and Android audit',
    'N3': 'E1 preparation, builds, selected primary/replay and actual per-condition invocations',
    'N4': 'E2 preparation, builds, selected primary/replay and actual per-condition invocations',
    'N5': 'Paired Android P2 actual-file reader, public stages and returned-value comparisons',
    'N6': 'Six-input P3 reference core and full positional display comparison',
    'N7': 'Two E1 interruptions, retained attempts, relocation and continuation selection',
    'N8': 'Retained failed setup/analysis and exact-message reader correction',
    'N9': 'Local archive packaging and verified member inventory; no remote deposit',
}


def identity(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return {'bytes': path.stat().st_size, 'sha256': digest.hexdigest()}


@lru_cache(maxsize=None)
def archived_sources(repo):
    return read_archive(repo)


def repository_identity(path):
    """Resolve old source bytes without claiming a Git blob is a working-tree file."""
    relative = path.relative_to(REPO).as_posix()
    archived = archived_sources(REPO)
    if relative in archived:
        data = archived[relative]
        return ({'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()},
                {'verified_from': 'archived_git_object',
                 'revision': json.loads((REPO / 'archive/manifest.json').read_text())['commit']})
    return identity(path), {'verified_from': 'working_tree'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--readback', type=Path, required=True,
                        help='Retained editorial readback directory, containing archive/ and core-readback/')
    parser.add_argument('--output', type=Path, required=True, help='Fresh text index path')
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError('Preserve the prior index; choose a fresh output')
    receipt_path = REPO / 'work/focal-rerun-20261110/delivery-record.json'
    receipt = json.loads(receipt_path.read_text())
    roots = {'run': Path(receipt['run_root']),
             'recovered-inputs': Path('/home/hsz/landmark-evidence/input-recovery-20261110'),
             'recovered-references': Path('/home/hsz/landmark-evidence/reference-recovery-20261110'),
             'rerun-source': REPO / 'work/focal-rerun-20261110'}
    manifest_path = args.readback / 'archive/archive-manifest.json'
    if identity(manifest_path)['sha256'] != receipt['archive']['manifest_sha256']:
        raise ValueError('Manifest does not match published receipt')
    manifest = json.loads(manifest_path.read_text())
    p2 = json.loads((roots['run'] / 'readback/p2-after-message-fix.json').read_text())
    p2_paths = set(p2['read_file_sha256'])
    fixed_setup = {
        'run/PROTOCOL.md', 'run/provenance/pre-execution-source-freeze.json',
        'run/provenance/fresh-environment.json', 'run/provenance/final-executed-source-identities.json',
        'run/python-setup/downloads.json', 'run/python-setup/requirements-hashed.txt',
        'run/android/prerequisites/prerequisite-integrity-check.json',
        'run/android/prerequisites/emulator-command.json',
        'run/android/prerequisites/emulator-readiness.json',
        'run/round/P2/prerequisites/dependency-pin-verification.json',
        'run/round/P2/EXECUTION_INPUT_FREEZE.json',
    }
    files = []
    for row in manifest['files']:
        name = row['path']
        prefix, relative = name.split('/', 1)
        path = roots[prefix] / relative
        groups = []
        if prefix == 'recovered-inputs' and '/' not in relative:
            groups.append('N0')
        if (name in fixed_setup or name.startswith('recovered-inputs/inputs/') or
                name in ['run/android/scripts/prepare_e1.py', 'run/android/scripts/prepare_e2.py',
                         'run/android/scripts/ContractInstrumentation.java',
                         'run/round/P2/scripts/ContractInstrumentation.java',
                         'run/round/P2/scripts/TaskInstrumentation.java']):
            groups.append('N1')
        if (name in ['run/android/model-preservation-audit.json', 'run/android/audit-results.json']
                or name.startswith('recovered-inputs/models/')
                or (name.startswith('run/android/') and '/variants/' in name and
                    (name.endswith(('.tflite', '.apk', '.class', '.dex', '/ContractModel.java'))))):
            groups.append('N2')
        for experiment, group in [('E1', 'N3'), ('E2', 'N4')]:
            base = 'run/android/' + experiment + '/'
            if ((name.startswith(base) and (name in
                    [base + f for f in ['static-results.json', 'build-results.json', 'results.json']] or
                    (name.startswith(base + 'executions/') and
                     '-interrupted-' not in name and '-provenance/' not in name) or
                    (name.startswith(base + 'variants/') and
                     (name.endswith('/codegen-status.json') or '/logs/codegen.' in name)))) or
                    name.startswith('run/stages/' + experiment.lower() + '-prepare/')):
                groups.append(group)
        if str(path) in p2_paths or name in ['run/readback/p2-after-message-fix.json',
                                            'run/round/P2/EXECUTION_INPUT_FREEZE.json']:
            groups.append('N5')
        if prefix == 'recovered-references' or name.startswith('run/p3-core-attempt2/'):
            groups.append('N6')
        if (name.startswith('run/android/E1/executions/') and
                ('-interrupted-' in name or '-provenance/' in name)) or name.startswith((
                    'run/provenance/primary-attempt1-relocation.json',
                    'run/stages/e1-primary/', 'run/stages/e1-primary-attempt2/')):
            groups.append('N7')
        if name.startswith(('run/readback/', 'run/p3-core/', 'run/stages/p3-core/',
                            'run/stages/android-metadata/', 'run/stages/p2-readback/')):
            groups.append('N8')
        if name == 'rerun-source/package_evidence.py':
            groups.append('N9')
        if not groups:
            continue
        actual, source_location = (repository_identity(path) if prefix == 'rerun-source'
                                   else (identity(path), {'verified_from': 'live_evidence'}))
        if actual != {k: row[k] for k in ['bytes', 'sha256']}:
            raise ValueError('Live file differs from archived member: ' + name)
        if str(path) in p2_paths and actual['sha256'] != p2['read_file_sha256'][str(path)]:
            raise ValueError('P2 read-file identity differs: ' + name)
        files.append({'archive_member': name, 'root': prefix, 'relative_path': relative,
                      **actual, **source_location, 'groups': sorted(set(groups))})
    legacy_path = REPO / 'work/paper-rewrite-20261004/claim-sources.json'
    legacy = json.loads(legacy_path.read_text())
    resolved_sources = []
    for row in legacy['source_records']:
        expected = {k: row[k] for k in ['bytes', 'sha256']}
        try:
            actual, source_location = repository_identity(REPO / row['path'])
        except FileNotFoundError:
            actual, source_location = None, {'verified_from': 'missing_working_tree'}
        resolved = {'id': row['id'], 'path': row['path'], 'expected': expected,
                    'current': actual, **source_location}
        if actual != expected:
            # A maintained document may have changed since the old ledger.
            # Recover its exact pinned Git version, never refresh the old pin.
            revision = legacy['local_base_revision']
            data = subprocess.check_output(['git', '-C', str(REPO), 'show', revision + ':' + row['path']])
            if {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()} != expected:
                raise ValueError('Historical claim source cannot be resolved: ' + row['id'])
            resolved.update(verified_from='historical_git_object', revision=revision,
                            limitation='Current document differs; this identity supports only the historical source.')
        resolved_sources.append(resolved)
    editorial = []
    for path in sorted(args.readback.rglob('*')):
        if path.is_file():
            editorial.append({'local_path': str(path.resolve()), **identity(path),
                              'scope': 'New saved-byte review output; not a member of the November run archive'})
    sources = [receipt_path, legacy_path,
               REPO / 'work/review-fixes-20261021/verify_p2_records.py',
               REPO / 'work/focal-rerun-20261110/analyze_p3_core.py',
               REPO / 'sources/repro-audit-20261004/android/audit_android_results.py',
               REPO / 'sources/repro-audit-20261004/android/audit_model_preservation.py']
    sources += list(AREA.glob('*.py'))
    data = {'schema_version': 1, 'created_utc': datetime.now(timezone.utc).isoformat(),
            'scope': 'Selected evidence identities for the November short-paper revision; no raw payloads.',
            'human_verification': 'PENDING', 'archive': receipt['archive'],
            'roots': {k: str(v) for k, v in roots.items()}, 'groups': GROUPS,
            'selected_members': len(files), 'files': files,
            'historical_source_records_verified': len(legacy['source_records']),
            'historical_source_resolution': resolved_sources,
            'repository_records': [{'path': str(p.relative_to(REPO)), **repository_identity(p)[0],
                                    **repository_identity(p)[1]} for p in sources],
            'editorial_readbacks': editorial}
    with args.output.open('x') as stream:
        json.dump(data, stream, indent=2)
        stream.write('\n')
    print(json.dumps({'selected_members': len(files), 'historical_sources': len(legacy['source_records']),
                      'group_counts': {g: sum(g in r['groups'] for r in files) for g in GROUPS}}))


if __name__ == '__main__':
    main()
