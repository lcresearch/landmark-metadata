"""Fresh E7 preservation audit; no dependency on unavailable historical logs/classes."""
import hashlib
import io
import json
from pathlib import Path
import struct
import zipfile

import flatbuffers
import numpy as np
from tensorflow_lite_support.metadata import schema_py_generated as schema
from tensorflow_lite_support.metadata import metadata_schema_py_generated as ms

ROOT = Path(__file__).resolve().parents[1]
FOCAL = '6acda74af3fbf40e68265c20c7394b2bad81a16a481dcd79ad7a081887c3d6b9'
SWAPPED = '5c4a32919676d6645c082b4b2912ae4881862af967b5aa5b40e0ef6d616a3025'
PINNED = '11c272b891e1a99ab034208e23937a8008388cf11ed2a9d776ed3d01d0ba00e3'
CANONICAL = 'fb3baefeb2c67e5c11013ede2408204bc431e99cffc34e81f19df16a7b711793'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def parse(data):
    return schema.Model.GetRootAsModel(data, 0)


def metadata(data):
    model = parse(data)
    index = next(model.Metadata(i).Buffer() for i in range(model.MetadataLength()) if model.Metadata(i).Name() == b'TFLITE_METADATA')
    return index, model.Buffers(index).DataAsNumpy().tobytes()


def canonical(data):
    model = schema.ModelT.InitFromObj(parse(data))
    index, _ = metadata(data)
    model.buffers[index].data = None
    model.metadata = [x for x in model.metadata if x.name != b'TFLITE_METADATA']
    builder = flatbuffers.Builder(0)
    builder.Finish(model.Pack(builder), file_identifier=b'TFL3')
    return bytes(builder.Output())


def outputs(data):
    model = parse(data)
    graph = model.Subgraphs(0)
    _, content = metadata(data)
    subgraph = ms.ModelMetadata.GetRootAsModelMetadata(content, 0).SubgraphMetadata(0)
    return [{'position': i, 'tensor_id': int(graph.Outputs(i)), 'tensor_name': graph.Tensors(graph.Outputs(i)).Name().decode(), 'shape': graph.Tensors(graph.Outputs(i)).ShapeAsNumpy().tolist(), 'metadata_name': subgraph.OutputTensorMetadata(i).Name().decode()} for i in range(graph.OutputsLength())]


def compare_buffers(left, right):
    a, b = parse(left), parse(right)
    require(a.BuffersLength() == b.BuffersLength(), 'Different buffer counts')
    return [i for i in range(a.BuffersLength()) if not np.array_equal(a.Buffers(i).DataAsNumpy(), b.Buffers(i).DataAsNumpy())]


def unpack(data):
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)), 'Duplicate bundle members')
        return {name: archive.read(name) for name in names}


def pack(entries):
    target = io.BytesIO()
    with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_STORED) as archive:
        for name, content in entries.items():
            archive.writestr(zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0)), content)
    return target.getvalue()


def main():
    original_bundle = (ROOT / 'assets/official-v1.task').read_bytes()
    original_entries = unpack(original_bundle)
    original = original_entries['hand_landmarks_detector.tflite']
    reference_entries = unpack((ROOT / 'assets/source-pinned.task').read_bytes())
    reference = reference_entries['hand_landmarks_detector.tflite']
    require(sha(original) == FOCAL and sha(reference) == PINNED, 'Component hash differs from predeclared exact artifact')
    metadata_index, content = metadata(original)
    require(metadata_index == 172 and parse(original).BuffersLength() == 173, 'Unexpected buffer layout')
    require(compare_buffers(original, reference) == [metadata_index], 'Source-component bridge differs outside metadata')
    require(canonical(original) == canonical(reference), 'Canonical graph/weight bridge failed')
    require(sha(canonical(original)) == CANONICAL, 'Canonical serialization differs from historical hash')
    subgraph = ms.ModelMetadata.GetRootAsModelMetadata(content, 0).SubgraphMetadata(0)
    start = original.find(content)
    require(start >= 0 and original.count(content) == 1, 'Metadata not uniquely located')
    vector = subgraph._tab.Vector(subgraph._tab.Offset(10))
    swapped = bytearray(original)
    for destination, source in [(0, 2), (2, 0)]:
        position = vector + destination * 4
        struct.pack_into('<I', swapped, start + position, subgraph.OutputTensorMetadata(source)._tab.Pos - position)
    swapped = bytes(swapped)
    require(sha(swapped) == SWAPPED, 'Mutated hash differs from historical predeclared mutation')
    exchange_entries = dict(original_entries, hand_landmarks_detector=swapped)
    del exchange_entries['hand_landmarks_detector']
    exchange_entries['hand_landmarks_detector.tflite'] = swapped
    control = pack(original_entries)
    variants = {'original': original_bundle, 'container_control': control, 'metadata_exchange': pack(exchange_entries), 'restoration': pack(dict(exchange_entries, **{'hand_landmarks_detector.tflite': original}))}
    require(variants['restoration'] == control, 'Restoration differs from container control')
    records = []
    for name, bundle in variants.items():
        entries = unpack(bundle)
        component = entries['hand_landmarks_detector.tflite']
        require(canonical(component) == canonical(original), f'{name} graph differs')
        require(all(i == metadata_index for i in compare_buffers(component, original)), f'{name} non-metadata buffers differ')
        require(all(entries[n] == original_entries[n] for n in original_entries if n != 'hand_landmarks_detector.tflite'), f'{name} other member differs')
        destination = ROOT / 'variants' / name
        destination.mkdir(parents=True, exist_ok=False)
        (destination / 'hand_landmarker.task').write_bytes(bundle)
        (destination / 'hand_landmarks_detector.tflite').write_bytes(component)
        changed = [i for i, (a, b) in enumerate(zip(original, component)) if a != b]
        require(len(component) == len(original) and all(start <= i < start + len(content) for i in changed), 'Intervention changes bytes outside metadata')
        records.append({'variant': name, 'bundle_sha256': sha(bundle), 'component_sha256': sha(component), 'canonical_sha256': sha(canonical(component)), 'members': {n: sha(b) for n, b in entries.items()}, 'changed_offsets': changed, 'changed_buffers': compare_buffers(original, component), 'outputs': outputs(component), 'path': str(destination / 'hand_landmarker.task')})
    bridge = {'focal_sha256': sha(original), 'reference_sha256': sha(reference), 'buffer_count': 173, 'only_differing_buffer': 172, 'non_metadata_buffers_equal': True, 'canonical_equal': True, 'canonical_sha256': CANONICAL, 'focal_outputs': outputs(original), 'reference_outputs': outputs(reference), 'source_role_reference': ['landmarks', 'presence', 'handedness', 'world_landmarks'], 'source_role_reference_human_verified': False}
    (ROOT / 'results/source-component-equivalence.json').write_text(json.dumps(bridge, indent=2))
    (ROOT / 'results/variants.json').write_text(json.dumps(records, indent=2))
    print(json.dumps({'bridge': bridge, 'variant_count': len(records)}, indent=2))


if __name__ == '__main__':
    main()
