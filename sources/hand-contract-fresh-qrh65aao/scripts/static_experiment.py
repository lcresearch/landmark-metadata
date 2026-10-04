"""Rebuild minimal same-length metadata interventions and official generated Java."""
from pathlib import Path
import copy
import hashlib
import json
import struct
import zipfile
import flatbuffers
import numpy as np
from tflite_support import metadata
from tensorflow_lite_support.metadata import schema_py_generated as schema
from tensorflow_lite_support.metadata import metadata_schema_py_generated as ms
from tensorflow_lite_support.codegen.python import _pywrap_codegen

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = '6acda74af3fbf40e68265c20c7394b2bad81a16a481dcd79ad7a081887c3d6b9'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def parse(data):
    return schema.Model.GetRootAsModel(data, 0)

def metadata_bytes(data):
    m = parse(data)
    idx = next(m.Metadata(i).Buffer() for i in range(m.MetadataLength()) if m.Metadata(i).Name() == b'TFLITE_METADATA')
    return idx, m.Buffers(idx).DataAsNumpy().tobytes()

def canonical(data):
    model = schema.ModelT.InitFromObj(parse(data))
    idx, _ = metadata_bytes(data)
    model.buffers[idx].data = None
    model.metadata = [x for x in model.metadata if x.name != b'TFLITE_METADATA']
    builder = flatbuffers.Builder(0)
    builder.Finish(model.Pack(builder), file_identifier=b'TFL3')
    return bytes(builder.Output())

def inspect_model(data):
    m = parse(data)
    g = m.Subgraphs(0)
    idx, md = metadata_bytes(data)
    s = ms.ModelMetadata.GetRootAsModelMetadata(md, 0).SubgraphMetadata(0)
    return {'buffers': m.BuffersLength(), 'metadata_buffer': idx, 'outputs': [
        {'position': i, 'tensor_id': int(g.Outputs(i)), 'tensor_name': g.Tensors(g.Outputs(i)).Name().decode(),
         'shape': g.Tensors(g.Outputs(i)).ShapeAsNumpy().tolist(),
         'metadata_name': s.OutputTensorMetadata(i).Name().decode(),
         'description': s.OutputTensorMetadata(i).Description().decode()}
        for i in range(g.OutputsLength())]}

def main():
    raw = (ROOT / 'artifacts/original.tflite').read_bytes()
    assert sha(raw) == EXPECTED
    idx, md = metadata_bytes(raw)
    start = raw.find(md)
    assert start >= 0 and raw.count(md) == 1
    s = ms.ModelMetadata.GetRootAsModelMetadata(md, 0).SubgraphMetadata(0)
    vector = s._tab.Vector(s._tab.Offset(10))
    swapped = bytearray(raw)
    for destination, source in [(0, 2), (2, 0)]:
        target = s.OutputTensorMetadata(source)._tab.Pos
        pos = vector + destination * 4
        struct.pack_into('<I', swapped, start + pos, target - pos)
    description = bytearray(raw)
    needle = b'The score of left or right handedness.'
    where = raw.find(needle, start, start + len(md))
    assert where >= start
    description[where] = ord('t')
    # A sham repeats the swap on the already swapped vector; exact original recovery.
    reverted = bytearray(swapped)
    smd = metadata_bytes(swapped)[1]
    ss = ms.ModelMetadata.GetRootAsModelMetadata(smd, 0).SubgraphMetadata(0)
    for destination, source in [(0, 2), (2, 0)]:
        pos = vector + destination * 4
        struct.pack_into('<I', reverted, start + pos, ss.OutputTensorMetadata(source)._tab.Pos - pos)
    assert reverted == raw
    variants = {'original': raw, 'swapped': bytes(swapped), 'description_control': bytes(description), 'swap_back_control': bytes(reverted)}
    original_canonical = canonical(raw)
    (ROOT / 'artifacts/graph-without-tflite-metadata.tflite').write_bytes(original_canonical)
    report = {'original_expected_sha256': EXPECTED, 'intervention': 'Swap only two relative table offsets in output_tensor_metadata, in place. No whole-model repacking.', 'variants': {}}
    for name, data in variants.items():
        path = ROOT / 'artifacts' / f'{name}.tflite'
        path.write_bytes(data)
        m = parse(data)
        changed_buffers = [i for i in range(m.BuffersLength()) if not np.array_equal(m.Buffers(i).DataAsNumpy(), parse(raw).Buffers(i).DataAsNumpy())]
        delta = [i for i, (a,b) in enumerate(zip(raw,data)) if a != b]
        assert len(data) == len(raw)
        assert all(start <= i < start + len(md) for i in delta)
        assert canonical(data) == original_canonical
        display = metadata.MetadataDisplayer.with_model_buffer(data)
        (ROOT / 'results' / f'{name}-metadata.json').write_text(display.get_metadata_json())
        # Exercise the public structural validation/population path on a disposable copy.
        validator = {'entry_point': 'MetadataPopulator.with_model_buffer; load_metadata_buffer; populate'}
        try:
            pop = metadata.MetadataPopulator.with_model_buffer(data)
            pop.load_metadata_buffer(metadata_bytes(data)[1])
            pop.populate()
            validator['accepted'] = True
        except Exception as exc:
            validator.update(accepted=False, error=repr(exc))
        dest = ROOT / 'generated' / name
        generator = _pywrap_codegen.AndroidJavaGenerator(str(dest))
        result = generator.generate(data, 'org.example.hand', 'HandModel', 'hand.tflite')
        assert result.files, generator.get_error_message()
        generated_files = []
        for file in result.files:
            p = Path(file.path)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(file.content)
            generated_files.append(str(p.relative_to(ROOT)))
        with zipfile.ZipFile(path) as z:
            attachments = {n: {'sha256': sha(z.read(n)), 'content': z.read(n).decode(errors='replace')} for n in z.namelist()}
        report['variants'][name] = dict(sha256=sha(data), bytes=len(data), changed_byte_offsets=delta, changed_buffers=changed_buffers,
            non_metadata_buffers_equal=all(i == idx for i in changed_buffers), canonical_sha256=sha(canonical(data)),
            model=inspect_model(data), structural_validator=validator, generated_files=generated_files,
            generation_diagnostics=generator.get_error_message(), associated_files=attachments)
        print(name, 'sha256', sha(data), 'changed_bytes', len(delta), 'changed_buffers', changed_buffers, 'validator',validator, flush=True)
    (ROOT / 'results/static-results.json').write_text(json.dumps(report, indent=2))

if __name__ == '__main__':
    main()
