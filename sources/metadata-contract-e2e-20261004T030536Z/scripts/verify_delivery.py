"""Read-only evidence verification; no generation, compiler, interpreter or inference run."""
import argparse
import collections
import datetime
import hashlib
import json
import pathlib
import struct
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
ap = argparse.ArgumentParser()
ap.add_argument('--record', help='Optional NEW JSON path relative to evidence root')
args = ap.parse_args()
cache = {}
failures = []

def digest(path):
    path = pathlib.Path(path)
    if path not in cache:
        with path.open('rb') as handle:
            cache[path] = hashlib.file_digest(handle, 'sha256').hexdigest()
    return cache[path]

def read(path):
    return json.loads(pathlib.Path(path).read_text())

def verify_rows(base, rows):
    bad = []
    for row in rows:
        p = pathlib.Path(base) / row['path']
        if not p.is_file() or digest(p) != row['sha256']:
            bad.append(str(p))
    failures.extend(bad)
    return {'entries': len(rows), 'matches': len(rows) - len(bad), 'mismatches': bad}

def sums(path):
    rows = []
    for line in path.read_text().splitlines():
        expected, name = line.split('  ', 1)
        rows.append({'path': name, 'sha256': expected})
    result = verify_rows(path.parent, rows)
    result['manifest_sha256'] = digest(path)
    return result

report = {'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'evidence_status': 'Fresh read-only hash and saved-result audit; no new experiment execution',
          'human_verification': 'PENDING'}
report['phase0_inventory'] = verify_rows('/', read(ROOT / 'phase0/inventory.json'))
report['historical_manifests'] = {}
for folder, name in [('/workspace/metadata-contract-paper', 'WORKSPACE-EVIDENCE-MANIFEST.json'),
                     ('/workspace/hand-contract-repro', 'MANIFEST.json')]:
    p = pathlib.Path(folder) / name
    report['historical_manifests'][str(p)] = verify_rows(p.parent, read(p)['files'])
report['sealed_experiments'] = {x: sums(ROOT / x / 'SHA256SUMS') for x in ['E1','E2','E3','E4','E5','E7']}

def assert_android():
    out = {}
    for ex in ['E1', 'E2']:
        data = read(ROOT / ex / 'results.json')
        assert len(data['units']) == 4
        base = ROOT / ex / 'variants/original'
        source_name = 'generated/src/main/java/org/example/contract/ContractModel.java'
        source = (base / source_name).read_bytes()
        classes = {str(p.relative_to(base / 'build/classes')): p.read_bytes()
                   for p in (base / 'build/classes').rglob('ContractModel*.class')}
        dex = {p.name: p.read_bytes() for p in (base / 'build/dex').glob('*.dex')}
        assert classes and dex
        original_device = ROOT / ex / 'executions/primary/original/device'
        records = []
        for unit in data['units']:
            variant = unit['variant']
            folder = ROOT / ex / 'variants' / variant
            assert (folder / source_name).read_bytes() == source
            assert {str(p.relative_to(folder / 'build/classes')): p.read_bytes()
                    for p in (folder / 'build/classes').rglob('ContractModel*.class')} == classes
            assert {p.name: p.read_bytes() for p in (folder / 'build/dex').glob('*.dex')} == dex
            assert digest(folder / 'model.tflite') == unit['variant_sha256']
            assert unit['preservation_check']['canonical_equal']
            assert unit['preservation_check']['nonmetadata_buffers_equal']
            if variant != 'description_control':
                assert unit['preservation_check']['embedded_metadata_equal']
                assert unit['preservation_check']['flatbuffer_prefix_equal']
            for record in [unit, unit['replay_record']]:
                assert record is not None
                device = ROOT / record['artifact_paths']['execution'] / 'device'
                observed = read(device / 'result.json')
                assert observed['model_loading_status'] == 'PASS'
                assert len(observed['observations']) == 2
                for item in observed['observations']:
                    case = item['input']
                    raw = (device / (case + '-output-0.f32')).read_bytes()
                    assert len(raw) == 4000
                    assert raw == (original_device / (case + '-output-0.f32')).read_bytes()
                    assert (device / (case + '-input.rgb')).read_bytes() == (original_device / (case + '-input.rgb')).read_bytes()
                    assert digest(device / (case + '-output-0.f32')) == item['raw_output_sha256']
                    scores = struct.unpack('<1000f', raw)
                    bits = struct.unpack('<1000I', raw)
                    expected_top = sorted(range(1000), key=lambda i: (-scores[i], i))[:5]
                    assert [i['index'] for i in item['top5_raw']] == expected_top
                    assert item['input_preparation_status'] == item['inference_status'] == 'PASS'
                    decoded_file = device / (case + '-decoded.json')
                    if variant == 'label_deletion':
                        assert item['generated_getter_status'] == 'FAIL'
                        assert item['earliest_failing_stage'] == 'generated_getter'
                        assert item['exception_type'] == 'java.lang.IllegalArgumentException'
                        assert item['exception_message'] == 'Label number 999 mismatch the shape on axis 1'
                        assert 'ContractModel$Outputs.getProbabilityAsCategoryList' in item['stack_trace']
                        assert not decoded_file.exists()
                    else:
                        assert item['generated_getter_status'] == 'PASS'
                        decoded = read(decoded_file)
                        reference = read(original_device / (case + '-decoded.json'))
                        assert len(decoded) == 1000
                        assert [i['score_float_bits'] for i in decoded] == list(bits)
                        assert all(i['list_position'] == j and i['category_index_field'] == -1 for j,i in enumerate(decoded))
                        if variant == 'label_permutation':
                            assert all(i['label'] == reference[(j+1)%1000]['label'] for j,i in enumerate(decoded))
                            assert sum(a['label'] != b['label'] for a,b in zip(decoded,reference)) == 999
                        else:
                            assert decoded == reference
            records.append({'variant': variant, 'primary_and_replay_verified': True,
                            'decoded_replay_comparison': 'NOT_APPLICABLE_DECODER_FAILED' if variant == 'label_deletion' else 'EQUAL'})
        out[ex] = records
    labels = lambda p: (ROOT / p / 'associated/labels_without_background.txt').read_text().splitlines()
    original = labels('E1/variants/original')
    perm = labels('E2/variants/label_permutation')
    assert perm == original[1:] + original[:1]
    assert collections.Counter(perm) == collections.Counter(original)
    assert labels('E1/variants/label_deletion') == original[:-1]
    assert labels('E1/variants/label_restoration') == original
    assert labels('E2/variants/permutation_restoration') == original
    freeze = read(ROOT / 'phase0/pre-E2-freeze.json')
    assert freeze['plan_sha256'] == digest(ROOT / 'EXPERIMENT_E2_PLAN.md')
    return out

