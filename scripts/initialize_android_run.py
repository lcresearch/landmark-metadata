"""Copy preserved Android sources to a new external run without asserting retrieval.

This maintained adapter only prepares source files. Model acquisition, dependency
installation and all device execution are separate operations.
"""
import argparse
import hashlib
import json
from pathlib import Path


E2E = 'metadata-contract-e2e-20261004T030536Z'
AUDIT = 'metadata-contract-audit-20261004T062010Z'
LOCAL_INPUT_PROVENANCE = (
    'local model input bytes; acquisition method is not established by this initializer'
)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def replace_required(text, before, after, name):
    if before not in text:
        raise ValueError('Expected adapter anchor missing: ' + name)
    return text.replace(before, after)


def initialize(repo, root, port=5554):
    repo, root = Path(repo).resolve(), Path(root)
    checkout = Path(__file__).resolve().parents[1]
    if any(root.resolve().is_relative_to(base) for base in (repo, checkout)):
        raise ValueError('Evidence root must stay outside source-only repository')
    if root.exists() or root.is_symlink():
        raise FileExistsError('Use a fresh evidence root: ' + str(root))
    old = repo / 'sources' / E2E
    audit = repo / 'sources' / AUDIT / 'rebuild/scripts'
    helpers = repo / 'sources/repro-audit-20261004/android'
    inputs, scripts, plans = [], {}, {}

    def source(path):
        data = path.read_bytes()
        inputs.append({'source': str(path), 'sha256': digest(data), 'bytes': len(data)})
        return data

    # Read and adapt every required source before creating the output directory.
    for path in sorted((old / 'scripts').iterdir()):
        if path.suffix in ('.py', '.java'):
            scripts[path.name] = source(path)
    for name in ('EXPERIMENT_E1_PLAN.md', 'EXPERIMENT_E2_PLAN.md'):
        plans[name] = source(old / name)
    for name in ('ContractInstrumentation.java', 'prepare_e2.py'):
        scripts[name] = source(audit / name)
    for name in ('audit_android_results.py', 'audit_model_preservation.py',
                 'check_android_ready.py'):
        scripts[name] = source(helpers / name)

    changes = [('prepare_e1.py', 'exact bytes recovered from frozen local evidence',
                LOCAL_INPUT_PROVENANCE)]
    if port != 5554:
        changes.extend([
            ('run_android.py', 'emulator-5554', f'emulator-{port}'),
            ('start_emulator.py', 'emulator-5554', f'emulator-{port}'),
            ('start_emulator.py', "'5554'", repr(str(port))),
        ])
    for name, before, after in changes:
        scripts[name] = replace_required(scripts[name].decode('utf-8'), before, after,
                                         name).encode('utf-8')

    startup = replace_required(
        scripts['start_emulator.py'].decode('utf-8'),
        'import json, os, pathlib, subprocess, time',
        'import json, os, pathlib, subprocess, time, sys', 'startup imports')
    startup = replace_required(
        startup, "        if q.stdout.strip()=='1':\n",
        "        if q.stdout.strip()=='1':\n"
        "            readiness_log=pre/('functional-readiness-'+str(len(observations)))\n"
        "            functional=run([sys.executable,ROOT/'scripts/check_android_ready.py',"
        f"'--adb',adb,'--serial','emulator-{port}','--evidence',readiness_log.with_suffix('.json'),"
        "'--timeout','60'],readiness_log,timeout=70)\n"
        "            if functional.returncode!=0: continue\n", 'functional readiness')
    scripts['start_emulator.py'] = startup.encode('utf-8')
    provenance = {
        'base_source': str(old / 'scripts'),
        'source_files': inputs,
        'adapter': {'path': str(Path(__file__).resolve()),
                    'sha256': digest(Path(__file__).read_bytes())},
        'input_acquisition': {
            'status': 'NOT_ESTABLISHED',
            'source_bundle_note': LOCAL_INPUT_PROVENANCE,
            'scope': 'The initializer reads source files only; it does not read or download model inputs.',
        },
        'adaptations': [
            'Audit harness adds pre-initialization AssetManager hashing; generated model source remains unmodified.',
            'Audit prepare_e2 gates on completed E1 primary; all replays remain required.',
            'Copied E1 source identifies local model inputs without asserting a retrieval method.',
            'Copied startup requires functional package/activity readiness and stable system_server observations.',
            f'Copied runner and startup use emulator console port {port}.',
            'Default parent dependencies remain /workspace/{hand-contract-repro,metadata-contract-paper}.',
        ],
        'scripts': {name: digest(data) for name, data in sorted(scripts.items())},
        'plans': {name: digest(data) for name, data in sorted(plans.items())},
        'models_read_or_downloaded': False,
        'model_or_device_execution': False,
    }
    root.mkdir(parents=True)
    for directory in ('scripts', 'prerequisites', 'logs'):
        (root / directory).mkdir()
    for name, data in scripts.items():
        (root / 'scripts' / name).write_bytes(data)
    for name, data in plans.items():
        (root / name).write_bytes(data)
    (root / 'SOURCE_PROVENANCE.json').write_text(json.dumps(provenance, indent=2) + '\n')
    return provenance


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--port', type=int, default=5554)
    args = parser.parse_args()
    initialize(args.repo, args.root, args.port)
    print('Initialized fresh external run:', args.root)


if __name__ == '__main__':
    main()
