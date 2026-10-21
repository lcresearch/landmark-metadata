"""Saved parser-record regressions; synthetic files, no Java/model execution."""
import base64
import contextlib
import copy
import importlib.util
import io
import json
from pathlib import Path
import shutil
import struct
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

sys.dont_write_bytecode = True
REPO = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('strict_parser_readback',
    REPO / 'work/review-fixes-20261021/verify_parser_probe.py')
V = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(V)


class ParserReadbackTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)
        self.root = self.base / 'evidence'
        self.root.mkdir()
        self.contract = V.load_contract()
        self.original = ''.join('label-%s\n' % i for i in range(1000)).encode()
        self.model = self.base / 'synthetic-model.tflite'
        with zipfile.ZipFile(self.model, 'w') as archive:
            archive.writestr('labels_without_background.txt', self.original)
        # Test-only trusted anchor: production CLI never accepts candidate-derived pins.
        self.contract['model_sha256'] = V.sha(self.model.read_bytes())
        self.addCleanup(patch.stopall)
        patch.object(V, 'load_contract', return_value=self.contract).start()
        self.seed()

    def write(self, relative, value):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(value if isinstance(value, bytes) else json.dumps(value).encode())
        return path

    def read(self, relative):
        return json.loads((self.root / relative).read_text())

    def identity(self, relative):
        path = self.root / relative
        return {'path': str(path), 'bytes': path.stat().st_size, 'sha256': V.sha(path.read_bytes())}

    def seal(self):
        self.write('evidence-files.json', [self.identity(path.relative_to(self.root))
                   for path in sorted(self.root.rglob('*'))
                   if path.is_file() and path.name != 'evidence-files.json'])

    def command(self, name, args, stdout=b'', stderr=b''):
        self.write('commands/' + name + '.command.json',
                   {'command': args, 'cwd': str(self.root), 'exit_code': 0})
        self.write('commands/' + name + '.stdout', stdout)
        self.write('commands/' + name + '.stderr', stderr)

    def oracle(self, name, payload, labels=None):
        labels = self.contract['helper'].load_java_utf8_labels(payload) if labels is None else labels
        transport = str(len(labels)) + '\n' + ''.join(
            base64.b64encode(label.encode()).decode() + '\n' for label in labels)
        self.command(name, self.java + ['LabelOracle', base64.b64encode(payload).decode()],
                     transport.encode('ascii'))
        return labels

    def seed(self):
        sources = copy.deepcopy(list(self.contract['sources'].values()))
        for relative in V.SOURCE_PATHS:
            self.write('sources/' + Path(relative).name, (REPO / relative).read_bytes())
        dependencies = copy.deepcopy(list(self.contract['dependencies'].values()))
        cp = ':'.join(sorted(row['path'] for row in dependencies))
        self.java = ['/fixed/jdk/bin/java', '-cp', str(self.root / 'classes') + ':' + cp]
        environment = {'model': {'sha256': self.contract['model_sha256']},
                       'sources': sources, 'dependencies': dependencies,
                       'java_executable': {'path': '/fixed/jdk/bin/java'},
                       'javac_executable': {'path': '/fixed/jdk/bin/javac'}, 'versions': {}}
        self.write('invocation.json', {'command': ['/fixed/python', 'run_probe.py']})
        versions = [('java-version', ['/fixed/jdk/bin/java', '-version'], b'', b'openjdk version "17.0.12"\n'),
                    ('javac-version', ['/fixed/jdk/bin/javac', '-version'], b'javac 17.0.12\n', b''),
                    ('python-version', ['/fixed/python', '--version'], b'Python synthetic\n', b'')]
        for name, command, stdout, stderr in versions:
            self.command(name, command, stdout, stderr)
            environment['versions'][name] = {'stdout': stdout.decode(), 'stderr': stderr.decode()}
        self.command('javac', ['/fixed/jdk/bin/javac', '--release', '8', '-cp', cp,
                              '-d', str(self.root / 'classes'), str(self.root / 'sources/DecoderProbe.java'),
                              str(self.root / 'sources/LabelOracle.java')])
        self.write('environment.json', environment)
        self.write('scores.f32', struct.pack('<1000f', *[i / 1000 for i in range(1000)]))
        result = {'status': 'PASS', 'passed_comparisons': 28, 'failed_comparisons': 0,
                  'decoder_conditions': [], 'valid_utf8_cases': [], 'malformed_cases': [],
                  'scores': self.identity('scores.f32')}
        payloads = {'original': self.original,
                    'lf_replaced_by_vertical_tab': self.original.replace(b'\n', b'\v', 1),
                    'unicode_separator_inside_first_label': self.original.replace(b'\n', '\u2028suffix\n'.encode(), 1)}
        for name, payload in payloads.items():
            relative = 'decoder/' + name + '/labels.txt'
            self.write(relative, payload)
            labels = self.oracle(name + '-oracle', payload)
            python_count, count, status = V.EXPECTED[name]
            actual = {'status': status, 'labels': count}
            if status == 'PASS':
                actual['categories'] = 1000
            else:
                actual.update(exception='java.lang.IllegalArgumentException',
                              message='Label number 999 mismatch the shape on axis 1')
            self.command(name + '-decoder', self.java + ['DecoderProbe', '1,1000',
                         str(self.root / 'scores.f32'), str(self.root / relative)], json.dumps(actual).encode())
            result['decoder_conditions'].append({'condition': name, 'label_input': self.identity(relative),
                'python_splitlines_count': python_count, 'actual_library': actual,
                'maintained_equals_actual_labels': True, 'passed_declared_comparison': True})
        for name, payload in self.contract['cases'].items():
            relative = 'differential/' + name + '.bin'
            self.write(relative, payload)
            labels = self.oracle('valid-' + name, payload)
            result['valid_utf8_cases'].append({'case': name, 'input': self.identity(relative),
                'oracle_labels': labels, 'helper_labels': labels, 'equal_strings': True})
        for name, payload in self.contract['malformed'].items():
            relative = 'malformed/' + name + '.bin'
            self.write(relative, payload)
            labels = self.oracle('malformed-' + name, payload, labels=['synthetic retained Java stdout'])
            result['malformed_cases'].append({'case': name, 'input': self.identity(relative),
                'oracle_labels': labels, 'helper_abstained': True,
                'python_replace_text': payload.decode('utf8', errors='replace')})
        self.write('results.json', result)
        self.write('completion.json', {'exit_code': 0})
        self.seal()

    def verify(self):
        self.seal()  # Mutations remain internally hash-consistent to expose semantic gaps.
        return V.verify(self.root, self.model)

    def assert_fail(self, fragment):
        report = self.verify()
        self.assertEqual(report['status'], 'FAIL')
        self.assertTrue(any(fragment in row['check'] and not row['passed']
                            for row in report['checks']), report)

    def test_valid_fixed_protocol_and_model_anchor(self):
        self.assertEqual(self.verify()['status'], 'PASS')

    def test_no_original_label_anchor_fails(self):
        report = V.verify(self.root)
        self.assertEqual(report['status'], 'FAIL')
        self.assertTrue(any(row['check'] == 'independent historical manifest pin' and not row['passed']
                            for row in report['checks']))

    def test_historical_pin_allows_relocated_copy_without_model(self):
        self.contract['manifest_sha256'] = V.sha((self.root / 'evidence-files.json').read_bytes())
        relocated = self.base / 'relocated'
        shutil.copytree(self.root, relocated)
        self.assertEqual(V.verify(relocated)['status'], 'PASS')

    def test_self_consistent_wrong_dependency_pin_fails(self):
        value = self.read('environment.json')
        value['dependencies'][0].update(sha256='0' * 64, expected_sha256='0' * 64, matches_pin=True)
        self.write('environment.json', value)
        self.assert_fail('trusted dependency pin:')

    def test_repeated_dependency_cannot_replace_another(self):
        value = self.read('environment.json')
        value['dependencies'][-1] = value['dependencies'][0]
        self.write('environment.json', value)
        self.assert_fail('exact dependency identities')

    def test_duplicate_valid_or_malformed_cases_fail(self):
        original = self.read('results.json')
        for key, label in [('valid_utf8_cases', 'exact 22 valid cases'),
                           ('malformed_cases', 'exact 3 malformed cases')]:
            with self.subTest(key=key):
                value = copy.deepcopy(original)
                value[key][-1] = value[key][0]
                self.write('results.json', value)
                self.assert_fail(label)

    def test_missing_payload_even_with_updated_manifest_fails(self):
        (self.root / 'differential/empty.bin').unlink()
        self.assert_fail('required evidence and schema')

    def test_missing_or_changed_copied_source_fails(self):
        path = self.root / 'sources/LabelOracle.java'
        path.write_bytes(b'changed source with updated manifest')
        value = self.read('environment.json')
        row = next(row for row in value['sources'] if Path(row['path']).name == path.name)
        row.update(bytes=path.stat().st_size, sha256=V.sha(path.read_bytes()))
        self.write('environment.json', value)
        self.assert_fail('trusted source pin: LabelOracle.java')
        path.unlink()
        self.assert_fail('required evidence and schema')

    def test_empty_source_inventory_fails(self):
        value = self.read('environment.json')
        value['sources'] = []
        self.write('environment.json', value)
        self.assert_fail('exact source identities')

    def test_wrong_decoder_transformation_with_same_counts_fails(self):
        name = 'lf_replaced_by_vertical_tab'
        path = 'decoder/' + name + '/labels.txt'
        payload = self.original.replace(b'label-1\n', b'label-1\v', 1)
        self.write(path, payload)
        value = self.read('results.json')
        row = next(row for row in value['decoder_conditions'] if row['condition'] == name)
        row['label_input'] = self.identity(path)
        self.write('results.json', value)
        self.oracle(name + '-oracle', payload)
        self.assert_fail('exact decoder transformation:')

    def test_unknown_zero_exit_command_fails(self):
        self.command('unrelated-command', ['true'])
        self.assert_fail('exact 35 command identities')

    def test_oracle_command_must_match_payload_and_classpath(self):
        relative = 'commands/valid-empty.command.json'
        value = self.read(relative)
        value['command'][0] = '/unrelated/program'
        self.write(relative, value)
        self.assert_fail('oracle command payload: valid-empty')

    def test_output_is_fresh_and_outside_evidence(self):
        output = self.base / 'report.json'
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(V.main(['--evidence', str(self.root), '--model', str(self.model),
                                     '--report', str(output)]), 0)
        preserved = output.read_bytes()
        for path in (output, self.root / 'new-report.json'):
            with self.subTest(path=path), self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
                V.main(['--evidence', str(self.root), '--report', str(path)])
        self.assertEqual(output.read_bytes(), preserved)

    def test_dangling_report_symlink_is_rejected(self):
        output = self.base / 'report-link.json'
        target = self.base / 'unexpected-target.json'
        output.symlink_to(target)
        with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
            V.main(['--evidence', str(self.root), '--model', str(self.model), '--report', str(output)])
        self.assertTrue(output.is_symlink())
        self.assertFalse(target.exists())


if __name__ == '__main__':
    unittest.main()
