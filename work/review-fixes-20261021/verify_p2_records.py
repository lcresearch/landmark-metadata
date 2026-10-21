#!/usr/bin/env python3
"""Read P2 saved files and explicitly test the recorded historical outcome targets.

This maintained reader leaves the original review script unchanged. A PASS is a
bounded consistency result, not authentication of an execution or a new model run.
Task comparisons concern returned category scores, never native raw tensors.
"""
import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import struct
import zipfile


REPOSITORY = Path(__file__).resolve().parents[2]
VARIANTS = ('original', 'description_control', 'label_deletion',
            'label_permutation', 'restoration')
CONSUMERS = ('wrapper', 'task')
CASES = ('gray127', 'rgb_pattern')
AREAS = ('evidence_validity', 'coverage', 'historical_outcomes')
REQUIRED_INPUTS = ('EXPERIMENT_P2_PLAN.md', 'PLAN_FREEZE.json',
                   'dependencies/resolved-lock.json', 'static-results.json', 'build-results.json')
# Preparation/build/runtime sources from the preserved P2 snapshot. Postprocessing
# tools may legitimately be added after execution; any explicitly frozen copy is
# still checked, but its later presence alone does not make the freeze incomplete.
REQUIRED_SCRIPTS = ('ContractInstrumentation.java', 'TaskInstrumentation.java',
                    'build.py', 'capture_versions.py', 'codegen_one.py',
                    'common.py', 'fetch_dependencies.py', 'freeze_execution_inputs.py',
                    'prepare.py', 'run.py', 'start_emulator.py')
POSTPROCESSING_SCRIPTS = ('analyze.py', 'normalize_results.py', 'write_report.py', 'seal_p2.py')
TASK_MESSAGE = 'Got 1000 class(es) for output index 0, expected 999 according to the label map.'
ERRORS = (OSError, ValueError, TypeError, KeyError, IndexError, OverflowError,
          struct.error, zipfile.BadZipFile)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def reject_constant(value):
    raise ValueError('Non-finite JSON number: ' + value)


def identities(rows, fields, expected):
    if not isinstance(rows, list) or any(not isinstance(row, dict) or
            any(not isinstance(row.get(field), str) for field in fields) for row in rows):
        return False
    return Counter(tuple(row[field] for field in fields) for row in rows) == Counter(expected)


def word(value):
    if type(value) is not int or not -(2**31) <= value < 2**32:
        raise ValueError('Expected a 32-bit score pattern')
    return value & 0xffffffff


