#!/usr/bin/env python3
"""Inspect bounded saved E1/E2/build-audit/P2 evidence in a relocated package.

No model/build/device execution, graph audit, P3 recomputation or human review.
The package manifest is checked for files read here; its historical trust anchor
must be verified separately with stage_evidence.py. Failure exits nonzero and is
written explicitly, including missing files. No assertion-dependent validation.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import stat
import struct
import zipfile


ROOTS = {
    'original': 'metadata-contract-e2e-20261004T030536Z',
    'audit': 'metadata-contract-audit-20261004T062010Z/rebuild',
    'p2': 'metadata-contract-p2p3-20261004T073824Z/P2',
}
PHASES = {
    'E1': ['original', 'description_control', 'label_deletion', 'label_restoration'],
    'E2': ['original', 'description_control', 'label_permutation', 'permutation_restoration'],
}
P2_VARIANTS = ['original', 'description_control', 'label_deletion', 'label_permutation', 'restoration']
# Previously recorded identities: docs/reproduction/inputs.json (not a new run).
MODEL_HASHES = {
    'original': '6c7ab0a6e5dcbf38a8c33b960996a55a3b4300b36a018c4545801de3a3c8bde0',
    'description_control': 'ed16d9573d8fe3e489c27637036a4e5c8476d15f013b7116f89864d55432f51d',
    'label_deletion': '739f08462e831806db6a9bce7ed5b70a037fce593003028e5d6911dbd284fd83',
    'label_permutation': '455a04a2c6193ea81bef8fbc47e193aee0449b8cebdc9cc487c7e9e85fe42da7',
    'restoration': '0a605ed10a38fc6f92fc4e266f5560756d2809e2669c45aa3b5a631cd88cea72',
}
INPUT_HASHES = {
    'gray127': '0748107f4221d0bb4ed8bada6a865b9348fb3b2a4c83b46f8e5eee704078b0ca',
    'rgb_pattern': 'fb23d2aecf5083dd57637ecebd7e80993a33af2561208c4cdd732cfe9249052f',
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def model_hash(variant):
    return MODEL_HASHES['restoration' if variant.endswith('restoration') else variant]


class Inspection:
    def __init__(self, package):
        self.package = package
        self.seen = {}
        self.apks = []
        self.records = []
        self.decoded = {}
        manifest_bytes = self.path('MANIFEST.json').read_bytes()
        manifest = json.loads(manifest_bytes)
        self.manifest_sha256 = sha(manifest_bytes)
        rows = manifest['files']
        require(len(rows) == len({r['path'] for r in rows}), 'Duplicate package manifest paths')
        self.manifest = {r['path']: r for r in rows}

    def path(self, name):
        rel = PurePosixPath(name)
        require(not rel.is_absolute() and '..' not in rel.parts and str(rel) == name,
                f'Unsafe relative path: {name}')
        path = self.package / name
        require(not any(p.is_symlink() for p in [path, *path.parents]), f'Symlink path: {name}')
        require(path.is_file() and stat.S_ISREG(path.stat().st_mode), f'Missing/nonregular file: {name}')
        return path

    def read(self, name):
        data = self.path(name).read_bytes()
        row = self.manifest.get(name)
        require(row is not None, f'File missing from package manifest: {name}')
        identity = {'bytes': len(data), 'sha256': sha(data)}
        require(all(identity[k] == row[k] for k in identity), f'Package byte mismatch: {name}')
        historical = row.get('historical_expected_sha256')
        require(historical is not None and historical == identity['sha256'],
                f'Inspected focal file lacks matching recorded historical identity: {name}')
        self.seen[name] = identity
        return data

    def load(self, name):
        return json.loads(self.read(name))

    def exact_files(self, directory, pattern, expected):
        actual = {p.relative_to(self.package).as_posix()
                  for p in (self.package / directory).rglob(pattern)
                  if p.is_file() or p.is_symlink()}
        require(actual == set(expected), f'Exact file-set mismatch for {directory}/{pattern}: '
                f'missing={sorted(set(expected)-actual)}, extra={sorted(actual-set(expected))}')

    def apk(self, build, model, variant, record, group):
        apk_name = build + '/consumer.apk'
        apk = self.read(apk_name)
        working = self.read(model)
        staged = self.read(build + '/assets/model.tflite')
        with zipfile.ZipFile(self.package / apk_name) as archive:
            require(archive.namelist().count('assets/model.tflite') == 1,
                    f'APK must contain one model asset: {apk_name}')
            asset = archive.read('assets/model.tflite')
        expected = model_hash(variant)
        require(sha(working) == sha(staged) == sha(asset) == expected,
                f'Working/staged/APK/model identity mismatch: {apk_name}')
        require(sha(apk) == record['apk_sha256'], f'Saved build APK digest mismatch: {apk_name}')
        self.apks.append({'path': apk_name, 'group': group, 'variant': variant,
                          'sha256': sha(apk), 'model_sha256': expected,
                          'working_staged_apk_model_equal': True})

    def run_record(self, directory, variant, consumer, family, apk):
        result = self.load(directory + '/device/result.json')
        install = self.load(directory + '/logs/install.command.json')
        require('/workspace/' + apk.removeprefix('payload/') in install['command'],
                f'Install record does not name the selected APK: {directory}')
        require(install['exit_code'] == 0, f'Nonzero saved install result: {directory}')
        require(result['variant'] == variant and result['api'] == 30,
                f'Wrong saved variant/API: {directory}')
        if family != 'original':
            require(result.get('loaded_asset_sha256') == model_hash(variant),
                    f'Saved pre-load asset identity mismatch: {directory}')
        task = consumer == 'task'
        deleted = variant == 'label_deletion'
        observations = result.get('observations', [])
        expected_inputs = [] if task and deleted else sorted(INPUT_HASHES)
        require(sorted(x['input'] for x in observations) == expected_inputs,
                f'Wrong input-observation identities: {directory}')
        device = directory + '/device'
        expected_payloads = [device + '/result.json']
        summary = Counter(records=1, observations=len(observations))
        if task and deleted:
            require(result.get('model_initialization_status') == 'FAIL'
                    and result.get('earliest_failing_stage') == 'model_initialization',
                    f'Wrong Task deletion stage: {directory}')
            chain = result.get('cause_chain', [])
            require([x['type'] for x in chain] == ['java.lang.IllegalStateException',
                                                 'java.lang.IllegalArgumentException']
                    and '1000 class(es)' in chain[1]['message']
                    and 'expected 999' in chain[1]['message'],
                    f'Missing Task deletion cause chain: {directory}')
            summary['constructor_failures'] = 1
        else:
            field = 'model_initialization_status' if task else 'model_loading_status'
            require(result.get(field) == 'PASS', f'Saved constructor did not pass: {directory}')
        for ob in observations:
            name = ob['input']
            inp_path = f'{device}/{name}-input.rgb'
            inp = self.read(inp_path)
            expected_payloads.append(inp_path)
            require(len(inp) == 224 * 224 * 3 and sha(inp) == ob['input_sha256'] == INPUT_HASHES[name],
                    f'Input payload/record mismatch: {inp_path}')
            require(ob['input_preparation_status'] == 'PASS', f'Input stage failure: {directory}/{name}')
            raw = None
            if not task:
                raw_path = f'{device}/{name}-output-0.f32'
                raw = self.read(raw_path)
                expected_payloads.append(raw_path)
                require(len(raw) == 4000 and ob['raw_output_bytes'] == 4000
                        and sha(raw) == ob['raw_output_sha256'], f'Raw payload/record mismatch: {raw_path}')
                require(ob['inference_status'] == ob['raw_output_observation_status'] == 'PASS',
                        f'Wrong wrapper pre-getter stages: {directory}/{name}')
                summary['raw_tensors'] += 1
            if deleted:
                require(ob.get('generated_getter_status') == 'FAIL'
                        and ob.get('earliest_failing_stage') == 'generated_getter'
                        and ob.get('exception_type') == 'java.lang.IllegalArgumentException'
                        and ob.get('exception_message') == 'Label number 999 mismatch the shape on axis 1'
                        and 'ContractModel$Outputs.getProbabilityAsCategoryList' in ob.get('stack_trace', ''),
                        f'Wrong caught getter failure: {directory}/{name}')
                summary['caught_getter_failures'] += 1
                continue
            field = 'classify_inference_and_decoding_status' if task else 'generated_getter_status'
            require(ob.get(field) == 'PASS', f'Saved successful call missing: {directory}/{name}')
            decoded_path = f'{device}/{name}-decoded.json'
            decoded = self.load(decoded_path)
            expected_payloads.append(decoded_path)
            if task:
                require(len(decoded) == 1 and decoded[0]['head_index'] == 0,
                        f'Wrong Task head identity: {decoded_path}')
                decoded = sorted(decoded[0]['categories'], key=lambda x: x['category_index_field'])
            index = 'category_index_field' if task else 'list_position'
            require([x[index] for x in decoded] == list(range(1000)),
                    f'Wrong decoded category identities: {decoded_path}')
            bits = [x['score_float_bits'] for x in decoded]
            require(bits == [struct.unpack('<i', struct.pack('<f', x['score']))[0] for x in decoded],
                    f'Decoded score/bit mismatch: {decoded_path}')
            if raw is not None:
                require(bits == list(struct.unpack('<1000i', raw)), f'Decoded/raw bits mismatch: {decoded_path}')
            self.decoded[(directory, name)] = [(x['label'], x['score_float_bits']) for x in decoded]
            summary['decoded_lists'] += 1
        self.exact_files(device, '*', expected_payloads)
        self.records.append({'directory': directory, 'family': family,
                             'consumer': consumer, 'variant': variant, **summary})

    def inspect(self):
        expected_apks = []
        for family in ('original', 'audit'):
            root = 'payload/' + ROOTS[family]
            for phase, variants in PHASES.items():
                base = root + '/' + phase
                builds = self.load(base + '/build-results.json')
                require(sorted(x['variant'] for x in builds) == sorted(variants), f'Wrong build units: {base}')
                records = []
                for row in builds:
                    v = row['variant']
                    build = f'{base}/variants/{v}/build'
                    apk = build + '/consumer.apk'
                    expected_apks.append(apk)
                    self.apk(build, f'{base}/variants/{v}/model.tflite', v, row, family + '_executed')
                    runs = ['primary'] if family == 'audit' else ['primary', 'replay']
                    for run in runs:
                        if phase == 'E2' and run == 'replay' and v == 'permutation_restoration':
                            run = 'replay-recovery-20261004T034600Z'
                        directory = f'{base}/executions/{run}/{v}'
                        self.run_record(directory, v, 'wrapper', family, apk)
                        records.append(directory + '/device/result.json')
                self.exact_files(base + '/executions', 'result.json', records)
            if family == 'original':
                base = root + '/E1'
                attempts = self.load(base + '/build-results-before-dependency-closure.json')
                require(sorted(x['variant'] for x in attempts) == sorted(PHASES['E1']), 'Wrong original initial builds')
                for row in attempts:
                    v = row['variant']
                    build = f'{base}/variants/{v}/build-before-dependency-closure'
                    expected_apks.append(build + '/consumer.apk')
                    self.apk(build, f'{base}/variants/{v}/model.tflite', v, row, 'original_initial_unexecuted')
        incomplete = 'payload/' + ROOTS['original'] + '/E2/executions/replay/permutation_restoration'
        files = [incomplete + '/logs/install.' + suffix for suffix in ['command.json', 'stderr', 'stdout']]
        self.exact_files(incomplete, '*', files)
        for name in files:
            self.read(name)
        p2 = 'payload/' + ROOTS['p2']
        for attempt, record_file, group in [('build', 'build-results.json', 'p2_executed'),
                                             ('build-attempt-1', 'build-results-attempt-1.json', 'p2_initial_unexecuted')]:
            rows = self.load(p2 + '/' + record_file)
            identities = [(x['consumer'], x['variant']) for x in rows]
            expected = [(c, v) for c in ['wrapper', 'task'] for v in P2_VARIANTS]
            require(sorted(identities) == sorted(expected), f'Wrong exact P2 build identities: {record_file}')
            for row in rows:
                c, v = row['consumer'], row['variant']
                build = f'{p2}/{attempt}/{c}/{v}'
                apk = build + '/consumer.apk'
                expected_apks.append(apk)
                self.apk(build, f'{p2}/variants/{v}/model.tflite', v, row, group)
                if attempt == 'build':
                    self.run_record(f'{p2}/executions/primary/{c}/{v}', v, c, 'p2', apk)
        records = [f'{p2}/executions/primary/{c}/{v}/device/result.json'
                   for c in ['wrapper', 'task'] for v in P2_VARIANTS]
        self.exact_files(p2 + '/executions', 'result.json', records)
        self.exact_files('payload', 'consumer.apk', expected_apks)
        shared_pairs = 0
        for v in P2_VARIANTS:
            if v == 'label_deletion':
                continue
            for name in INPUT_HASHES:
                wrapper = self.decoded[(f'{p2}/executions/primary/wrapper/{v}', name)]
                task = self.decoded[(f'{p2}/executions/primary/task/{v}', name)]
                require(wrapper == task, f'P2 shared score/label mismatch: {v}/{name}')
                shared_pairs += 1
        totals = {}
        for family in ROOTS:
            total = Counter()
            for record in self.records:
                if record['family'] == family:
                    total.update({k: v for k, v in record.items() if isinstance(v, int)})
            totals[family] = dict(total)
        require(totals == {
            'original': {'records': 16, 'observations': 32, 'raw_tensors': 32, 'decoded_lists': 28, 'caught_getter_failures': 4},
            'audit': {'records': 8, 'observations': 16, 'raw_tensors': 16, 'decoded_lists': 14, 'caught_getter_failures': 2},
            'p2': {'records': 10, 'observations': 18, 'raw_tensors': 10, 'decoded_lists': 16, 'caught_getter_failures': 2, 'constructor_failures': 1},
        }, f'Unexpected saved-record denominator: {totals}')
        return {'denominators': totals, 'interrupted_original_replay_attempts': 1,
                'p2_shared_successful_score_label_pairs': shared_pairs,
                'apk_counts': dict(Counter(row['group'] for row in self.apks))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--package', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True, help='New JSON report outside repository and package')
    args = parser.parse_args()
    package, output = args.package.resolve(), args.output.resolve()
    repo = Path(__file__).resolve().parents[2]
    require(not args.package.is_symlink() and package.is_dir(), 'Package must be an existing directory')
    require(not output.exists() and not args.output.is_symlink()
            and not any(p.is_symlink() for p in args.output.parents)
            and not output.is_relative_to(repo) and not output.is_relative_to(package),
            'Report must be a new nonsymlink file outside repository/package')
    report = {'created_utc': datetime.now(timezone.utc).isoformat(), 'package': str(package),
              'scope': 'Saved bytes only: 26 executed APK/model/asset identities, 14 separate initial build APKs, '
                       '34 complete saved run records and one interrupted attempt, payload lengths/hashes, '
                       'stages, category identities/score bits and eight P2 shared score/label pairs. '
                       'No model execution, device-pulled APK, P3/graph/code audit or human verification. '
                       'Does not independently authenticate the historical manifest trust anchor.'}
    inspection = None
    try:
        inspection = Inspection(package)
        report.update(inspection.inspect())
        report['status'] = 'PASS_BOUNDED_SAVED_EVIDENCE_CHECKS'
    except (OSError, ValueError, KeyError, TypeError, IndexError, zipfile.BadZipFile, struct.error) as error:
        report.update(status='FAIL_BOUNDED_SAVED_EVIDENCE_CHECKS', error_type=type(error).__name__, error=str(error))
    if inspection is not None:
        report.update(manifest_sha256=inspection.manifest_sha256, files_read=inspection.seen,
                      apks=inspection.apks, saved_records=inspection.records)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('x') as stream:
        stream.write(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ['files_read', 'apks', 'saved_records']}, indent=2))
    return 0 if report['status'].startswith('PASS') else 1


if __name__ == '__main__':
    raise SystemExit(main())
