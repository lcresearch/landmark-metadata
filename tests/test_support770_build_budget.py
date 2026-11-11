"""Exercise shared deadlines with fake clocks/processes, never Android builds."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

SOURCE = Path(__file__).resolve().parents[1] / 'work/support770-reconstruction-20261111'


def load(name):
    spec = importlib.util.spec_from_file_location('budget_test_' + name, SOURCE / (name + '.py'))
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


BUILD = load('build_consumers')
RECORDER = load('record_command')


class BuildBudgetTest(unittest.TestCase):
    def test_slow_steps_share_600_seconds_instead_of_resetting_each_step(self):
        clock = [100.0]
        calls = []
        def child(command, env):
            timeout = float(command[command.index('--timeout') + 1])
            deadline = float(command[command.index('--deadline-monotonic') + 1])
            calls.append((timeout, deadline))
            clock[0] += min(179, timeout)
            return SimpleNamespace(returncode=0)
        with patch.object(BUILD.time, 'monotonic', lambda: clock[0]), patch.object(BUILD.subprocess, 'run', child):
            budget = BUILD.ConsumerBudget()
            with self.assertRaises(TimeoutError):
                for name in ('compile', 'dex', 'resources', 'align', 'sign'):
                    BUILD.run_stage(Path('/synthetic'), {}, name, ['synthetic-build'], budget)
        self.assertEqual([call[0] for call in calls], [180, 180, 180, 63])
        self.assertEqual([call[1] for call in calls], [700] * 4)

    def test_expired_budget_starts_no_next_process(self):
        clock = [0.0]
        with patch.object(BUILD.time, 'monotonic', lambda: clock[0]), patch.object(BUILD.subprocess, 'run') as child:
            budget = BUILD.ConsumerBudget(); clock[0] = 600
            with self.assertRaises(TimeoutError):
                BUILD.run_stage(Path('/synthetic'), {}, 'sign', ['synthetic-build'], budget)
            child.assert_not_called()

    def test_main_retains_budget_failure_and_gives_each_consumer_a_fresh_budget(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / 'run'; root.mkdir()
            previous = Path(temporary) / 'previous'
            for name in ('java', 'javac'):
                path = previous / 'hand/toolchains/jdk-17.0.12+7/bin' / name
                path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(b'synthetic')
            lock = previous / 'round/P2/dependencies/resolved-lock.json'; lock.parent.mkdir(parents=True)
            lock.write_text(json.dumps({name: {'classpaths': [], 'natives': []} for name in ('wrapper', 'task')}))
            generated = root / 'project/app/build/generated/ml_source_out/debug/org/example/support770/ml/LiteModelDeeplabv31Metadata2.java'
            generated.parent.mkdir(parents=True); generated.write_text('synthetic source')
            source = Path(temporary) / 'source'; source.mkdir(); (source / 'record_command.py').write_text('# boundary mocked')
            clock = [0.0]; calls = []
            def child(command, env):
                stage = Path(command[command.index('--output') + 1]).name
                calls.append(stage)
                if stage != 'keytool': clock[0] += 601  # Misreported late success must still fail.
                return SimpleNamespace(returncode=0)
            with patch.object(BUILD, 'SOURCE', source), patch.object(BUILD.time, 'monotonic', lambda: clock[0]), \
                 patch.object(BUILD.subprocess, 'run', child), \
                 patch('sys.argv', ['build', '--root', str(root), '--previous', str(previous)]):
                with self.assertRaises(SystemExit) as result: BUILD.main()
            self.assertEqual(result.exception.code, 1)
            records = json.loads((root / 'build-results.json').read_text())
            self.assertEqual([r['status'] for r in records], ['FAIL', 'FAIL'])
            self.assertTrue(all(r['elapsed_seconds'] == 601 and '600-second budget' in r['error'] for r in records))
            self.assertEqual(calls, ['keytool', 'wrapper-compile', 'task-compile'])


class RecorderDeadlineTest(unittest.TestCase):
    def invoke(self, root, deadline):
        with patch('sys.argv', ['record', '--output', str(root / 'stage'), '--cwd', str(root),
             '--timeout', '180', '--deadline-monotonic', str(deadline), '--', 'synthetic-command']), \
             contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit) as result: RECORDER.main()
        return result.exception.code, json.loads((root / 'stage/command.json').read_text())

    def test_expired_absolute_deadline_does_not_launch(self):
        with tempfile.TemporaryDirectory() as temporary, patch.object(RECORDER.time, 'monotonic', return_value=10), \
             patch.object(RECORDER.subprocess, 'Popen') as child:
            code, record = self.invoke(Path(temporary), 9)
            child.assert_not_called()
        self.assertEqual(code, 1)
        self.assertEqual(record['status'], 'FAIL')
        self.assertTrue(record['timeout'])

    def test_process_launch_delay_consumes_the_shared_budget(self):
        process = Mock(); process.wait.return_value = 0
        with tempfile.TemporaryDirectory() as temporary, patch.object(RECORDER.time, 'monotonic', side_effect=[0, 4, 8, 8]), \
             patch.object(RECORDER.subprocess, 'Popen', return_value=process):
            code, _ = self.invoke(Path(temporary), 10)
        process.wait.assert_called_once_with(timeout=2)
        self.assertEqual(code, 0)

    def test_timed_out_child_is_killed_even_if_wait_then_returns_zero(self):
        process = Mock(pid=123)
        process.wait.side_effect = [subprocess.TimeoutExpired('synthetic', 5), 0]
        with tempfile.TemporaryDirectory() as temporary, patch.object(RECORDER.time, 'monotonic', return_value=0), \
             patch.object(RECORDER.subprocess, 'Popen', return_value=process), patch.object(RECORDER.os, 'killpg') as kill:
            code, record = self.invoke(Path(temporary), 5)
            kill.assert_called_once_with(123, RECORDER.signal.SIGKILL)
        self.assertEqual(code, 1)
        self.assertEqual(record['status'], 'FAIL')
        self.assertTrue(record['timeout'])


if __name__ == '__main__':
    unittest.main()
