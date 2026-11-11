"""Current paper readback must resolve both promoted code and historical pins."""
import hashlib
import importlib.util
from pathlib import Path
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


if __name__ == '__main__':
    unittest.main()
