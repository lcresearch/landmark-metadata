#!/usr/bin/env python3
"""Read new raw records independently; does not execute models or infer missing runs."""
import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
import struct
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[2] /
                       'sources/repro-audit-20261004/maintained'))
from evidence_validation import required_fixture_digests, require_exact_identities

HAND_VARIANTS = ('original', 'container_control', 'metadata_exchange', 'restoration')
CORE_VARIANTS = ('original', 'description_control', 'label_deletion',
                 'label_permutation', 'label_restoration')
BASELINE_MODES = ('displayer', 'populator', 'simple_baseline', 'task_init')
E5_MANIFEST_SHA256 = 'bf49a475696eec4b38fb17587f6541a8393da14297e5dca1d433a051ba166e79'
ANDROID_VARIANTS = {
    'E1': ('original', 'description_control', 'label_deletion', 'label_restoration'),
    'E2': ('original', 'description_control', 'label_permutation', 'permutation_restoration'),
}
files = {}
checks = []


def read(path):
    path = Path(path)
    data = path.read_bytes()
    files[str(path)] = hashlib.sha256(data).hexdigest()
    return json.loads(data)


def check(name, condition, detail=None):
    checks.append({'check': name, 'passed': bool(condition), 'detail': detail})


def exact_records(name, records, fields, expected):
    """Require each prescribed identity once, before following record paths."""
    if not isinstance(records, list) or any(
            not isinstance(row, dict) or
            any(not isinstance(row.get(field), str) for field in fields)
            for row in records):
        check(name, False, {'error': 'Expected a list of records with string identity fields'})
        return False
    counts = Counter(tuple(row[field] for field in fields) for row in records)
    expected = set(expected)
    detail = {'missing': sorted(expected - counts.keys()),
              'unexpected': sorted(counts.keys() - expected),
              'duplicates': sorted(key for key, count in counts.items() if count > 1)}
    passed = not any(detail.values())
    check(name, passed, detail)
    return passed


def task():
    observations = []
    for phase in ('primary', 'replay'):
        original = {}
        for variant in CORE_VARIANTS:
            folder = Path('/workspace/repro-task') / phase / variant
            result = read(folder / 'result.json')
            if variant == 'label_deletion':
                check(f'{phase}/{variant}/early_rejection',
                      result['initialization_status'] == 'FAIL' and
                      all(result[k] == 'NOT_REACHED' for k in
                          ('classify_status', 'inference_status', 'decoder_status')) and
                      result['exception_type'] == 'ValueError' and
                      result['exception_message'] == 'Got 1000 class(es) for output index 0, expected 999 according to the label map.' and
                      len(result['observations']) == 0)
                continue
            valid_inputs = exact_records(f'{phase}/{variant}/exact_two_inputs',
                                         result.get('observations'), ('input',),
                                         [('gray127',), ('rgb_pattern',)])
            completed = all(result.get(k) == 'PASS' for k in
                            ('initialization_status', 'classify_status',
                             'inference_status', 'decoder_status'))
            check(f'{phase}/{variant}/completed', completed)
            if not valid_inputs or not completed:
                continue
            input_records = {item['input']: item for item in result['observations']}
            for input_name in ('gray127', 'rgb_pattern'):
                first_check = len(checks)
                prefix = f'{phase}/{variant}/{input_name}'
                item = input_records[input_name]
                # Task classify combines inference and decoding; the worker records
                # only input preparation, classify status and the returned count here.
                input_completed = (item.get('input_preparation_status') == 'PASS' and
                                   item.get('classify_status') == 'PASS' and
                                   item.get('returned_categories') == 1000)
                check(prefix+'/input_completed', input_completed)
                if not input_completed:
                    continue
                input_path = Path('/workspace/repro-task/inputs') / f'{input_name}-input.rgb'
                try:
                    input_bytes = input_path.read_bytes()
                except OSError as exc:
                    check(prefix+'/prescribed_input', False, {'error': str(exc)})
                    continue
                files[str(input_path)] = hashlib.sha256(input_bytes).hexdigest()
                expected_input = (bytes([127]) * (224*224*3) if input_name == 'gray127'
                                  else bytes((37*i+17) % 256 for i in range(224*224*3)))
                valid_input = (input_bytes == expected_input and
                               files[str(input_path)] == item.get('input_sha256'))
                check(prefix+'/prescribed_input', valid_input)
                if not valid_input:
                    continue
                path = folder / f'{input_name}-decoded.json'
                heads = read(path)
                categories = heads[0]['categories']
                by_index = {x['index']: x for x in categories}
                check(f'{phase}/{variant}/{input_name}/1000_unique_indices',
                      len(heads) == 1 and len(categories) == 1000 and set(by_index) == set(range(1000)))
                check(f'{phase}/{variant}/{input_name}/score_bits',
                      all(struct.unpack('<I', struct.pack('<f', x['score']))[0] == x['score_float_bits']
                          for x in categories))
                if variant == 'original':
                    original[input_name] = by_index
                if input_name not in original:
                    check(prefix+'/validated_original_available', False)
                    continue
                reference = original[input_name]
                changed = sum(x['label'] != reference[i]['label'] for i, x in by_index.items())
                check(f'{phase}/{variant}/{input_name}/score_preservation',
                      all(x['score_float_bits'] == reference[i]['score_float_bits'] for i, x in by_index.items()))
                check(f'{phase}/{variant}/{input_name}/label_changes',
                      changed == (999 if variant == 'label_permutation' else 0), changed)
                if variant == 'label_permutation':
                    check(f'{phase}/{variant}/{input_name}/complete_cyclic_mapping',
                          all(x['label'] == reference[(i + 1) % 1000]['label'] for i, x in by_index.items()))
                if phase == 'replay':
                    primary = read(Path('/workspace/repro-task/primary') / variant / path.name)
                    check(f'{phase}/{variant}/{input_name}/equal_primary', heads == primary)
                if all(row['passed'] for row in checks[first_check:]):
                    observations.append({'phase': phase, 'variant': variant, 'input': input_name,
                                         'changed_labels': changed})
    task_baseline()
    return {'execution_records': 10, 'successful_decoded_observations': len(observations),
            'categories_read': len(observations) * 1000, 'observations': observations}


