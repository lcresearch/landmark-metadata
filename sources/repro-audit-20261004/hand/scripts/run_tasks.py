"""Run unchanged E7 worker and explicitly validate completion/outcome evidence."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    run = sys.argv[1]
    if run not in ['primary', 'replay']:
        raise ValueError('Expected primary or replay')
    variants = json.loads((ROOT / 'results/variants.json').read_text())
    expected = {'original', 'container_control', 'metadata_exchange', 'restoration'}
    if len(variants) != 4 or {row['variant'] for row in variants} != expected:
        raise ValueError('Required four Hand conditions are missing or duplicated')
    destination = ROOT / 'executions' / run
    destination.mkdir(parents=True, exist_ok=False)
    records = []
    for variant in variants:
        folder = destination / variant['variant']
        folder.mkdir()
        command = [str(ROOT / '.venv/bin/python'), str(ROOT / 'scripts/hand_task_one.py'), variant['path'], str(ROOT / 'assets/thumb_up.jpg'), str(folder / 'outputs')]
        environment = dict(os.environ, MPLCONFIGDIR=str(ROOT / 'cache/matplotlib'), XDG_CACHE_HOME=str(ROOT / 'cache'), PYTHONDONTWRITEBYTECODE='1')
        process = subprocess.run(command, capture_output=True, timeout=120, env=environment)
        (folder / 'stdout.log').write_bytes(process.stdout)
        (folder / 'stderr.log').write_bytes(process.stderr)
        result_path = folder / 'outputs/result.json'
        observed = json.loads(result_path.read_text()) if result_path.exists() else {'earliest_failing_stage': 'worker_process'}
        complete = process.returncode == 0 and all(observed.get(key) == 'PASS' for key in ['initialization_status', 'input_preparation_status', 'detect_status'])
        complete = complete and observed.get('detected_hands') == 1 and observed.get('landmarks_per_hand') == [21] and observed.get('world_landmarks_per_hand') == [21]
        if complete:
            decoded = json.loads((folder / 'outputs/decoded.json').read_text())
            bits = (folder / 'outputs/decoded-float-bits.bin').read_bytes()
            complete = (hashlib.sha256(json.dumps(decoded, sort_keys=True, separators=(',', ':')).encode()).hexdigest() == observed.get('decoded_sha256')
                        and hashlib.sha256(bits).hexdigest() == observed.get('decoded_float_bits_sha256')
                        and observed.get('bundle_sha256') == hashlib.sha256(Path(variant['path']).read_bytes()).hexdigest()
                        and observed.get('image_sha256') == hashlib.sha256((ROOT / 'assets/thumb_up.jpg').read_bytes()).hexdigest())
        records.append({'variant': variant['variant'], 'command': command, 'exit_code': process.returncode, 'completed': complete, 'observed': observed})
        (destination / 'results.json').write_text(json.dumps(records, indent=2))
        print(variant['variant'], 'COMPLETED' if complete else 'FAILED', observed.get('path_exercised'), flush=True)
    baseline = next(row['observed'] for row in records if row['variant'] == 'original')
    for row in records:
        row['same_decoded_sha256_as_original'] = 'decoded_sha256' in row['observed'] and row['observed']['decoded_sha256'] == baseline.get('decoded_sha256')
        row['same_float_bits_sha256_as_original'] = 'decoded_float_bits_sha256' in row['observed'] and row['observed']['decoded_float_bits_sha256'] == baseline.get('decoded_float_bits_sha256')
        if run == 'replay':
            primary = json.loads((ROOT / 'executions/primary/results.json').read_text())
            previous = next(x for x in primary if x['variant'] == row['variant'])
            row['same_observed_as_primary'] = row['observed'] == previous['observed']
    (destination / 'results.json').write_text(json.dumps(records, indent=2))
    return int(not all(row['completed'] and row['same_decoded_sha256_as_original']
                       and row['same_float_bits_sha256_as_original']
                       and (run != 'replay' or row['same_observed_as_primary'])
                       for row in records))


if __name__ == '__main__':
    raise SystemExit(main())
