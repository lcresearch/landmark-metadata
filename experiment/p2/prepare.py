import sys,json,shutil,pathlib,zipfile,io
import numpy as np
from common import ROOT,sha,save,run,PYTHON
sys.dont_write_bytecode=True
sys.path.insert(0,'/workspace/metadata-contract-paper/scripts')
from suite_static import canonical,md_bytes,associated,parse
from tflite_support import metadata
inputs=json.loads((ROOT.parent/'INPUTS.json').read_text())['input_models'];base=pathlib.Path(inputs[0]['path']).read_bytes();model0=parse(base);mid,md0=md_bytes(base)
with zipfile.ZipFile(io.BytesIO(base)) as z:prefix=min(x.header_offset for x in z.infolist())
rows=[]
for item in inputs:
    data=pathlib.Path(item['path']).read_bytes();assert sha(data)==item['sha256'];v=item['variant'];folder=ROOT/'variants'/v;folder.mkdir(parents=True,exist_ok=False);(folder/'model.tflite').write_bytes(data)
    model=parse(data);md=md_bytes(data)[1];assoc=associated(data)
    for name,b in assoc.items():p=folder/'associated'/name;p.parent.mkdir(exist_ok=True,parents=True);p.write_bytes(b)
    row={'variant':v,'component_sha256':sha(base),'variant_sha256':sha(data),'canonical_graph_sha256':sha(canonical(data)),'metadata_sha256':sha(md),'associated_sha256':{n:sha(b) for n,b in assoc.items()},'label_counts':{n:len(b.decode().splitlines()) for n,b in assoc.items()},'preservation':{'canonical_equal':canonical(data)==canonical(base),'nonmetadata_buffers_equal':model.BuffersLength()==model0.BuffersLength() and all(np.array_equal(model.Buffers(i).DataAsNumpy(),model0.Buffers(i).DataAsNumpy()) for i in range(model0.BuffersLength()) if i!=mid),'embedded_metadata_equal':md==md0,'prefix_equal':data[:prefix]==base[:prefix]}}
    assert row['preservation']['canonical_equal'] and row['preservation']['nonmetadata_buffers_equal']
    try:
        dis=metadata.MetadataDisplayer.with_model_buffer(data);(folder/'metadata.json').write_text(dis.get_metadata_json());row['metadata_read_status']='PASS'
        pop=metadata.MetadataPopulator.with_model_buffer(data);pop.load_metadata_buffer(md);pop.populate();row['metadata_population_status']='PASS'
    except Exception as exc:row['metadata_population_status']='FAIL';row['metadata_exception']=repr(exc)
    p=run([PYTHON,ROOT/'scripts/codegen_one.py',folder/'model.tflite',folder/'generated',folder/'codegen-status.json'],folder/'logs/codegen')
    row['generation_status']='PASS' if p.returncode==0 else 'FAIL';source=folder/'generated/src/main/java/org/example/contract/ContractModel.java';row['source_sha256']=sha(source.read_bytes()) if source.exists() else None
    rows.append(row);save(ROOT/'static-results.json',rows)
for r in rows:r['generated_source_equal_original']=r['source_sha256']==rows[0]['source_sha256']
save(ROOT/'static-results.json',rows)
print(json.dumps(rows,indent=2))
