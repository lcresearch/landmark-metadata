"""Check saved identities/completion without requiring the reported failure to recur."""
import argparse
from datetime import datetime
import hashlib
import json
import math
from pathlib import Path
import tarfile
import zipfile


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_outputs(folder, consumer, observed, output_shape, labels, check):
    """Require artifacts implied by reached stages, without forcing a scientific PASS."""
    stages = ['construction', 'process', 'raw_observation', 'category_getter'] if consumer == 'wrapper' else [
        'construction', 'segment', 'mask_observation']
    stages = ['asset_identity', 'input', *stages]
    failure = observed.get('earliest_failing_stage')
    states = [observed.get(stage + '_status') for stage in stages]
    if observed.get('scientific_status') == 'PASS':
        check(consumer + ' successful stage sequence', all(state == 'PASS' for state in states) and failure is None)
    elif failure in stages:
        index = stages.index(failure)
        check(consumer + ' failed stage sequence', all(state == 'PASS' for state in states[:index]) and
              states[index] == 'FAIL' and all(state in (None, 'NOT_REACHED') for state in states[index + 1:]))
    else:
        check(consumer + ' known failing stage', False)

    def tensor(name, shape, element_bytes):
        value = observed.get(name)
        valid = isinstance(value, dict) and {'shape', 'bytes', 'sha256'} <= value.keys()
        check(consumer + ' required output ' + name, valid)
        if not valid:
            return
        check(consumer + ' output shape ' + name, value['shape'] == shape and
              isinstance(value['shape'], list) and all(type(d) is int for d in value['shape']))
        check(consumer + ' output size ' + name, type(value['bytes']) is int and
              value['bytes'] == math.prod(shape) * element_bytes)
        path = folder / 'device' / (name + '.bin')
        check(consumer + ' output ' + name, path.is_file() and sha(path) == value['sha256'] and
              path.stat().st_size == value['bytes'])

    if consumer == 'wrapper':
        if observed.get('raw_observation_status') == 'PASS':
            tensor('raw_output', output_shape, 4)
        if observed.get('category_getter_status') == 'PASS':
            categories = observed.get('categories')
            check('wrapper returned categories', isinstance(categories, list) and len(categories) == len(labels) and
                  all(isinstance(c, dict) and isinstance(c.get('label'), str) and
                      type(c.get('index')) is int and type(c.get('score')) in (int, float) and
                      math.isfinite(c['score']) for c in categories))
    else:
        if observed.get('segment_status') == 'PASS':
            check('task returned segmentation count', type(observed.get('segmentations')) is int and
                  observed['segmentations'] == 1)
        if observed.get('mask_observation_status') == 'PASS':
            check('task requested output kind', observed.get('requested_output_type') == 'CATEGORY_MASK')
            outputs = observed.get('outputs')
            valid = isinstance(outputs, list) and len(outputs) == 1 and isinstance(outputs[0], dict)
            check('task required output descriptions', valid)
            if valid:
                output = outputs[0]
                check('task mask kind and count', output.get('output_type') == 'CATEGORY_MASK' and
                      type(output.get('mask_count')) is int and output['mask_count'] == 1)
                returned = output.get('labels')
                check('task associated labels', isinstance(returned, list) and len(returned) == len(labels) and
                      all(isinstance(item, dict) and item.get('label') == label
                          for item, label in zip(returned, labels)))
            tensor('mask_0_0', output_shape[1:3], 1)


