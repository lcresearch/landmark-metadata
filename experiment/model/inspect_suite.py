from pathlib import Path
import hashlib
import io
import json
import zipfile
from tflite_support import metadata
from tensorflow_lite_support.metadata import schema_py_generated as s

ROOT=Path(__file__).resolve().parents[1]

def inspect(data):
    model=s.Model.GetRootAsModel(data,0)
    graph=model.Subgraphs(0)
    def tensor(index):
        t=graph.Tensors(index)
        return {'tensor_id':index,'name':t.Name().decode(errors='replace'),'shape':t.ShapeAsNumpy().tolist(),'type':int(t.Type())}
    info={'input_tensors':[tensor(int(graph.Inputs(i))) for i in range(graph.InputsLength())],
      'output_tensors':[tensor(int(graph.Outputs(i))) for i in range(graph.OutputsLength())],
      'buffers':model.BuffersLength(),'metadata_entries':[{'name':model.Metadata(i).Name().decode(),'buffer':model.Metadata(i).Buffer()} for i in range(model.MetadataLength())]}
    info['associated_files']={}
    if zipfile.is_zipfile(io.BytesIO(data)):
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            for name in z.namelist():
                content=z.read(name)
                info['associated_files'][name]={'bytes':len(content),'sha256':hashlib.sha256(content).hexdigest(),'line_count':len(content.decode(errors='replace').splitlines())}
    try:
        info['metadata']=json.loads(metadata.MetadataDisplayer.with_model_buffer(data).get_metadata_json())
    except Exception as exc:info['metadata_error']=repr(exc)
    return info

def main():
    rows=[]
    for component in json.loads((ROOT/'results/components.json').read_text()):
        info=inspect((ROOT/component['path']).read_bytes())
        row=dict(component,inspection=info);rows.append(row)
        names=[m.get('name') for sg in info.get('metadata',{}).get('subgraph_metadata',[]) for m in sg.get('output_tensor_metadata',[])]
        print(component['sha256'][:12],component['occurrences'],[t['shape'] for t in info['output_tensors']],names,info.get('metadata_error',''),info['associated_files'],flush=True)
    (ROOT/'results/inspection.json').write_text(json.dumps(rows,indent=2))

if __name__=='__main__':main()