def core_model_digests(prefix):
    """Bind the five named conditions to the actual Android model bytes."""
    digests = {}
    for variant in CORE_VARIANTS:
        experiment = 'E2' if variant == 'label_permutation' else 'E1'
        path = Path('/workspace/repro-android') / experiment / 'variants' / variant / 'model.tflite'
        try:
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
        except OSError as exc:
            check(prefix+'/core_model/'+variant, False, {'error': str(exc)})
            continue
        files[str(path)] = digest
        digests[variant] = digest
    return digests


def task_baseline(core_digests=None, prefix='baseline'):
    first_check = len(checks)
    if core_digests is None:
        core_digests = core_model_digests(prefix)
    baseline = read('/workspace/repro-task/baseline-results.json')
    if not exact_records(prefix+'/exact_20_conditions', baseline, ('variant', 'mode'),
                         [(variant, mode) for variant in CORE_VARIANTS for mode in BASELINE_MODES]):
        return None
    for record in baseline:
        key = prefix+'/' + record['variant'] + '/' + record['mode']
        result = record.get('result')
        result = result if isinstance(result, dict) else {}
        expected_digest = core_digests.get(record['variant'])
        check(key+'/exact_core_artifact', expected_digest is not None and
              result.get('model_sha256') == expected_digest,
              {'observed': result.get('model_sha256'), 'expected': expected_digest})
        actual = result.get('status')
        expected = {'displayer': 'READABLE', 'populator': 'ACCEPTED',
                    'simple_baseline': 'COMPATIBLE_PRECONDITIONS', 'task_init': 'PASS'}[record['mode']]
        if record['variant'] == 'label_deletion':
            if record['mode'] == 'simple_baseline': expected = 'INCOMPATIBLE'
            if record['mode'] == 'task_init': expected = 'FAIL'
        check(key, actual == expected,
              {'observed': actual, 'expected': expected})
    return baseline if all(row['passed'] for row in checks[first_check:]) else None


