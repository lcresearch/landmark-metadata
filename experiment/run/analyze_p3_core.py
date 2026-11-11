"""Fresh six-input P3 core analysis, without claiming the old bounded search.

Graph normalization follows the byte-preserved P3 analyzer. This is a rerun of
that method, not an independent implementation or a stable-class-ID oracle.
"""
import argparse
import copy
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
from pathlib import Path
import sys
import zipfile

import flatbuffers
import numpy as np
from tensorflow_lite_support.metadata import schema_py_generated as schema

REPO = Path(__file__).resolve().parents[2]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def normal(value):
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, bytes):
        return {'bytes_hex': value.hex()}
    if isinstance(value, (list, tuple)):
        return [normal(v) for v in value]
    if isinstance(value, dict):
        return {k: normal(v) for k, v in value.items()}
    if hasattr(value, '__dict__'):
        return normal(vars(value))
    return value


def graph(data):
    obj = schema.ModelT.InitFromObj(schema.Model.GetRootAsModel(data, 0))
    metadata = [m for m in obj.metadata or [] if m.name == b'TFLITE_METADATA']
    if len(metadata) != 1:
        raise ValueError('Expected one TFLITE_METADATA entry')
    index = metadata[0].buffer
    refs = sorted({int(t.buffer) for sg in obj.subgraphs for t in sg.tensors})
    if index in refs:
        raise ValueError('Metadata buffer is tensor-referenced')
    canonical = copy.deepcopy(obj)
    canonical.buffers[index].data = None
    canonical.metadata = [m for m in canonical.metadata or [] if m.name != b'TFLITE_METADATA']
    builder = flatbuffers.Builder(0)
    builder.Finish(canonical.Pack(builder), file_identifier=b'TFL3')
    return {'index': index, 'buffers': [b'' if b.data is None else bytes(b.data) for b in obj.buffers],
            'references': refs, 'canonical_sha256': sha(bytes(builder.Output())),
            'descriptor': normal({k: v for k, v in vars(obj).items() if k not in ['buffers', 'metadata']}),
            'other_metadata': normal([m for m in obj.metadata or [] if m.name != b'TFLITE_METADATA']),
            'outputs': [{'subgraph': si, 'output_position': pos, 'tensor_id': int(tid),
                         'tensor': normal(sg.tensors[int(tid)])}
                        for si, sg in enumerate(obj.subgraphs) for pos, tid in enumerate(sg.outputs)]}


