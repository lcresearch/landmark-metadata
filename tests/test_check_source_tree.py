"""Regression checks for failures hidden by the original navigation check."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location(
    'check_source_tree', Path(__file__).resolve().parents[1]/'scripts/check_source_tree.py')
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


class SourceTreeChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.write('README.md', '[Guide](docs/guide.md)\n')
        self.write('docs/guide.md', '[Home](../README.md)\n')
        self.write('TODO.md', '# Pending\n')
        self.write('sources/snapshot/manuscript/paper.tex', 'Preserved source\n')
        self.old_hash = self.digest('sources/snapshot/manuscript/paper.tex')
        self.row = {'repository_path':'sources/snapshot/manuscript/paper.tex',
                    'original_path':'/workspace/snapshot/manuscript/paper.tex',
                    'sha256':self.old_hash, 'bytes':17}
        self.write('docs/SOURCE_IMPORT.json', json.dumps({'files':[self.row]}))
        self.write('docs/SOURCE_P2P3.json', json.dumps({'files':[]}))
        self.write('MEMORY.md', '| `/workspace/snapshot` | Revised `manuscript/paper.tex` '
                   'SHA-256: `'+self.old_hash+'` |\n')

    def write(self, name, content):
        p = self.root/name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding='utf-8')

    def digest(self, name):
        return hashlib.sha256((self.root/name).read_bytes()).hexdigest()

    def report(self):
        return CHECKER.check_tree(self.root)

    def test_relative_navigation_and_matching_three_way_digest(self):
        self.write('docs/spaced note.md', '# Note\n')
        self.write('docs/guide.md', '[Note](spaced%20note.md)\n[Home](../README.md#top)\n'
                   '[Web](https://example.org/missing)\n')
        report = self.report()
        self.assertEqual(report['status'], 'PASS', report)
        self.assertEqual(report['checks']['memory_import_hashes'], 1)

    def test_missing_current_doc_link_is_a_failure(self):
        self.write('docs/guide.md', '[Missing](missing.md)\n')
        report = self.report()
        self.assertEqual(report['status'], 'FAIL')
        self.assertIn('missing.md', [f.get('target') for f in report['failures']])

    def test_protocol_relative_external_links_are_ignored(self):
        self.write('docs/guide.md', '[CDN](//cdn.example.org/guide.md)\n'
                   '![Image](//cdn.example.org/image.png)\n[Home](../README.md)\n')
        self.assertEqual(self.report()['status'], 'PASS')

    def test_historical_links_and_backtick_evidence_warn_without_failing(self):
        self.write('sources/snapshot/README.md', 'Read `manuscript/paper.pdf`, '
                   '`SHA256SUMS`, and [results](results.json). Run `bash commands.sh`.\n')
        report = self.report()
        self.assertEqual(report['status'], 'PASS', report)
        self.assertEqual({w['target'] for w in report['warnings']},
                         {'manuscript/paper.pdf', 'SHA256SUMS', 'results.json'})

    def test_corrupt_import_is_fatal_even_when_navigation_only_warns(self):
        self.write(self.row['repository_path'], 'Changed source\n')
        report = self.report()
        self.assertEqual(report['status'], 'FAIL')
        self.assertIn('imported bytes differ', [f['issue'] for f in report['failures']])
        self.assertEqual(report['imported_files_verified'], 0)

    def test_stale_memory_hash_is_fatal_and_external_archive_hash_is_unchecked(self):
        self.write('MEMORY.md', '| `/workspace/snapshot` | Revised `manuscript/paper.tex` '
                   'SHA-256: `'+('0'*64)+'` |\n'
                   '| `/workspace/sealed` | `SHA256SUMS` SHA-256: `'+('1'*64)+'` |\n')
        report = self.report()
        self.assertEqual(report['status'], 'FAIL')
        self.assertIn('MEMORY/import/source hash mismatch',
                      [f['issue'] for f in report['failures']])
        self.assertIn('external evidence digest not checked',
                      [w['issue'] for w in report['warnings']])

    def test_current_manuscript_digest_detects_changed_working_copy(self):
        name = 'work/revision/manuscript/paper.tex'
        self.write(name, 'Current source\n')
        self.write('README.md', '[Current manuscript source]('+name+')\n')
        self.write('docs/CURRENT_MANUSCRIPT.json', json.dumps({
            'repository_path':name, 'sha256':self.digest(name),
            'derived_from_repository_path':self.row['repository_path'],
            'derived_from_sha256':self.old_hash}))
        self.assertEqual(self.report()['status'], 'PASS')
        self.write(name, 'Changed after indexing\n')
        report = self.report()
        self.assertEqual(report['status'], 'FAIL')
        self.assertIn('manuscript digest mismatch', [f['issue'] for f in report['failures']])

    def test_p2p3_parent_and_current_navigation_are_both_checked(self):
        parent = 'research/p2p3/manuscript/paper.tex'
        name = 'work/revision/manuscript/paper.tex'
        self.write(parent, 'Completed P2/P3\n')
        self.write(name, 'Editorial follow-up\n')
        self.write('docs/SOURCE_P2P3.json', json.dumps({'files':[{
            'source_path':'/workspace/p2p3/manuscript/paper.tex',
            'repository_path':parent, 'sha256':self.digest(parent),
            'bytes':len((self.root/parent).read_bytes())}]}))
        self.write('docs/CURRENT_MANUSCRIPT.json', json.dumps({
            'repository_path':name, 'sha256':self.digest(name),
            'derived_from_repository_path':parent,
            'derived_from_sha256':self.digest(parent)}))
        self.write('README.md', '[Current manuscript source]('+name+')\n')
        self.assertEqual(self.report()['status'], 'PASS')
        self.write('README.md', '[Current manuscript source]('+parent+')\n')
        self.assertIn('current manuscript navigation/index mismatch',
                      [f['issue'] for f in self.report()['failures']])
        self.write('README.md', '[Current manuscript source]('+name+')\n')
        self.write(parent, 'Corrupted P2/P3\n')
        self.assertIn('imported bytes differ', [f['issue'] for f in self.report()['failures']])

    def test_binary_artifact_is_rejected(self):
        self.write('model.tflite', 'Excluded artifact\n')
        report = self.report()
        self.assertEqual(report['status'], 'FAIL')
        self.assertIn('excluded artifact type/path', [f['issue'] for f in report['failures']])


if __name__ == '__main__':
    unittest.main()