def hand():
    base = Path('/workspace/repro-hand/executions')
    manifests = {}
    complete = True
    for phase in ('primary', 'replay'):
        manifests[phase] = read(base / phase / 'results.json')
        valid = exact_records(f'hand/{phase}/exact_four_conditions', manifests[phase],
                              ('variant',), [(variant,) for variant in HAND_VARIANTS])
        complete = complete and valid
    if not complete:
        return {'expected_execution_records': 8, 'execution_records_read': 0,
                'complete': False, 'records': []}
    reference = read(base / 'primary/original/outputs/decoded.json')
    reference_bits = (base / 'primary/original/outputs/decoded-float-bits.bin').read_bytes()
    records = []
    for phase in ('primary', 'replay'):
        for record in manifests[phase]:
            variant = record['variant']
            first_check = len(checks)
            result = read(base / phase / variant / 'outputs/result.json')
            completed = (record.get('exit_code') == 0 and record.get('completed') is True and
                         all(result.get(key) == 'PASS' for key in
                             ('initialization_status', 'input_preparation_status', 'detect_status')))
            check(f'hand/{phase}/{variant}/actual_completed', completed)
            if not completed:
                continue
            decoded = read(base / phase / variant / 'outputs/decoded.json')
            check(f'hand/{phase}/{variant}/one_hand_21_landmarks',
                  len(decoded['handedness']) == 1 and
                  len(decoded['hand_landmarks']) == 1 and len(decoded['hand_landmarks'][0]) == 21 and
                  len(decoded['hand_world_landmarks']) == 1 and len(decoded['hand_world_landmarks'][0]) == 21)
            check(f'hand/{phase}/{variant}/decoded_equal', decoded == reference)
            bits_path = base / phase / variant / 'outputs/decoded-float-bits.bin'
            bits = bits_path.read_bytes()
            files[str(bits_path)] = hashlib.sha256(bits).hexdigest()
            check(f'hand/{phase}/{variant}/exact_float_bits_equal',
                  len(bits) > 0 and bits == reference_bits and files[str(bits_path)] == result['decoded_float_bits_sha256'])
            if all(row['passed'] for row in checks[first_check:]):
                records.append({'phase': phase, 'variant': variant})
    return {'expected_execution_records': 8, 'execution_records_read': len(records),
            'complete': len(records) == 8, 'records': records}


def external():
    root = Path('/workspace/repro-external')
    results = read(root / 'E4/results.json')
    http = Counter(x['http_status'] for x in results['downloads'])
    counts = Counter(x['status'] for x in results['component_occurrences'])
    included = [x for x in results['component_occurrences'] if x['status'] == 'CHECKED']
    structural = Counter(x['structural_status'] for x in included)
    compile_outcomes = Counter(x['compile_status'] for x in included)
    semantic = Counter(x['semantic_check'] for x in included)
    decoder = Counter('inapplicable' if x['decoder_check'] == 'INAPPLICABLE_NO_GENERATED_CATEGORY_PATH' else
                      'compatible' if all(c['status'] == 'PASS' for c in x['decoder_check']) else
                      'incompatible' for x in included)
    check('E4/candidates_HTTP', len(results['downloads']) == 20 and http == {200: 16, 404: 4}, dict(http))
    check('E4/occurrences', counts == {'CHECKED': 15, 'EXCLUDED_PRIOR_COMPONENT': 1, 'EXCLUDED_PRIOR_GRAPH': 2}, dict(counts))
    check('E4/unique_graphs', len({x['canonical_graph_sha256'] for x in included}) == 15)
    check('E4/S', structural == {'PASS': 15}, dict(structural))
    check('E4/javac', compile_outcomes == {'PASS': 8, 'FAIL': 7}, dict(compile_outcomes))
    check('E4/I', semantic == {'ABSTAIN_NO_SEMANTIC_REFERENCE': 15}, dict(semantic))
    check('E4/D', decoder == {'compatible': 4, 'incompatible': 9, 'inapplicable': 2}, dict(decoder))
    failing = [x for x in included if isinstance(x['decoder_check'], list) and any(c['status'] != 'PASS' for c in x['decoder_check'])]
    check('E4/five_D_failures_already_uncompilable', sum(x['compile_status'] == 'FAIL' for x in failing) == 5)
    warned = [x for x in failing if x['compile_status'] == 'PASS']
    check('E4/four_compiling_D_failures_have_nonRGB_warning', len(warned) == 4 and
          all('non-rgb' in x['checker']['generation']['diagnostics'].lower() for x in warned))
    for model in included:
        p = root / model['artifact_paths']['model']
        actual = hashlib.sha256(p.read_bytes()).hexdigest()
        files[str(p)] = actual
        check('E4/model_digest/' + model['candidate'], actual == model['component_sha256'])
    return {'candidates': len(results['downloads']), 'HTTP': dict(http), 'occurrences': dict(counts),
            'S': dict(structural), 'javac': dict(compile_outcomes), 'I': dict(semantic), 'D': dict(decoder)}