class Reader:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.p2 = self.root / 'P2'
        self.checks = []
        self.files = {}
        self.units = []
        self.decoded = {}
        self.raw = {}
        self.platforms = set()

    def check(self, area, name, passed, **detail):
        self.checks.append({'area': area, 'name': name,
                            'status': 'PASS' if passed else 'FAIL', **detail})
        return bool(passed)

    def read_bytes(self, path):
        path = Path(path)
        data = path.read_bytes()
        self.files[str(path)] = sha(data)
        return data

    def load(self, path):
        return json.loads(self.read_bytes(path), parse_constant=reject_constant)

    def inputs_and_freeze(self):
        rows = self.load(self.root / 'INPUTS.json')['input_models']
        if not self.check('coverage', 'exact five model identities',
                          identities(rows, ('variant',), [(v,) for v in VARIANTS])):
            raise ValueError('INPUTS.json must name each of the five variants once')
        inputs = {row['variant']: row for row in rows}
        labels = {}
        names = None
        base_payload = None
        for variant in VARIANTS:
            row = inputs[variant]
            path = self.root / row['path']
            data = self.read_bytes(path)
            self.check('evidence_validity', variant + ': source model digest', sha(data) == row['sha256'])
            with zipfile.ZipFile(path) as archive:
                members = archive.namelist()
                if names is None:
                    names = members
                self.check('evidence_validity', variant + ': unique preserved associated filenames',
                           len(members) == len(set(members)) and members == names)
                payload = archive.read('labels_without_background.txt')
            labels[variant] = payload.decode('utf-8').splitlines()
            if base_payload is None:
                base_payload = payload
            base = labels['original']
            expected = base[:-1] if variant == 'label_deletion' else (
                base[1:] + base[:1] if variant == 'label_permutation' else base)
            self.check('historical_outcomes', variant + ': planned label resource', labels[variant] == expected)
            if variant in ('original', 'description_control', 'restoration'):
                self.check('historical_outcomes', variant + ': original resource bytes', payload == base_payload)
        self.check('coverage', 'original has 1000 labels', len(labels['original']) == 1000)

        frozen = self.load(self.p2 / 'EXECUTION_INPUT_FREEZE.json')['files']
        seen = set()
        for row in frozen:
            relative = Path(row['path'])
            path = (self.p2 / relative).resolve()
            if (relative.is_absolute() or '..' in relative.parts or
                    not path.is_relative_to(self.p2) or str(relative) in seen):
                raise ValueError('Unsafe or duplicate frozen input path')
            seen.add(str(relative))
            self.check('evidence_validity', 'frozen input ' + str(relative),
                       sha(self.read_bytes(path)) == row['sha256'])
        required = set(REQUIRED_INPUTS) | {'scripts/' + name for name in REQUIRED_SCRIPTS} | {
            f'build/{consumer}/{variant}/consumer.apk' for consumer in CONSUMERS for variant in VARIANTS}
        postprocessing = {'scripts/' + name for name in POSTPROCESSING_SCRIPTS}
        required.update(str(path.relative_to(self.p2)) for path in (self.p2 / 'scripts').rglob('*')
                        if path.is_file() and str(path.relative_to(self.p2)) not in postprocessing)
        self.check('coverage', 'freeze covers required plan, dependency, source and build inputs',
                   required <= seen, missing=sorted(required - seen))
        builds = self.load(self.p2 / 'build-results.json')
        self.check('coverage', 'exact ten build identities', identities(
            builds, ('consumer', 'variant'), [(c, v) for c in CONSUMERS for v in VARIANTS]))
        return inputs, labels

    def categories(self, path, consumer):
        values = self.load(path)
        if consumer == 'task':
            if not isinstance(values, list) or len(values) != 1 or values[0]['head_index'] != 0:
                raise ValueError('Expected exactly one Task head at index zero')
            values = values[0]['categories']
        key = 'list_position' if consumer == 'wrapper' else 'category_index_field'
        if not isinstance(values, list) or len(values) != 1000:
            raise ValueError('Expected 1000 categories')
        by_index = {}
        for value in values:
            index = value[key]
            if type(index) is not int or index in by_index or not 0 <= index < 1000:
                raise ValueError('Missing, duplicate or invalid category index')
            bits = word(value['score_float_bits'])
            score = value['score']
            if (type(score) not in (int, float) or not math.isfinite(score) or
                    struct.unpack('<I', struct.pack('<f', score))[0] != bits or
                    not isinstance(value['label'], str)):
                raise ValueError('Invalid score serialization or label')
            by_index[index] = {'score_float_bits': bits, 'label': value['label']}
        return [by_index[i] for i in range(1000)]

    def unit(self, consumer, variant, inputs, labels):
        prefix = consumer + '/' + variant
        folder = self.p2 / 'executions/primary' / consumer / variant / 'device'
        report = self.load(folder / 'result.json')
        platform, api = report['platform'], report['api']
        if not isinstance(platform, str) or not platform or type(api) is not int:
            raise ValueError('Invalid platform identity')
        self.platforms.add((platform, api))
        self.check('evidence_validity', prefix + ': device identifies variant', report['variant'] == variant)
        apk = self.p2 / 'build' / consumer / variant / 'consumer.apk'
        with zipfile.ZipFile(apk) as archive:
            if archive.namelist().count('assets/model.tflite') != 1:
                raise ValueError('Expected one APK model asset')
            asset = archive.read('assets/model.tflite')
        self.check('evidence_validity', prefix + ': APK/device/source asset identity',
                   report['asset_identity_status'] == 'PASS' and
                   sha(asset) == report['loaded_asset_sha256'] == inputs[variant]['sha256'])
        rejected = consumer == 'task' and variant == 'label_deletion'
        ctor = report['model_loading_status' if consumer == 'wrapper' else 'model_initialization_status']
        obs = report.get('observations', [])
        unit = {'consumer': consumer, 'variant': variant, 'constructor': ctor,
                'earliest_failing_stage': report.get('earliest_failing_stage'),
                'exception_type': report.get('exception_type'), 'exception_message': report.get('exception_message'),
                'cause_chain': report.get('cause_chain'),
                'observations': obs}
        self.units.append(unit)
        self.check('historical_outcomes', prefix + ': constructor outcome', ctor == ('FAIL' if rejected else 'PASS'))
        exact = identities(obs, ('input',), [] if rejected else [(n,) for n in CASES])
        self.check('coverage', prefix + ': exact reached inputs', exact)
        if rejected:
            chain = report.get('cause_chain', [])
            self.check('historical_outcomes', prefix + ': wrapped cardinality rejection',
                       report.get('earliest_failing_stage') == 'model_initialization' and
                       report.get('exception_type') == 'java.lang.IllegalStateException' and
                       isinstance(chain, list) and any(isinstance(x, dict) and
                           x.get('type') == 'java.lang.IllegalArgumentException' and
                           x.get('message') == TASK_MESSAGE for x in chain))
            self.check('coverage', prefix + ': no unreached input/output files',
                       not any(folder.glob('*-input.rgb')) and not any(folder.glob('*-decoded.json')) and
                       not any(folder.glob('*-output-0.f32')))
            self.check('historical_outcomes', prefix + ': later stages unreached',
                       all(report.get(stage, 'NOT_REACHED') == 'NOT_REACHED' for stage in
                           ('input_preparation_status', 'inference_status', 'classify_inference_and_decoding_status')))
            return
        self.check('historical_outcomes', prefix + ': no constructor failure marker',
                   not report.get('earliest_failing_stage') and not report.get('exception_type'))
        if not exact:
            return
        for case in obs:
            name = case['input']
            key = prefix + '/' + name
            try:
                pixels = self.read_bytes(folder / (name + '-input.rgb'))
                expected = bytes([127]) * (224*224*3) if name == 'gray127' else bytes(
                    (37*i + 17) % 256 for i in range(224*224*3))
                self.check('evidence_validity', key + ': prescribed input bytes',
                           pixels == expected and sha(pixels) == case['input_sha256'])
                self.check('historical_outcomes', key + ': input preparation', case['input_preparation_status'] == 'PASS')
                if consumer == 'wrapper':
                    self.check('historical_outcomes', key + ': process and raw observation',
                               case['inference_status'] == 'PASS' and case['raw_output_observation_status'] == 'PASS')
                    raw = self.read_bytes(folder / (name + '-output-0.f32'))
                    if not self.check('evidence_validity', key + ': raw length and digest',
                                      len(raw) == 4000 and sha(raw) == case['raw_output_sha256']):
                        continue
                    self.raw[(variant, name)] = raw
                    deletion = variant == 'label_deletion'
                    self.check('historical_outcomes', key + ': generated getter outcome',
                               case['generated_getter_status'] == ('FAIL' if deletion else 'PASS'))
                    if deletion:
                        self.check('historical_outcomes', key + ': getter cardinality rejection',
                                   case.get('earliest_failing_stage') == 'generated_getter' and
                                   case.get('exception_type') == 'java.lang.IllegalArgumentException' and
                                   case.get('exception_message') == 'Label number 999 mismatch the shape on axis 1')
                        self.check('coverage', key + ': no rejected getter output',
                                   not (folder / (name + '-decoded.json')).exists())
                        continue
                else:
                    self.check('historical_outcomes', key + ': atomic classify outcome',
                               case['classify_inference_and_decoding_status'] == 'PASS')
                self.check('historical_outcomes', key + ': no later failure marker',
                           not case.get('earliest_failing_stage') and not case.get('exception_type'))
                values = self.categories(folder / (name + '-decoded.json'), consumer)
                self.decoded[(consumer, variant, name)] = values
                self.check('historical_outcomes', key + ': labels match associated resource',
                           [v['label'] for v in values] == labels[variant])
                if consumer == 'wrapper':
                    self.check('evidence_validity', key + ': returned scores match raw bits',
                               [v['score_float_bits'] for v in values] == list(struct.unpack('<1000I', raw)))
            except ERRORS as exc:
                self.check('evidence_validity', key + ': readable complete files', False, error=f'{type(exc).__name__}: {exc}')

    def run(self):
        try:
            inputs, labels = self.inputs_and_freeze()
            for consumer in CONSUMERS:
                for variant in VARIANTS:
                    try:
                        self.unit(consumer, variant, inputs, labels)
                    except ERRORS as exc:
                        self.check('evidence_validity', consumer + '/' + variant + ': readable record',
                                   False, error=f'{type(exc).__name__}: {exc}')
        except ERRORS as exc:
            self.check('evidence_validity', 'readable input and freeze records', False, error=f'{type(exc).__name__}: {exc}')
        observed = sum(len(unit['observations']) for unit in self.units if isinstance(unit['observations'], list))
        for name, actual, expected in [('configuration_records', len(self.units), 10),
                ('observed_input_records', observed, 18), ('decoded_lists', len(self.decoded), 16),
                ('wrapper_raw_tensors', len(self.raw), 10)]:
            self.check('coverage', name, actual == expected, observed=actual, expected=expected)
        self.check('historical_outcomes', 'same API-30 platform',
                   len(self.platforms) == 1 and next(iter(self.platforms))[1] == 30 if self.platforms else False)
        comparisons, raw_comparisons, cross = [], [], []
        for (consumer, variant, name), values in self.decoded.items():
            base = self.decoded.get((consumer, 'original', name))
            same = base is not None and all(a['score_float_bits'] == b['score_float_bits'] for a, b in zip(values, base))
            changed = sum(a['label'] != b['label'] for a, b in zip(values, base)) if base else None
            comparisons.append({'consumer': consumer, 'variant': variant, 'input': name,
                                'same_score_bits': same, 'changed_label_count': changed})
            self.check('historical_outcomes', f'{consumer}/{variant}/{name}: score preservation', same)
            self.check('historical_outcomes', f'{consumer}/{variant}/{name}: historical changed-label count',
                       changed == (999 if variant == 'label_permutation' else 0))
        for (variant, name), raw in self.raw.items():
            same = raw == self.raw.get(('original', name))
            raw_comparisons.append({'variant': variant, 'input': name, 'equal_original': same})
            self.check('historical_outcomes', f'wrapper/{variant}/{name}: raw preservation', same)
        for variant in VARIANTS:
            if variant == 'label_deletion':
                continue
            for name in CASES:
                left = self.decoded.get(('wrapper', variant, name))
                right = self.decoded.get(('task', variant, name))
                available = left is not None and right is not None
                mismatch = sum(a['score_float_bits'] != b['score_float_bits'] for a, b in zip(left, right)) if available else None
                labels = sum(a['label'] != b['label'] for a, b in zip(left, right)) if available else None
                cross.append({'variant': variant, 'input': name, 'available': available,
                              'bitwise_differing_returned_scores': mismatch, 'label_disagreements': labels})
                self.check('historical_outcomes', f'{variant}/{name}: cross-consumer returned scores and labels',
                           available and mismatch == 0 and labels == 0)
        sections = {area: 'PASS' if any(c['area'] == area for c in self.checks) and
                    all(c['status'] == 'PASS' for c in self.checks if c['area'] == area) else 'FAIL' for area in AREAS}
        return {'status': 'PASS' if all(v == 'PASS' for v in sections.values()) else 'FAIL',
                'sections': sections, 'checks': self.checks, 'configuration_records': len(self.units),
                'observed_input_records': observed, 'decoded_lists': len(self.decoded), 'wrapper_raw_tensors': len(self.raw),
                'units': self.units, 'within_consumer_comparisons': comparisons,
                'wrapper_raw_comparisons': raw_comparisons, 'cross_consumer_returned_score_comparisons': cross,
                'read_file_sha256': self.files, 'model_experiments_run_by_review': False, 'human_verification': False,
                'scope': 'Saved-file consistency against P2 historical targets; no execution authentication, new inference, or native Task raw-tensor comparison.'}


def verify(round_root, output):
    root, output = Path(round_root).resolve(), Path(output)
    if output.exists() or output.is_symlink():
        raise FileExistsError('Preserve previous reviews; choose a fresh output path')
    if output.resolve().is_relative_to(root) or output.resolve().is_relative_to(REPOSITORY):
        raise ValueError('Write the review outside both the evidence round and source checkout')
    result = Reader(root).run()
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('x') as stream:
        json.dump(result, stream, indent=2, allow_nan=False)
        stream.write('\n')
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--round-root', type=Path, required=True, help='Saved round containing INPUTS.json and P2/')
    parser.add_argument('--output', type=Path, required=True, help='New JSON report outside evidence and checkout')
    args = parser.parse_args(argv)
    try:
        result = verify(args.round_root, args.output)
    except (OSError, ValueError) as exc:
        parser.exit(1, f'{type(exc).__name__}: {exc}\n')
    print(json.dumps({'status': result['status'], 'sections': result['sections'], 'output': str(args.output)}, indent=2))
    return 0 if result['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
