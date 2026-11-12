"""Read the unmodified candidate; stop on linkage mismatch, with evidence retained."""
import hashlib
import json
from pathlib import Path
import sys
import zipfile
import numpy as np
from tensorflow_lite_support.metadata import schema_py_generated as schema
from tensorflow_lite_support.metadata.python import metadata

model, output = map(Path, sys.argv[1:])
output.mkdir(parents=True, exist_ok=False)
data = model.read_bytes()
obj = schema.Model.GetRootAsModel(data, 0)
sg = obj.Subgraphs(0)


def normal(value):
    if isinstance(value, np.ndarray): return value.tolist()
    if isinstance(value, np.generic): return value.item()
    if isinstance(value, bytes): return {'bytes_hex': value.hex()}
    if isinstance(value, (list, tuple)): return [normal(v) for v in value]
    if isinstance(value, dict): return {k: normal(v) for k, v in value.items()}
    if hasattr(value, '__dict__'): return normal(vars(value))
    return value


graph = schema.ModelT.InitFromObj(obj)
descriptor = normal({k: v for k, v in vars(graph).items() if k != 'buffers'})
descriptor['buffers'] = [{'bytes': len(b.data) if b.data is not None else 0,
    'sha256': hashlib.sha256(bytes(b.data) if b.data is not None else b'').hexdigest()}
    for b in graph.buffers]
(output / 'graph.json').write_text(json.dumps(descriptor, indent=2) + '\n')

def tensor(index):
    t = sg.Tensors(index)
    return {'id': index, 'name': t.Name().decode(), 'type': t.Type(),
            'shape': [t.Shape(i) for i in range(t.ShapeLength())], 'buffer': t.Buffer()}

displayer = metadata.MetadataDisplayer.with_model_buffer(data)
metadata_text = displayer.get_metadata_json()
(output / 'metadata.json').write_text(metadata_text)
resources = []
with zipfile.ZipFile(model) as archive:
    for index, name in enumerate(archive.namelist()):
        payload = archive.read(name)
        (output / f'resource-{index}.bin').write_bytes(payload)
        resources.append({'name': name, 'bytes': len(payload),
                          'sha256': hashlib.sha256(payload).hexdigest(),
                          'lines': len(payload.decode('utf-8').splitlines())})
report = {'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data),
          'schema_version': obj.Version(), 'subgraphs': obj.SubgraphsLength(),
          'operators': sg.OperatorsLength(), 'buffers': obj.BuffersLength(),
          'inputs': [tensor(sg.Inputs(i)) for i in range(sg.InputsLength())],
          'outputs': [tensor(sg.Outputs(i)) for i in range(sg.OutputsLength())],
          'resources': resources, 'model_modified': False}
outmeta = json.loads(metadata_text)['subgraph_metadata'][0]['output_tensor_metadata']
names = [a['name'] for t in outmeta for a in t.get('associated_files', [])]
report['output_associated_files'] = names
report['linkage_pass'] = (len(report['outputs']) == 1 and
    report['outputs'][0]['shape'] == [1, 257, 257, 21] and
    len(names) == 1 and any(r['name'] == names[0] and r['lines'] == 21 for r in resources))
(output / 'inspection.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
raise SystemExit(0 if report['linkage_pass'] else 1)
