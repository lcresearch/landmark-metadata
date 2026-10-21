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

    def index_import(self, name):
        path = self.root/'docs/SOURCE_IMPORT.json'
        manifest = json.loads(path.read_text())
        manifest['files'].append({'repository_path':name, 'original_path':'/workspace/'+name,
                                  'sha256':self.digest(name), 'bytes':(self.root/name).stat().st_size})
        path.write_text(json.dumps(manifest))

    def current_pointer(self, name, parent=None):
        parent = parent or self.row['repository_path']
        current = {'repository_path':name, 'sha256':self.digest(name),
                   'bytes':(self.root/name).stat().st_size,
                   'derived_from_repository_path':parent, 'derived_from_sha256':self.digest(parent)}
        for key, path in [('full_companion', 'work/revision/manuscript/paper-full.tex'),
                          ('claim_crosswalk', 'work/revision/CLAIM_EVIDENCE.md'),
                          ('artifact_handoff', 'work/revision/ARTIFACT_HANDOFF.md')]:
            self.write(path, key+'\n')
            current[key] = {'path':path, 'sha256':self.digest(path),
                            'bytes':(self.root/path).stat().st_size}
        self.write('docs/CURRENT_MANUSCRIPT.json', json.dumps(current))
        self.write('README.md', '[Current manuscript source]('+name+')\n')
        return current

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
        self.index_import('sources/snapshot/README.md')
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
        self.current_pointer(name)
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
        self.current_pointer(name, parent)
        self.assertEqual(self.report()['status'], 'PASS')
        self.write('README.md', '[Current manuscript source]('+parent+')\n')
        self.assertIn('current manuscript navigation/index mismatch',
                      [f['issue'] for f in self.report()['failures']])
        self.write('README.md', '[Current manuscript source]('+name+')\n')
        self.write(parent, 'Corrupted P2/P3\n')
        self.assertIn('imported bytes differ', [f['issue'] for f in self.report()['failures']])

    def test_each_nested_current_artifact_pin_detects_changed_bytes(self):
        name = 'work/revision/manuscript/paper.tex'
        self.write(name, 'Current source\n')
        current = self.current_pointer(name)
        self.assertEqual(self.report()['status'], 'PASS')
        self.assertEqual(self.report()['checks']['manuscript_hashes'], 5)
        for key in ('full_companion', 'claim_crosswalk', 'artifact_handoff'):
            with self.subTest(key=key):
                path = current[key]['path']
                original = (self.root/path).read_text()
                self.write(path, original+'Changed after pinning\n')
                report = self.report()
                self.assertEqual(report['status'], 'FAIL')
                self.assertIn(path, [f['path'] for f in report['failures']])
                self.write(path, original)

    def test_nested_missing_path_wrong_size_and_omitted_pin_fail(self):
        name = 'work/revision/manuscript/paper.tex'
        self.write(name, 'Current source\n')
        current = self.current_pointer(name)
        for mutation in ('missing_path', 'wrong_size', 'omitted_pin', 'empty_pin'):
            with self.subTest(mutation=mutation):
                changed = json.loads(json.dumps(current))
                if mutation == 'missing_path':
                    changed['full_companion']['path'] = 'missing/paper-full.tex'
                    changed['full_companion']['sha256'] = '0'*64
                elif mutation == 'wrong_size':
                    changed['artifact_handoff']['bytes'] += 1
                elif mutation == 'omitted_pin':
                    del changed['claim_crosswalk']
                else:
                    changed['full_companion'] = {}
                self.write('docs/CURRENT_MANUSCRIPT.json', json.dumps(changed))
                self.assertEqual(self.report()['status'], 'FAIL')

    def test_present_predecessor_pins_are_checked(self):
        name = 'work/revision/manuscript/paper.tex'
        self.write(name, 'Current source\n')
        current = self.current_pointer(name)
        for filename, content in [('paper.tex', 'Old short\n'), ('paper-full.tex', 'Old full\n')]:
            self.write('work/old/'+filename, content)
        current.update({'editorial_predecessor_repository_path':'work/old/paper.tex',
                        'editorial_predecessor_sha256':self.digest('work/old/paper.tex'),
                        'editorial_predecessor_companion':{
                            'path':'work/old/paper-full.tex', 'sha256':self.digest('work/old/paper-full.tex'),
                            'bytes':len('Old full\n')}})
        self.write('docs/CURRENT_MANUSCRIPT.json', json.dumps(current))
        self.assertEqual(self.report()['status'], 'PASS')
        self.assertEqual(self.report()['checks']['manuscript_hashes'], 7)
        self.write('work/old/paper-full.tex', 'Edited old full\n')
        self.assertEqual(self.report()['status'], 'FAIL')

    def test_unindexed_file_in_snapshot_fails_but_new_source_area_is_allowed(self):
        self.write('sources/repro-audit/new_check.py', '# First-party new work\n')
        self.assertEqual(self.report()['status'], 'PASS')
        self.write('sources/snapshot/lost.py', '# No longer indexed\n')
        report = self.report()
        self.assertEqual(report['status'], 'FAIL')
        self.assertIn('unindexed imported snapshot file', [f['issue'] for f in report['failures']])
        self.assertEqual(report['imported_files_verified'], 0)

    def test_declared_snapshot_root_is_checked_after_all_rows_are_removed(self):
        self.write('MEMORY.md', '# No memory digest in this fixture\n')
        self.write('docs/SOURCE_IMPORT.json', json.dumps({'workspace_roots':['snapshot'], 'files':[]}))
        report = self.report()
        self.assertEqual(report['status'], 'FAIL')
        self.assertIn('unindexed imported snapshot file', [f['issue'] for f in report['failures']])

    def test_binary_artifact_is_rejected(self):
        self.write('model.tflite', 'Excluded artifact\n')
        report = self.report()
        self.assertEqual(report['status'], 'FAIL')
        self.assertIn('excluded artifact type/path', [f['issue'] for f in report['failures']])


if __name__ == '__main__':
    unittest.main()
