"""Local package safety and identity tests using only synthetic temporary bytes."""
import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tarfile
import tempfile
import unittest
from unittest.mock import patch


SCRIPT = (Path(__file__).resolve().parents[1]
          / 'work/evidence-recovery-20261005/stage_evidence.py')
SPEC = importlib.util.spec_from_file_location('stage_evidence', SCRIPT)
STAGER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(STAGER)
ARCHIVE_SPEC = importlib.util.spec_from_file_location('verify_archive',
                                                    SCRIPT.with_name('verify_archive.py'))
ARCHIVE = importlib.util.module_from_spec(ARCHIVE_SPEC)
with patch.dict(sys.modules, {'stage_evidence': STAGER}):
    ARCHIVE_SPEC.loader.exec_module(ARCHIVE)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class StageEvidenceTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='synthetic-evidence-review-')
        self.addCleanup(temporary.cleanup)
        self.home = Path(temporary.name)
        self.source = self.home / 'historical'
        self.source.mkdir()
        (self.source / 'selected').mkdir()
        self.record = self.source / 'selected/record.txt'
        self.record.write_bytes(b'saved synthetic observation\n')
        self.anchor = self.source / 'SHA256SUMS'
        self.anchor.write_text(f'{sha(self.record)}  selected/record.txt\n')
        self.output = self.home / 'package'
        self.plan_path = self.home / 'plan.json'
        self.plan = {
            'schema_version': 1,
            'scope': 'Synthetic tests only; no model execution.',
            'repository_base_commit': '0' * 40,
            'roots': [{
                'id': 'SYNTHETIC', 'source_root': str(self.source),
                'destination_prefix': 'synthetic', 'manifest': 'SHA256SUMS',
                'manifest_sha256': sha(self.anchor),
                'include_root_files': True, 'include_directories': ['selected'],
            }],
            'excluded_directory_names': ['sdk'],
            'excluded_file_names': ['unsigned.apk'],
            'excluded_file_suffixes': ['.key'],
        }
        self.save_plan()

    def save_plan(self):
        self.plan_path.write_text(json.dumps(self.plan))

    def stage(self):
        with contextlib.redirect_stdout(io.StringIO()) as stream:
            result = STAGER.stage(self.plan_path, self.output)
        return result, json.loads(stream.getvalue())

    def manifest(self):
        return json.loads((self.output / 'MANIFEST.json').read_text())

    def verify(self, anchor=None):
        anchor = anchor or sha(self.output / 'SHA256SUMS')
        with contextlib.redirect_stdout(io.StringIO()) as stream:
            result = STAGER.verify(self.output, anchor)
        return result, json.loads(stream.getvalue())

    def payload(self):
        return self.output / 'payload/synthetic/selected/record.txt'

    def repin_package(self):
        """Repin synthetic metadata to test structural checks, not trust renewal."""
        files = sorted(p for p in self.output.rglob('*')
                       if p.is_file() and p != self.output / 'SHA256SUMS')
        checksum_file = self.output / 'SHA256SUMS'
        checksum_file.write_text(''.join(
            f'{sha(p)}  {p.relative_to(self.output).as_posix()}\n' for p in files))
        return sha(checksum_file)

    def test_matching_saved_bytes_are_copied_without_changing_originals(self):
        before = {p.relative_to(self.source): (p.read_bytes(), p.stat().st_mtime_ns)
                  for p in self.source.rglob('*') if p.is_file()}
        result, summary = self.stage()
        self.assertFalse(result)
        self.assertEqual(summary['status'], 'SELECTED_HISTORICAL_BYTES_MATCH')
        self.assertEqual(self.payload().read_bytes(), self.record.read_bytes())
        self.assertNotEqual(self.payload().stat().st_ino, self.record.stat().st_ino)
        self.assertEqual(before, {
            p.relative_to(self.source): (p.read_bytes(), p.stat().st_mtime_ns)
            for p in self.source.rglob('*') if p.is_file()})
        code, verified = self.verify()
        self.assertEqual(code, 0)
        self.assertEqual(verified['package_integrity'], 'PASS')
        self.assertFalse(verified['experimental_truth_verified'])

    def test_wrong_historical_manifest_anchor_refuses_before_output_creation(self):
        self.plan['roots'][0]['manifest_sha256'] = '0' * 64
        self.save_plan()
        with self.assertRaisesRegex(ValueError, 'Historical manifest identity mismatch'):
            self.stage()
        self.assertFalse(self.output.exists())

    def test_modifying_historical_manifest_does_not_renew_its_anchor(self):
        self.anchor.write_text(self.anchor.read_text() + '0' * 64 + '  other.txt\n')
        with self.assertRaisesRegex(ValueError, 'Historical manifest identity mismatch'):
            self.stage()
        self.assertFalse(self.output.exists())

    def test_changed_saved_payload_remains_an_identity_issue_in_valid_package(self):
        self.record.write_bytes(b'changed synthetic observation\n')
        result, summary = self.stage()
        self.assertTrue(result)
        self.assertEqual(summary['status'], 'IDENTITY_ISSUES')
        row = next(r for r in self.manifest()['files'] if r['path'].endswith('record.txt'))
        self.assertEqual(row['identity_status'], 'HISTORICAL_DIGEST_MISMATCH')
        code, verified = self.verify()
        self.assertEqual(code, 0)
        self.assertEqual(verified['package_integrity'], 'PASS')
        self.assertEqual(verified['historical_identity_status'], 'IDENTITY_ISSUES')
        self.assertEqual(verified['historical_identity_issues'], 1)
        self.assertFalse(verified['experimental_truth_verified'])

    def test_source_changed_during_copy_cannot_report_complete_identity(self):
        copy = STAGER.shutil.copyfileobj

        def copy_then_modify(src, dst, length):
            copy(src, dst, length)
            if Path(src.name) == self.record:
                self.record.write_bytes(b'concurrently changed synthetic source')

        with patch.object(STAGER.shutil, 'copyfileobj', side_effect=copy_then_modify):
            result, _ = self.stage()
        self.assertTrue(result)
        self.assertEqual(self.manifest()['issues'][0]['issue'], 'SOURCE_CHANGED_DURING_COPY')
        self.assertEqual(self.verify()[1]['historical_identity_status'], 'IDENTITY_ISSUES')

    def test_missing_historical_payload_is_recorded_without_false_completion(self):
        self.record.unlink()
        result, _ = self.stage()
        self.assertTrue(result)
        self.assertEqual(self.manifest()['issues'][0]['issue'],
                         'EXPECTED_SELECTED_FILE_MISSING_OR_SYMLINK')
        self.assertEqual(self.verify()[1]['historical_identity_status'], 'IDENTITY_ISSUES')

    def test_unlisted_selected_payload_is_not_historically_authenticated(self):
        (self.source / 'selected/new.txt').write_text('new synthetic copy')
        result, _ = self.stage()
        self.assertTrue(result)
        self.assertEqual(self.manifest()['issues'][0]['issue'], 'UNLISTED_CURRENT_COPY')
        self.assertEqual(self.verify()[1]['identity_counts']['UNLISTED_CURRENT_COPY'], 1)

    def test_excluded_dependency_key_and_out_of_scope_bytes_are_not_copied(self):
        for name in ('selected/sdk/tool.txt', 'selected/secret.key',
                     'selected/unsigned.apk', 'other/observation.txt'):
            path = self.source / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('synthetic excluded content')
            with self.anchor.open('a') as stream:
                stream.write(f'{sha(path)}  {name}\n')
        self.plan['roots'][0]['manifest_sha256'] = sha(self.anchor)
        self.save_plan()
        result, _ = self.stage()
        self.assertFalse(result)
        self.assertEqual(len(self.manifest()['files']), 2)
        omitted = json.loads((self.output / 'EXCLUSIONS.json').read_text())
        self.assertEqual(len([r for r in omitted if r['kind'] == 'manifest_entry']), 4)
        self.assertEqual(self.verify()[1]['package_integrity'], 'PASS')

    def test_historical_payload_symlink_is_missing_and_never_followed(self):
        original = self.home / 'outside.txt'
        self.record.rename(original)
        self.record.symlink_to(original)
        result, _ = self.stage()
        self.assertTrue(result)
        self.assertFalse(self.payload().exists())
        self.assertEqual(self.manifest()['issues'][0]['issue'],
                         'EXPECTED_SELECTED_FILE_MISSING_OR_SYMLINK')

    def test_source_directory_symlink_is_not_traversed(self):
        original = self.home / 'outside-directory'
        (self.source / 'selected').rename(original)
        (self.source / 'selected').symlink_to(original, target_is_directory=True)
        result, _ = self.stage()
        self.assertTrue(result)
        self.assertFalse(self.payload().exists())
        omitted = json.loads((self.output / 'EXCLUSIONS.json').read_text())
        self.assertTrue(any(r['reason'] == 'EXCLUDED_SYMLINK' for r in omitted))

    def test_source_root_and_manifest_symlinks_are_refused(self):
        for which in ('root', 'manifest'):
            with self.subTest(which=which):
                if which == 'root':
                    link = self.home / 'source-link'
                    link.symlink_to(self.source, target_is_directory=True)
                    self.plan['roots'][0]['source_root'] = str(link)
                else:
                    self.plan['roots'][0]['source_root'] = str(self.source)
                    original = self.home / 'anchor.txt'
                    self.anchor.rename(original)
                    self.anchor.symlink_to(original)
                self.save_plan()
                with self.assertRaises(ValueError):
                    self.stage()
                self.assertFalse(self.output.exists())

    def test_staging_refuses_existing_output_and_preserves_sentinel(self):
        self.output.mkdir()
        sentinel = self.output / 'sentinel.txt'
        sentinel.write_text('keep this')
        with self.assertRaisesRegex(ValueError, 'new output directory'):
            self.stage()
        self.assertEqual(sentinel.read_text(), 'keep this')
        self.assertEqual(list(self.output.iterdir()), [sentinel])

    def test_staging_refuses_dangling_output_symlink(self):
        target = self.home / 'new-location'
        self.output.symlink_to(target, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'symlinks'):
            self.stage()
        self.assertTrue(self.output.is_symlink())
        self.assertFalse(target.exists())

    def test_staging_refuses_output_symlink_parent(self):
        link = self.home / 'parent-link'
        link.symlink_to(self.home, target_is_directory=True)
        self.output = link / 'package'
        with self.assertRaisesRegex(ValueError, 'symlinks'):
            self.stage()
        self.assertFalse((self.home / 'package').exists())

    def test_staging_refuses_manifest_symlink_parent(self):
        nested = self.source / 'alias'
        nested.symlink_to(self.source, target_is_directory=True)
        self.plan['roots'][0]['manifest'] = 'alias/SHA256SUMS'
        self.save_plan()
        with self.assertRaisesRegex(ValueError, 'ancestors must not be symlinks'):
            self.stage()
        self.assertFalse(self.output.exists())

    def test_staging_refuses_destination_inside_source_and_source_repository(self):
        for output in (self.source / 'new-package', SCRIPT.parent / 'synthetic-package'):
            with self.subTest(output=output):
                self.output = output
                with self.assertRaises(ValueError):
                    self.stage()
                self.assertFalse(output.exists())

    def test_unsafe_manifest_paths_are_refused_before_output_creation(self):
        for name in ('.', '../escape.txt', '/absolute.txt', 'selected/../../escape.txt',
                     'selected//record.txt', './record.txt', 'selected\\record.txt'):
            with self.subTest(name=name):
                self.anchor.write_text(f'{"a" * 64}  {name}\n')
                self.plan['roots'][0]['manifest_sha256'] = sha(self.anchor)
                self.save_plan()
                with self.assertRaises(ValueError):
                    self.stage()
                self.assertFalse(self.output.exists())

    def test_duplicate_historical_manifest_entries_are_refused(self):
        self.anchor.write_text(self.anchor.read_text() * 2)
        self.plan['roots'][0]['manifest_sha256'] = sha(self.anchor)
        self.save_plan()
        with self.assertRaisesRegex(ValueError, 'Duplicate manifest path'):
            self.stage()
        self.assertFalse(self.output.exists())

    def test_control_characters_cannot_enter_checksum_paths(self):
        for character in ('\0', '\t', '\n', '\r', '\x1f', '\x7f'):
            with self.subTest(character=repr(character)), self.assertRaises(ValueError):
                STAGER.safe_relative('selected/file' + character + '.txt')

    def test_unsafe_and_duplicate_destination_prefixes_are_refused(self):
        for prefix in ('../escape', '/absolute', 'synthetic/../escape'):
            with self.subTest(prefix=prefix):
                self.plan['roots'][0]['destination_prefix'] = prefix
                self.save_plan()
                with self.assertRaises(ValueError):
                    self.stage()
                self.assertFalse(self.output.exists())
        self.plan['roots'][0]['destination_prefix'] = 'synthetic'
        self.plan['roots'].append(dict(self.plan['roots'][0]))
        self.save_plan()
        with self.assertRaisesRegex(ValueError, 'Duplicate destination prefix'):
            self.stage()

    def test_payload_tampering_fails_with_original_package_anchor(self):
        self.stage()
        anchor = sha(self.output / 'SHA256SUMS')
        self.payload().write_text('modified synthetic observation')
        with self.assertRaisesRegex(ValueError, 'Package byte mismatch'):
            self.verify(anchor)

    def test_payload_omission_fails_with_original_package_anchor(self):
        self.stage()
        anchor = sha(self.output / 'SHA256SUMS')
        self.payload().unlink()
        with self.assertRaisesRegex(ValueError, 'inventory differs'):
            self.verify(anchor)

    def test_extra_file_fails_with_original_package_anchor(self):
        self.stage()
        anchor = sha(self.output / 'SHA256SUMS')
        (self.output / 'extra.txt').write_text('extra unlisted bytes')
        with self.assertRaisesRegex(ValueError, 'inventory differs'):
            self.verify(anchor)

    def test_modified_package_checksums_cannot_replace_external_anchor(self):
        self.stage()
        anchor = sha(self.output / 'SHA256SUMS')
        self.payload().write_text('modified synthetic observation')
        self.repin_package()
        with self.assertRaisesRegex(ValueError, 'Historical manifest identity mismatch'):
            self.verify(anchor)

    def test_package_file_and_directory_symlinks_are_refused(self):
        self.stage()
        anchor = sha(self.output / 'SHA256SUMS')
        saved = self.home / 'saved-payload.txt'
        self.payload().rename(saved)
        self.payload().symlink_to(saved)
        with self.assertRaisesRegex(ValueError, 'Symlink in staged package'):
            self.verify(anchor)
        self.payload().unlink()
        saved.rename(self.payload())
        (self.output / 'extra-link').symlink_to(self.source, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'Symlink in staged package'):
            self.verify(anchor)

    def test_structured_manifest_duplicate_missing_hash_and_size_disagree(self):
        self.stage()
        original = self.manifest()
        for fault in ('duplicate', 'missing', 'hash', 'size'):
            with self.subTest(fault=fault):
                manifest = json.loads(json.dumps(original))
                if fault == 'duplicate':
                    manifest['files'].append(dict(manifest['files'][0]))
                elif fault == 'missing':
                    manifest['files'].pop()
                elif fault == 'hash':
                    manifest['files'][0]['sha256'] = '0' * 64
                else:
                    manifest['files'][0]['bytes'] += 1
                (self.output / 'MANIFEST.json').write_text(json.dumps(manifest))
                with self.assertRaises(ValueError):
                    self.verify(self.repin_package())

    def seed_supplement(self):
        self.extra = self.home / 'schema.py'
        self.extra.write_text('# synthetic schema source, never executed\n')
        reference = self.source / 'selected/reference.json'
        reference.write_text(json.dumps({'parser': {'sha256': sha(self.extra)}}))
        with self.anchor.open('a') as stream:
            stream.write(f'{sha(reference)}  selected/reference.json\n')
        self.plan['roots'][0]['manifest_sha256'] = sha(self.anchor)
        self.plan['supplementary_files'] = [{
            'source_path': str(self.extra),
            'destination': 'SUPPLEMENTARY_SOURCE/schema.py',
            'expected_sha256': sha(self.extra),
            'reference_root_id': 'SYNTHETIC',
            'reference_record': 'selected/reference.json',
            'digest_selector': ['parser', 'sha256'],
        }]
        self.save_plan()
        return reference

    def test_supplementary_source_uses_independently_anchored_reference(self):
        self.seed_supplement()
        result, _ = self.stage()
        self.assertFalse(result)
        row = next(r for r in self.manifest()['files']
                   if r['root_id'] == 'SUPPLEMENTARY_SOURCE')
        self.assertEqual(row['identity_status'], 'MATCH_HISTORICAL_REFERENCE')
        self.assertEqual(row['reference_record'], 'selected/reference.json')
        self.assertEqual(row['sha256'], sha(self.extra))
        self.assertEqual(self.verify()[1]['identity_counts']['MATCH_HISTORICAL_REFERENCE'], 1)

    def test_changed_supplementary_source_is_an_identity_issue(self):
        self.seed_supplement()
        self.extra.write_text('# changed synthetic source\n')
        result, _ = self.stage()
        self.assertTrue(result)
        issue = next(r for r in self.manifest()['issues']
                     if r['root_id'] == 'SUPPLEMENTARY_SOURCE')
        self.assertEqual(issue['issue'], 'HISTORICAL_DIGEST_MISMATCH')
        self.assertEqual(self.verify()[1]['historical_identity_status'], 'IDENTITY_ISSUES')

    def test_supplement_reference_must_match_historical_anchor(self):
        reference = self.seed_supplement()
        reference.write_text(json.dumps({'parser': {'sha256': '0' * 64}}))
        with self.assertRaisesRegex(ValueError, 'not historically anchored'):
            self.stage()
        self.assertFalse(self.output.exists())

    def test_supplement_plan_digest_must_match_anchored_reference(self):
        self.seed_supplement()
        self.plan['supplementary_files'][0]['expected_sha256'] = '0' * 64
        self.save_plan()
        with self.assertRaisesRegex(ValueError, 'differs from its historical reference'):
            self.stage()
        self.assertFalse(self.output.exists())

    def test_supplement_reference_must_be_listed_in_anchored_manifest(self):
        self.seed_supplement()
        self.anchor.write_text(f'{sha(self.record)}  selected/record.txt\n')
        self.plan['roots'][0]['manifest_sha256'] = sha(self.anchor)
        self.save_plan()
        with self.assertRaisesRegex(ValueError, 'not historically anchored'):
            self.stage()
        self.assertFalse(self.output.exists())

    def test_supplementary_source_symlinks_are_refused(self):
        self.seed_supplement()
        original = self.home / 'original-schema.py'
        self.extra.rename(original)
        self.extra.symlink_to(original)
        with self.assertRaisesRegex(ValueError, 'non-symlink file'):
            self.stage()
        self.assertFalse(self.output.exists())

    def test_supplementary_reference_symlink_is_refused_before_read(self):
        reference = self.seed_supplement()
        original = self.home / 'saved-reference.json'
        reference.rename(original)
        reference.symlink_to(original)
        with self.assertRaisesRegex(ValueError, 'symlink'):
            self.stage()
        self.assertFalse(self.output.exists())

    def test_supplementary_destination_must_be_safe_and_separate(self):
        self.seed_supplement()
        for destination in ('../escape.py', 'SUPPLEMENTARY_SOURCE/../escape.py',
                            'synthetic/schema.py'):
            with self.subTest(destination=destination):
                self.plan['supplementary_files'][0]['destination'] = destination
                self.save_plan()
                with self.assertRaises(ValueError):
                    self.stage()
                self.assertFalse(self.output.exists())

    def seed_metadata(self):
        metadata = self.source / 'selected/sdk/lock.json'
        metadata.parent.mkdir()
        metadata.write_text('{"synthetic": "dependency identity"}\n')
        (metadata.parent / 'library.bin').write_bytes(b'excluded fake dependency')
        with self.anchor.open('a') as stream:
            stream.write(f'{sha(metadata)}  selected/sdk/lock.json\n')
        self.plan['roots'][0]['manifest_sha256'] = sha(self.anchor)
        self.plan['roots'][0]['include_metadata_files'] = ['selected/sdk/lock.json']
        self.save_plan()
        return metadata

    def test_metadata_whitelist_copies_only_selected_text_inside_excluded_tree(self):
        metadata = self.seed_metadata()
        result, _ = self.stage()
        self.assertFalse(result)
        saved = self.output / 'payload/synthetic/selected/sdk/lock.json'
        self.assertEqual(saved.read_bytes(), metadata.read_bytes())
        self.assertFalse((saved.parent / 'library.bin').exists())
        self.assertEqual(self.verify()[1]['package_integrity'], 'PASS')

    def test_metadata_whitelist_rejects_binary_and_traversal_requests(self):
        for name in ('selected/sdk/library.bin', '../escape.json'):
            with self.subTest(name=name):
                self.plan['roots'][0]['include_metadata_files'] = [name]
                self.save_plan()
                with self.assertRaises(ValueError):
                    self.stage()
                self.assertFalse(self.output.exists())

    def test_missing_anchored_whitelisted_metadata_is_an_identity_issue(self):
        metadata = self.seed_metadata()
        metadata.unlink()
        result, _ = self.stage()
        self.assertTrue(result)
        issue = next(r for r in self.manifest()['issues']
                     if r['path'] == 'selected/sdk/lock.json')
        self.assertEqual(issue['issue'], 'EXPECTED_SELECTED_FILE_MISSING_OR_SYMLINK')

    def test_metadata_whitelist_does_not_follow_symlink_parent(self):
        metadata = self.seed_metadata()
        outside = self.home / 'outside-sdk'
        metadata.parent.rename(outside)
        metadata.parent.symlink_to(outside, target_is_directory=True)
        result, _ = self.stage()
        self.assertTrue(result)
        self.assertFalse((self.output / 'payload/synthetic/selected/sdk/lock.json').exists())


class ArchiveIntegrityTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='synthetic-archive-review-')
        self.addCleanup(temporary.cleanup)
        self.home = Path(temporary.name)
        self.archive = self.home / 'synthetic.tar.gz'
        self.members = {
            'payload/synthetic/record.txt': b'saved synthetic observation\n',
            'MANIFEST.json': b'{"scope":"synthetic archive test"}\n',
        }
        self.checksums = ''.join(
            f'{hashlib.sha256(value).hexdigest()}  {name}\n'
            for name, value in self.members.items()).encode()
        self.pin = hashlib.sha256(self.checksums).hexdigest()

    def write_archive(self, members=None, extra_members=(), checksums=None,
                      initial_members=()):
        members = dict(self.members if members is None else members)
        members['SHA256SUMS'] = self.checksums if checksums is None else checksums
        with tarfile.open(self.archive, 'w:gz') as stream:
            directory = tarfile.TarInfo('focal-saved-evidence')
            directory.type = tarfile.DIRTYPE
            stream.addfile(directory)
            for member in initial_members:
                stream.addfile(member)
            for name, value in members.items():
                member = tarfile.TarInfo('focal-saved-evidence/' + name)
                member.size = len(value)
                stream.addfile(member, io.BytesIO(value))
            for member in extra_members:
                stream.addfile(member)

    def test_complete_archive_verifies_bytes_without_extracting(self):
        self.write_archive()
        result = ARCHIVE.verify(self.archive, self.pin)
        self.assertEqual(result['archive_integrity'], 'PASS')
        self.assertEqual(result['verified_files'], 3)
        self.assertEqual(result['payload_files'], 1)
        self.assertEqual(result['archive_sha256'], sha(self.archive))
        self.assertEqual(result['uncompressed_file_bytes'],
                         sum(map(len, self.members.values())) + len(self.checksums))
        self.assertFalse(result['extracted'])
        self.assertFalse(result['model_experiments_run'])
        self.assertEqual(list(self.home.iterdir()), [self.archive])

    def test_tampered_missing_and_extra_archive_files_are_refused(self):
        for fault in ('tampered', 'missing', 'extra'):
            with self.subTest(fault=fault):
                members = dict(self.members)
                if fault == 'tampered':
                    members['payload/synthetic/record.txt'] = b'changed observation\n'
                elif fault == 'missing':
                    del members['payload/synthetic/record.txt']
                else:
                    members['unlisted.txt'] = b'extra file\n'
                self.write_archive(members)
                with self.assertRaises(ValueError):
                    ARCHIVE.verify(self.archive, self.pin)

    def test_archive_cannot_replace_independently_pinned_checksum_index(self):
        self.write_archive()
        with self.assertRaisesRegex(ValueError, 'does not match independent pin'):
            ARCHIVE.verify(self.archive, '0' * 64)
        changed = {'payload/synthetic/record.txt': b'changed observation\n'}
        new_checksums = ''.join(
            f'{hashlib.sha256(value).hexdigest()}  {name}\n'
            for name, value in changed.items()).encode()
        self.write_archive(changed, checksums=new_checksums)
        with self.assertRaisesRegex(ValueError, 'does not match independent pin'):
            ARCHIVE.verify(self.archive, self.pin)

    def test_traversal_wrong_root_links_and_special_archive_members_are_refused(self):
        cases = [
            ('focal-saved-evidence/../escape.txt', tarfile.REGTYPE),
            ('/absolute.txt', tarfile.REGTYPE),
            ('other-root/file.txt', tarfile.REGTYPE),
            ('focal-saved-evidence/symlink', tarfile.SYMTYPE),
            ('focal-saved-evidence/hardlink', tarfile.LNKTYPE),
            ('focal-saved-evidence/fifo', tarfile.FIFOTYPE),
        ]
        for name, kind in cases:
            with self.subTest(name=name):
                member = tarfile.TarInfo(name)
                member.type = kind
                if kind in (tarfile.SYMTYPE, tarfile.LNKTYPE):
                    member.linkname = '../outside.txt'
                self.write_archive(extra_members=[member])
                with self.assertRaises(ValueError):
                    ARCHIVE.verify(self.archive, self.pin)
                self.assertEqual(list(self.home.iterdir()), [self.archive])

    def test_duplicate_archive_members_and_checksum_rows_are_refused(self):
        member = tarfile.TarInfo('focal-saved-evidence/payload/synthetic/record.txt')
        self.write_archive(extra_members=[member])
        with self.assertRaisesRegex(ValueError, 'Duplicate archive file'):
            ARCHIVE.verify(self.archive, self.pin)
        repeated = self.checksums + self.checksums.splitlines(keepends=True)[0]
        self.write_archive(checksums=repeated)
        with self.assertRaisesRegex(ValueError, 'Duplicate checksum row'):
            ARCHIVE.verify(self.archive, hashlib.sha256(repeated).hexdigest())

    def test_directory_cannot_replace_or_precede_a_verified_file(self):
        directory = tarfile.TarInfo('focal-saved-evidence/payload/synthetic/record.txt')
        directory.type = tarfile.DIRTYPE
        for order in ('before', 'after'):
            with self.subTest(order=order):
                self.write_archive(initial_members=[directory] if order == 'before' else [],
                                   extra_members=[directory] if order == 'after' else [])
                with self.assertRaisesRegex(ValueError, 'conflicting archive member'):
                    ARCHIVE.verify(self.archive, self.pin)

    def test_file_cannot_be_an_explicit_or_implicit_parent_directory(self):
        parent_name = 'payload/synthetic'
        for order in ('before', 'after'):
            with self.subTest(order=order):
                members = ({parent_name: b'', **self.members} if order == 'before'
                           else {**self.members, parent_name: b''})
                checksums = ''.join(f'{hashlib.sha256(value).hexdigest()}  {name}\n'
                                    for name, value in members.items()).encode()
                self.write_archive(members, checksums=checksums)
                with self.assertRaisesRegex(ValueError, 'directory'):
                    ARCHIVE.verify(self.archive, hashlib.sha256(checksums).hexdigest())

        parent_file = tarfile.TarInfo('focal-saved-evidence/payload/synthetic/record.txt/child')
        parent_file.type = tarfile.DIRTYPE
        self.write_archive(extra_members=[parent_file])
        with self.assertRaisesRegex(ValueError, 'parent directory'):
            ARCHIVE.verify(self.archive, self.pin)

    def test_duplicate_directory_members_are_refused(self):
        directory = tarfile.TarInfo('focal-saved-evidence')
        directory.type = tarfile.DIRTYPE
        self.write_archive(extra_members=[directory])
        with self.assertRaisesRegex(ValueError, 'Duplicate or conflicting archive member'):
            ARCHIVE.verify(self.archive, self.pin)

    def test_explicit_parent_directories_may_precede_or_follow_their_files(self):
        directory = tarfile.TarInfo('focal-saved-evidence/payload/synthetic')
        directory.type = tarfile.DIRTYPE
        for order in ('before', 'after'):
            with self.subTest(order=order):
                self.write_archive(initial_members=[directory] if order == 'before' else [],
                                   extra_members=[directory] if order == 'after' else [])
                self.assertEqual(ARCHIVE.verify(self.archive, self.pin)['archive_integrity'],
                                 'PASS')

    def test_corrupt_crc_length_and_truncated_gzip_footer_are_refused(self):
        for fault in ('crc', 'length', 'truncated'):
            with self.subTest(fault=fault):
                self.write_archive()
                data = bytearray(self.archive.read_bytes())
                if fault == 'truncated':
                    del data[-8:]
                else:
                    data[-8 if fault == 'crc' else -4] ^= 1
                self.archive.write_bytes(data)
                with self.assertRaises((OSError, EOFError)):
                    ARCHIVE.verify(self.archive, self.pin)

    def test_truncated_gzip_cli_exits_failure_without_pass_result(self):
        self.write_archive()
        self.archive.write_bytes(self.archive.read_bytes()[:-8])
        output, errors = io.StringIO(), io.StringIO()
        with patch.object(sys, 'argv', ['verify_archive.py', '--archive', str(self.archive),
                                      '--checksums-sha256', self.pin]), \
                contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
            with self.assertRaises(SystemExit) as raised:
                ARCHIVE.main()
        self.assertEqual(raised.exception.code, 1)
        self.assertEqual(output.getvalue(), '')
        self.assertIn('EOFError', errors.getvalue())


if __name__ == '__main__':
    unittest.main()
