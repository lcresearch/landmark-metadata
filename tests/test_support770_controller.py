"""Timeouts must stop device work and retain partial evidence without replay."""
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tarfile
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace

SCRIPT = Path(__file__).resolve().parents[1] / 'work/support770-reconstruction-20261111/run_consumers.py'
SPEC = importlib.util.spec_from_file_location('support770_controller', SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class TimeoutRetentionTest(unittest.TestCase):
    def exercise(self, stop_code, consumers):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / 'source'; source.mkdir()
            (source / 'record_command.py').write_text('# mocked command boundary\n')
            (root / 'boot').mkdir()
            (root / 'boot/readiness.json').write_text('{"status":"PASS"}')
            builds = []
            for consumer in consumers:
                folder = root / 'build' / consumer; folder.mkdir(parents=True)
                (folder / 'consumer.apk').write_bytes(b'synthetic APK identity')
                builds.append({'consumer': consumer, 'status': 'PASS',
                    'package': 'example.' + consumer, 'instrument': consumer,
                    'apk_sha256': hashlib.sha256(b'synthetic APK identity').hexdigest()})
            (root / 'build-results.json').write_text(json.dumps(builds))
            calls = []

            def fake_run(command):
                output = Path(command[command.index('--output') + 1]); output.mkdir()
                calls.append((output.parent.name, output.name))
                if output.name == 'install': (output / 'stdout').write_bytes(b'Success')
                if output.name == 'collect-incomplete':
                    payload = b'{"completed":false,"construction_status":"PASS"}'
                    with tarfile.open(output / 'stdout', 'w') as archive:
                        member = tarfile.TarInfo('result.json'); member.size = len(payload)
                        archive.addfile(member, io.BytesIO(payload))
                code = 1 if output.name == 'instrumentation' else stop_code if output.name == 'stop-incomplete' else 0
                return SimpleNamespace(returncode=code)

            with patch.object(MODULE, 'SOURCE', source), patch.object(MODULE.subprocess, 'run', fake_run), \
                 patch('sys.argv', ['run_consumers.py', '--root', str(root)]):
                with self.assertRaises(SystemExit) as result: MODULE.main()
                self.assertEqual(result.exception.code, 1)
            records = json.loads((root / 'runtime-results.json').read_text())
            self.assertFalse(records[0]['partial_observed']['completed'])
            self.assertEqual(records[0]['collection_status'], 'FAIL')
            self.assertEqual(calls.count(('wrapper', 'instrumentation')), 1)
            self.assertLess(calls.index(('wrapper', 'stop-incomplete')), calls.index(('wrapper', 'collect-incomplete')))
            return records, calls

    def test_timeout_stops_package_and_retains_partial_without_retry(self):
        records, _ = self.exercise(0, ['wrapper'])
        self.assertTrue(records[0]['incomplete_package_stopped'])

    def test_unconfirmed_stop_prevents_next_consumer(self):
        records, calls = self.exercise(1, ['wrapper', 'task'])
        self.assertEqual(len(records), 1)
        self.assertIn('stop_error', records[0])
        self.assertNotIn(('task', 'install'), calls)


if __name__ == '__main__':
    unittest.main()
