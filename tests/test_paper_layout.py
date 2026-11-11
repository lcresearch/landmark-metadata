"""Current paper readback must resolve both promoted code and historical pins."""
import hashlib
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[1]


def load(relative):
    spec = importlib.util.spec_from_file_location('paper_layout_' + Path(relative).stem, REPO / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


INDEX = load('work/rerun-paper-revision-20261111/index_evidence.py')
RECHECK = load('work/rerun-paper-revision-20261111/recheck_core.py')


class PaperSourcePaths(unittest.TestCase):
    def test_actual_preserved_audits_are_available_at_the_promoted_paths(self):
        for name, expected in RECHECK.PINS.items():
            self.assertEqual(hashlib.sha256((REPO / 'experiment/android' / name).read_bytes()).hexdigest(),
                             expected)
        self.assertTrue((REPO / 'experiment/run/analyze_p3_core.py').is_file())

    def test_old_packaging_source_resolves_to_the_exact_archived_blob(self):
        old = 'work/focal-rerun-20261110/package_evidence.py'
        self.assertFalse((REPO / old).exists())
        actual, location = INDEX.repository_identity(REPO / old)
        data = INDEX.archived_sources(REPO)[old]
        self.assertEqual(actual, {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
        self.assertEqual(location['verified_from'], 'archived_git_object')
        self.assertEqual(location['revision'], 'e9da459f6043684cdecba913c9c711433371909d')

    def test_working_source_is_not_mislabeled_as_historical(self):
        path = REPO / 'work/rerun-paper-revision-20261111/recheck_core.py'
        actual, location = INDEX.repository_identity(path)
        self.assertEqual(actual, INDEX.identity(path))
        self.assertEqual(location, {'verified_from': 'working_tree'})


class EvidenceIndexIntegrity(unittest.TestCase):
    def test_interrupted_failed_and_selected_records_keep_distinct_groups(self):
        routes = {
            'run/android/E1/executions/primary/original/device/result.json': ['N3'],
            'run/android/E1/executions/primary-interrupted-attempt1/results.json': ['N7'],
            'run/android/E1/executions/primary-continuation-1-provenance/continuation.json': ['N7'],
            'run/android/E2/executions/replay/original/device/result.json': ['N4'],
            'run/p3-core/results.json': ['N8'],
            'run/p3-core-attempt2/results.json': ['N6'],
            'run/round/P2/EXECUTION_INPUT_FREEZE.json': ['N1', 'N5'],
            'run/readback/p2-after-message-fix.json': ['N5', 'N8'],
            'run/unrelated.txt': [],
        }
        for member, expected in routes.items():
            with self.subTest(member=member):
                self.assertEqual(INDEX.member_groups(member, Path('/unused'), {}), expected)

    def test_both_archive_and_p2_hashes_are_required(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            relative = 'android/E1/executions/primary/result.json'
            path = root / relative
            path.parent.mkdir(parents=True)
            path.write_bytes(b'saved observation')
            row = {'path': 'run/' + relative, **INDEX.identity(path)}
            manifest = {'files': [row]}
            p2 = {str(path): row['sha256']}
            records = INDEX.verified_members(manifest, {'run': root}, p2)
            self.assertEqual(records[0]['groups'], ['N3', 'N5'])
            with self.assertRaisesRegex(ValueError, 'P2 read-file identity differs'):
                INDEX.verified_members(manifest, {'run': root}, {str(path): '0' * 64})
            path.write_bytes(b'altered observation')
            with self.assertRaisesRegex(ValueError, 'Live file differs'):
                INDEX.verified_members(manifest, {'run': root}, {str(path): INDEX.identity(path)['sha256']})

    def test_cli_preserves_existing_index_without_starting_readback(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'index.json'
            output.write_text('retained index')
            with patch.object(sys, 'argv', ['index_evidence.py', '--readback', directory,
                                          '--output', str(output)]), \
                    patch.object(INDEX, 'build_index') as build:
                with self.assertRaisesRegex(ValueError, 'Preserve the prior index'):
                    INDEX.main()
                build.assert_not_called()
            self.assertEqual(output.read_text(), 'retained index')


if __name__ == '__main__':
    unittest.main()
