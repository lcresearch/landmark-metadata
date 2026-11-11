"""Create fresh run/source copies, verify inputs and record every path adaptation."""
import argparse
from datetime import datetime, timezone
import difflib
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

REPO = Path(__file__).resolve().parents[2]
SCRIPT_AREAS = ('android/scripts', 'round/P2/scripts')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2) + '\n')


def stage_sources(repo, root):
    repo, root = Path(repo).resolve(), Path(root).resolve()
    if root.is_relative_to(repo):
        raise ValueError('Evidence root must stay outside the source repository')
    catalog = json.loads((repo / 'experiment/source-map.json').read_text())
    selected = {destination: relative for destination, relative in catalog.items()
                if destination.startswith(('corpus/scripts/', 'round/P2/scripts/'))}
    selected['hand/requirements.lock'] = 'experiment/toolchain/requirements.lock'
    # Validate the complete selection before writing anything.
    records = []
    for destination, relative in selected.items():
        source, target = repo / relative, root / destination
        if (not source.resolve().is_relative_to(repo) or source.is_symlink()
                or not target.resolve().is_relative_to(root) or target.exists()):
            raise ValueError('Unsafe or occupied staging path: ' + destination)
        data = source.read_bytes()
        records.append((target, data, {'source': relative, 'destination': destination,
                                     'sha256': sha(data), 'bytes': len(data)}))
    for target, data, record in records:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    for relative in ('hand/logs', 'hand/results', 'corpus/logs', 'corpus/results'):
        (root / relative).mkdir(parents=True, exist_ok=True)
    return [record for _, _, record in records]


def verify_inputs(inputs, refs):
    """Check every model/reference pin before creating a run directory."""
    inventory = json.loads((REPO / 'docs/reproduction/inputs.json').read_text())
    verified = []
    for row in inventory['model_conditions']:
        path = inputs / 'models' / (row['id'] + '.tflite')
        actual = sha(path.read_bytes())
        if actual != row['primary_model']['expected_sha256']:
            raise ValueError('Model identity differs: ' + row['id'])
        verified.append({'path': str(path), 'sha256': actual})
    for row in inventory['p3_reference_prerequisites']:
        path = refs / row['id'] / 'body'
        actual = sha(path.read_bytes())
        if actual != row['body']['expected_sha256']:
            raise ValueError('Reference identity differs: ' + row['id'])
        verified.append({'path': str(path), 'sha256': actual})
    return inventory, verified


def initialize_android(root):
    """Retain the adapter's command and logs even if source preparation fails."""
    provenance = root / 'provenance'
    command = [sys.executable, str(REPO / 'scripts/initialize_android_run.py'),
               '--repo', str(REPO), '--root', str(root / 'android')]
    result = subprocess.run(command, capture_output=True)
    (provenance / 'initialize-android.stdout').write_bytes(result.stdout)
    (provenance / 'initialize-android.stderr').write_bytes(result.stderr)
    # Preserve this existing record's formatting, including its absent final newline.
    (provenance / 'initialization-commands.json').write_text(
        json.dumps([{'command': command, 'exit_code': result.returncode}], indent=2))
    result.check_returncode()


def prepare_consumer_layout(root, inputs, inventory, protocol):
    """Populate the model aliases and P2 inputs expected by preserved producers."""
    provenance = root / 'provenance'
    for name, condition in [('original', 'original'), ('description_control', 'description_control'),
                            ('label_drop_1', 'label_deletion')]:
        folder = root / 'corpus/runs/6c7ab0a6e5dc' / name
        folder.mkdir(parents=True)
        shutil.copyfile(inputs / 'models' / (condition + '.tflite'), folder / 'model.tflite')
    source = REPO / 'research/20261004-p2-p3/P2'
    p2 = root / 'round/P2'
    (p2 / 'prerequisites').mkdir()
    (p2 / 'EXPERIMENT_P2_PLAN.md').write_bytes(protocol)
    (p2 / 'sdk').symlink_to(root / 'android/sdk', target_is_directory=True)
    for name in ['EXPERIMENT_P2_PLAN.md', 'INPUTS.json']:
        origin = source / name if name != 'INPUTS.json' else source.parent / name
        shutil.copyfile(origin, provenance / ('historical-' + name))
    input_rows = [{'variant': row['id'], 'path': str(inputs / 'models' / (row['id'] + '.tflite')),
                   'sha256': row['primary_model']['expected_sha256']} for row in inventory['model_conditions']]
    write_json(root / 'round/INPUTS.json', {'created_utc': datetime.now(timezone.utc).isoformat(),
        'scope': 'New execution with newly recovered inputs; no historical manifests asserted present.',
        'input_models': input_rows})


