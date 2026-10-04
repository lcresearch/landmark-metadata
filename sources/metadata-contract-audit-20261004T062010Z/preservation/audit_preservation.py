#!/usr/bin/env python3
"""Read-only independent reconstruction of E1/E2 preservation and observed values.

Does not import the study checker, preparation, summarization, or mutation code.
Does not load a TensorFlow Lite interpreter, regenerate code, or run inference.
"""
import base64
import collections
import datetime
import hashlib
import io
import json
import math
import os
import pathlib
import platform
import struct
import sys
import zipfile

from tensorflow_lite_support.metadata import schema_py_generated as schema
from tensorflow_lite_support.metadata import metadata_schema_py_generated as ms
import numpy as np

ROOT = pathlib.Path('/workspace/metadata-contract-e2e-20261004T030536Z')
OUT = pathlib.Path('/workspace/metadata-contract-audit-20261004T062010Z/preservation')
inventory = {}
checks = []

def digest(data):
    return hashlib.sha256(data).hexdigest()

def read(path):
    path = pathlib.Path(path)
    data = path.read_bytes()
    inventory[str(path)] = {'sha256': digest(data), 'bytes': len(data)}
    return data

def check(name, ok, **detail):
    row = {'name': name, 'status': 'PASS' if ok else 'FAIL', **detail}
    checks.append(row)
    return row

def normalized(value):
    if isinstance(value, bytes):
        return {'bytes_base64': base64.b64encode(value).decode('ascii')}
    if isinstance(value, np.ndarray):
        return {'dtype': str(value.dtype), 'shape': list(value.shape),
                'bytes_base64': base64.b64encode(value.tobytes()).decode('ascii')}
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, (list, tuple)):
        return [normalized(x) for x in value]
    if isinstance(value, dict):
        return {str(k): normalized(v) for k, v in sorted(value.items())}
    if hasattr(value, '__dict__'):
        return {'schema_type': type(value).__name__, 'fields': normalized(vars(value))}
    return value

def object_bytes(value):
    return json.dumps(normalized(value), sort_keys=True, separators=(',', ':'), allow_nan=False).encode()

def buf_bytes(buffer):
    value = buffer.DataAsNumpy()
    return b'' if isinstance(value, int) else value.tobytes()

def inspect_model(path):
    raw = read(path)
    model = schema.Model.GetRootAsModel(raw, 0)
    metadata_entries = [(model.Metadata(i).Name().decode(), model.Metadata(i).Buffer())
                        for i in range(model.MetadataLength())]
    md_indices = [index for name, index in metadata_entries if name == 'TFLITE_METADATA']
    assert len(md_indices) == 1, metadata_entries
    md_index = md_indices[0]
    buffers = [buf_bytes(model.Buffers(i)) for i in range(model.BuffersLength())]
    metadata = buffers[md_index]
    semantic_model = schema.ModelT.InitFromObj(model)
    semantic_model.metadata = [entry for entry in semantic_model.metadata
                               if entry.name != b'TFLITE_METADATA']
    # Retain the buffer position rather than reuse/remap the study's canonicalizer.
    # Replacing only the metadata payload preserves all graph/weight/schema fields.
    semantic_model.buffers[md_index].data = None
    computational_bytes = object_bytes(semantic_model)
    tensor_references = []
    output_details = []
    for sg_index in range(model.SubgraphsLength()):
        sg = model.Subgraphs(sg_index)
        for t_index in range(sg.TensorsLength()):
            tensor = sg.Tensors(t_index)
            tensor_references.append(tensor.Buffer())
        output_details.append({'subgraph': sg_index,
          'inputs': [int(sg.Inputs(i)) for i in range(sg.InputsLength())],
          'outputs': [{'tensor_index': int(sg.Outputs(i)),
             'shape': [int(x) for x in sg.Tensors(sg.Outputs(i)).ShapeAsNumpy()],
             'name': sg.Tensors(sg.Outputs(i)).Name().decode(),
             'type': int(sg.Tensors(sg.Outputs(i)).Type())}
              for i in range(sg.OutputsLength())]})
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        info = archive.infolist()
        names = [entry.filename for entry in info]
        assert len(names) == len(set(names)), 'duplicate ZIP names'
        files = {entry.filename: archive.read(entry) for entry in info}
        prefix_end = min(entry.header_offset for entry in info)
        zip_info = [{'filename': e.filename, 'crc32': e.CRC, 'file_size': e.file_size,
                     'header_offset': e.header_offset, 'compression': e.compress_type}
                    for e in info]
    md_object = ms.ModelMetadataT.InitFromObj(ms.ModelMetadata.GetRootAsModelMetadata(metadata, 0))
    label_payload = files['labels_without_background.txt']
    lines = label_payload.decode('utf-8').splitlines()
    labels = [line for line in lines if line.strip()]
    return {'path': str(path), 'raw': raw, 'model_sha256': digest(raw), 'buffers': buffers,
      'metadata_index': md_index, 'metadata': metadata, 'metadata_sha256': digest(metadata),
      'metadata_object': normalized(md_object), 'metadata_entries': metadata_entries,
      'computational_serialization_sha256': digest(computational_bytes),
      'computational_serialization': computational_bytes,
      'prefix': raw[:prefix_end], 'prefix_size': prefix_end, 'prefix_sha256': digest(raw[:prefix_end]),
      'associated': files, 'zip_entries': zip_info, 'labels': labels, 'lines': lines,
      'metadata_buffer_referenced_by_tensor': md_index in tensor_references,
      'outputs': output_details}