def android():
    root = Path('/workspace/repro-android')
    original_folder = root / 'E1/executions/primary/original/device'
    missing = []
    completed = []
    for experiment, variants in ANDROID_VARIANTS.items():
        for phase in ('primary', 'replay'):
            for variant in variants:
                folder = root / experiment / 'executions' / phase / variant / 'device'
                path = folder / 'result.json'
                key = f'android/{experiment}/{phase}/{variant}'
                if not path.is_file():
                    missing.append(str(path))
                    continue
                result = read(path)
                observations = result.get('observations', [])
                if not exact_records(key+'/exact_two_inputs', observations, ('input',),
                                     [('gray127',), ('rgb_pattern',)]):
                    missing.append(str(path) + ': incomplete or duplicate input identities')
                    continue
                check(key+'/load', result['model_loading_status'] == 'PASS')
                model = root / experiment / 'variants' / variant / 'model.tflite'
                actual = hashlib.sha256(model.read_bytes()).hexdigest()
                files[str(model)] = actual
                check(key+'/asset_identity', result['loaded_asset_sha256'] == actual)
                for item in observations:
                    input_name = item['input']
                    prefix = key+'/'+input_name
                    check(prefix+'/inference', item['input_preparation_status'] == 'PASS' and item['inference_status'] == 'PASS')
                    input_path = folder / (input_name + '-input.rgb')
                    input_bytes = input_path.read_bytes()
                    files[str(input_path)] = hashlib.sha256(input_bytes).hexdigest()
                    expected_input = bytes([127]) * (224*224*3) if input_name == 'gray127' else bytes((37*i+17) % 256 for i in range(224*224*3))
                    check(prefix+'/prescribed_input', input_bytes == expected_input and files[str(input_path)] == item['input_sha256'])
                    raw_path = folder / (input_name + '-output-0.f32')
                    raw = raw_path.read_bytes()
                    files[str(raw_path)] = hashlib.sha256(raw).hexdigest()
                    baseline_raw = (original_folder / raw_path.name).read_bytes()
                    check(prefix+'/1000_raw_values_and_recorded_digest',
                          len(raw) == 4000 and files[str(raw_path)] == item['raw_output_sha256'])
                    check(prefix+'/raw_equal_new_original', raw == baseline_raw)
                    if variant == 'label_deletion':
                        check(prefix+'/getter_rejection', item['generated_getter_status'] == 'FAIL')
                        check(prefix+'/exact_generated_getter_exception',
                              item.get('earliest_failing_stage') == 'generated_getter' and
                              item.get('exception_type') == 'java.lang.IllegalArgumentException' and
                              item.get('exception_message') == 'Label number 999 mismatch the shape on axis 1' and
                              'ContractModel$Outputs.getProbabilityAsCategoryList' in item.get('stack_trace', ''))
                        continue
                    check(prefix+'/getter_success', item['generated_getter_status'] == 'PASS')
                    decoded = read(folder / (input_name + '-decoded.json'))
                    original = read(original_folder / (input_name + '-decoded.json'))
                    bits = struct.unpack('<1000I', raw)
                    check(prefix+'/complete_positions', len(decoded) == 1000 and
                          [v['list_position'] for v in decoded] == list(range(1000)))
                    check(prefix+'/decoded_bits_equal_raw',
                          all(v['score_float_bits'] == bits[i] ==
                              struct.unpack('<I', struct.pack('<f', v['score']))[0]
                              for i, v in enumerate(decoded)))
                    check(prefix+'/category_index_unset', all(v['category_index_field'] == -1 for v in decoded))
                    offset = 1 if variant == 'label_permutation' else 0
                    changed = sum(v['label'] != original[i]['label'] for i, v in enumerate(decoded))
                    check(prefix+'/complete_labels',
                          all(v['label'] == original[(i+offset) % 1000]['label'] for i, v in enumerate(decoded)) and
                          changed == (999 if offset else 0), changed)
                    position, score, label = ((649, 0.001122338930144906, 'microphone' if offset else 'megalith')
                                              if input_name == 'gray127' else
                                              (904, 0.23542051017284393, 'window shade' if offset else 'window screen'))
                    check(prefix+'/published_specific_score', decoded[position]['score'] == score and decoded[position]['label'] == label)
                completed.append({'experiment': experiment, 'phase': phase, 'variant': variant,
                                  'model_sha256': actual})
    return {'expected_execution_records': 16, 'completed_execution_records': len(completed),
            'complete': not missing, 'missing': missing, 'records': completed,
            'historical_raw_comparison': 'Not available; equal_new_original checks only freshly generated arrays.'}


