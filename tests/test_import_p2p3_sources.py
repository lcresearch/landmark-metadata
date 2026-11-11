"""P2/P3 import failures must not change the preserved snapshot or index."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


SPEC = importlib.util.spec_from_file_location(
    'import_p2p3_sources', Path(__file__).resolve().parents[1] / 'scripts/import_p2p3_sources.py')
IMPORTER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(IMPORTER)


class P2P3ImportTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)
        self.source = self.base / 'source'
        self.source.mkdir()
        self.repository = self.base / 'repository'
        self.destination = self.repository / 'research/20261004-p2-p3'
        self.manifest = self.repository / 'docs/SOURCE_P2P3.json'
        (self.source / 'README.md').write_text('Preserved readme\n')
        (self.source / 'z-last.md').write_text('Preserved later source\n')
        (self.source / 'SHA256SUMS').write_text('Synthetic historical manifest\n')
        self.import_sources()
        self.before = self.snapshot()

    def import_sources(self):
        return IMPORTER.import_sources(self.source, self.repository)

    def snapshot(self):
        return {str(p.relative_to(self.repository)): (p.read_bytes(), p.stat().st_mtime_ns)
                for p in self.repository.rglob('*') if p.is_file()}

    def add_source(self):
        (self.source / 'a-new.md').write_text('New file sorts before the preserved sources\n')

    def test_initial_import_and_identical_reimport_preserve_bytes_and_mtimes(self):
        result = self.import_sources()
        self.assertEqual(result['selected_files'], 2)
        self.assertEqual(self.snapshot(), self.before)

    def test_added_source_is_refused_before_any_write(self):
        self.add_source()
        with self.assertRaisesRegex(ValueError, 'changed existing source manifest'):
            self.import_sources()
        self.assertEqual(self.snapshot(), self.before)

    def test_missing_source_with_new_file_does_not_partially_import(self):
        self.add_source()
        (self.source / 'z-last.md').unlink()
        with self.assertRaisesRegex(ValueError, 'changed existing source manifest'):
            self.import_sources()
        self.assertEqual(self.snapshot(), self.before)

    def test_changed_later_source_does_not_write_earlier_new_file(self):
        self.add_source()
        (self.source / 'z-last.md').write_text('Changed historical source\n')
        with self.assertRaisesRegex(ValueError, 'changed existing import'):
            self.import_sources()
        self.assertEqual(self.snapshot(), self.before)

    def test_changed_destination_is_not_overwritten_or_resealed(self):
        (self.destination / 'z-last.md').write_text('Changed existing copy\n')
        before = self.snapshot()
        self.add_source()
        with self.assertRaisesRegex(ValueError, 'changed existing import'):
            self.import_sources()
        self.assertEqual(self.snapshot(), before)

    def test_orphan_is_rejected_even_if_manifest_was_already_shrunk(self):
        manifest = json.loads(self.manifest.read_text())
        manifest['files'] = [r for r in manifest['files'] if r['repository_path'].endswith('/README.md')]
        self.manifest.write_text(json.dumps(manifest, indent=2) + '\n')
        (self.source / 'z-last.md').unlink()
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, 'unindexed imported source'):
            self.import_sources()
        self.assertEqual(self.snapshot(), before)

    def test_binary_source_is_refused_before_writes(self):
        self.add_source()
        (self.source / 'z-binary.md').write_bytes(b'source\x00binary')
        with self.assertRaisesRegex(ValueError, 'binary or large source'):
            self.import_sources()
        self.assertEqual(self.snapshot(), self.before)

    def test_linked_source_is_refused_before_writes(self):
        self.add_source()
        (self.source / 'z-link.md').symlink_to(self.source / 'README.md')
        with self.assertRaisesRegex(ValueError, 'linked/non-file source'):
            self.import_sources()
        self.assertEqual(self.snapshot(), self.before)

    def test_linked_destination_is_refused_without_following_it(self):
        target = self.destination / 'z-last.md'
        target.unlink()
        external = self.base / 'external.md'
        external.write_text('Preserved later source\n')
        target.symlink_to(external)
        self.add_source()
        with self.assertRaisesRegex(ValueError, 'linked import destination'):
            self.import_sources()
        self.assertTrue(target.is_symlink())
        self.assertEqual(external.read_text(), 'Preserved later source\n')
        self.assertFalse((self.destination / 'a-new.md').exists())
        self.assertEqual(self.manifest.read_bytes(), self.before['docs/SOURCE_P2P3.json'][0])


if __name__ == '__main__':
    unittest.main()
