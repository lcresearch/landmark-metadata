"""Exercise the maintained readback with synthetic evidence, without ML dependencies."""
import contextlib
import hashlib
import importlib.util
import io
import json
from collections import Counter
from pathlib import Path
import struct
import tempfile
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / 'work/observation-review-20261004/verify_observations.py'


class ReadbackTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        spec = importlib.util.spec_from_file_location('observation_review', SCRIPT)
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)
        # Redirect the actual reader's absolute evidence paths, retaining file I/O.
        self.module.Path = lambda value: (
            self.root / str(value).removeprefix('/workspace/')
            if str(value).startswith('/workspace/') else Path(value))

    def write(self, relative, value):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value))
        return path

    def assert_checks_pass(self):
        self.assertTrue(self.module.checks)
        self.assertEqual([row for row in self.module.checks if not row['passed']], [])

    def seed_hand(self):
        bits = b'synthetic float bits'
        decoded = {'handedness': [['synthetic']], 'hand_landmarks': [[0] * 21],
                   'hand_world_landmarks': [[0] * 21]}
        for phase in ('primary', 'replay'):
            self.write(f'repro-hand/executions/{phase}/results.json',
                       [{'variant': variant, 'exit_code': 0, 'completed': True}
                        for variant in reversed(self.module.HAND_VARIANTS)])
            for variant in self.module.HAND_VARIANTS:
                folder = f'repro-hand/executions/{phase}/{variant}/outputs'
                self.write(folder + '/decoded.json', decoded)
                self.write(folder + '/result.json', {
                    'initialization_status': 'PASS', 'input_preparation_status': 'PASS',
                    'detect_status': 'PASS',
                    'decoded_float_bits_sha256': hashlib.sha256(bits).hexdigest()})
                (self.root / folder / 'decoded-float-bits.bin').write_bytes(bits)

    def test_hand_accepts_all_eight_records_in_any_manifest_order(self):
        self.seed_hand()
        result = self.module.hand()
        self.assertTrue(result['complete'])
        self.assertEqual(result['execution_records_read'], 8)
        self.assertEqual({(r['phase'], r['variant']) for r in result['records']},
                         {(phase, variant) for phase in ('primary', 'replay')
                          for variant in self.module.HAND_VARIANTS})
        self.assert_checks_pass()

    def test_hand_rejects_empty_missing_duplicate_and_unknown_variants_in_each_phase(self):
        self.seed_hand()
        variants = list(self.module.HAND_VARIANTS)
        for phase in ('primary', 'replay'):
            for bad in ([], variants[:-1], variants[:-1] + [variants[0]],
                        variants + [variants[0]], variants[:-1] + ['unknown']):
                with self.subTest(phase=phase, variants=bad):
                    self.seed_hand()
                    self.module.checks.clear()
                    self.write(f'repro-hand/executions/{phase}/results.json',
                               [{'variant': v, 'exit_code': 0} for v in bad])
                    result = self.module.hand()
                    self.assertFalse(result['complete'])
                    self.assertEqual(result['execution_records_read'], 0)
                    failure = next(r for r in self.module.checks if not r['passed'])
                    self.assertEqual(failure['check'], f'hand/{phase}/exact_four_conditions')

    def test_invalid_manifest_is_rejected_before_any_output_is_read(self):
        for manifest in ({}, None, [{}], [{'variant': None}], [{'variant': ['original']}]):
            with self.subTest(manifest=manifest):
                self.module.checks.clear()
                for phase in ('primary', 'replay'):
                    self.write(f'repro-hand/executions/{phase}/results.json', manifest)
                self.assertFalse(self.module.hand()['complete'])
                self.assertEqual(sum(not r['passed'] for r in self.module.checks), 2)

    def test_hand_rejects_failed_or_missing_preparation_and_controller_completion(self):
        for phase in ('primary', 'replay'):
            for field, value in [('input_preparation_status', 'FAIL'),
                                 ('input_preparation_status', None),
                                 ('detect_status', 'FAIL'),
                                 ('completed', False), ('completed', None)]:
                with self.subTest(phase=phase, field=field, value=value):
                    self.seed_hand()
                    self.module.checks.clear()
                    if field == 'completed':
                        path = self.root / f'repro-hand/executions/{phase}/results.json'
                        rows = json.loads(path.read_text())
                        row = next(row for row in rows if row['variant'] == 'metadata_exchange')
                    else:
                        path = self.root / f'repro-hand/executions/{phase}/metadata_exchange/outputs/result.json'
                        rows = row = json.loads(path.read_text())
                    if value is None:
                        row.pop(field)
                    else:
                        row[field] = value
                    path.write_text(json.dumps(rows))
                    result = self.module.hand()
                    self.assertFalse(result['complete'])
                    self.assertEqual(result['execution_records_read'], 7)
                    self.assertNotIn({'phase': phase, 'variant': 'metadata_exchange'}, result['records'])
                    self.assertEqual([r['check'] for r in self.module.checks if not r['passed']],
                                     [f'hand/{phase}/metadata_exchange/actual_completed'])
        self.assert_main_status(1)
        report = json.loads((self.root / 'report/observation-readback.json').read_text())
        self.assertFalse(report['hand']['complete'])
        self.assertEqual(report['hand']['execution_records_read'], 7)

    def test_hand_still_checks_output_shape_and_bits_before_counting_completion(self):
        self.seed_hand()
        folder = self.root / 'repro-hand/executions/replay/restoration/outputs'
        decoded = json.loads((folder / 'decoded.json').read_text())
        decoded['hand_landmarks'][0].pop()
        (folder / 'decoded.json').write_text(json.dumps(decoded))
        (folder / 'decoded-float-bits.bin').write_bytes(b'changed')
        result = self.module.hand()
        self.assertFalse(result['complete'])
        self.assertEqual(result['execution_records_read'], 7)
        failures = {r['check'] for r in self.module.checks if not r['passed']}
        self.assertEqual(failures, {'hand/replay/restoration/' + name for name in
                                   ('one_hand_21_landmarks',
                                    'decoded_equal', 'exact_float_bits_equal')})

    def test_main_rejects_empty_hand_and_writes_failed_report(self):
        for phase in ('primary', 'replay'):
            self.write(f'repro-hand/executions/{phase}/results.json', [])
        self.assert_main_status(1)
        report = json.loads((self.root / 'report/observation-readback.json').read_text())
        self.assertEqual(report['failed'], 2)
        self.assertFalse(report['hand']['complete'])

    def assert_main_status(self, expected):
        # Keep the Hand reader and aggregation real; unrelated evidence is out of scope.
        with contextlib.ExitStack() as stack:
            for section in ('task', 'external', 'android_code', 'preflight'):
                stack.enter_context(patch.object(self.module, section, return_value={}))
            stack.enter_context(patch.object(self.module, 'android', return_value={
                'complete': True, 'completed_execution_records': 16, 'missing': []}))
            stack.enter_context(contextlib.redirect_stdout(io.StringIO()))
            self.assertEqual(self.module.main(self.root / 'report'), expected)

    def test_main_accepts_complete_hand_and_preserves_existing_report(self):
        self.seed_hand()
        self.assert_main_status(0)
        path = self.root / 'report/observation-readback.json'
        original = path.read_bytes()
        with self.assertRaises(FileExistsError):
            self.assert_main_status(0)
        self.assertEqual(path.read_bytes(), original)

    def baseline_rows(self):
        rows = []
        for variant in self.module.CORE_VARIANTS:
            experiment = 'E2' if variant == 'label_permutation' else 'E1'
            path = self.root / f'repro-android/{experiment}/variants/{variant}/model.tflite'
            path.parent.mkdir(parents=True, exist_ok=True)
            if not path.exists():
                path.write_bytes(f'synthetic core {variant}'.encode())
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            for mode, status in zip(self.module.BASELINE_MODES,
                                    ('READABLE', 'ACCEPTED', 'COMPATIBLE_PRECONDITIONS', 'PASS')):
                if variant == 'label_deletion':
                    status = {'simple_baseline': 'INCOMPATIBLE', 'task_init': 'FAIL'}.get(mode, status)
                rows.append({'variant': variant, 'mode': mode,
                             'result': {'status': status, 'model_sha256': digest}})
        return rows

    def test_task_baseline_accepts_reordering_and_rejects_replaced_identity(self):
        rows = self.baseline_rows()
        self.write('repro-task/baseline-results.json', list(reversed(rows)))
        self.module.task_baseline()
        self.assert_checks_pass()
        for bad in ([], rows[:-1], rows[:-1] + rows[:1]):
            with self.subTest(count=len(bad)):
                self.module.checks.clear()
                self.write('repro-task/baseline-results.json', bad)
                self.module.task_baseline()
                self.assertFalse(self.module.checks[0]['passed'])

    def test_android_rejects_duplicate_inputs_before_following_artifacts(self):
        for inputs in ([], ['gray127'], ['gray127', 'gray127'], ['gray127', 'unknown']):
            with self.subTest(inputs=inputs):
                self.module.checks.clear()
                self.write('repro-android/E1/executions/primary/original/device/result.json',
                           {'observations': [{'input': value} for value in inputs]})
                result = self.module.android()
                self.assertFalse(result['complete'])
                self.assertEqual(result['completed_execution_records'], 0)
                self.assertFalse(self.module.checks[0]['passed'])
                self.assertIn('input identities', result['missing'][0])

    def seed_builds(self):
        for experiment, variants in self.module.ANDROID_VARIANTS.items():
            rows = []
            for variant in variants:
                base = self.root / 'repro-android' / experiment / 'variants' / variant
                relative = ['generated/src/main/java/org/example/contract/ContractModel.java',
                            'build/classes/ContractModel.class', 'build/classes/ContractModel$Inputs.class',
                            'build/classes/ContractModel$Outputs.class', 'build/dex/classes.dex']
                for name in relative:
                    path = base / name
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(b'synthetic ' + name.encode())
                digest = lambda name: hashlib.sha256((base / name).read_bytes()).hexdigest()
                rows.append({'variant': variant,
                             'generated_class_hashes': {Path(n).name: digest(n) for n in relative[1:4]},
                             'dex_hashes': {'classes.dex': digest(relative[4])},
                             'stages': {str(i): {'status': 'PASS', 'exit_code': 0} for i in range(6)}})
            self.write(f'repro-android/{experiment}/build-results.json', list(reversed(rows)))

    def test_build_readback_accepts_all_conditions_and_rejects_duplicate_replacement(self):
        self.seed_builds()
        self.module.android_code()
        self.assert_checks_pass()
        for experiment in self.module.ANDROID_VARIANTS:
            with self.subTest(experiment=experiment):
                self.seed_builds()
                path = self.root / 'repro-android' / experiment / 'build-results.json'
                rows = json.loads(path.read_text())
                rows[-1] = rows[0]
                path.write_text(json.dumps(rows))
                self.module.checks.clear()
                result = self.module.android_code()
                self.assertEqual(result['generated_sources'], 4)
                check = next(r for r in self.module.checks
                             if r['check'] == f'code/{experiment}/exact_four_builds')
                self.assertFalse(check['passed'])

    def seed_task(self):
        labels = [f'label-{i}' for i in range(1000)]
        labels[1] = labels[0]  # One adjacent duplicate yields 999 changed strings.
        inputs = {'gray127': bytes([127]) * (224*224*3),
                  'rgb_pattern': bytes((37*i+17) % 256 for i in range(224*224*3))}
        input_dir = self.root / 'repro-task/inputs'
        input_dir.mkdir(parents=True, exist_ok=True)
        for name, payload in inputs.items():
            (input_dir / f'{name}-input.rgb').write_bytes(payload)
        for phase in ('primary', 'replay'):
            for variant in self.module.CORE_VARIANTS:
                folder = f'repro-task/{phase}/{variant}'
                result = {'initialization_status': 'PASS', 'classify_status': 'PASS',
                          'inference_status': 'PASS', 'decoder_status': 'PASS',
                          'observations': []}
                if variant == 'label_deletion':
                    result.update(initialization_status='FAIL', classify_status='NOT_REACHED',
                                  inference_status='NOT_REACHED', decoder_status='NOT_REACHED',
                                  exception_type='ValueError',
                                  exception_message='Got 1000 class(es) for output index 0, expected 999 according to the label map.')
                else:
                    for case_id, name in enumerate(inputs):
                        categories = []
                        for index in range(1000):
                            score = struct.unpack('<f', struct.pack('<f', (index+case_id)/1000))[0]
                            categories.append({'index': index, 'score': score,
                                               'score_float_bits': struct.unpack('<I', struct.pack('<f', score))[0],
                                               'label': labels[(index+(variant == 'label_permutation')) % 1000]})
                        self.write(f'{folder}/{name}-decoded.json',
                                   [{'head_index': 0, 'categories': categories}])
                        result['observations'].append({
                            'input': name, 'input_sha256': hashlib.sha256(inputs[name]).hexdigest(),
                            'input_preparation_status': 'PASS', 'classify_status': 'PASS',
                            'returned_categories': 1000})
                    result['observations'].reverse()
                self.write(f'{folder}/result.json', result)
        self.write('repro-task/baseline-results.json', self.baseline_rows())

    def change_task_result(self, observations, phase='replay', variant='description_control'):
        path = self.root / f'repro-task/{phase}/{variant}/result.json'
        result = json.loads(path.read_text())
        if observations is None:
            result.pop('observations')
        else:
            result['observations'] = observations
        path.write_text(json.dumps(result))

    def test_task_accepts_complete_reordered_input_records(self):
        self.seed_task()
        result = self.module.task()
        self.assertEqual(result['successful_decoded_observations'], 16)
        self.assertEqual(result['categories_read'], 16000)
        self.assert_checks_pass()

    def test_task_rejects_missing_duplicate_or_malformed_inputs_before_decoded_read(self):
        self.seed_task()
        folder = self.root / 'repro-task/replay/description_control'
        valid = json.loads((folder / 'result.json').read_text())['observations']
        for path in folder.glob('*-decoded.json'):
            path.unlink()
        for observations in (None, [], valid[:1], valid[:1]*2,
                             [{'input': 'unknown'}, valid[0]], {}, [{'input': None}]):
            with self.subTest(observations=observations):
                self.change_task_result(observations)
                self.module.checks.clear()
                result = self.module.task()
                self.assertEqual(result['successful_decoded_observations'], 14)
                failed = [r['check'] for r in self.module.checks if not r['passed']]
                self.assertEqual(failed, ['replay/description_control/exact_two_inputs'])
                # Restore this result's observations field after testing its absence.
                self.change_task_result(valid)

    def test_task_old_empty_and_contradictory_record_counterexamples_fail(self):
        self.seed_task()
        for phase in ('primary', 'replay'):
            for variant in self.module.CORE_VARIANTS:
                if variant != 'label_deletion':
                    self.change_task_result([], phase, variant)
        result = self.module.task()
        self.assertEqual(result['successful_decoded_observations'], 0)
        self.assertEqual(sum(not r['passed'] for r in self.module.checks), 8)
        self.seed_task()
        bad = {'input': 'gray127', 'input_sha256': '0'*64,
               'input_preparation_status': 'FAIL', 'classify_status': 'NOT_REACHED',
               'returned_categories': 0}
        self.change_task_result([bad, bad], 'primary', 'original')
        self.module.checks.clear()
        result = self.module.task()
        self.assertEqual(result['successful_decoded_observations'], 8)
        self.assertTrue(any(not row['passed'] for row in self.module.checks))

    def test_task_rejects_failed_input_status_count_and_hash(self):
        self.seed_task()
        path = self.root / 'repro-task/replay/description_control/result.json'
        valid = json.loads(path.read_text())['observations']
        for field, value in [('input_preparation_status', 'FAIL'),
                             ('classify_status', 'NOT_REACHED'),
                             ('returned_categories', 0), ('input_sha256', '0'*64)]:
            with self.subTest(field=field):
                changed = [dict(row) for row in valid]
                changed[0][field] = value
                self.change_task_result(changed)
                self.module.checks.clear()
                result = self.module.task()
                self.assertEqual(result['successful_decoded_observations'], 15)
                self.assertEqual(sum(not row['passed'] for row in self.module.checks), 1)

    def test_task_requires_prescribed_input_bytes_even_with_matching_record_hash(self):
        self.seed_task()
        input_path = self.root / 'repro-task/inputs/gray127-input.rgb'
        input_path.write_bytes(b'wrong input')
        for phase in ('primary', 'replay'):
            for variant in self.module.CORE_VARIANTS:
                if variant == 'label_deletion':
                    continue
                path = self.root / f'repro-task/{phase}/{variant}/result.json'
                result = json.loads(path.read_text())
                for row in result['observations']:
                    if row['input'] == 'gray127':
                        row['input_sha256'] = hashlib.sha256(input_path.read_bytes()).hexdigest()
                path.write_text(json.dumps(result))
        result = self.module.task()
        self.assertEqual(result['successful_decoded_observations'], 8)
        self.assertEqual(sum(not row['passed'] for row in self.module.checks), 8)
        input_path.unlink()
        self.module.checks.clear()
        result = self.module.task()
        self.assertEqual(result['successful_decoded_observations'], 8)
        self.assertEqual(sum(not row['passed'] for row in self.module.checks), 8)

    def test_task_still_requires_full_decoded_indices_scores_and_labels(self):
        self.seed_task()
        path = self.root / 'repro-task/replay/description_control/rgb_pattern-decoded.json'
        original = path.read_text()
        for field, value in [('index', 0), ('score_float_bits', 0), ('label', 'wrong label')]:
            with self.subTest(field=field):
                decoded = json.loads(original)
                decoded[0]['categories'][-1][field] = value
                path.write_text(json.dumps(decoded))
                self.module.checks.clear()
                result = self.module.task()
                self.assertEqual(result['successful_decoded_observations'], 15)
                self.assertTrue(any(not row['passed'] for row in self.module.checks))

    def seed_e5(self):
        counts = Counter({'INCOMPATIBLE': 27, 'NOT_REACHED': 11,
                          'INAPPLICABLE_NO_SELECTED_GETTER': 14, 'ABSTAIN_NO_METADATA': 2,
                          'ABSTAIN': 3, 'COMPATIBLE_PRECONDITIONS': 8})
        decoder = ['COMPATIBLE_PRECONDITIONS', 'COMPATIBLE_PRECONDITIONS', 'INCOMPATIBLE',
                   'COMPATIBLE_PRECONDITIONS', 'COMPATIBLE_PRECONDITIONS']
        counts.subtract(decoder)
        decoder.extend(status for status, count in counts.items() for _ in range(count))
        fixtures = []
        for i, d_status in enumerate(decoder):
            s_status = ('REJECTED_BY_METADATA_POPULATOR_0_4_4' if d_status == 'NOT_REACHED'
                        else 'ABSTAIN_NO_METADATA' if d_status == 'ABSTAIN_NO_METADATA'
                        else 'ACCEPTED_BY_METADATA_POPULATOR_0_4_4')
            path = self.root / f'fixture-{i}'
            path.write_bytes(f'synthetic fixture {i}'.encode())
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            report = {'artifact_sha256': digest, 'STRUCTURAL': {'status': s_status},
                      'DECODER_COMPATIBILITY': {'status': d_status},
                      'REFERENCE_BACKED_SEMANTIC': {'status': 'ABSTAIN'}}
            fixtures.append({'path': str(path), 'model_sha256': digest, 'report': report})
            self.write(f'repro-external/E5/checks/{digest}/result.json', report)
        baseline = self.baseline_rows()
        for i, variant in enumerate(self.module.CORE_VARIANTS):
            experiment = 'E2' if variant == 'label_permutation' else 'E1'
            path = self.root / f'repro-android/{experiment}/variants/{variant}/model.tflite'
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(Path(fixtures[i]['path']).read_bytes())
            for row in baseline:
                if row['variant'] == variant:
                    row['result']['model_sha256'] = fixtures[i]['model_sha256']
        self.write('repro-task/baseline-results.json', baseline)
        self.write('repro-external/E5/results.json', {'fixtures': list(reversed(fixtures))})
        manifest = self.write('frozen-e5.json', {'artifact_sha256s': [f['model_sha256'] for f in fixtures]})
        return fixtures, manifest, hashlib.sha256(manifest.read_bytes()).hexdigest()

    def test_e5_accepts_exact_frozen_identities_in_reordered_catalog(self):
        _, manifest, digest = self.seed_e5()
        result = self.module.preflight(manifest, digest)
        self.assertTrue(result['complete'])
        self.assertEqual(result['fixtures'], 65)
        self.assert_checks_pass()

    def test_baseline_and_e5_reject_same_status_substitutions_for_every_mode(self):
        fixtures, manifest, digest = self.seed_e5()
        path = self.root / 'repro-task/baseline-results.json'
        original = path.read_text()
        for mode in self.module.BASELINE_MODES:
            with self.subTest(mode=mode):
                rows = json.loads(original)
                for i, variant in enumerate(self.module.CORE_VARIANTS):
                    expected = fixtures[i]
                    replacement = next(f for f in fixtures
                                       if f['model_sha256'] != expected['model_sha256'] and
                                       f['report']['DECODER_COMPATIBILITY']['status'] ==
                                       expected['report']['DECODER_COMPATIBILITY']['status'])
                    row = next(row for row in rows if row['variant'] == variant and row['mode'] == mode)
                    row['result']['model_sha256'] = replacement['model_sha256']
                path.write_text(json.dumps(rows))
                self.module.checks.clear()
                self.assertIsNone(self.module.task_baseline())
                failed = [r['check'] for r in self.module.checks if not r['passed']]
                self.assertEqual(len(failed), 5)
                self.assertTrue(all(name.endswith('/exact_core_artifact') for name in failed))
                self.module.checks.clear()
                result = self.module.preflight(manifest, digest)
                self.assertFalse(result['complete'])
                self.assertIsNone(result['core_extra_rejections_over_simple_and_Task_init'])
                self.assertEqual(sum(not r['passed'] for r in self.module.checks), 5)
        self.assert_section_main('preflight', 1, required_manifest=manifest,
                                 required_manifest_sha256=digest)

    def test_baseline_rejects_missing_digest_and_missing_expected_model(self):
        rows = self.baseline_rows()
        rows[0]['result'].pop('model_sha256')
        self.write('repro-task/baseline-results.json', rows)
        self.assertIsNone(self.module.task_baseline())
        self.assertEqual([r['check'] for r in self.module.checks if not r['passed']],
                         ['baseline/original/displayer/exact_core_artifact'])
        rows = self.baseline_rows()
        self.write('repro-task/baseline-results.json', rows)
        (self.root / 'repro-android/E1/variants/original/model.tflite').unlink()
        self.module.checks.clear()
        self.assertIsNone(self.module.task_baseline())
        self.assertEqual(sum(not r['passed'] for r in self.module.checks), 5)

    def test_e5_rejects_missing_wrong_or_malformed_manifest_before_catalog_read(self):
        for kind in ('missing', 'wrong_digest', 'malformed', 'wrong_count'):
            with self.subTest(kind=kind):
                manifest = self.root / 'frozen-e5.json'
                manifest.write_text('not JSON' if kind == 'malformed' else '{"artifact_sha256s": []}')
                digest = hashlib.sha256(manifest.read_bytes()).hexdigest()
                if kind == 'missing':
                    manifest.unlink()
                elif kind == 'wrong_digest':
                    digest = '0'*64
                self.module.checks.clear()
                result = self.module.preflight(manifest, digest)
                self.assertFalse(result['complete'])
                self.assertEqual(self.module.checks[0]['check'], 'E5/frozen_required_manifest')
                self.assertFalse(self.module.checks[0]['passed'])

    def test_e5_rejects_incomplete_duplicate_and_substituted_catalog_before_payloads(self):
        for kind in ('missing', 'duplicate', 'substituted'):
            with self.subTest(kind=kind):
                fixtures, manifest, digest = self.seed_e5()
                if kind == 'missing':
                    fixtures.pop()
                elif kind == 'duplicate':
                    fixtures[-1] = fixtures[0]
                else:
                    replacement = fixtures[-1]
                    path = Path(replacement['path'])
                    path.write_bytes(b'fixture absent from the frozen original manifest')
                    replacement['model_sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
                    replacement['report']['artifact_sha256'] = replacement['model_sha256']
                    self.write(f"repro-external/E5/checks/{replacement['model_sha256']}/result.json",
                               replacement['report'])
                self.write('repro-external/E5/results.json', {'fixtures': fixtures})
                Path(fixtures[0]['path']).unlink()  # Identity failure must precede any model read.
                self.module.checks.clear()
                result = self.module.preflight(manifest, digest)
                self.assertFalse(result['complete'])
                self.assertEqual([r['check'] for r in self.module.checks if not r['passed']],
                                 ['E5/exact_required_65'])
                self.assertFalse(any('/counts' in row['check'] for row in self.module.checks))

    def assert_section_main(self, section, expected, **kwargs):
        with contextlib.ExitStack() as stack:
            for other in ('task', 'hand', 'external', 'android_code', 'preflight'):
                if other != section:
                    stack.enter_context(patch.object(self.module, other, return_value={}))
            stack.enter_context(patch.object(self.module, 'android', return_value={
                'complete': True, 'completed_execution_records': 16, 'missing': []}))
            stack.enter_context(contextlib.redirect_stdout(io.StringIO()))
            self.assertEqual(self.module.main(self.root / 'report', **kwargs), expected)

    def test_task_failed_records_make_aggregate_fail_and_preserve_report(self):
        self.seed_task()
        self.change_task_result([])
        self.assert_section_main('task', 1)
        report = self.root / 'report/observation-readback.json'
        original = report.read_bytes()
        self.assertEqual(json.loads(original)['task']['successful_decoded_observations'], 14)
        with self.assertRaises(FileExistsError):
            self.assert_section_main('task', 1)
        self.assertEqual(report.read_bytes(), original)

    def test_e5_manifest_failure_makes_aggregate_fail_and_valid_override_passes(self):
        _, manifest, digest = self.seed_e5()
        self.assert_section_main('preflight', 1)
        report = self.root / 'report/observation-readback.json'
        self.assertFalse(json.loads(report.read_text())['preflight']['complete'])
        report.unlink()
        self.assert_section_main('preflight', 0, required_manifest=manifest,
                                 required_manifest_sha256=digest)
        self.assertTrue(json.loads(report.read_text())['preflight']['complete'])


if __name__ == '__main__':
    unittest.main()