def android_code():
    root = Path('/workspace/repro-android')
    source_hashes = set()
    class_maps = []
    dex_maps = []
    for experiment, variants in ANDROID_VARIANTS.items():
        rows = read(root / experiment / 'build-results.json')
        if not exact_records('code/'+experiment+'/exact_four_builds', rows, ('variant',),
                             [(variant,) for variant in variants]):
            continue
        for row in rows:
            prefix = 'code/'+experiment+'/'+row['variant']
            folder = root / experiment / 'variants' / row['variant']
            source = folder / 'generated/src/main/java/org/example/contract/ContractModel.java'
            source_hashes.add(hashlib.sha256(source.read_bytes()).hexdigest())
            actual_classes = {}
            for path in (folder/'build/classes').rglob('ContractModel*.class'):
                actual_classes[str(path.relative_to(folder/'build/classes'))] = hashlib.sha256(path.read_bytes()).hexdigest()
            actual_dex = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in (folder/'build/dex').glob('*.dex')}
            check(prefix+'/actual_classes_match_record', len(actual_classes) == 3 and actual_classes == row['generated_class_hashes'])
            check(prefix+'/actual_dex_match_record', len(actual_dex) >= 1 and actual_dex == row['dex_hashes'])
            check(prefix+'/all_build_stages_complete', len(row['stages']) == 6 and all(x['status'] == 'PASS' and x['exit_code'] == 0 for x in row['stages'].values()))
            class_maps.append(actual_classes)
            dex_maps.append(actual_dex)
    check('code/all_eight_generated_Java_identical', len(source_hashes) == 1)
    check('code/all_eight_generated_class_sets_identical', len(class_maps) == 8 and all(x == class_maps[0] for x in class_maps))
    check('code/all_eight_DEX_sets_identical', len(dex_maps) == 8 and all(x == dex_maps[0] for x in dex_maps))
    return {'generated_sources': len(class_maps), 'distinct_source_hashes': sorted(source_hashes),
            'scope': 'Direct fresh on-disk file hashing; no comparison with missing historical binaries.'}