def assert_other_results():
    for run in ['primary', 'replay']:
        task = read(ROOT / 'E3/executions' / run / 'label_deletion/outputs/result.json')
        assert task['model_sha256'] == digest(ROOT / 'E1/variants/label_deletion/model.tflite')
        assert task['earliest_failing_stage'] == 'task_initialization'
        assert task['initialization_status'] == 'FAIL'
        assert task['inference_status'] == task['decoder_status'] == 'NOT_REACHED'
        assert task['exception_message'] == 'Got 1000 class(es) for output index 0, expected 999 according to the label map.'
    base = ROOT / 'E7/executions/primary/original/outputs'
    for run in ['primary', 'replay']:
        for name in ['original', 'container_control', 'metadata_exchange', 'restoration']:
            folder = ROOT / 'E7/executions' / run / name / 'outputs'
            item = read(folder / 'result.json')
            assert item['initialization_status'] == item['detect_status'] == 'PASS'
            assert item['detected_hands'] == 1
            assert item['landmarks_per_hand'] == item['world_landmarks_per_hand'] == [21]
            for filename in ['decoded.json', 'decoded-float-bits.bin']:
                assert (folder / filename).read_bytes() == (base / filename).read_bytes()
            assert digest(folder / 'decoded-float-bits.bin') == item['decoded_float_bits_sha256']
    ext = read(ROOT / 'E4/summary.json')
    assert (ext['candidate_urls'],ext['downloaded'],len(ext['unavailable']),ext['new_canonical_graphs']) == (20,16,4,15)
    assert ext['fresh_runtime_invocations'] == 0
    assert len(read(ROOT / 'E5/results.json')['fixtures']) == 65
    return {'task_deletion_earliest_failure': 'task_initialization', 'Hand_task_primary_and_replay_decoded_bytes': 'EQUAL',
            'external_new_graphs': 15, 'preflight_distinct_byte_fixtures': 65}

for key, operation in [('android_saved_evidence', assert_android), ('other_saved_evidence', assert_other_results)]:
    try:
        report[key] = operation()
    except Exception as exc:
        import traceback
        failures.append({'check': key, 'exception': repr(exc), 'traceback': traceback.format_exc()})

if (ROOT / 'SHA256SUMS').exists():
    report['global_manifest'] = sums(ROOT / 'SHA256SUMS')
report['failures'] = failures
report['status'] = 'PASS' if not failures else 'FAIL'
if args.record:
    path = ROOT / args.record
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as handle:
        json.dump(report, handle, indent=2)
print(json.dumps({'status': report['status'], 'phase0_inventory': report['phase0_inventory'],
                  'historical_manifests': report['historical_manifests'],
                  'sealed_experiments': report['sealed_experiments'],
                  'global_manifest': report.get('global_manifest', 'NOT_CREATED_YET'),
                  'saved_result_cross_checks': 'PASS' if not failures else 'SEE_FAILURES',
                  'failures': failures}, indent=2))
sys.exit(1 if failures else 0)
