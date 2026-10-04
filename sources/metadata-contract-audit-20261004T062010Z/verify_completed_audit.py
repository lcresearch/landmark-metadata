#!/usr/bin/env python3
"""Root cross-check of completed new device records, without running models."""
import hashlib, json, pathlib, struct, zipfile

ROOT = pathlib.Path(__file__).resolve().parent
FRESH = ROOT / 'rebuild'
OLD = pathlib.Path('/workspace/metadata-contract-e2e-20261004T030536Z')
VARIANTS = {
    'E1': ['original', 'description_control', 'label_deletion', 'label_restoration'],
    'E2': ['original', 'description_control', 'label_permutation', 'permutation_restoration'],
}
def sha(b):
    return hashlib.sha256(b).hexdigest()
def read(p):
    return json.loads(p.read_text())

records = []
all_dex = set()
input_count = successful_lists = decoder_failures = 0
for phase, variants in VARIANTS.items():
    for variant in variants:
        folder = FRESH / phase / 'variants' / variant
        old_folder = OLD / phase / 'variants' / variant
        model = (folder / 'model.tflite').read_bytes()
        assert model == (old_folder / 'model.tflite').read_bytes(), (phase, variant, 'model identity')
        with zipfile.ZipFile(folder / 'build/consumer.apk') as apk:
            assert apk.read('assets/model.tflite') == model
            dex = apk.read('classes.dex')
            assert dex == (folder / 'build/dex/classes.dex').read_bytes()
            all_dex.add(sha(dex))
        source = 'generated/src/main/java/org/example/contract/ContractModel.java'
        assert (folder / source).read_bytes() == (old_folder / source).read_bytes()
        generated_classes = sorted((folder / 'build/classes').rglob('ContractModel*.class'))
        assert len(generated_classes) == 3
        for p in generated_classes:
            rel = p.relative_to(folder / 'build/classes')
            assert p.read_bytes() == (old_folder / 'build/classes' / rel).read_bytes()
        with zipfile.ZipFile(folder / 'model.tflite') as z:
            labels = [x for x in z.read('labels_without_background.txt').decode('utf-8').splitlines() if x.strip()]
        device = FRESH / phase / 'executions/primary' / variant / 'device'
        old_device = OLD / phase / 'executions/primary' / variant / 'device'
        result = read(device / 'result.json')
        assert result['asset_identity_status'] == result['model_loading_status'] == 'PASS'
        assert result['loaded_asset_name'] == 'model.tflite'
        assert result['loaded_asset_sha256'] == sha(model)
        assert len(result['observations']) == 2
        observations = []
        for obs in result['observations']:
            name = obs['input']
            assert name in ('gray127', 'rgb_pattern')
            expected_input = bytes([127]) * (224 * 224 * 3) if name == 'gray127' else bytes((37*i+17)%256 for i in range(224*224*3))
            assert (device / f'{name}-input.rgb').read_bytes() == expected_input
            assert expected_input == (old_device / f'{name}-input.rgb').read_bytes()
            raw = (device / f'{name}-output-0.f32').read_bytes()
            assert len(raw) == 4000
            assert raw == (old_device / f'{name}-output-0.f32').read_bytes()
            assert sha(raw) == obs['raw_output_sha256']
            assert obs['input_preparation_status'] == obs['inference_status'] == obs['raw_output_observation_status'] == 'PASS'
            values = struct.unpack('<1000f', raw)
            bits = struct.unpack('<1000i', raw)
            top = sorted(range(1000), key=lambda i: (-values[i], i))[:5]
            assert top == [x['index'] for x in obs['top5_raw']]
            decoded_file = device / f'{name}-decoded.json'
            if variant == 'label_deletion':
                assert len(labels) == 999 and not decoded_file.exists()
                assert obs['generated_getter_status'] == 'FAIL'
                assert obs['earliest_failing_stage'] == 'generated_getter'
                assert obs['exception_type'] == 'java.lang.IllegalArgumentException'
                assert obs['exception_message'] == 'Label number 999 mismatch the shape on axis 1'
                assert 'ContractModel$Outputs.getProbabilityAsCategoryList' in obs['stack_trace']
                decoder_failures += 1
            else:
                assert obs['generated_getter_status'] == 'PASS'
                decoded = read(decoded_file)
                assert len(decoded) == len(labels) == 1000
                assert decoded == read(old_device / decoded_file.name)
                assert [x['label'] for x in decoded] == labels
                assert [x['score_float_bits'] for x in decoded] == list(bits)
                assert all(x['list_position'] == i and x['category_index_field'] == -1 for i,x in enumerate(decoded))
                assert all(struct.pack('<f', x['score']) == raw[i*4:i*4+4] for i,x in enumerate(decoded))
                successful_lists += 1
            input_count += 1
            observations.append({'input': name, 'raw_sha256': sha(raw), 'getter_status': obs['generated_getter_status'], 'top5': top})
        records.append({'phase': phase, 'variant': variant, 'model_sha256': sha(model), 'asset_identity': 'PASS', 'observations': observations})

assert len(records) == 8 and len({x['model_sha256'] for x in records}) == 5
assert input_count == 16 and successful_lists == 14 and decoder_failures == 2
assert len(all_dex) == 1
result = {
    'status': 'PASS',
    'scope': 'Root independently cross-checks completed fresh device records and raw files; no model invocation by this verifier.',
    'phase_variant_execution_records': len(records),
    'unique_artifact_consumer_configurations': 5,
    'input_observations': input_count,
    'successful_category_lists': successful_lists,
    'recorded_getter_exceptions': decoder_failures,
    'all_fresh_DEX_equal': True,
    'all_generated_sources_and_generated_classes_equal_historical': True,
    'all_models_equal_historical_and_APK_and_preload_AssetManager_digest': True,
    'all_inputs_and_raw_outputs_equal_historical': True,
    'human_verification': 'PENDING',
    'records': records,
}
target = ROOT / 'verification/fresh-runtime-crosscheck.json'
target.write_text(json.dumps(result, indent=2))
print(json.dumps({k:v for k,v in result.items() if k != 'records'}, indent=2))