models = {}
model_rows = []
for phase in ('E1', 'E2'):
    for folder in sorted((ROOT / phase / 'variants').iterdir()):
        if (folder / 'model.tflite').is_file():
            models[(phase, folder.name)] = inspect_model(folder / 'model.tflite')
baseline = models[('E1', 'original')]
for (phase, variant), model in models.items():
    ident = f'{phase}/{variant}'
    check(f'{ident}: metadata is not tensor data', not model['metadata_buffer_referenced_by_tensor'])
    check(f'{ident}: all parsed computation/weights fields equal',
          model['computational_serialization'] == baseline['computational_serialization'])
    changed_buffers = [i for i in range(len(baseline['buffers']))
                       if i >= len(model['buffers']) or baseline['buffers'][i] != model['buffers'][i]]
    check(f'{ident}: nonmetadata buffers equal',
          len(model['buffers']) == len(baseline['buffers']) and
          all(i == baseline['metadata_index'] for i in changed_buffers),
          total_buffers=len(model['buffers']), changed_buffer_indices=changed_buffers)
    md_equal = model['metadata'] == baseline['metadata']
    prefix_equal = model['prefix'] == baseline['prefix']
    check(f'{ident}: expected metadata/prefix preservation',
          (not md_equal and not prefix_equal) if variant == 'description_control' else md_equal and prefix_equal)
    if variant == 'description_control':
        diffs = [i for i, (a, b) in enumerate(zip(model['metadata'], baseline['metadata'])) if a != b]
        check(f'{ident}: exactly one description byte changes',
              len(model['metadata']) == len(baseline['metadata']) and len(diffs) == 1,
              metadata_byte_diffs=[{'offset': i, 'before': baseline['metadata'][i],
                                   'after': model['metadata'][i]} for i in diffs])
        full_file_diffs = [i for i, (a, b) in enumerate(zip(model['raw'], baseline['raw'])) if a != b]
        check(f'{ident}: entire model differs by exactly that one byte',
              len(model['raw']) == len(baseline['raw']) and len(full_file_diffs) == 1,
              full_file_byte_diffs=[{'offset': i, 'before': baseline['raw'][i],
                                    'after': model['raw'][i]} for i in full_file_diffs])
    check(f'{ident}: associated filenames unchanged',
          set(model['associated']) == set(baseline['associated']))
    if variant == 'label_deletion':
        expected_labels = baseline['labels'][:-1]
    elif variant == 'label_permutation':
        expected_labels = baseline['labels'][1:] + baseline['labels'][:1]
    else:
        expected_labels = baseline['labels']
    check(f'{ident}: expected label operation', model['labels'] == expected_labels,
          label_count=len(model['labels']), changed_positions=(None if len(model['labels']) != 1000 else
             [i for i in range(1000) if model['labels'][i] != baseline['labels'][i]]))
    if variant in ('original', 'description_control', 'label_restoration', 'permutation_restoration'):
        check(f'{ident}: original associated payloads restored/preserved', model['associated'] == baseline['associated'])
    folder = pathlib.Path(model['path']).parent
    source = folder / 'generated/src/main/java/org/example/contract/ContractModel.java'
    source_hash = digest(read(source))
    class_hashes = {str(p.relative_to(folder / 'build/classes')): digest(read(p))
                    for p in sorted((folder / 'build/classes').rglob('*.class'))}
    dex = read(folder / 'build/dex/classes.dex')
    apk_path = folder / 'build/consumer.apk'
    apk_bytes = read(apk_path)
    with zipfile.ZipFile(io.BytesIO(apk_bytes)) as apk:
        apk_model = apk.read('assets/model.tflite')
        apk_dex = apk.read('classes.dex')
        apk_entries = {e.filename: {'sha256': digest(apk.read(e)), 'bytes': e.file_size}
                       for e in apk.infolist() if not e.is_dir()}
    staging_model = read(folder / 'build/assets/model.tflite')
    check(f'{ident}: APK/staging asset equals model file', apk_model == model['raw'] == staging_model,
          apk_path=str(apk_path), apk_model_sha256=digest(apk_model))
    check(f'{ident}: APK DEX equals build DEX', apk_dex == dex,
          dex_sha256=digest(dex), apk_dex_sha256=digest(apk_dex))
    row = {k: model[k] for k in ('path', 'model_sha256', 'metadata_index', 'metadata_sha256',
       'metadata_entries', 'computational_serialization_sha256', 'prefix_size', 'prefix_sha256',
       'zip_entries', 'outputs')}
    row.update(phase=phase, variant=variant, total_buffers=len(model['buffers']),
       buffer_hashes=[{'index': i, 'sha256': digest(b), 'bytes': len(b)} for i, b in enumerate(model['buffers'])],
       metadata_object=model['metadata_object'],
       associated_hashes={name: digest(data) for name, data in model['associated'].items()},
       label_count=len(model['labels']), source_sha256=source_hash, class_hashes=class_hashes,
       dex_sha256=digest(dex), apk_sha256=digest(apk_bytes), apk_entries=apk_entries,
       whole_file_equal_original=model['raw'] == baseline['raw'])
    model_rows.append(row)

