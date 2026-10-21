"""Source-copy regressions; never download inputs, import ML code or run Android."""
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / 'scripts/initialize_android_run.py'
spec = importlib.util.spec_from_file_location('initialize_android_run', SCRIPT)
initializer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(initializer)


class InitializeAndroidRunTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)
        self.output = self.base / 'fresh-run'

    def test_copy_records_local_inputs_and_source_identities(self):
        provenance = initializer.initialize(REPO, self.output)
        self.assertEqual(provenance['input_acquisition']['status'], 'NOT_ESTABLISHED')
        self.assertFalse(provenance['models_read_or_downloaded'])
        self.assertFalse(provenance['model_or_device_execution'])
        self.assertEqual(json.loads((self.output / 'SOURCE_PROVENANCE.json').read_text()), provenance)
        for row in provenance['source_files']:
            data = Path(row['source']).read_bytes()
            self.assertEqual(row['sha256'], hashlib.sha256(data).hexdigest())
            self.assertEqual(row['bytes'], len(data))
        for name, expected in provenance['scripts'].items():
            data = (self.output / 'scripts' / name).read_bytes()
            self.assertEqual(hashlib.sha256(data).hexdigest(), expected)
            if name.endswith('.py'):
                ast.parse(data, filename=name)
        source = (self.output / 'scripts/prepare_e1.py').read_text()
        calls = [node for node in ast.walk(ast.parse(source)) if isinstance(node, ast.Call)
                 and isinstance(node.func, ast.Name) and node.func.id == 'prepare']
        self.assertEqual(len(calls), 1)
        statement = ast.literal_eval(calls[0].args[-1])
        self.assertIn(initializer.LOCAL_INPUT_PROVENANCE, statement)
        self.assertNotIn('fresh HTTPS publisher download', source)
        self.assertNotIn('recovered from frozen local evidence', source)
        for name in ('ContractInstrumentation.java', 'prepare_e2.py'):
            expected = REPO / 'sources' / initializer.AUDIT / 'rebuild/scripts' / name
            self.assertEqual((self.output / 'scripts' / name).read_bytes(), expected.read_bytes())
        self.assertEqual(list((self.output / 'prerequisites').iterdir()), [])
        self.assertFalse(list(self.output.rglob('*.tflite')))

    def test_cli_preserves_port_and_functional_readiness_adaptations(self):
        result = subprocess.run([sys.executable, '-B', str(SCRIPT), '--repo', str(REPO),
                                 '--root', str(self.output), '--port', '5556'],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        startup = (self.output / 'scripts/start_emulator.py').read_text()
        runner = (self.output / 'scripts/run_android.py').read_text()
        self.assertNotIn('5554', startup + runner)
        self.assertIn("'-port','5556'", startup)
        self.assertIn("'--serial','emulator-5556'", startup)
        self.assertIn("prefix=[adb,'-s','emulator-5556']", runner)
        tree = ast.parse(startup)
        gate = next(node for node in ast.walk(tree) if isinstance(node, ast.If)
                    and ast.unparse(node.test) == "q.stdout.strip() == '1'")
        readiness_call = gate.body[1].value
        self.assertIsInstance(readiness_call, ast.Call)
        self.assertIn('check_android_ready.py', ast.unparse(readiness_call))
        self.assertEqual(ast.unparse(gate.body[2].test), 'functional.returncode != 0')
        self.assertIsInstance(gate.body[2].body[0], ast.Continue)
        helper = REPO / 'sources/repro-audit-20261004/android/check_android_ready.py'
        self.assertEqual((self.output / 'scripts/check_android_ready.py').read_bytes(), helper.read_bytes())

    def test_refuses_existing_root_without_touching_it(self):
        self.output.mkdir()
        marker = self.output / 'marker.txt'
        marker.write_text('preserve')
        with self.assertRaises(FileExistsError):
            initializer.initialize(REPO, self.output)
        self.assertEqual(list(self.output.iterdir()), [marker])
        self.assertEqual(marker.read_text(), 'preserve')

    def test_refuses_repository_or_symlink_target(self):
        repository = self.base / 'repository'
        repository.mkdir()
        with self.assertRaises(ValueError):
            initializer.initialize(repository, repository / 'run')
        self.assertEqual(list(repository.iterdir()), [])
        link = self.base / 'linked-repository'
        link.symlink_to(repository, target_is_directory=True)
        with self.assertRaises(ValueError):
            initializer.initialize(repository, link / 'run')
        broken = self.base / 'broken-root'
        broken.symlink_to(self.base / 'missing')
        with self.assertRaises(FileExistsError):
            initializer.initialize(REPO, broken)
        self.assertTrue(broken.is_symlink())
        self.assertFalse((self.base / 'missing').exists())

    def test_missing_adapter_anchor_refuses_before_output_creation(self):
        repository = self.base / 'source-copy'
        source_dirs = [Path('sources') / initializer.E2E,
                       Path('sources') / initializer.AUDIT / 'rebuild/scripts',
                       Path('sources/repro-audit-20261004/android')]
        for relative in source_dirs:
            shutil.copytree(REPO / relative, repository / relative)
        prepare = repository / 'sources' / initializer.E2E / 'scripts/prepare_e1.py'
        prepare.write_text(prepare.read_text().replace('exact bytes recovered from frozen local evidence',
                                                      'changed upstream provenance'))
        with self.assertRaisesRegex(ValueError, 'Expected adapter anchor missing'):
            initializer.initialize(repository, self.output)
        self.assertFalse(self.output.exists())


if __name__ == '__main__':
    unittest.main()
