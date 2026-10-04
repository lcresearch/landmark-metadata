"""Synthetic evidence regressions; no models, network or optional ML packages."""
import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

AREA = Path(__file__).resolve().parents[1] / 'sources/repro-audit-20261004'


def load(relative):
    path = AREA / relative
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


V = load('maintained/evidence_validation.py')


class EvidenceIdentityTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.required = [hashlib.sha256(str(i).encode()).hexdigest() for i in range(65)]

    def test_frozen_manifest_and_reordered_complete_catalog(self):
        p = self.root / 'required.json'
        p.write_text(json.dumps({'artifact_sha256s': self.required}))
        expected = V.required_fixture_digests(p, hashlib.sha256(p.read_bytes()).hexdigest())
        V.require_exact_identities(reversed(self.required), expected, 'fixtures')
        p.write_text(json.dumps({'fixtures':[{'model_sha256':d} for d in self.required]}))
        expected = V.required_fixture_digests(p, hashlib.sha256(p.read_bytes()).hexdigest())
        V.require_exact_identities(self.required, expected, 'frozen original catalog')

    def test_manifest_digest_and_count_are_required(self):
        p = self.root / 'required.json'
        p.write_text(json.dumps({'artifact_sha256s': self.required[:1]}))
        for digest in ['0'*64, hashlib.sha256(p.read_bytes()).hexdigest()]:
            with self.subTest(digest=digest), self.assertRaises(ValueError):
                V.required_fixture_digests(p, digest)

    def test_truncated_duplicate_and_replaced_catalogs_fail(self):
        for actual in [self.required[:1], self.required[:-1]+self.required[:1],
                       self.required[:-1]+['f'*64]]:
            with self.subTest(actual=actual), self.assertRaises(ValueError):
                V.require_exact_identities(actual, self.required, 'fixtures')

    def test_catalog_prior_report_and_actual_bytes_must_agree(self):
        model = self.root / 'synthetic.txt'
        model.write_bytes(b'synthetic model placeholder')
        digest = hashlib.sha256(model.read_bytes()).hexdigest()
        fixture = {'path': str(model), 'model_sha256': digest,
                   'report': {'artifact_sha256': digest}}
        V.require_fixture_digest(fixture, {'artifact_sha256': digest})
        with self.assertRaises(ValueError):
            V.require_fixture_digest(fixture, {'artifact_sha256': '0'*64})
        fixture['report']['artifact_sha256'] = '0'*64
        with self.assertRaises(ValueError):
            V.require_fixture_digest(fixture)
        fixture['report']['artifact_sha256'] = digest
        model.write_bytes(b'changed but hypothetical judgments unchanged')
        with self.assertRaises(ValueError):
            V.require_fixture_digest(fixture)

    def test_each_output_position_is_required_once(self):
        self.assertTrue(V.complete_output_positions([{'position':1},{'position':0}],2))
        for positions in [[0,0],[0],[0,2],[0,True]]:
            self.assertFalse(V.complete_output_positions([{'position':p} for p in positions],2))

    def decoder_design(self):
        predictions = [{'field':f'output{i}','output_position':i,'status':'PASS',
                        'label_count':2} for i in range(23)]
        static = [{'id':'component','variants':[{'variant':'original',
                                               'decoder_checks':predictions}]}]
        records = [{'id':'component','variant':'original','prediction':dict(p)}
                   for p in predictions]
        return static, records

    def test_decoder_requires_every_static_identity(self):
        static, records = self.decoder_design()
        V.require_decoder_records(static,list(reversed(records)))
        for bad in [[records[0]]*23, records[:-1]]:
            with self.assertRaises(ValueError):
                V.require_decoder_records(static,bad)

    def test_decoder_prediction_must_match_static_suite(self):
        static, records = self.decoder_design()
        records[0]['prediction']['label_count'] = 999
        with self.assertRaises(ValueError):
            V.require_decoder_records(static,records)

    def test_generation_needs_every_digest(self):
        variants = ['original','vt','unicode']
        records = [{'variant':v,'generated_source_sha256':'a'*64} for v in variants]
        self.assertTrue(V.generated_sources_identical(records,variants))
        self.assertFalse(V.generated_sources_identical(records[:1],variants))
        records[1]['generated_source_sha256'] = 'b'*64
        self.assertFalse(V.generated_sources_identical(records,variants))
        for row in records: row['generated_source_sha256'] = None
        self.assertFalse(V.generated_sources_identical(records,variants))


class ReconstructionIOTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)

    def test_fresh_fetch_records_all_failed_downloads(self):
        module = load('hand/scripts/fetch_assets.py')
        module.ROOT = self.root
        module.pinned_asset = lambda name: ('https://example.org/'+name,'0'*64)
        with patch.object(module.urllib.request,'urlopen',side_effect=OSError('offline')), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(module.main(),1)
        self.assertTrue((self.root/'assets').is_dir())
        rows = json.loads((self.root/'results/assets.json').read_text())
        self.assertEqual(len(rows),3)
        self.assertTrue(all(r['status']=='FAIL' for r in rows))

    def test_fresh_fetch_can_write_downloads(self):
        module = load('hand/scripts/fetch_assets.py')
        module.ROOT = self.root
        component = b'synthetic component'
        module.FOCAL = hashlib.sha256(component).hexdigest()
        bundle = io.BytesIO()
        with zipfile.ZipFile(bundle,'w') as archive:
            archive.writestr('hand_landmarks_detector.tflite',component)
        payload = bundle.getvalue()
        module.pinned_asset = lambda name: ('https://example.org/'+name,hashlib.sha256(payload).hexdigest())
        class Response(io.BytesIO):
            status=200
            url='https://example.org/asset'
        with patch.object(module.urllib.request,'urlopen',side_effect=lambda *a,**kw:Response(payload)), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(module.main(),0)
        self.assertEqual(len(list((self.root/'assets').iterdir())),3)

    def test_conversion_timeout_preserves_batch_and_pdf_provenance(self):
        module = load('reproduction/retrieve_literature.py')
        class Response(io.BytesIO):
            status=200
            headers={'Content-Type':'application/pdf'}
            def geturl(self): return 'https://example.org/final'
        out = self.root/'retrieval'
        with patch.object(module.urllib.request,'urlopen',side_effect=lambda *a,**kw:Response(b'%PDF-synthetic')), patch.object(module.subprocess,'run',side_effect=subprocess.TimeoutExpired('pdftotext',45)), patch.object(sys,'argv',['retrieve','--output-dir',str(out)]), contextlib.redirect_stdout(io.StringIO()):
            module.main()
        rows = json.loads((out/'retrieval.json').read_text())
        self.assertEqual(len(rows),14)
        pdfs = [r for r in rows if r['name'].endswith('.pdf')]
        self.assertEqual(len(pdfs),4)
        for row in pdfs:
            self.assertEqual(row['status'],'DOWNLOADED')
            self.assertEqual(row['text_status'],'TIMEOUT')
            self.assertEqual(row['sha256'],hashlib.sha256(Path(row['path']).read_bytes()).hexdigest())


if __name__ == '__main__':
    unittest.main()