def adapt_sources(root):
    """Replace historical roots only in staged copies and retain complete patches."""
    provenance = root / 'provenance'
    mapping = {'/workspace/hand-contract-repro': str(root / 'hand'),
               '/workspace/metadata-contract-paper': str(root / 'corpus'),
               '/workspace/metadata-contract-e2e-20261004T030536Z': str(root / 'android')}
    adaptations = []
    for area in SCRIPT_AREAS:
        for path in sorted((root / area).glob('*.py')):
            before = path.read_text()
            after = before
            for old, new in mapping.items():
                after = after.replace(old, new)
            if before == after:
                continue
            path.write_text(after)
            name = str(path.relative_to(root))
            adaptations.append({'path': name, 'before_sha256': sha(before.encode()), 'after_sha256': sha(after.encode())})
            patch = ''.join(difflib.unified_diff(before.splitlines(True), after.splitlines(True),
                                                fromfile='historical/' + name, tofile='new/' + name))
            (provenance / (name.replace('/', '_') + '.patch')).write_text(patch)
    return mapping, adaptations


def freeze_sources(root, inputs, refs, protocol, verified, source_copies):
    """Record the exact staged sources after all path adaptations."""
    mapping, adaptations = adapt_sources(root)
    freeze = {'created_utc': datetime.now(timezone.utc).isoformat(),
              'protocol_sha256': sha(protocol), 'input_files': verified, 'path_mapping': mapping,
              'adaptations': adaptations, 'inputs_root': str(inputs), 'references_root': str(refs),
              'source_base_revision': subprocess.check_output(['git', '-C', str(REPO), 'rev-parse', 'HEAD'], text=True).strip(),
              'new_source_files': {p.name: sha(p.read_bytes()) for p in Path(__file__).parent.iterdir() if p.is_file()},
              'model_execution_started': False, 'historical_results_known': True,
              'staged_source_inputs': source_copies,
              'source_map_sha256': sha((REPO / 'experiment/source-map.json').read_bytes()),
              'source_files': {str(p.relative_to(root)): sha(p.read_bytes())
                               for area in SCRIPT_AREAS
                               for p in (root / area).glob('*') if p.is_file()}}
    write_json(root / 'provenance/pre-execution-source-freeze.json', freeze)
    write_json(root / 'round/P2/PLAN_FREEZE.json', {
        'created_utc': freeze['created_utc'], 'protocol_sha256': sha(protocol),
        'new_run': True, 'historical_results_known': True})
    return len(adaptations)


def initialize(root, inputs, refs):
    root, inputs, refs = (Path(p).resolve() for p in (root, inputs, refs))
    if root.exists() or root.is_relative_to(REPO):
        raise ValueError('Choose a new external run root')
    inventory, verified = verify_inputs(inputs, refs)
    root.mkdir(parents=True, exist_ok=False)
    (root / 'provenance').mkdir()
    protocol = Path(__file__).with_name('PROTOCOL.md').read_bytes()
    (root / 'PROTOCOL.md').write_bytes(protocol)
    source_copies = stage_sources(REPO, root)
    initialize_android(root)
    prepare_consumer_layout(root, inputs, inventory, protocol)
    adapted = freeze_sources(root, inputs, refs, protocol, verified, source_copies)
    return {'root': str(root), 'status': 'INITIALIZED_NO_MODEL_EXECUTION',
            'adapted_files': adapted}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True, type=Path)
    parser.add_argument('--inputs', required=True, type=Path)
    parser.add_argument('--references', required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(initialize(args.root, args.inputs, args.references), indent=2))


if __name__ == '__main__':
    main()
