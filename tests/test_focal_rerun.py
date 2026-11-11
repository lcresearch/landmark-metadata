"""Retention guards for fresh execution archives; no model dependencies needed."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tarfile
import tempfile
import unittest
from unittest.mock import patch


SOURCE = Path(__file__).resolve().parents[1] / 'experiment/run/package_evidence.py'
spec = importlib.util.spec_from_file_location('focal_package', SOURCE)
package = importlib.util.module_from_spec(spec)
spec.loader.exec_module(package)
RESUME_SOURCE = SOURCE.with_name('resume_android_phase.py')
resume_spec = importlib.util.spec_from_file_location('focal_resume', RESUME_SOURCE)
resume = importlib.util.module_from_spec(resume_spec)
resume_spec.loader.exec_module(resume)


class EvidenceRetention(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.root = self.base / 'run'
        self.inputs = self.base / 'inputs'
        self.refs = self.base / 'refs'
        self.stage = self.root / 'stages/finished/command.json'
        self.stage.parent.mkdir(parents=True)
        self.stage.write_text(json.dumps({'status': 'COMPLETED', 'exit_code': 1}))
        self.inputs.mkdir()
        self.refs.mkdir()
        (self.inputs / 'model').write_bytes(b'retained evidence')
        self.target = self.base / 'evidence.tar.gz'

    def invoke(self):
        argv = [str(SOURCE), '--root', str(self.root), '--inputs', str(self.inputs),
                '--references', str(self.refs), '--archive', str(self.target)]
        with patch.object(sys, 'argv', argv), patch('builtins.print'):
            package.main()

    def test_archive_retains_failure_and_bytes_but_excludes_keys_and_symlinks(self):
        (self.inputs / 'research.keystore').write_bytes(b'disposable key')
        (self.inputs / 'link').symlink_to(self.inputs / 'research.keystore')
        self.invoke()
        with tarfile.open(self.target) as archive:
            manifest = json.load(archive.extractfile('MANIFEST.json'))
            names = archive.getnames()
            self.assertNotIn('recovered-inputs/research.keystore', names)
            self.assertNotIn('recovered-inputs/link', names)
            self.assertEqual(len(manifest['excluded']), 2)
            self.assertEqual(json.load(archive.extractfile('run/stages/finished/command.json'))['exit_code'], 1)
            for row in manifest['files']:
                data = archive.extractfile(row['path']).read()
                self.assertEqual(hashlib.sha256(data).hexdigest(), row['sha256'])
                self.assertEqual(len(data), row['bytes'])
        receipt = json.loads(self.target.with_name(self.target.name + '.json').read_text())
        self.assertEqual(receipt['sha256'], hashlib.sha256(self.target.read_bytes()).hexdigest())
        self.assertFalse(receipt['remote_backup'])

    def test_running_stage_prevents_a_premature_archive(self):
        self.stage.write_text(json.dumps({'status': 'RUNNING'}))
        with self.assertRaisesRegex(ValueError, 'still running'):
            self.invoke()
        self.assertFalse(self.target.exists())
        self.assertFalse(self.target.with_name(self.target.name + '.partial').exists())

    def test_existing_archive_is_preserved(self):
        self.target.write_bytes(b'existing archive')
        with self.assertRaisesRegex(ValueError, 'fresh archive'):
            self.invoke()
        self.assertEqual(self.target.read_bytes(), b'existing archive')


class InterruptedCollection(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.area = self.root / 'android/E1'
        self.view = self.area / 'executions/primary'
        self.view.mkdir(parents=True)
        scripts = self.root / 'android/scripts'
        scripts.mkdir()
        (scripts / 'run_android.py').write_text('# original collector identity\n')
        variants = ['original', 'description_control', 'label_deletion', 'label_restoration']
        (self.area / 'static-results.json').write_text(json.dumps([{'variant': v} for v in variants]))
        rows = []
        for variant in variants:
            # A scientifically unexpected observed failure must remain visible,
            # not be rerun simply to obtain the historical expected PASS.
            observed = {'variant': variant, 'model_loading_status': 'FAIL'}
            device = self.view / variant / 'device/result.json'
            device.parent.mkdir(parents=True)
            device.write_text(json.dumps(observed))
            rows.append({'variant': variant, 'instrumentation_exit_code': 0, 'observed': observed})
        self.results = self.view / 'results.json'
        self.results.write_text(json.dumps(rows))

    def invoke(self):
        argv = [str(RESUME_SOURCE), '--root', str(self.root), '--experiment', 'E1', '--run', 'primary']
        with patch.object(sys, 'argv', argv), patch.object(resume.subprocess, 'run') as launch:
            resume.main()
            launch.assert_not_called()

    def test_complete_scientific_failures_are_retained_without_retry(self):
        before = self.results.read_bytes()
        self.invoke()
        self.invoke()
        self.assertEqual(self.results.read_bytes(), before)
        self.assertTrue((self.view.parent / 'primary-continuation-2-provenance/continuation.json').is_file())

    def test_controller_device_mismatch_stops_before_new_selection(self):
        device = self.view / 'original/device/result.json'
        device.write_text(json.dumps({'variant': 'different'}))
        with self.assertRaisesRegex(ValueError, 'differs from controller'):
            self.invoke()
        self.assertFalse((self.view.parent / 'primary-continuation-1-provenance').exists())


if __name__ == '__main__':
    unittest.main()
