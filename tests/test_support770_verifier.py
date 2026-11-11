"""Synthetic saved-record regressions; no SDK, model execution or sealed inputs."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import tarfile
import tempfile
import unittest
import zipfile

SCRIPT = Path(__file__).resolve().parents[1] / 'work/support770-reconstruction-20261111/verify_results.py'
SPEC = importlib.util.spec_from_file_location('support770_verifier', SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
RAW = bytes(257 * 257 * 21 * 4)
MASK = bytes(257 * 257)
RGB = bytes([127]) * (257 * 257 * 3)


def digest(data):
    return hashlib.sha256(data).hexdigest()


class VerifierTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.labels = [f'class-{i}' for i in range(21)]
        model = self.root / 'model-download/complete.body'
        model.parent.mkdir()
        # A synthetic ZIP exercises record binding, not TFLite model validity.
        with zipfile.ZipFile(model, 'w') as archive:
            archive.writestr('labelmap.txt', '\n'.join(self.labels) + '\n')
        self.model = model.read_bytes()
        self.save('model-inspection/inspection.json', {'sha256': digest(self.model), 'bytes': len(self.model),
            'linkage_pass': True, 'outputs': [{'shape': [1, 257, 257, 21], 'type': 0}]})
        self.save('stages/agp-generation/command.json', {'status': 'PASS', 'exit_code': 0,
            'command': ['synthetic-gradle', ':app:generateDebugMlModelClass']})
        self.write('project/app/build/generated/ml_source_out/debug/org/example/support770/ml/LiteModelDeeplabv31Metadata2.java', b'generated source')
        self.write('runtime-source/Harness.java', b'harness')
        self.save('boot/launch.json', {'serial': 'emulator-5556'})
        freeze = {'generated_source_sha256': digest(b'generated source'), 'source_files': {'Harness.java': digest(b'harness')}, 'consumers': {}}
        self.builds, self.results = [], []
        for consumer in ('wrapper', 'task'):
            instrument = 'WrapperInstrumentation' if consumer == 'wrapper' else 'TaskInstrumentation'
            package = 'org.example.support770.' + consumer
            class_name = 'org.example.support770.' + instrument
            prefix = [str(self.root / 'sdk/platform-tools/adb'), '-s', 'emulator-5556']
            apk = self.root / 'build' / consumer / 'consumer.apk'
            self.write(f'build/{consumer}/dex/classes.dex', b'dex')
            self.write(f'build/{consumer}/classes/Harness.class', b'class')
            dep = self.write(f'deps/{consumer}/dependency.jar', b'dependency')
            native = self.write(f'deps/{consumer}/native.so', b'native')
            freeze['consumers'][consumer] = {'classpaths': [{'path': str(dep), 'sha256': digest(b'dependency')}],
                'natives': [{'path': str(native), 'sha256': digest(b'native')}]}
            with zipfile.ZipFile(apk, 'w') as archive:
                archive.writestr('assets/lite_model_deeplabv3_1_metadata_2.tflite', self.model)
                archive.writestr('classes.dex', b'dex')
                archive.writestr('lib/x86_64/native.so', b'native')
            build = {'consumer': consumer, 'package': package, 'instrument': instrument, 'status': 'PASS',
                'apk_sha256': digest(apk.read_bytes()), 'packaged_model_sha256': digest(self.model),
                'class_hashes': {'Harness.class': digest(b'class')}}
            self.builds.append(build)
            observed = {'completed': True, 'instrumentation': class_name, 'model_sha256': digest(self.model),
                'model_bytes': len(self.model), 'input_sha256': digest(RGB), 'asset_identity_status': 'PASS',
                'input_status': 'PASS', 'construction_status': 'PASS'}
            self.write(f'executions/{consumer}/device/input.rgb', RGB)
            if consumer == 'wrapper':
                observed.update(process_status='PASS', raw_observation_status='PASS', category_getter_status='FAIL',
                    scientific_status='FAIL', earliest_failing_stage='category_getter', exception_type='IllegalArgumentException',
                    exception_message='synthetic getter failure', stack_trace='synthetic stack', causes=[{'type': 'IllegalArgumentException'}],
                    raw_output={'shape': [1, 257, 257, 21], 'bytes': len(RAW), 'sha256': digest(RAW)})
                self.write('executions/wrapper/device/raw_output.bin', RAW)
            else:
                observed.update(segment_status='PASS', mask_observation_status='PASS', scientific_status='PASS',
                    requested_output_type='CATEGORY_MASK', segmentations=1,
                    outputs=[{'output_type': 'CATEGORY_MASK', 'mask_count': 1, 'labels': [{'label': s} for s in self.labels]}],
                    mask_0_0={'shape': [257, 257], 'bytes': len(MASK), 'sha256': digest(MASK)})
                self.write('executions/task/device/mask_0_0.bin', MASK)
            commands = {
                'install': [*prefix, 'install', str(apk)],
                'instrumentation': [*prefix, 'shell', 'am', 'instrument', '-w', package + '/' + class_name],
                'collect': [*prefix, 'exec-out', 'run-as', package, 'tar', '-C', 'files/evidence', '-cf', '-', '.'],
            }
            for i, (stage, command) in enumerate(commands.items()):
                self.save(f'executions/{consumer}/{stage}/command.json', {'command': command, 'cwd': str(self.root),
                    'status': 'PASS', 'exit_code': 0, 'started_utc': f'2026-11-11T00:0{i}:00+00:00',
                    'finished_utc': f'2026-11-11T00:0{i}:01+00:00'})
            self.write(f'executions/{consumer}/install/stdout', b'Success\n')
            self.results.append({'consumer': consumer, 'build': build, 'collection_status': 'PASS',
                                 'scientific_status': observed['scientific_status'], 'observed': observed})
        self.save('runtime-freeze.json', freeze)
        self.save('build-results.json', self.builds)
        self.persist()

    def write(self, relative, data):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def save(self, relative, data):
        self.write(relative, json.dumps(data).encode())

    def persist(self):
        self.save('runtime-results.json', self.results)
        for result in self.results:
            consumer = result['consumer']
            self.save(f'executions/{consumer}/device/result.json', result['observed'])
            device = self.root / 'executions' / consumer / 'device'
            with tarfile.open(device.parent / 'collect/stdout', 'w') as archive:
                for path in sorted(device.iterdir()): archive.add(path, arcname=path.name)

    def rejected(self, expected):
        report = MODULE.verify(self.root)
        self.assertEqual(report['status'], 'FAIL')
        self.assertIn(expected, [c['check'] for c in report['checks'] if c['status'] == 'FAIL'])

    def test_complete_getter_failure_and_task_success_are_valid(self):
        report = MODULE.verify(self.root)
        self.assertEqual(report['status'], 'PASS')
        self.assertEqual([o['scientific_status'] for o in report['outcomes']], ['FAIL', 'PASS'])

    def test_removing_output_descriptors_cannot_reduce_required_coverage(self):
        originals = copy.deepcopy(self.results)
        for index, key, check in [(0, 'raw_output', 'wrapper required output raw_output'),
                                 (1, 'mask_0_0', 'task required output mask_0_0'),
                                 (1, 'outputs', 'task required output descriptions'),
                                 (1, 'segmentations', 'task returned segmentation count')]:
            with self.subTest(key=key):
                self.results = copy.deepcopy(originals)
                del self.results[index]['observed'][key]
                self.persist()
                self.rejected(check)

    def test_missing_raw_or_mask_file_is_rejected(self):
        for consumer, key, data in [('wrapper', 'raw_output', RAW), ('task', 'mask_0_0', MASK)]:
            with self.subTest(consumer=consumer):
                path = self.root / f'executions/{consumer}/device/{key}.bin'
                path.unlink(); self.persist()
                self.rejected(consumer + ' output ' + key)
                path.write_bytes(data); self.persist()

    def test_shape_and_byte_count_are_checked_independently_of_hash(self):
        for index, key, consumer in [(0, 'raw_output', 'wrapper'), (1, 'mask_0_0', 'task')]:
            original = copy.deepcopy(self.results[index]['observed'][key])
            for field, value, check in [('shape', [1], 'output shape '), ('bytes', 1, 'output size ')]:
                with self.subTest(consumer=consumer, field=field):
                    self.results[index]['observed'][key][field] = value
                    self.persist(); self.rejected(consumer + ' ' + check + key)
                    self.results[index]['observed'][key] = copy.deepcopy(original)

    def test_task_count_kind_and_labels_are_required(self):
        task = self.results[1]['observed']
        original = copy.deepcopy(task['outputs'])
        cases = [('mask_count', 0, 'task mask kind and count'), ('output_type', 'CONFIDENCE_MASK', 'task mask kind and count'),
                 ('labels', original[0]['labels'][:-1], 'task associated labels')]
        for key, value, check in cases:
            with self.subTest(key=key):
                task['outputs'] = copy.deepcopy(original); task['outputs'][0][key] = value
                self.persist(); self.rejected(check)

    def test_later_success_requires_prior_stage_success(self):
        self.results[1]['observed']['segment_status'] = 'FAIL'
        self.persist(); self.rejected('task successful stage sequence')

    def test_construction_failure_does_not_require_unreached_outputs(self):
        task = self.results[1]['observed']
        for key in ('segment_status', 'mask_observation_status', 'segmentations', 'outputs', 'mask_0_0'):
            del task[key]
        task.update(construction_status='FAIL', scientific_status='FAIL', earliest_failing_stage='construction',
                    exception_type='RuntimeException', stack_trace='synthetic stack', causes=[{'type': 'RuntimeException'}])
        self.results[1]['scientific_status'] = 'FAIL'
        (self.root / 'executions/task/device/mask_0_0.bin').unlink()
        self.persist()
        self.assertEqual(MODULE.verify(self.root)['status'], 'PASS')

    def test_complete_input_failure_preserves_recorded_identity_without_outputs(self):
        wrapper = self.results[0]['observed']
        for key in ('construction_status', 'process_status', 'raw_observation_status', 'category_getter_status', 'raw_output'):
            del wrapper[key]
        wrapper.update(input_status='FAIL', earliest_failing_stage='input')
        (self.root / 'executions/wrapper/device/raw_output.bin').unlink()
        self.persist()
        self.assertEqual(MODULE.verify(self.root)['status'], 'PASS')

    def test_true_command_is_not_an_instrumentation_invocation(self):
        for consumer in ('wrapper', 'task'):
            path = f'executions/{consumer}/instrumentation/command.json'
            record = json.loads((self.root / path).read_text()); record['command'] = ['/bin/true']; self.save(path, record)
            self.rejected(consumer + ' instrumentation command identity')

    def test_wrong_apk_serial_class_and_collect_package_are_rejected(self):
        cases = [('install', -1, '/tmp/stale.apk'), ('install', 2, 'emulator-9999'),
                 ('instrumentation', -1, 'wrong.package/WrongClass'), ('collect', 5, 'wrong.package')]
        for stage, index, replacement in cases:
            with self.subTest(stage=stage, replacement=replacement):
                path = f'executions/task/{stage}/command.json'
                original = json.loads((self.root / path).read_text())
                changed = copy.deepcopy(original); changed['command'][index] = replacement; self.save(path, changed)
                self.rejected('task ' + stage + ' command identity')
                self.save(path, original)

    def test_failed_install_cannot_be_hidden_by_successful_instrumentation(self):
        path = 'executions/task/install/command.json'
        record = json.loads((self.root / path).read_text()); record.update(status='FAIL', exit_code=1); self.save(path, record)
        self.rejected('task install completed')

    def test_stale_invocation_order_is_rejected(self):
        path = 'executions/task/instrumentation/command.json'
        record = json.loads((self.root / path).read_text()); record['started_utc'] = '2026-11-10T00:00:00+00:00'; self.save(path, record)
        self.rejected('task invocation chronology')

    def test_matching_wrong_build_and_summary_do_not_change_consumer_identity(self):
        self.builds[1]['package'] = 'wrong.package'
        self.save('build-results.json', self.builds); self.persist()
        self.rejected('task frozen consumer identity')

    def test_reported_instrumentation_must_match_invoked_class(self):
        self.results[1]['observed']['instrumentation'] = 'wrong.Instrumentation'
        self.persist(); self.rejected('task observed instrumentation')

    def test_saved_device_record_must_match_collected_stream(self):
        path = self.root / 'executions/task/device/mask_0_0.bin'
        path.write_bytes(b'\1' + MASK[1:])
        self.rejected('task collected bytes')


if __name__ == '__main__':
    unittest.main()
