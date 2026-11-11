"""Input recovery must refuse wrong provenance and preserve existing material."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


SPEC = importlib.util.spec_from_file_location(
    'recover_focal_inputs', Path(__file__).resolve().parents[1] /
    'work/input-recovery-20261110/recover_inputs.py')
RECOVERY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RECOVERY)


class InputRecoveryTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.source = self.root / 'original.tflite'
        self.source.write_bytes(b'wrong input')
        self.output = self.root / 'new-recovery'

    def test_wrong_model_does_not_create_output(self):
        with self.assertRaisesRegex(ValueError, 'size mismatch'):
            RECOVERY.reconstruct(self.source, self.output)
        self.assertFalse(self.output.exists())
        size = RECOVERY.inventory()['model_conditions'][0]['primary_model']['bytes']
        with self.source.open('wb') as stream:
            stream.truncate(size)
        with self.assertRaisesRegex(ValueError, 'digest mismatch'):
            RECOVERY.reconstruct(self.source, self.output)
        self.assertFalse(self.output.exists())

    def test_changed_index_does_not_create_output(self):
        index = self.root / 'inputs.json'
        index.write_text('{}\n')
        with patch.object(RECOVERY, 'INDEX', index):
            with self.assertRaisesRegex(ValueError, 'index differs'):
                RECOVERY.reconstruct(self.source, self.output)
        self.assertFalse(self.output.exists())

    def test_existing_output_is_preserved(self):
        self.output.mkdir()
        marker = self.output / 'saved.txt'
        marker.write_text('preserve these bytes')
        with self.assertRaises(FileExistsError):
            RECOVERY.reconstruct(self.source, self.output)
        self.assertEqual(marker.read_text(), 'preserve these bytes')
        self.assertEqual(list(self.output.iterdir()), [marker])

    def test_repository_output_is_refused(self):
        output = RECOVERY.REPOSITORY / 'input-recovery-artifacts-forbidden'
        with self.assertRaisesRegex(ValueError, 'outside the source-only'):
            RECOVERY.reconstruct(self.source, output)
        self.assertFalse(output.exists())

    def test_symlink_output_and_parent_are_refused(self):
        target = self.root / 'target'
        target.mkdir()
        link = self.root / 'linked'
        link.symlink_to(target, target_is_directory=True)
        with self.assertRaises(FileExistsError):
            RECOVERY.reconstruct(self.source, link)
        with self.assertRaisesRegex(ValueError, 'traverse symlinks'):
            RECOVERY.reconstruct(self.source, link / 'new')
        self.assertEqual(list(target.iterdir()), [])


if __name__ == '__main__':
    unittest.main()
