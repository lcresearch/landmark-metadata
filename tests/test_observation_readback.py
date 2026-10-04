"""Exercise the maintained readback with synthetic evidence, without ML dependencies."""
import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
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
                       [{'variant': variant, 'exit_code': 0}
                        for variant in reversed(self.module.HAND_VARIANTS)])
            for variant in self.module.HAND_VARIANTS:
                folder = f'repro-hand/executions/{phase}/{variant}/outputs'
                self.write(folder + '/decoded.json', decoded)
                self.write(folder + '/result.json', {
                    'initialization_status': 'PASS', 'detect_status': 'PASS',
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

    def test_hand_still_checks_execution_status_shape_and_bits(self):
        self.seed_hand()
        folder = self.root / 'repro-hand/executions/replay/restoration/outputs'
        result = json.loads((folder / 'result.json').read_text())
        result['detect_status'] = 'FAIL'
        (folder / 'result.json').write_text(json.dumps(result))
        decoded = json.loads((folder / 'decoded.json').read_text())
        decoded['hand_landmarks'][0].pop()
        (folder / 'decoded.json').write_text(json.dumps(decoded))
        (folder / 'decoded-float-bits.bin').write_bytes(b'changed')
        self.module.hand()
        failures = {r['check'] for r in self.module.checks if not r['passed']}
        self.assertEqual(failures, {'hand/replay/restoration/' + name for name in
                                   ('actual_completed', 'one_hand_21_landmarks',
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
            for mode, status in zip(self.module.BASELINE_MODES,
                                    ('READABLE', 'ACCEPTED', 'COMPATIBLE_PRECONDITIONS', 'PASS')):
                if variant == 'label_deletion':
                    status = {'simple_baseline': 'INCOMPATIBLE', 'task_init': 'FAIL'}.get(mode, status)
                rows.append({'variant': variant, 'mode': mode, 'result': {'status': status}})
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


if __name__ == '__main__':
    unittest.main()