base_row = next(r for r in model_rows if r['phase'] == 'E1' and r['variant'] == 'original')
for row in model_rows:
    ident = f"{row['phase']}/{row['variant']}"
    check(f'{ident}: generated Java equals original', row['source_sha256'] == base_row['source_sha256'])
    check(f'{ident}: all generated/harness classes equal original', row['class_hashes'] == base_row['class_hashes'])
    check(f'{ident}: DEX equals original', row['dex_sha256'] == base_row['dex_sha256'])

baseline_device = ROOT / 'E1/executions/primary/original/device'
observations = []
execution_rows = []
incomplete = []
for phase in ('E1', 'E2'):
    for run in sorted((ROOT / phase / 'executions').iterdir()):
        if not run.is_dir():
            continue
        for unit in sorted(run.iterdir()):
            if not unit.is_dir():
                continue
            variant = unit.name
            device = unit / 'device'
            result_path = device / 'result.json'
            ident = f'{phase}/{run.name}/{variant}'
            if not result_path.exists():
                incomplete.append({'phase_run_variant_record': ident, 'status': 'UNVERIFIABLE',
                    'consumer_outcome': 'UNCLASSIFIED_INCOMPLETE_ATTEMPT',
                    'reason': 'No recovered device/result.json; not treated as pass/fail of consumer.',
                    'present_files': sorted(str(p) for p in unit.rglob('*') if p.is_file())})
                continue
            result = json.loads(read(result_path))
            check(f'{ident}: result identifies intended variant', result['variant'] == variant)
            check(f'{ident}: model loading success in raw device record', result['model_loading_status'] == 'PASS')
            check(f'{ident}: raw loaded label count matches model ZIP',
                  result['loaded_label_count'] == len(models[(phase, variant)]['labels']))
            observed = {o['input']: o for o in result['observations']}
            check(f'{ident}: exactly the two prescribed input observations',
                  set(observed) == {'gray127', 'rgb_pattern'} and len(result['observations']) == 2)
            for inp in ('gray127', 'rgb_pattern'):
                ob = observed[inp]
                input_bytes = read(device / f'{inp}-input.rgb')
                expected_input = (bytes([127]) * (224*224*3) if inp == 'gray127' else
                                  bytes((37*i+17) % 256 for i in range(224*224*3)))
                check(f'{ident}/{inp}: prescribed input bytes', input_bytes == expected_input)
                raw = read(device / f'{inp}-output-0.f32')
                base_raw = read(baseline_device / f'{inp}-output-0.f32')
                check(f'{ident}/{inp}: raw outputs equal original', raw == base_raw)
                check(f'{ident}/{inp}: expected raw tensor size', len(raw) == 4000)
                score_bits = list(struct.unpack('<1000I', raw))
                scores = list(struct.unpack('<1000f', raw))
                check(f'{ident}/{inp}: all scores finite', all(math.isfinite(x) for x in scores))
                top5 = sorted(range(1000), key=lambda i: (-scores[i], i))[:5]
                raw_top5 = [{'index': i, 'score': scores[i], 'score_float_bits': score_bits[i]} for i in top5]
                check(f'{ident}/{inp}: reported top5 reconstruct from raw bits', ob['top5_raw'] == raw_top5)
                check(f'{ident}/{inp}: recorded raw hash matches raw file', ob['raw_output_sha256'] == digest(raw))
                check(f'{ident}/{inp}: recorded input hash matches input file', ob['input_sha256'] == digest(input_bytes))
                check(f'{ident}/{inp}: preparation/inference/buffer observation success',
                      all(ob[k] == 'PASS' for k in ('input_preparation_status', 'inference_status', 'raw_output_observation_status')))
                decoded_path = device / f'{inp}-decoded.json'
                row = {'unit': ident, 'input': inp, 'input_sha256': digest(input_bytes),
                       'raw_sha256': digest(raw), 'top5': raw_top5, 'decoder_file': str(decoded_path),
                       'raw_device_observation': ob}
                if variant == 'label_deletion':
                    check(f'{ident}/{inp}: no deletion decoded file', not decoded_path.exists())
                    check(f'{ident}/{inp}: exact getter failure in device record',
                          ob['generated_getter_status'] == 'FAIL' and ob['earliest_failing_stage'] == 'generated_getter'
                          and ob['exception_type'] == 'java.lang.IllegalArgumentException'
                          and ob['exception_message'] == 'Label number 999 mismatch the shape on axis 1'
                          and 'ContractModel$Outputs.getProbabilityAsCategoryList' in ob['stack_trace'])
                    row.update(decoded_status='NOT_APPLICABLE_EXCEPTION', changed_label_positions=None)
                else:
                    decoded_bytes = read(decoded_path)
                    decoded = json.loads(decoded_bytes)
                    check(f'{ident}/{inp}: actual returned list length', len(decoded) == 1000)
                    check(f'{ident}/{inp}: positions sequential and Java index unset',
                          [x['list_position'] for x in decoded] == list(range(1000)) and
                          all(x['category_index_field'] == -1 for x in decoded))
                    check(f'{ident}/{inp}: every returned score bit equals raw',
                          [x['score_float_bits'] & 0xffffffff for x in decoded] == score_bits)
                    check(f'{ident}/{inp}: numeric JSON scores encode same float bits',
                          [struct.unpack('<I', struct.pack('<f', x['score']))[0] for x in decoded] == score_bits)
                    labels = [x['label'] for x in decoded]
                    check(f'{ident}/{inp}: all exposed labels match actual ZIP order',
                          labels == models[(phase, variant)]['labels'])
                    changes = [i for i in range(1000) if labels[i] != baseline['labels'][i]]
                    expected_changes = [i for i in range(1000) if i != 638] if variant == 'label_permutation' else []
                    check(f'{ident}/{inp}: exact changed label positions', changes == expected_changes,
                          count=len(changes))
                    if variant == 'label_permutation':
                        check(f'{ident}/{inp}: full cyclic association equality',
                              all(labels[i] == baseline['labels'][(i+1) % 1000] for i in range(1000)))
                    else:
                        check(f'{ident}/{inp}: entire decoded JSON restored/preserved',
                              decoded_bytes == read(baseline_device / f'{inp}-decoded.json'))
                    check(f'{ident}/{inp}: getter succeeds in device record',
                          ob['generated_getter_status'] == 'PASS' and ob['category_count'] == 1000)
                    row.update(decoded_status='PASS', decoded_sha256=digest(decoded_bytes),
                        changed_label_positions=changes, label_witnesses=[{
                            'position': i, 'original_label': baseline['labels'][i],
                            'exposed_label': labels[i], 'score': scores[i], 'score_float_bits': score_bits[i]}
                            for i in (638, 649, 904)])
                observations.append(row)
            execution_rows.append({'unit': ident, 'device_result': str(result_path),
                                   'device_result_sha256': inventory[str(result_path)]['sha256']})

