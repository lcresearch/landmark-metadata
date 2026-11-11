"""Offline archive, exact source selection and dependency-closure regressions."""
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from archive import catalog

REPO = Path(__file__).resolve().parents[1]

def load(relative):
    spec = importlib.util.spec_from_file_location('layout_' + Path(relative).stem, REPO / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

INIT = load('experiment/run/initialize.py')
ANDROID = load('scripts/initialize_android_run.py')


class CurrentSourceBundle(unittest.TestCase):
    def test_staged_sources_are_exact_and_local_imports_are_available(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / 'run'
            rows = INIT.stage_sources(REPO, root)
            ANDROID.initialize(REPO, root / 'android')
            mapping = json.loads((REPO / 'experiment/source-map.json').read_text())
            actual = {str(p.relative_to(root)) for p in root.rglob('*')
                      if p.suffix in ('.py', '.java')}
            self.assertEqual(actual, set(mapping))
            for row in rows:
                self.assertEqual((root / row['destination']).read_bytes(),
                                 (REPO / row['source']).read_bytes())
            # These modules are imported at runtime from the external staged layout.
            for directory in ('android/scripts', 'round/P2/scripts', 'corpus/scripts'):
                for path in (root / directory).glob('*.py'):
                    for node in ast.walk(ast.parse(path.read_text())):
                        if isinstance(node, ast.ImportFrom) and node.module in {
                            'common', 'prepare_e1', 'suite_static', 'inspect_suite'}:
                            module_dir = ('corpus/scripts' if node.module in
                                          {'suite_static', 'inspect_suite'} else directory)
                            self.assertTrue((root / module_dir / (node.module + '.py')).is_file(), path)
            for name in ('prepare_hand.py', 'external_validation.py', 'preflight.py',
                         'seal_delivery.py', 'write_report.py', 'seal_p2.py'):
                self.assertFalse(list(root.rglob(name)))

    def test_selected_producers_still_match_pre_cleanup_bytes(self):
        records = catalog.read_archive(REPO)
        index = json.loads((REPO / 'archive/manifest.json').read_text())
        promoted = [row for row in index['files'] if row['replacement'] and
                    row['replacement'].startswith(('experiment/android/', 'experiment/model/',
                                                    'experiment/p2/', 'experiment/shared/', 'experiment/toolchain/'))]
        self.assertGreater(len(promoted), 20)
        for row in promoted:
            self.assertEqual((REPO / row['replacement']).read_bytes(), records[row['path']], row['path'])

    def test_missing_source_or_existing_target_does_not_partially_stage(self):
        with tempfile.TemporaryDirectory() as directory:
            repo, root = Path(directory) / 'repo', Path(directory) / 'run'
            (repo / 'experiment').mkdir(parents=True)
            (repo / 'one.py').write_text('# source\n')
            index = {'corpus/scripts/one.py': 'one.py', 'corpus/scripts/missing.py': 'missing.py'}
            (repo / 'experiment/source-map.json').write_text(json.dumps(index))
            with self.assertRaises(FileNotFoundError):
                INIT.stage_sources(repo, root)
            self.assertFalse(root.exists())
            target = root / 'corpus/scripts/one.py'
            target.parent.mkdir(parents=True)
            target.write_text('keep')
            with self.assertRaises(ValueError):
                INIT.stage_sources(repo, root)
            self.assertEqual(target.read_text(), 'keep')

    def test_parent_path_escape_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory) / 'repo'
            (repo / 'experiment').mkdir(parents=True)
            (repo / 'one.py').write_text('# source\n')
            (repo / 'experiment/source-map.json').write_text(json.dumps({
                'corpus/scripts/../../../escaped.py': 'one.py'}))
            with self.assertRaises(ValueError):
                INIT.stage_sources(repo, Path(directory) / 'run')
            self.assertFalse((Path(directory) / 'escaped.py').exists())


class HistoricalArchive(unittest.TestCase):
    def fixture(self, folder):
        root = Path(folder)
        (root / 'archive').mkdir()
        data = b'print("old")\n'
        row = {'path': 'old.py', 'sha256': hashlib.sha256(data).hexdigest(),
               'bytes': len(data), 'replacement': None}
        index = {'commit': catalog.ARCHIVE_COMMIT, 'files': [row]}
        (root / 'archive/manifest.json').write_text(json.dumps(index))
        batch = b'a'*40 + b' blob ' + str(len(data)).encode() + b'\n' + data + b'\n'
        return root, index, batch

    def test_corrupt_missing_duplicate_and_omitted_archive_records_fail(self):
        for mutation in ('digest', 'size', 'commit', 'duplicate', 'omitted', 'missing_git'):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as directory:
                root, index, batch = self.fixture(directory)
                if mutation == 'digest': index['files'][0]['sha256'] = '0'*64
                if mutation == 'size': index['files'][0]['bytes'] += 1
                if mutation == 'commit': index['commit'] = '0'*40
                if mutation == 'duplicate': index['files'] *= 2
                if mutation == 'omitted': index['files'] = []
                if mutation == 'missing_git': batch = b'old.py missing\n'
                (root / 'archive/manifest.json').write_text(json.dumps(index))
                with patch.object(catalog.subprocess, 'check_output', return_value=b'old.py\0'), \
                     patch.object(catalog.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, batch)), \
                     self.assertRaises(ValueError):
                    catalog.read_archive(root)

    def test_restored_tree_preserves_every_archived_byte_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'historical-tree'
            catalog.restore(REPO, target)
            for path, data in catalog.read_archive(REPO).items():
                self.assertEqual((target / path).read_bytes(), data, path)
            with self.assertRaises(ValueError):
                catalog.restore(REPO, target)
            with self.assertRaises(ValueError):
                catalog.restore(REPO, REPO / 'bad-restore')

    def test_reintroduced_archived_path_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'old.py').write_text('new bytes')
            with self.assertRaises(ValueError):
                catalog.preserved_bytes(root, 'old.py', {'old.py': b'old bytes'})


if __name__ == '__main__':
    unittest.main()