def preflight(required_manifest=None, required_manifest_sha256=E5_MANIFEST_SHA256):
    first_check = len(checks)
    root = Path('/workspace/repro-external/E5')
    manifest = Path(required_manifest) if required_manifest is not None else root / 'results.json'
    try:
        required = required_fixture_digests(manifest, required_manifest_sha256)
    except (OSError, ValueError, TypeError, KeyError) as exc:
        check('E5/frozen_required_manifest', False, {'error': str(exc)})
        return {'expected_fixtures': 65, 'complete': False}
    files[str(manifest)] = required_manifest_sha256
    check('E5/frozen_required_manifest', True,
          {'path': str(manifest), 'sha256': required_manifest_sha256})
    fixtures = read(root / 'results.json')['fixtures']
    try:
        require_exact_identities((x['model_sha256'] for x in fixtures), required,
                                 'Original E5 fixtures')
    except (TypeError, KeyError, ValueError) as exc:
        check('E5/exact_required_65', False, {'error': str(exc)})
        return {'expected_fixtures': 65, 'complete': False}
    check('E5/exact_required_65', True)
    counts = {}
    for dimension, expected in {
        'STRUCTURAL': {'ACCEPTED_BY_METADATA_POPULATOR_0_4_4': 52, 'REJECTED_BY_METADATA_POPULATOR_0_4_4': 11, 'ABSTAIN_NO_METADATA': 2},
        'DECODER_COMPATIBILITY': {'INCOMPATIBLE': 27, 'NOT_REACHED': 11, 'INAPPLICABLE_NO_SELECTED_GETTER': 14, 'ABSTAIN_NO_METADATA': 2, 'ABSTAIN': 3, 'COMPATIBLE_PRECONDITIONS': 8},
        'REFERENCE_BACKED_SEMANTIC': {'ABSTAIN': 65}}.items():
        counts[dimension] = dict(Counter(x['report'][dimension]['status'] for x in fixtures))
        check('E5/'+dimension+'/counts', counts[dimension] == expected, counts[dimension])
    by_hash = {}
    for fixture in fixtures:
        path = Path(fixture['path'])
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        files[str(path)] = actual
        check('E5/model_identity/'+fixture['model_sha256'], actual == fixture['model_sha256'] == fixture['report']['artifact_sha256'])
        report = read(root / 'checks' / actual / 'result.json')
        check('E5/individual_result/'+actual, report == fixture['report'])
        by_hash[actual] = report
    core_digests = core_model_digests('E5')
    baseline = task_baseline(core_digests, 'E5/baseline')
    for record in baseline or []:
        if record['mode'] not in ('simple_baseline', 'task_init'): continue
        report = by_hash.get(record['result']['model_sha256'])
        expected_reject = record['variant'] == 'label_deletion'
        check('E5/core_rejection/'+record['mode']+'/'+record['variant'],
              report is not None and
              (report['DECODER_COMPATIBILITY']['status'] == 'INCOMPATIBLE') == expected_reject)
    for variant in CORE_VARIANTS:
        digest = core_digests.get(variant)
        check('E5/exact_Android_artifact/'+variant, digest in by_hash and
              (by_hash[digest]['DECODER_COMPATIBILITY']['status'] == 'INCOMPATIBLE') == (variant == 'label_deletion'))
    complete = all(row['passed'] for row in checks[first_check:])
    return {'fixtures': len(fixtures), 'complete': complete, 'counts': counts,
            'core_extra_rejections_over_simple_and_Task_init': 0 if complete else None,
            'scope': 'Static on actual recovered files; no Android success/failure is inferred.'}


def main(output_dir, required_manifest=None, required_manifest_sha256=E5_MANIFEST_SHA256):
    files.clear()
    checks.clear()
    result = {'scope': 'Independent readback of new records; no historical raw-byte comparison or new model execution.',
              'task': task(), 'hand': hand(), 'external': external(), 'android': android(),
              'android_code': android_code(),
              'preflight': preflight(required_manifest, required_manifest_sha256)}
    result['checks'] = checks
    result['passed'] = sum(x['passed'] for x in checks)
    result['failed'] = sum(not x['passed'] for x in checks)
    result['read_file_sha256'] = files
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    with (output_dir / 'observation-readback.json').open('x') as stream:
        stream.write(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'passed': result['passed'], 'failed': result['failed'],
                      'Android_complete': result['android']['complete'],
                      'Android_completed_records': result['android']['completed_execution_records'],
                      'Android_missing_records': result['android']['missing'],
                      'failures': [x for x in checks if not x['passed']]}, indent=2))
    return 1 if result['failed'] else 2 if not result['android']['complete'] else 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, required=True,
                        help='New report directory outside sealed evidence; existing reports are never overwritten')
    parser.add_argument('--required-manifest', type=Path,
                        help='Frozen original E5 catalog or manifest of 65 artifact_sha256s; defaults to the original E5 catalog path')
    parser.add_argument('--required-manifest-sha256', default=E5_MANIFEST_SHA256,
                        help='Previously recorded manifest digest; default pins claim C32, never derive from the run being checked')
    args = parser.parse_args()
    raise SystemExit(main(args.output_dir, args.required_manifest, args.required_manifest_sha256))