# Re-read each inspected input to catch changes during the audit itself.
changed_during_audit = [name for name, record in inventory.items()
                        if digest(pathlib.Path(name).read_bytes()) != record['sha256']]
check('inspected evidence bytes unchanged during audit', not changed_during_audit,
      changed_paths=changed_during_audit)
check('exactly one known incomplete replay unit',
      [x['phase_run_variant_record'] for x in incomplete] == ['E2/replay/permutation_restoration'])
check('complete phase/run/variant record count (including replay)', len(execution_rows) == 16, count=len(execution_rows))
check('complete raw observation count', len(observations) == 32, count=len(observations))
check('duplicate-label explanation', baseline['labels'][638] == baseline['labels'][639] == 'maillot')
status_counts = collections.Counter(c['status'] for c in checks)
result = {'audit_kind': 'AI agent static/raw-artifact audit; no fresh inference or human verification',
 'time_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'evidence_root': str(ROOT), 'audit_root': str(OUT),
 'audit_script': {'path': str(pathlib.Path(__file__).resolve()),
                 'sha256': digest(pathlib.Path(__file__).read_bytes()),
                 'command_argv': [sys.executable] + sys.argv,
                 'environment_overrides': {'PYTHONDONTWRITEBYTECODE': os.environ.get('PYTHONDONTWRITEBYTECODE')}},
 'method': 'Independent parsing of model/ZIP/APK/class/DEX/raw/decoded artifacts; not study summary/checker execution.',
 'parser': {'schema_module': schema.__file__, 'schema_module_sha256': digest(pathlib.Path(schema.__file__).read_bytes()),
            'metadata_schema_module': ms.__file__, 'metadata_schema_module_sha256': digest(pathlib.Path(ms.__file__).read_bytes()),
            'python': sys.version, 'executable': sys.executable, 'numpy': np.__version__,
            'platform': platform.platform()},
 'status': 'FAIL' if status_counts['FAIL'] else 'PASS', 'check_counts': dict(status_counts),
 'checks': checks, 'models': model_rows, 'completed_phase_run_variant_records': execution_rows,
 'observations': observations, 'incomplete_units': incomplete,
 'input_inventory': inventory,
 'limitations': [
  'This audits retained local evidence and does not independently re-execute Android or prove historical execution provenance.',
  'No independent class-order ground truth is established; label comparisons are relative to retained original labels.',
  'No device-pulled installed APK was used to prove installed bytes independently of retained commands and artifacts.',
  'Two fixed synthetic inputs cannot establish accuracy or universal output invariance across inputs/runtimes.',
  'Structural metadata acceptance was not rerun; parser use is limited to reading model data.',
  'Computational fingerprint uses a fresh deterministic schema-object representation and differs intentionally from the study canonical-hash format.',
  'Old environment-generated schema packages remain a common dependency; their source paths/hashes are recorded.']}
bytecode_results = OUT / 'bytecode/results.json'
if bytecode_results.exists():
    bytecode_bytes = bytecode_results.read_bytes()
    bytecode = json.loads(bytecode_bytes)
    result['companion_bytecode_audit'] = {
        'path': str(bytecode_results), 'sha256': digest(bytecode_bytes),
        'status': bytecode.get('status', 'UNVERIFIABLE'),
        'review_findings': bytecode.get('review_findings', {}),
        'report': str(OUT / 'bytecode/report.md'),
        'commands': str(OUT / 'bytecode/commands.json')}
    if bytecode.get('status') == 'FAIL':
        result['status'] = 'FAIL'
else:
    result['companion_bytecode_audit'] = {'status': 'UNVERIFIABLE', 'reason': 'Companion result not present.'}
OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'results.json').write_text(json.dumps(result, indent=2))
print(json.dumps({'status': result['status'], 'checks': dict(status_counts), 'model_paths': len(model_rows),
 'completed_phase_run_variant_records': len(execution_rows), 'observations': len(observations), 'incomplete': len(incomplete),
 'failures': [c for c in checks if c['status'] == 'FAIL']}, indent=2))
sys.exit(1 if status_counts['FAIL'] else 0)
