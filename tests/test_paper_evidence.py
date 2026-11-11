"""A valid outer archive digest cannot excuse bad member or manifest identities."""
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

SOURCE = Path(__file__).resolve().parents[1] / 'work/rerun-paper-revision-20261111/verify_new_archive.py'
SPEC = importlib.util.spec_from_file_location('paper_archive_readback', SOURCE)
READER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(READER)


class PaperArchiveReadback(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / 'repo'
        self.receipt = self.repo / 'work/focal-rerun-20261110/delivery-record.json'
        self.receipt.parent.mkdir(parents=True)
        self.archive = self.root / 'saved.tar.gz'
        self.output = self.root / 'new-review'

    def prepare(self, payload=b'original observation', duplicate=False, wrong_manifest_pin=False):
        original = b'original observation'
        manifest = json.dumps({'files': [{'path': 'run/observation.txt', 'bytes': len(original),
                                         'sha256': hashlib.sha256(original).hexdigest()}]}).encode()
        members = [('run/observation.txt', payload), ('MANIFEST.json', manifest)]
        if duplicate:
            members.append(('run/observation.txt', payload))
        with tarfile.open(self.archive, 'w:gz') as out:
            for name, data in members:
                info = tarfile.TarInfo(name)
                info.size = len(data)
                out.addfile(info, io.BytesIO(data))
        self.receipt.write_text(json.dumps({'run_root': str(self.root / 'run'), 'archive': {
            'bytes': self.archive.stat().st_size,
            'sha256': hashlib.sha256(self.archive.read_bytes()).hexdigest(),
            'manifest_sha256': '0' * 64 if wrong_manifest_pin else hashlib.sha256(manifest).hexdigest(),
            'verified_members': 2}}))

    def invoke(self):
        with patch.object(READER, 'REPO', self.repo), patch.object(sys, 'argv', [str(SOURCE),
                '--archive', str(self.archive), '--output', str(self.output)]), patch('builtins.print'):
            READER.main()

    def test_valid_archive_records_readback_without_extracting_payloads(self):
        self.prepare()
        before = self.archive.read_bytes()
        self.invoke()
        self.assertEqual(self.archive.read_bytes(), before)
        self.assertEqual({p.name for p in self.output.iterdir()},
                         {'archive-manifest.json', 'archive-readback.json'})
        report = json.loads((self.output / 'archive-readback.json').read_text())
        self.assertEqual(report['verified_members'], 2)
        self.assertFalse(report['human_verification'])

    def test_changed_member_fails_even_with_matching_outer_archive_digest(self):
        self.prepare(payload=b'different observation')
        with self.assertRaisesRegex(ValueError, 'inventory or payload digest mismatch'):
            self.invoke()
        self.assertFalse(self.output.exists())

    def test_duplicate_members_and_wrong_manifest_pin_fail(self):
        for args, error in [({'duplicate': True}, 'duplicate'),
                            ({'wrong_manifest_pin': True}, 'Manifest differs')]:
            with self.subTest(args=args):
                self.prepare(**args)
                with self.assertRaisesRegex(ValueError, error):
                    self.invoke()
                self.assertFalse(self.output.exists())

    def test_existing_review_output_is_preserved(self):
        self.prepare()
        self.output.mkdir()
        marker = self.output / 'saved.txt'
        marker.write_text('retained prior readback')
        with self.assertRaisesRegex(ValueError, 'fresh external'):
            self.invoke()
        self.assertEqual(marker.read_text(), 'retained prior readback')


if __name__ == '__main__':
    unittest.main()