def labels(path):
    with zipfile.ZipFile(path) as archive:
        if archive.namelist() != ['labels_without_background.txt']:
            raise ValueError('Unexpected associated-file membership')
        data = archive.read('labels_without_background.txt')
    return data, data.decode('utf8').splitlines()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--inputs', required=True, type=Path)
    ap.add_argument('--references', required=True, type=Path)
    ap.add_argument('--output', required=True, type=Path)
    args = ap.parse_args()
    out = args.output.resolve()
    if out.exists() or out.is_relative_to(REPO):
        raise ValueError('Choose a fresh external output directory')
    out.mkdir(parents=True)

    def save(name, value):
        (out / name).write_text(json.dumps(value, indent=2) + '\n')

    inventory = json.loads((REPO / 'docs/reproduction/inputs.json').read_text())
    refs, models, identities = {}, {}, []
    save('analysis-start.json', {'created_utc': datetime.now(timezone.utc).isoformat(),
         'analyzer_sha256': sha(Path(__file__).read_bytes()), 'historical_results_known': True,
         'scope': 'Six pinned reference bodies and five recovered model conditions; offline core only.'})
    for row in inventory['p3_reference_prerequisites']:
        path = args.references / row['id'] / 'body'
        data = path.read_bytes()
        if sha(data) != row['body']['expected_sha256']:
            raise ValueError('Reference pin mismatch: ' + row['id'])
        refs[row['id']] = data
        identities.append({'id': row['id'], 'path': str(path), 'sha256': sha(data)})
    for row in inventory['model_conditions']:
        path = args.inputs / 'models' / (row['id'] + '.tflite')
        if sha(path.read_bytes()) != row['primary_model']['expected_sha256']:
            raise ValueError('Model pin mismatch: ' + row['id'])
        models[row['id']] = path
        identities.append({'id': row['id'], 'path': str(path), 'sha256': sha(path.read_bytes())})
    save('input-identities.json', identities)
    a = graph(models['original'].read_bytes())
    b = graph(refs['I06-tfhub-lite-model'])
    same_shape = len(a['buffers']) == len(b['buffers']) and a['index'] == b['index']
    buffers = [{'index': i, 'focal_sha256': sha(x), 'bridge_sha256': sha(y),
                'equal': x == y, 'is_metadata': i == a['index']}
               for i, (x, y) in enumerate(zip(a['buffers'], b['buffers']))]
    focal_raw, focal_labels = labels(models['original'])
    bridge_raw, _ = labels(args.references / 'I06-tfhub-lite-model/body')
    lite = refs['F07-pinned-lite-card'].decode()
    parent = refs['F10-pinned-parent-card'].decode()
    external = refs['F11-explicit-class-order'].decode().splitlines()
    checks = {
        'publisher_model_equals_focal': refs['I01-publisher-model'] == models['original'].read_bytes(),
        'buffer_structure_equal': same_shape,
        'nonmetadata_buffers_equal': same_shape and all(r['equal'] for r in buffers if not r['is_metadata']),
        'graph_descriptor_equal': a['descriptor'] == b['descriptor'],
        'other_metadata_equal': a['other_metadata'] == b['other_metadata'],
        'ordered_outputs_equal': a['outputs'] == b['outputs'],
        'canonical_graph_equal': a['canonical_sha256'] == b['canonical_sha256'],
        'associated_resource_equal': focal_raw == bridge_raw,
        'lite_card_names_parent': '<!-- parent-model: tensorflow/efficientnet/lite0/classification/1 -->' in lite,
        'parent_prescribes_external_labels': 'https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt' in parent,
        'parent_prescribes_1000_classes': 'num_classes` = 1000' in parent,
        'parent_prescribes_background_offset': 'please ignore the first background class, ie. index 0 corresponds to' in parent and '"tench"' in parent,
        'external_background_present': len(external) == 1001 and external[0] == 'background',
        'external_label_sources_equal': refs['F01-publisher-labels'] == refs['F11-explicit-class-order'],
    }
    save('bridge.json', {'checks': checks, 'buffers': buffers, 'metadata_buffer_index': a['index'],
                        'canonical_graph_sha256': a['canonical_sha256'], 'ordered_outputs': a['outputs']})
    save('graph-descriptor.json', a['descriptor'])
    if not all(checks.values()):
        save('results.json', {'status': 'FAIL_REFERENCE_CHAIN', 'checks': checks})
        raise SystemExit(1)
    reference = external[1:]
    variants = {}
    for name in ['original', 'label_permutation', 'restoration']:
        raw, strings = labels(models[name])
        g = graph(models[name].read_bytes())
        if len(strings) != 1000 or g['canonical_sha256'] != a['canonical_sha256']:
            raise ValueError('Unexpected graph/order length: ' + name)
        variants[name] = strings
    positions = [{'output_position': i, 'external_line_1based': i + 2,
                  'reference_display_label': expected,
                  **{name: {'label': strings[i], 'matches': strings[i] == expected}
                     for name, strings in variants.items()}}
                 for i, expected in enumerate(reference)]
    save('display-order-comparison.json', positions)
    counts = {name: sum(p[name]['matches'] for p in positions) for name in variants}
    replicated = counts == {'original': 1000, 'label_permutation': 1, 'restoration': 1000}
    results = {'status': 'PASS_WITHIN_CORE_SCOPE' if replicated else 'DIFFERS_FROM_HISTORICAL_COUNTS',
               'created_utc': datetime.now(timezone.utc).isoformat(), 'positions': len(positions),
               'matching_positions': counts, 'canonical_graph_sha256': a['canonical_sha256'],
               'equal_nonmetadata_buffers': sum(r['equal'] and not r['is_metadata'] for r in buffers),
               'stable_class_id_reference': 'ABSTAIN', 'prediction_accuracy': 'NOT_EVALUATED',
               'new_inference': False, 'human_verification': False,
               'historical_30_request_search': 'NOT_RERUN', 'auxiliary_synset_comparison': 'NOT_RERUN',
               'versions': {name: importlib.metadata.version(name) for name in ['flatbuffers', 'numpy', 'tflite-support']},
               'python': sys.version,
               'limitations': ['Known-outcome offline rerun of the historical graph method.',
                               'Pinned publisher catalog revision is not claimed to be the original release-time documentation.',
                               'Display-label order does not establish stable IDs or prediction correctness.',
                               'Mutated conditions are injected; only one independent graph is examined.']}
    save('results.json', results)
    print(json.dumps(results, indent=2))
    if not replicated:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
