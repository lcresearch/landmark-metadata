"""Check saved identities/completion without requiring the reported failure to recur."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(root):
    checks = []
    def check(name, condition):
        checks.append({'check': name, 'status': 'PASS' if condition else 'FAIL'})
    model = root / 'model-download/complete.body'
    model_sha = sha(model)
    inspection = json.loads((root / 'model-inspection/inspection.json').read_text())
    check('model inspection identity', inspection['sha256'] == model_sha and inspection['bytes'] == model.stat().st_size)
    check('model linkage', inspection['linkage_pass'] is True)
    generation = json.loads((root / 'stages/agp-generation/command.json').read_text())
    check('actual AGP command completed', generation['status'] == 'PASS' and generation['exit_code'] == 0 and
          generation['command'][-1] == ':app:generateDebugMlModelClass' and not generation.get('timeout'))
    freeze = json.loads((root / 'runtime-freeze.json').read_text())
    generated = root / 'project/app/build/generated/ml_source_out/debug/org/example/support770/ml/LiteModelDeeplabv31Metadata2.java'
    check('unchanged generated source', sha(generated) == freeze['generated_source_sha256'])
    for name, digest in freeze['source_files'].items():
        check('frozen build source ' + name, sha(root / 'runtime-source' / name) == digest)
    expected_input = hashlib.sha256(bytes([127]) * (257 * 257 * 3)).hexdigest()
    builds = json.loads((root / 'build-results.json').read_text())
    results = json.loads((root / 'runtime-results.json').read_text())
    check('exactly two consumers', sorted(r['consumer'] for r in results) == ['task', 'wrapper'])
    outcomes = []
    for result in results:
        consumer = result['consumer']
        build = next(b for b in builds if b['consumer'] == consumer)
        check(consumer + ' build link', result['build'] == build and build['status'] == 'PASS')
        apk = root / 'build' / consumer / 'consumer.apk'
        check(consumer + ' APK identity', sha(apk) == build['apk_sha256'])
        with zipfile.ZipFile(apk) as archive:
            check(consumer + ' packaged model', hashlib.sha256(archive.read('assets/lite_model_deeplabv3_1_metadata_2.tflite')).hexdigest() == model_sha == build['packaged_model_sha256'])
            for path in (root / 'build' / consumer / 'dex').glob('*.dex'):
                check(consumer + ' packaged dex ' + path.name, archive.read(path.name) == path.read_bytes())
            for entry in freeze['consumers'][consumer]['natives']:
                path = Path(entry['path'])
                check(consumer + ' native ' + path.name, sha(path) == entry['sha256'] and archive.read('lib/x86_64/' + path.name) == path.read_bytes())
        for relative, digest in build['class_hashes'].items():
            check(consumer + ' class ' + relative, sha(root / 'build' / consumer / 'classes' / relative) == digest)
        for entry in freeze['consumers'][consumer]['classpaths']:
            check(consumer + ' dependency ' + entry['path'], sha(Path(entry['path'])) == entry['sha256'])
        folder = root / 'executions' / consumer
        command = json.loads((folder / 'instrumentation/command.json').read_text())
        check(consumer + ' invocation completed', command['status'] == 'PASS' and command['exit_code'] == 0 and not command.get('timeout'))
        observed = json.loads((folder / 'device/result.json').read_text())
        check(consumer + ' observed record link', result['observed'] == observed and result['collection_status'] == 'PASS')
        check(consumer + ' scientific status link', result['scientific_status'] == observed['scientific_status'])
        check(consumer + ' completed', observed.get('completed') is True)
        check(consumer + ' device model', observed.get('model_sha256') == model_sha and observed.get('model_bytes') == model.stat().st_size)
        check(consumer + ' same input', observed.get('input_sha256') == expected_input == sha(folder / 'device/input.rgb'))
        for key, value in observed.items():
            if isinstance(value, dict) and {'sha256', 'bytes', 'shape'} <= value.keys():
                path = folder / 'device' / (key + '.bin')
                check(consumer + ' output ' + key, sha(path) == value['sha256'] and path.stat().st_size == value['bytes'])
        if observed.get('scientific_status') == 'FAIL':
            stage = observed.get('earliest_failing_stage')
            check(consumer + ' retained failure detail', observed.get(str(stage) + '_status') == 'FAIL' and
                  bool(observed.get('exception_type')) and bool(observed.get('stack_trace')) and bool(observed.get('causes')))
        else:
            endpoint = 'category_getter_status' if consumer == 'wrapper' else 'mask_observation_status'
            check(consumer + ' successful endpoint', observed.get('scientific_status') == 'PASS' and observed.get(endpoint) == 'PASS')
        outcomes.append({'consumer': consumer, 'scientific_status': observed['scientific_status'],
                         'earliest_failing_stage': observed.get('earliest_failing_stage'),
                         'exception': observed.get('exception_message')})
    return {'status': 'PASS' if all(c['status'] == 'PASS' for c in checks) else 'FAIL',
            'checks': checks, 'outcomes': outcomes,
            'scope': 'saved-byte consistency and completed calls, not human verification or historical identity'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists(): raise FileExistsError(args.output)
    try:
        report = verify(args.root.resolve())
    except Exception as exc:
        report = {'status': 'FAIL', 'error': repr(exc)}
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': report['status'], 'checks': len(report.get('checks', [])),
                      'outcomes': report.get('outcomes'), 'error': report.get('error')}))
    raise SystemExit(0 if report['status'] == 'PASS' else 1)


if __name__ == '__main__':
    main()
