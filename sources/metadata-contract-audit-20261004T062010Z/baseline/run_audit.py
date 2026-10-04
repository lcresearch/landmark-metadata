"""Orchestrate fixed independent checks and retain every outcome."""
import concurrent.futures
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
OLD = Path('/workspace/metadata-contract-e2e-20261004T030536Z')
PYTHON = Path('/workspace/hand-contract-repro/.venv/bin/python')
def sha(data): return hashlib.sha256(data).hexdigest()
def save(path, obj): path.write_text(json.dumps(obj, indent=2) + '\n')
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()

def run_one(task):
    key, mode, command = task
    log = ROOT / 'logs' / (key + '--' + mode)
    log.parent.mkdir(exist_ok=True)
    env = os.environ.copy(); env['PYTHONDONTWRITEBYTECODE'] = '1'; env['TMPDIR'] = str(ROOT / 'tmp')
    record = {'command': list(map(str, command)), 'cwd': str(ROOT), 'started_utc': now(),
              'env_overrides': {'PYTHONDONTWRITEBYTECODE': '1', 'TMPDIR': str(ROOT / 'tmp')}}
    try:
        p = subprocess.run(record['command'], cwd=ROOT, env=env, capture_output=True, timeout=180)
        record['exit_code'] = p.returncode
        log.with_suffix('.stdout').write_bytes(p.stdout); log.with_suffix('.stderr').write_bytes(p.stderr)
    except subprocess.TimeoutExpired as exc:
        record.update(exit_code=None, timeout_seconds=180)
        log.with_suffix('.stdout').write_bytes(exc.stdout or b''); log.with_suffix('.stderr').write_bytes(exc.stderr or b'')
    record['finished_utc'] = now(); save(log.with_suffix('.command.json'), record)
    return {'condition': key, 'check': mode, 'log_prefix': str(log), **record}

def main():
    (ROOT / 'tmp').mkdir(exist_ok=True); (ROOT / 'sources').mkdir(exist_ok=True)
    models = {}
    for phase in ['E1', 'E2']:
        for path in sorted((OLD / phase / 'variants').glob('*/model.tflite')):
            digest = sha(path.read_bytes())
            row = models.setdefault(digest, {'sha256': digest, 'path': str(path), 'aliases': []})
            row['aliases'].append({'phase': phase, 'variant': path.parent.name})
    assert len(models) == 5 and sum(len(v['aliases']) for v in models.values()) == 8
    order = ['original', 'description_control', 'label_deletion', 'label_permutation', 'label_restoration']
    rows = []
    for key in order:
        row = next(v for v in models.values() if any(a['variant'] == key for a in v['aliases']))
        row['condition'] = key; rows.append(row)
    protected = [OLD / 'commands-executed.sh', OLD / 'scripts/preflight.py', OLD / 'E5/preflight.py', OLD / 'scripts/common.py']
    protected += [Path(v['path']) for v in rows]
    structural = Path('/workspace/metadata-contract-paper/runs/6c7ab0a6e5dc/count_minus_one/model.tflite')
    protected.append(structural)
    snapshot = {str(p): {'sha256': sha(p.read_bytes()), 'bytes': p.stat().st_size} for p in protected}
    save(ROOT / 'protected-before.json', snapshot)
    save(ROOT / 'inputs.json', {'distinct_files': 5, 'aliases': 8, 'models': rows})
    sources = [OLD / 'scripts/preflight.py', OLD / 'scripts/common.py', OLD / 'scripts/codegen_one.py',
               OLD / 'E3/sources/image_classifier.cc', OLD / 'E3/sources/_pywrap_image_classifier.cc',
               OLD / 'E3/sources/image_classifier.py', OLD / 'E3/sources/classification_postprocessor.cc',
               Path('/workspace/hand-contract-repro/sources/TensorLabel.java'),
               Path('/workspace/metadata-contract-paper/sources/FileUtil.java')]
    source_rows = []
    for p in sources:
        if p.exists():
            target = ROOT / 'sources' / p.name
            shutil.copyfile(p, target)
            source_rows.append({'original': str(p), 'snapshot': str(target), 'sha256': sha(p.read_bytes())})
        else: source_rows.append({'original': str(p), 'status': 'UNAVAILABLE'})
    save(ROOT / 'source-snapshots.json', source_rows)
    save(ROOT / 'plan-freeze.json', {'time_utc': now(), 'plan_sha256': sha((ROOT / 'PLAN.md').read_bytes()),
                                    'inputs_sha256': sha((ROOT / 'inputs.json').read_bytes()),
                                    'implementation_sha256': {p.name: sha(p.read_bytes()) for p in ROOT.glob('*.py')}})
    tasks = []
    original = next(v['path'] for v in rows if v['condition'] == 'original')
    for row in rows:
        key = row['condition']; base = ROOT / 'conditions' / key
        base.mkdir(parents=True, exist_ok=False)
        for mode in ['displayer', 'populator', 'simple_baseline', 'task_init']:
            tasks.append((key, mode, [PYTHON, ROOT / 'audit_one.py', mode, row['path'], base / mode]))
        tasks.append((key, 'e5', [PYTHON, ROOT / 'launch_e5.py', row['path'], '--evidence-dir', base / 'e5', '--baseline', original]))
    structural_base = ROOT / 'conditions' / 'structural_count_minus_one'
    structural_base.mkdir(parents=True, exist_ok=False)
    for mode in ['displayer', 'populator']:
        tasks.append(('structural_count_minus_one', mode, [PYTHON, ROOT / 'audit_one.py', mode, structural, structural_base / mode]))
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        commands = list(pool.map(run_one, tasks))
    save(ROOT / 'commands.json', commands)
    after = {str(p): {'sha256': sha(p.read_bytes()), 'bytes': p.stat().st_size} for p in protected}
    save(ROOT / 'protected-after.json', {'unchanged': after == snapshot, 'files': after})
    for row in rows:
        row['checks'] = {}
        for mode in ['displayer', 'populator', 'simple_baseline', 'task_init', 'e5']:
            file = ROOT / 'conditions' / row['condition'] / mode / 'result.json'
            row['checks'][mode] = json.loads(file.read_text()) if file.exists() else {'status': 'NO_COMPLETE_RESULT', 'path': str(file)}
    results = {'completed_utc': now(), 'review_type': 'AI-agent execution audit; not independent human audit',
               'experimental_unit': 'five exact byte-distinct core artifacts × selected check; eight phase aliases retained',
               'emulator_runs': 0, 'task_inference_runs': 0, 'preserved_inputs_unchanged': after == snapshot,
               'e5_adaptation': 'Unchanged old scripts/preflight.py loaded by runpy; only common.run logging shim avoids sealed log writes and changes subprocess cwd to the new audit directory.',
               'models': rows, 'commands_path': str(ROOT / 'commands.json')}
    results['separate_structural_negative_control'] = {'path': str(structural), 'sha256': sha(structural.read_bytes()),
        'checks': {mode: json.loads((structural_base / mode / 'result.json').read_text()) if (structural_base / mode / 'result.json').exists() else {'status': 'NO_COMPLETE_RESULT'} for mode in ['displayer', 'populator']}}
    save(ROOT / 'results.json', results)
    print(json.dumps({'complete': True, 'conditions': len(rows), 'check_invocations': len(tasks), 'protected_unchanged': after == snapshot}, indent=2))

if __name__ == '__main__': main()
