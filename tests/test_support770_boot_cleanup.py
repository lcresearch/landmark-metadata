"""Boot failures must release the owned emulator; no real processes or SDKs."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, call, patch

SCRIPT = Path(__file__).resolve().parents[1] / 'work/support770-reconstruction-20261111/boot_device.py'
SPEC = importlib.util.spec_from_file_location('support770_boot_cleanup', SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class BootCleanupTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name) / 'run'
        self.root.mkdir()
        (self.root / 'build-results.json').write_text('[{"status":"PASS"}]')
        self.process = Mock(pid=123)
        self.process.poll.return_value = None
        self.process.wait.return_value = -15
        self.ready = SimpleNamespace(returncode=0, stdout=b'1\n', stderr=b'')
        self.properties = SimpleNamespace(returncode=0, stdout=b'[ro.test]: [value]\n', stderr=b'')
        self.socket = Mock()
        self.socket.__enter__ = Mock(return_value=self.socket)
        self.socket.__exit__ = Mock(return_value=False)

    def invoke(self, responses=None, write_failure=None, launch_error=None, write_failure_once=False):
        write_text, write_bytes = Path.write_text, Path.write_bytes
        failures = []

        def fail_write(path):
            if path.name == write_failure and (not write_failure_once or not failures):
                failures.append(path)
                raise OSError('synthetic evidence write failure')

        def guarded_text(path, data, *args, **kwargs):
            fail_write(path)
            return write_text(path, data, *args, **kwargs)

        def guarded_bytes(path, data, *args, **kwargs):
            fail_write(path)
            return write_bytes(path, data, *args, **kwargs)

        with patch.object(MODULE.shutil, 'copytree'), \
             patch.object(MODULE.socket, 'socket', return_value=self.socket), \
             patch.object(MODULE.subprocess, 'Popen', return_value=self.process, side_effect=launch_error) as launch, \
             patch.object(MODULE.subprocess, 'run', side_effect=responses or [self.ready, self.properties]), \
             patch.object(MODULE.time, 'sleep'), \
             patch.object(Path, 'write_text', guarded_text), patch.object(Path, 'write_bytes', guarded_bytes), \
             patch('sys.argv', ['boot', '--root', str(self.root), '--previous', str(self.root / 'previous')]), \
             contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            try:
                MODULE.main()
            except BaseException as exc:
                error = exc
            else:
                self.fail('Expected explicit exit or retained failure')
        launch.assert_called_once()
        path = self.root / 'boot/readiness.json'
        return error, json.loads(path.read_text()) if path.exists() else None

    def assert_cleaned_failure(self, report):
        self.assertEqual(report['status'], 'FAIL')
        self.assertEqual(report['cleanup']['status'], 'PASS')
        self.assertEqual(report['cleanup']['exit_code'], -15)
        self.process.terminate.assert_called_once_with()
        self.process.wait.assert_called_once_with(timeout=10)
        self.process.kill.assert_not_called()

    def test_post_ready_getprop_timeout_stops_and_reaps_owned_emulator(self):
        error, report = self.invoke([self.ready, subprocess.TimeoutExpired('getprop', 30)])
        self.assertIsInstance(error, subprocess.TimeoutExpired)
        self.assertIn('TimeoutExpired', report['error'])
        self.assert_cleaned_failure(report)

    def test_graceful_stop_timeout_escalates_and_waits_after_kill(self):
        self.process.wait.side_effect = [subprocess.TimeoutExpired('emulator', 10), -9]
        error, report = self.invoke([self.ready, subprocess.TimeoutExpired('getprop', 30)])
        self.assertIsInstance(error, subprocess.TimeoutExpired)
        self.assertEqual(report['cleanup']['status'], 'PASS')
        self.assertEqual(report['cleanup']['exit_code'], -9)
        self.assertEqual(self.process.method_calls[-4:], [call.terminate(), call.wait(timeout=10), call.kill(), call.wait(timeout=10)])

    def test_success_keeps_emulator_for_consumer_handoff(self):
        error, report = self.invoke()
        self.assertIsInstance(error, SystemExit)
        self.assertEqual(error.code, 0)
        self.assertEqual(report['status'], 'PASS')
        self.assertEqual((self.root / 'boot/getprop.stdout').read_bytes(), self.properties.stdout)
        self.process.terminate.assert_not_called()
        self.process.kill.assert_not_called()
        self.process.wait.assert_not_called()

    def test_launch_record_write_failure_still_cleans_owned_process(self):
        error, report = self.invoke(write_failure='launch.json')
        self.assertIsInstance(error, OSError)
        self.assert_cleaned_failure(report)

    def test_property_output_write_failure_does_not_leave_pass_or_process(self):
        error, report = self.invoke(write_failure='getprop.stdout')
        self.assertIsInstance(error, OSError)
        self.assert_cleaned_failure(report)

    def test_final_readiness_write_failure_cleans_process_and_records_fail(self):
        error, report = self.invoke(write_failure='readiness.json', write_failure_once=True)
        self.assertIsInstance(error, OSError)
        self.assert_cleaned_failure(report)

    def test_persistent_report_write_failure_cannot_prevent_cleanup(self):
        error, report = self.invoke(write_failure='readiness.json')
        self.assertIsInstance(error, OSError)
        self.assertIsNone(report)
        self.process.terminate.assert_called_once_with()
        self.process.wait.assert_called_once_with(timeout=10)

    def test_readiness_deadline_cleans_process_without_starting_consumers(self):
        with patch.object(MODULE.time, 'monotonic', side_effect=[0, 901]):
            error, report = self.invoke()
        self.assertIsInstance(error, RuntimeError)
        self.assertIn('deadline elapsed', report['error'])
        self.assert_cleaned_failure(report)

    def test_failed_property_command_retains_outputs_and_cleans_process(self):
        failed = SimpleNamespace(returncode=1, stdout=b'', stderr=b'synthetic adb failure')
        error, report = self.invoke([self.ready, failed])
        self.assertIsInstance(error, RuntimeError)
        self.assertEqual((self.root / 'boot/getprop.stderr').read_bytes(), failed.stderr)
        self.assert_cleaned_failure(report)

    def test_interrupt_during_readiness_also_cleans_owned_process(self):
        error, report = self.invoke([KeyboardInterrupt()])
        self.assertIsInstance(error, KeyboardInterrupt)
        self.assertIn('KeyboardInterrupt', report['error'])
        self.assert_cleaned_failure(report)

    def test_already_exited_emulator_is_reaped_without_signalling(self):
        self.process.poll.return_value = 7
        self.process.wait.return_value = 7
        error, report = self.invoke()
        self.assertIsInstance(error, RuntimeError)
        self.assertEqual(report['status'], 'FAIL')
        self.assertEqual(report['cleanup']['exit_code'], 7)
        self.process.terminate.assert_not_called()
        self.process.kill.assert_not_called()
        self.process.wait.assert_called_once_with(timeout=10)

    def test_cleanup_failure_does_not_hide_original_timeout(self):
        self.process.wait.side_effect = subprocess.TimeoutExpired('emulator', 10)
        error, report = self.invoke([self.ready, subprocess.TimeoutExpired('getprop', 30)])
        self.assertIsInstance(error, subprocess.TimeoutExpired)
        self.assertEqual(error.cmd, 'getprop')
        self.assertEqual(report['status'], 'FAIL')
        self.assertEqual(report['cleanup']['status'], 'FAIL')
        self.assertIn('TimeoutExpired', report['cleanup']['error'])
        self.assertEqual(self.process.wait.call_count, 2)
        self.process.kill.assert_called_once_with()

    def test_launch_failure_records_fail_without_signalling_any_process(self):
        error, report = self.invoke(launch_error=OSError('synthetic launch failure'))
        self.assertIsInstance(error, OSError)
        self.assertEqual(report['status'], 'FAIL')
        self.process.terminate.assert_not_called()
        self.process.kill.assert_not_called()
        self.process.wait.assert_not_called()


if __name__ == '__main__':
    unittest.main()
