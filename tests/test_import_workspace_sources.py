"""Immutable reimports must fail before changing files or preservation coverage."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location(
    'import_workspace_sources', Path(__file__).resolve().parents[1]/'scripts/import_workspace_sources.py')
IMPORTER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(IMPORTER)


class SourceImportTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.workspace = self.root/'workspace'
        self.repository = self.root/'repository'
        (self.workspace/'snapshot').mkdir(parents=True)
        self.repository.mkdir()
        self.write_source('kept.py', '# Kept\n')
        self.write_source('lost.py', '# Preserved\n')
        patched = patch.object(IMPORTER, 'ROOT_NAMES', ['snapshot'])
        patched.start()
        self.addCleanup(patched.stop)
        self.import_sources()
        self.manifest_path = self.repository/'docs/SOURCE_IMPORT.json'
        self.manifest = self.manifest_path.read_bytes()

    def write_source(self, name, data):
        (self.workspace/'snapshot'/name).write_text(data)

    def import_sources(self):
        return IMPORTER.import_sources(self.workspace, self.repository)

    def assert_preserved(self):
        self.assertEqual(self.manifest_path.read_bytes(), self.manifest)
        self.assertEqual((self.repository/'sources/snapshot/lost.py').read_text(), '# Preserved\n')
        self.assertFalse((self.repository/'sources/snapshot/a_new.py').exists())

    def test_identical_reimport_preserves_manifest_bytes(self):
        result = self.import_sources()
        self.assertEqual(result['imported_files'], 2)
        self.assert_preserved()

    def test_missing_original_refuses_before_any_new_file_is_written(self):
        (self.workspace/'snapshot/lost.py').unlink()
        self.write_source('a_new.py', '# New file sorted before the missing source\n')
        with self.assertRaisesRegex(ValueError, 'changed existing source manifest'):
            self.import_sources()
        self.assert_preserved()

    def test_changed_original_refuses_before_any_new_file_is_written(self):
        self.write_source('lost.py', '# Changed original\n')
        self.write_source('a_new.py', '# New file\n')
        with self.assertRaisesRegex(ValueError, 'overwrite imported source'):
            self.import_sources()
        self.assert_preserved()

    def test_changed_imported_copy_cannot_be_resealed(self):
        path = self.repository/'sources/snapshot/lost.py'
        path.write_text('# Tampered preserved copy\n')
        with self.assertRaisesRegex(ValueError, 'overwrite imported source'):
            self.import_sources()
        self.assertEqual(path.read_text(), '# Tampered preserved copy\n')
        self.assertEqual(self.manifest_path.read_bytes(), self.manifest)

    def test_existing_orphan_is_rejected_even_if_manifest_has_already_shrunk(self):
        manifest = json.loads(self.manifest)
        manifest['files'] = [row for row in manifest['files'] if row['repository_path'].endswith('/kept.py')]
        self.manifest_path.write_text(json.dumps(manifest))
        shrunk = self.manifest_path.read_bytes()
        (self.workspace/'snapshot/lost.py').unlink()
        with self.assertRaisesRegex(ValueError, 'unindexed imported source'):
            self.import_sources()
        self.assertEqual(self.manifest_path.read_bytes(), shrunk)
        self.assertEqual((self.repository/'sources/snapshot/lost.py').read_text(), '# Preserved\n')

    def test_added_original_requires_a_new_snapshot(self):
        self.write_source('a_new.py', '# Added after original import\n')
        with self.assertRaisesRegex(ValueError, 'changed existing source manifest'):
            self.import_sources()
        self.assert_preserved()


if __name__ == '__main__':
    unittest.main()
