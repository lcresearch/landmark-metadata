"""Exercise the maintained P2 reader with synthetic files, without model execution."""
import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import struct
import tempfile
import unittest
import zipfile


SCRIPT = Path(__file__).resolve().parents[1] / 'work/review-fixes-20261021/verify_p2_records.py'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def zipped(name, data):
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, 'w') as archive:
        archive.writestr(name, data)
    return stream.getvalue()


class P2ReadbackTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.scratch = Path(temporary.name)
        self.root = self.scratch / 'round'
        self.p2 = self.root / 'P2'
        spec = importlib.util.spec_from_file_location('p2_readback', SCRIPT)
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)
        self.seed()

    def write(self, path, value):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value))

    def folder(self, consumer='wrapper', variant='description_control'):
        return self.p2 / 'executions/primary' / consumer / variant / 'device'

    def seed(self):
        labels = [f'label-{i}' for i in range(1000)]
        labels[639] = labels[638]
        models, inputs, builds = {}, [], []
        for variant in self.module.VARIANTS:
            variant_labels = labels[:-1] if variant == 'label_deletion' else (
                labels[1:] + labels[:1] if variant == 'label_permutation' else labels)
            blob = zipped('labels_without_background.txt', ('\n'.join(variant_labels) + '\n').encode())
            path = self.p2 / 'models' / (variant + '.tflite')
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(blob)
            models[variant] = (blob, variant_labels)
            inputs.append({'variant': variant, 'path': str(path), 'sha256': digest(blob)})
        self.write(self.root / 'INPUTS.json', {'input_models': inputs})
        for consumer in self.module.CONSUMERS:
            for variant in self.module.VARIANTS:
                blob, variant_labels = models[variant]
                builds.append({'consumer': consumer, 'variant': variant})
                apk = self.p2 / 'build' / consumer / variant / 'consumer.apk'
                apk.parent.mkdir(parents=True, exist_ok=True)
                apk.write_bytes(zipped('assets/model.tflite', blob))
                folder = self.folder(consumer, variant)
                folder.mkdir(parents=True)
                rejected = consumer == 'task' and variant == 'label_deletion'
                report = {'platform': 'synthetic-api-30', 'api': 30, 'variant': variant,
                          'asset_identity_status': 'PASS', 'loaded_asset_sha256': digest(blob),
                          'model_loading_status' if consumer == 'wrapper' else 'model_initialization_status':
                          'FAIL' if rejected else 'PASS'}
                if rejected:
                    report.update({'earliest_failing_stage': 'model_initialization',
                                   'exception_type': 'java.lang.IllegalStateException',
                                   'cause_chain': [{'type': 'java.lang.IllegalArgumentException',
                                                    'message': self.module.TASK_MESSAGE}]})
                else:
                    report['observations'] = []
                    for name in self.module.CASES:
                        pixels = bytes([127]) * (224*224*3) if name == 'gray127' else bytes(
                            (37*i + 17) % 256 for i in range(224*224*3))
                        (folder / (name + '-input.rgb')).write_bytes(pixels)
                        raw = struct.pack('<1000f', *([0.25] * 1000))
                        case = {'input': name, 'input_sha256': digest(pixels), 'input_preparation_status': 'PASS'}
                        if consumer == 'wrapper':
                            (folder / (name + '-output-0.f32')).write_bytes(raw)
                            case.update({'inference_status': 'PASS', 'raw_output_observation_status': 'PASS',
                                         'raw_output_sha256': digest(raw), 'generated_getter_status': 'PASS'})
                            if variant == 'label_deletion':
                                case.update({'generated_getter_status': 'FAIL', 'earliest_failing_stage': 'generated_getter',
                                             'exception_type': 'java.lang.IllegalArgumentException',
                                             'exception_message': 'Label number 999 mismatch the shape on axis 1'})
                        else:
                            case['classify_inference_and_decoding_status'] = 'PASS'
                        if variant != 'label_deletion':
                            values = [{'list_position' if consumer == 'wrapper' else 'category_index_field': i,
                                       'score': 0.25, 'score_float_bits': struct.unpack('<I', struct.pack('<f', 0.25))[0],
                                       'label': label} for i, label in enumerate(variant_labels)]
                            if consumer == 'task':
                                values = [{'head_index': 0, 'categories': list(reversed(values))}]
                            self.write(folder / (name + '-decoded.json'), values)
                        report['observations'].append(case)
                self.write(folder / 'result.json', report)
        self.write(self.p2 / 'build-results.json', builds)
        for name in self.module.REQUIRED_INPUTS:
            path = self.p2 / name
            if not path.exists():
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('synthetic frozen input\n')
        for name in self.module.REQUIRED_SCRIPTS:
            path = self.p2 / 'scripts' / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('// synthetic source; never executed\n')
        self.freeze()

    def freeze(self):
        paths = [self.p2 / name for name in self.module.REQUIRED_INPUTS] + sorted(
            (self.p2 / 'build').glob('*/*/consumer.apk')) + sorted((self.p2 / 'scripts').glob('*'))
        self.write(self.p2 / 'EXECUTION_INPUT_FREEZE.json', {'files': [
            {'path': str(path.relative_to(self.p2)), 'sha256': digest(path.read_bytes())} for path in paths]})

    def readback(self, expected='FAIL'):
        result = self.module.verify(self.root, self.scratch / 'review.json')
        self.assertEqual(result['status'], expected, [c for c in result['checks'] if c['status'] == 'FAIL'])
        return result

    def change_report(self, transform, consumer='wrapper', variant='description_control'):
        path = self.folder(consumer, variant) / 'result.json'
        data = json.loads(path.read_text())
        transform(data)
        self.write(path, data)

    def test_complete_control_aligns_task_by_index_and_passes_all_sections(self):
        result = self.readback('PASS')
        self.assertEqual(set(result['sections'].values()), {'PASS'})
        self.assertEqual((result['configuration_records'], result['observed_input_records'],
                          result['decoded_lists'], result['wrapper_raw_tensors']), (10, 18, 16, 10))
        self.assertEqual(len(result['cross_consumer_returned_score_comparisons']), 8)
        self.assertFalse(result['model_experiments_run_by_review'])

    def test_internally_consistent_changed_scores_fail_historical_outcomes(self):
        for consumer in self.module.CONSUMERS:
            folder = self.folder(consumer)
            report = json.loads((folder / 'result.json').read_text())
            for case in report['observations']:
                name = case['input']
                path = folder / (name + '-decoded.json')
                values = json.loads(path.read_text())
                for value in values if consumer == 'wrapper' else values[0]['categories']:
                    value.update({'score': 0.5, 'score_float_bits': struct.unpack('<I', struct.pack('<f', 0.5))[0]})
                self.write(path, values)
                if consumer == 'wrapper':
                    raw = struct.pack('<1000f', *([0.5] * 1000))
                    (folder / (name + '-output-0.f32')).write_bytes(raw)
                    case['raw_output_sha256'] = digest(raw)
            self.write(folder / 'result.json', report)
        result = self.readback()
        self.assertEqual(result['sections'], {'evidence_validity': 'PASS', 'coverage': 'PASS', 'historical_outcomes': 'FAIL'})
        self.assertTrue(any(not c['same_score_bits'] for c in result['within_consumer_comparisons']))
        self.assertTrue(any(not c['equal_original'] for c in result['wrapper_raw_comparisons']))

    def test_missing_interventions_fail_coverage_and_stages(self):
        for consumer in self.module.CONSUMERS:
            for variant in self.module.VARIANTS[1:]:
                key = 'model_loading_status' if consumer == 'wrapper' else 'model_initialization_status'
                self.change_report(lambda r: r.update({key: 'FAIL', 'observations': []}), consumer, variant)
        result = self.readback()
        self.assertEqual(result['observed_input_records'], 4)
        self.assertEqual(result['sections']['coverage'], 'FAIL')
        self.assertEqual(result['sections']['historical_outcomes'], 'FAIL')

    def test_duplicate_input_names_are_rejected(self):
        self.change_report(lambda r: r['observations'].__setitem__(1, dict(r['observations'][0])))
        result = self.readback()
        self.assertTrue(any(c['name'].endswith('exact reached inputs') and c['status'] == 'FAIL' for c in result['checks']))

    def test_missing_decoded_file_fails_and_preserves_other_results(self):
        (self.folder() / 'gray127-decoded.json').unlink()
        result = self.readback()
        self.assertEqual(result['decoded_lists'], 15)
        self.assertEqual(result['sections']['evidence_validity'], 'FAIL')
        self.assertEqual(result['sections']['coverage'], 'FAIL')

    def test_missing_raw_file_fails(self):
        (self.folder() / 'gray127-output-0.f32').unlink()
        self.readback()

    def test_wrong_failure_stage_does_not_match_deletion_target(self):
        self.change_report(lambda r: r.update({'earliest_failing_stage': 'asset_identity'}), 'task', 'label_deletion')
        result = self.readback()
        self.assertEqual(result['sections']['historical_outcomes'], 'FAIL')

    def test_task_deletion_cannot_claim_later_classify_success(self):
        self.change_report(lambda r: r.update({'classify_inference_and_decoding_status': 'PASS'}), 'task', 'label_deletion')
        self.readback()

    def test_failed_preparation_is_not_hidden_by_valid_output(self):
        self.change_report(lambda r: r['observations'][0].update({'input_preparation_status': 'FAIL'}))
        self.readback()

    def test_missing_required_stage_key_reports_failure(self):
        self.change_report(lambda r: r['observations'][0].pop('inference_status'))
        result = self.readback()
        self.assertEqual(result['sections']['evidence_validity'], 'FAIL')

    def test_wrong_cross_consumer_score_is_detected(self):
        path = self.folder('task', 'original') / 'gray127-decoded.json'
        data = json.loads(path.read_text())
        data[0]['categories'][0].update({'score': 0.5, 'score_float_bits': struct.unpack('<I', struct.pack('<f', 0.5))[0]})
        self.write(path, data)
        result = self.readback()
        self.assertTrue(any(c['bitwise_differing_returned_scores'] == 1 for c in result['cross_consumer_returned_score_comparisons']))

    def test_duplicate_category_indices_fail(self):
        path = self.folder('task') / 'gray127-decoded.json'
        data = json.loads(path.read_text())
        data[0]['categories'][1]['category_index_field'] = data[0]['categories'][0]['category_index_field']
        self.write(path, data)
        self.readback()

    def test_empty_freeze_does_not_pass(self):
        self.write(self.p2 / 'EXECUTION_INPUT_FREEZE.json', {'files': []})
        result = self.readback()
        self.assertEqual(result['sections']['coverage'], 'FAIL')

    def test_apks_and_build_index_alone_do_not_establish_freeze_coverage(self):
        path = self.p2 / 'EXECUTION_INPUT_FREEZE.json'
        data = json.loads(path.read_text())
        data['files'] = [row for row in data['files'] if row['path'] == 'build-results.json' or row['path'].endswith('.apk')]
        self.write(path, data)
        result = self.readback()
        check = next(c for c in result['checks'] if c['name'].startswith('freeze covers'))
        self.assertIn('EXPERIMENT_P2_PLAN.md', check['missing'])
        self.assertIn('scripts/ContractInstrumentation.java', check['missing'])
        self.assertEqual(result['sections']['coverage'], 'FAIL')

    def test_new_script_also_requires_a_freeze_entry(self):
        (self.p2 / 'scripts/new_adapter.py').write_text('# synthetic new copied source\n')
        result = self.readback()
        check = next(c for c in result['checks'] if c['name'].startswith('freeze covers'))
        self.assertEqual(check['missing'], ['scripts/new_adapter.py'])

    def test_unfrozen_postprocessing_tools_can_be_added_after_execution(self):
        for name in self.module.POSTPROCESSING_SCRIPTS:
            (self.p2 / 'scripts' / name).write_text('# synthetic later postprocessing\n')
        self.readback('PASS')

    def test_explicitly_frozen_postprocessor_bytes_are_still_checked(self):
        path = self.p2 / 'scripts/normalize_results.py'
        path.write_text('# synthetic frozen postprocessing\n')
        self.freeze()
        path.write_text('# changed frozen bytes\n')
        result = self.readback()
        self.assertEqual(result['sections']['evidence_validity'], 'FAIL')

    def test_duplicate_build_identity_does_not_pass(self):
        path = self.p2 / 'build-results.json'
        data = json.loads(path.read_text())
        data[1] = dict(data[0])
        self.write(path, data)
        self.freeze()
        self.readback()

    def test_duplicate_model_identity_does_not_pass(self):
        path = self.root / 'INPUTS.json'
        data = json.loads(path.read_text())
        data['input_models'][1] = dict(data['input_models'][0])
        self.write(path, data)
        self.readback()

    def test_cli_returns_failure_for_malformed_json(self):
        (self.folder() / 'result.json').write_text('{')
        with contextlib.redirect_stdout(io.StringIO()):
            code = self.module.main(['--round-root', str(self.root), '--output', str(self.scratch / 'review.json')])
        self.assertEqual(code, 1)

    def test_nonfinite_json_number_is_reported_as_invalid_evidence(self):
        self.change_report(lambda r: r.update({'untrusted_extra_field': float('nan')}))
        result = self.readback()
        self.assertEqual(result['sections']['evidence_validity'], 'FAIL')

    def test_output_cannot_replace_a_review_or_write_into_evidence(self):
        output = self.scratch / 'existing.json'
        output.write_text('preserved')
        with self.assertRaises(FileExistsError):
            self.module.verify(self.root, output)
        self.assertEqual(output.read_text(), 'preserved')
        with self.assertRaises(ValueError):
            self.module.verify(self.root, self.root / 'review.json')
        self.assertFalse((self.root / 'review.json').exists())
        with self.assertRaises(ValueError):
            self.module.verify(self.root, SCRIPT.parent / 'not-created.json')


if __name__ == '__main__':
    unittest.main()