def check_invocation(root, consumer, build, observed, check):
    """Bind install, execution and collection to this fixed consumer and device."""
    folder = root / 'executions' / consumer
    instrument = {'wrapper': 'WrapperInstrumentation', 'task': 'TaskInstrumentation'}[consumer]
    package = 'org.example.support770.' + consumer
    class_name = 'org.example.support770.' + instrument
    check(consumer + ' frozen consumer identity', build.get('package') == package and build.get('instrument') == instrument)
    check(consumer + ' observed instrumentation', observed.get('instrumentation') == class_name)
    boot = json.loads((root / 'boot/launch.json').read_text())
    check(consumer + ' owned device', boot.get('serial') == 'emulator-5556')
    prefix = [str(root / 'sdk/platform-tools/adb'), '-s', 'emulator-5556']
    expected = {
        'install': [*prefix, 'install', str(root / 'build' / consumer / 'consumer.apk')],
        'instrumentation': [*prefix, 'shell', 'am', 'instrument', '-w', package + '/' + class_name],
        'collect': [*prefix, 'exec-out', 'run-as', package, 'tar', '-C', 'files/evidence', '-cf', '-', '.'],
    }
    intervals = []
    for stage, arguments in expected.items():
        record = json.loads((folder / stage / 'command.json').read_text())
        check(consumer + ' ' + stage + ' command identity', record.get('command') == arguments and record.get('cwd') == str(root))
        check(consumer + ' ' + stage + ' completed', record.get('status') == 'PASS' and
              type(record.get('exit_code')) is int and record['exit_code'] == 0 and not record.get('timeout'))
        try:
            start, finish = (datetime.fromisoformat(record[key]) for key in ('started_utc', 'finished_utc'))
            valid = start.tzinfo is not None and finish.tzinfo is not None and start <= finish
        except (KeyError, TypeError, ValueError):
            valid = False
        check(consumer + ' ' + stage + ' timestamps', valid)
        if valid:
            intervals.append((start, finish))
    check(consumer + ' invocation chronology', len(intervals) == 3 and
          all(left[1] <= right[0] for left, right in zip(intervals, intervals[1:])))
    check(consumer + ' install confirmed', b'Success' in (folder / 'install/stdout').read_bytes())
    # Bind device records to the collected stream, not only a duplicate summary JSON.
    members = {}
    with tarfile.open(folder / 'collect/stdout') as archive:
        for member in archive:
            if member.isdir():
                continue
            name = Path(member.name.removeprefix('./'))
            if not member.isfile() or name.is_absolute() or '..' in name.parts or name in members:
                raise ValueError('Unexpected/duplicate collected member')
            members[name] = archive.extractfile(member).read()
    device = folder / 'device'
    actual = {p.relative_to(device) for p in device.rglob('*') if p.is_file()}
    check(consumer + ' collected member set', set(members) == actual)
    check(consumer + ' collected bytes', all((device / name).read_bytes() == data for name, data in members.items()))


def verify(root):
    root = root.resolve()
    checks = []
    def check(name, condition):
        checks.append({'check': name, 'status': 'PASS' if condition else 'FAIL'})
    model = root / 'model-download/complete.body'
    model_sha = sha(model)
    inspection = json.loads((root / 'model-inspection/inspection.json').read_text())
    check('model inspection identity', inspection['sha256'] == model_sha and inspection['bytes'] == model.stat().st_size)
    check('model linkage', inspection['linkage_pass'] is True)
    output_shape = [1, 257, 257, 21]
    check('inspected float32 output', len(inspection['outputs']) == 1 and
          inspection['outputs'][0]['shape'] == output_shape and inspection['outputs'][0]['type'] == 0)
    with zipfile.ZipFile(model) as archive:
        labels = archive.read('labelmap.txt').decode('utf-8').splitlines()
    check('associated label count', len(labels) == output_shape[-1])
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
        observed = json.loads((folder / 'device/result.json').read_text())
        check_invocation(root, consumer, build, observed, check)
        check(consumer + ' observed record link', result['observed'] == observed and result['collection_status'] == 'PASS')
        check(consumer + ' scientific status link', result['scientific_status'] == observed['scientific_status'])
        check(consumer + ' completed', observed.get('completed') is True)
        check(consumer + ' device model', observed.get('model_sha256') == model_sha and observed.get('model_bytes') == model.stat().st_size)
        check(consumer + ' same input', observed.get('input_sha256') == expected_input == sha(folder / 'device/input.rgb'))
        check_outputs(folder, consumer, observed, output_shape, labels, check)
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
