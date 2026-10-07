#!/usr/bin/env python3
"""Fresh read-only HA03 comparisons; schema decoding only, no generator/runtime import."""
from pathlib import Path
import sys, hashlib, json, io, zipfile, re, collections, copy, datetime
sys.dont_write_bytecode=True
ROOT=Path('/workspace/evidence-recovery-20261005T170453Z/package-v2/payload')
OUT=Path(sys.argv[1]) if len(sys.argv)>1 else Path('/workspace/agent-preaudit-20261007T0749Z/preservation')
OUT.mkdir(parents=True,exist_ok=True)
if (OUT/'findings.json').exists():raise FileExistsError('Refusing to overwrite findings.json; supply a new output directory')
REPO=Path('/workspace/landmark-agent-preaudit')
sys.path.insert(0,str(ROOT/'SUPPLEMENTARY_SOURCE'))
import schema_py_generated as s
import metadata_schema_py_generated as ms
import numpy as np
import flatbuffers
inv={}
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):
 p=Path(p);b=p.read_bytes();inv[str(p)]={'sha256':sha(b),'bytes':len(b)};return b
def normalize(x):
 if isinstance(x,np.ndarray):return {'ndarray_type':str(x.dtype),'shape':list(x.shape),'hex':x.tobytes().hex()}
 if isinstance(x,np.generic):return x.item()
 if isinstance(x,bytes):return {'hexbytes':x.hex()}
 if isinstance(x,(list,tuple)):return [normalize(a) for a in x]
 if isinstance(x,dict):return {k:normalize(v) for k,v in sorted(x.items())}
 if hasattr(x,'__dict__'):return {'class':type(x).__name__,'fields':normalize(vars(x))}
 return x
def serialize(x):return json.dumps(normalize(x),sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def bdata(b):
 d=b.DataAsNumpy();return b'' if isinstance(d,int) else d.tobytes()
def inspect(p):
 raw=read(p);m=s.Model.GetRootAsModel(raw,0)
 entries=[{'name':m.Metadata(i).Name().decode(),'buffer':m.Metadata(i).Buffer()} for i in range(m.MetadataLength())]
 ids=[e['buffer'] for e in entries if e['name']=='TFLITE_METADATA']
 if len(ids)!=1:raise ValueError(entries)
 idx=ids[0];buffers=[bdata(m.Buffers(i)) for i in range(m.BuffersLength())]
 obj=s.ModelT.InitFromObj(m)
 obj.metadata=[e for e in (obj.metadata or []) if e.name!=b'TFLITE_METADATA']
 obj.buffers[idx].data=None
 comp=serialize(obj)
 # Exact original algorithm, reimplemented without importing suite_static and its runtime imports.
 builder=flatbuffers.Builder(0);builder.Finish(obj.Pack(builder),file_identifier=b'TFL3');canonical=bytes(builder.Output())
 refs=[];outputs=[]
 for j in range(m.SubgraphsLength()):
  sg=m.Subgraphs(j)
  refs += [{'subgraph':j,'tensor':k,'buffer':sg.Tensors(k).Buffer()} for k in range(sg.TensorsLength())]
  outputs.append({'subgraph':j,'inputs':[sg.Inputs(k) for k in range(sg.InputsLength())], 'outputs':[{'position':k,'tensor_index':sg.Outputs(k),'tensor':normalize(s.TensorT.InitFromObj(sg.Tensors(sg.Outputs(k))))} for k in range(sg.OutputsLength())]})
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  info=z.infolist();names=[x.filename for x in info]
  if len(names)!=len(set(names)):raise ValueError('Duplicate member')
  associated={x.filename:z.read(x) for x in info};offset=min(x.header_offset for x in info)
  zi=[{'name':x.filename,'header_offset':x.header_offset,'compression':x.compress_type,'size':x.file_size,'date_time':x.date_time} for x in info]
 label=associated['labels_without_background.txt']
 text=label.decode('utf-8')
 # Java BufferedReader newline conventions and String.trim() U+0000..U+0020.
 lines=[x for x in re.split(r'\r\n|\n|\r',text) if x.strip(''.join(chr(i) for i in range(33)))]
 md=buffers[idx];mdobj=ms.ModelMetadataT.InitFromObj(ms.ModelMetadata.GetRootAsModelMetadata(md,0))
 return {'path':str(p),'raw':raw,'buffers':buffers,'comp':comp,'canonical':canonical,'prefix':raw[:offset],'metadata':md,'associated':associated,'labels':lines,
  'record':{'path':str(p),'model_sha256':sha(raw),'bytes':len(raw),'metadata_entries':entries,'metadata_index':idx,'buffer_count':len(buffers),'nonmetadata_count':len(buffers)-len(set(ids)), 'buffer_hashes':[{'index':i,'bytes':len(b),'sha256':sha(b)} for i,b in enumerate(buffers)],'computational_serialization_sha256':sha(comp),'canonical_repack_sha256':sha(canonical),'metadata_sha256':sha(md),'metadata_object':normalize(mdobj),'prefix_bytes':offset,'prefix_sha256':sha(raw[:offset]),'zip_entries':zi,'zip_payloads':{k:{'bytes':len(v),'sha256':sha(v)} for k,v in associated.items()},'label_count':len(lines),'ordered_outputs':outputs,'tensor_references':refs,'metadata_tensor_references':[r for r in refs if r['buffer']==idx]}}
E=ROOT/'metadata-contract-e2e-20261004T030536Z'
A=ROOT/'metadata-contract-audit-20261004T062010Z/rebuild'
P=ROOT/'metadata-contract-p2p3-20261004T073824Z/P2'
models={}
for family,root in [('original',E),('rebuild',A)]:
 for phase in ('E1','E2'):
  paths=sorted((root/phase/'variants').glob('*/model.tflite'))
  if len(paths)!=4:raise ValueError((family,phase,len(paths)))
  for p in paths:models[f'{family}/{phase}/{p.parent.name}']=inspect(p)
paths=sorted((P/'variants').glob('*/model.tflite'))
if len(paths)!=5:raise ValueError(('P2',len(paths)))
for p in paths:models[f'P2/{p.parent.name}']=inspect(p)
base=models['original/E1/original'];checks=[]
def ck(name,value,**kw):checks.append({'name':name,'passed':bool(value),**kw})
for key,m in models.items():
 row=m['record'];variant=key.split('/')[-1];description=variant=='description_control'
 dif=[i for i,(a,b) in enumerate(zip(base['buffers'],m['buffers'])) if a!=b]
 ck(key+': all computational fields equal',m['comp']==base['comp'])
 ck(key+': canonical repack equal',m['canonical']==base['canonical'])
 ck(key+': all 165 nonmetadata buffers byte equal',len(m['buffers'])==166 and row['metadata_index']==165 and all(m['buffers'][i]==base['buffers'][i] for i in range(165)))
 ck(key+': metadata not referenced by tensors',not row['metadata_tensor_references'])
 ck(key+': ordered output tensors equal',row['ordered_outputs']==base['record']['ordered_outputs'])
 ck(key+': expected metadata equality',(m['metadata']==base['metadata'])!=description)
 ck(key+': expected preZIP equality',(m['prefix']==base['prefix'])!=description)
 expected=base['labels'][:-1] if variant=='label_deletion' else base['labels'][1:]+base['labels'][:1] if variant=='label_permutation' else base['labels']
 ck(key+': exact label operation',m['labels']==expected)
 if variant=='label_permutation':ck(key+': label multiset equal',collections.Counter(m['labels'])==collections.Counter(base['labels']))
 ck(key+': associated names equal',m['associated'].keys()==base['associated'].keys())
 row['changed_buffer_indices']=dif
 row['label_differences_to_original']=None if len(m['labels'])!=len(base['labels']) else [i for i,(a,b) in enumerate(zip(base['labels'],m['labels'])) if a!=b]
 row['whole_model_equal_original']=m['raw']==base['raw']
 row['whole_metadata_equal_original']=m['metadata']==base['metadata']
 row['whole_prefix_equal_original']=m['prefix']==base['prefix']
 if variant not in ('label_deletion','label_permutation'):ck(key+': associated payload bytes equal original',m['associated']==base['associated'])
 if 'restoration' in variant:ck(key+': publisher ZIP container not restored',m['raw']!=base['raw'])
 if description:
  delta=[{'offset':i,'original':x,'variant':y} for i,(x,y) in enumerate(zip(base['metadata'],m['metadata'])) if x!=y]
  rawdelta=[{'offset':i,'original':x,'variant':y} for i,(x,y) in enumerate(zip(base['raw'],m['raw'])) if x!=y]
  row['metadata_byte_changes']=delta;row['whole_file_byte_changes']=rawdelta
  ck(key+': exactly one metadata byte changes',len(delta)==1 and len(m['metadata'])==len(base['metadata']))
  ck(key+': exactly one whole model byte changes',len(rawdelta)==1 and len(m['raw'])==len(base['raw']))
# Compare byte identities for each historical/rebuild/P2 condition, no substitute provenance.
for key,m in models.items():
 variant=key.split('/')[-1]
 sourcekey=('original/E2/label_permutation' if variant=='label_permutation' else 'original/E1/label_restoration' if 'restoration' in variant else 'original/E1/'+variant)
 ck(key+': model equals original condition bytes',m['raw']==models[sourcekey]['raw'])
code=[];code_data={}
for family,root in [('original',E),('rebuild',A)]:
 for phase in ('E1','E2'):
  for vp in sorted((root/phase/'variants').iterdir()):
   key=f'{family}/{phase}/{vp.name}'
   src=vp/'generated/src/main/java/org/example/contract/ContractModel.java';build=vp/'build'
   if (vp/'model.tflite').exists():code_data[key]=(src,build)
for variant in sorted(p.name for p in (P/'variants').iterdir()):
 code_data[f'P2/wrapper/{variant}']=(P/'variants'/variant/'generated/src/main/java/org/example/contract/ContractModel.java',P/'build/wrapper'/variant)
 code_data[f'P2/task/{variant}']=(None,P/'build/task'/variant)
bytecode={}
for key,(source,build) in code_data.items():
 classes={str(p.relative_to(build/'classes')):read(p) for p in sorted((build/'classes').rglob('*.class'))}
 if not classes:raise ValueError('No classes '+key)
 dex=read(build/'dex/classes.dex');src=read(source) if source else None
 bytecode[key]={'source':src,'classes':classes,'generated_classes':{k:v for k,v in classes.items() if '/ContractModel' in k},'dex':dex}
 code.append({'key':key,'source_path':str(source) if source else None,'source_sha256':sha(src) if src else None,'build_path':str(build),'class_hashes':{k:sha(v) for k,v in classes.items()},'dex_sha256':sha(dex)})
for key,unit in bytecode.items():
 family=key.split('/')[0];ref='original/E1/original' if family=='original' else 'rebuild/E1/original' if family=='rebuild' else '/'.join(key.split('/')[:2])+'/original'
 for field in ('source','classes','dex'):
  if field=='source' and unit[field] is None:continue
  ck(key+': within family '+field+' exact equality',unit[field]==bytecode[ref][field])
 if family=='rebuild':
  hist='original/'+key.split('/',1)[1]
  ck(key+': generated Java equals original',unit['source']==bytecode[hist]['source'])
  ck(key+': generated classes equal original',unit['generated_classes']==bytecode[hist]['generated_classes'])
  ck(key+': full DEX differs from original as expected',unit['dex']!=bytecode[hist]['dex'])
# Fresh cross-family observations, without requiring unsupported identity.
cross=[]
for ref in ('rebuild/E1/original','P2/wrapper/original','P2/task/original'):
 cross.append({'left':'original/E1/original','right':ref,**{f+'_equal':bytecode['original/E1/original'][f]==bytecode[ref][f] for f in ('source','classes','generated_classes','dex')}})
# Hash parser, reference source and target provenance. No historical PASS consumed as assertions.
for p in [Path(s.__file__),Path(ms.__file__),ROOT/'SUPPLEMENTARY_SOURCE/suite_static.py',REPO/'work/workshop-convergence-20261007/manuscript/paper.tex',REPO/'work/workshop-convergence-20261007/CLAIM_EVIDENCE.md',REPO/'docs/human-audit/CHECKLIST.md',REPO/'work/agent-preaudit-20261007/PROTOCOL.md',E/'E1/static-results.json',E/'E2/static-results.json',ROOT/'metadata-contract-audit-20261004T062010Z/preservation/audit_preservation.py',ROOT/'metadata-contract-audit-20261004T062010Z/preservation/results.json',A/'results.json',P/'static-results.json',P/'build-results.json']:
 if p.exists():read(p)
read(Path(__file__))
result={'audit':'HA03 independent agent pre-audit, not human','time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'SUPPORTED_WITHIN_INSPECTED_SCOPE' if all(x['passed'] for x in checks) else 'DISCREPANCY_FOUND','runtime':{'python':sys.executable,'version':sys.version,'flatbuffers':flatbuffers.__version__,'numpy':np.__version__,'bytecode_write_disabled':sys.dont_write_bytecode},'denominators':{'models_parsed':len(models),'unique_model_bytes':len({x['record']['model_sha256'] for x in models.values()}),'nonmetadata_buffers_each':165,'code_builds':len(code),'original_builds':8,'rebuild_builds':8,'P2_wrapper_builds':5,'P2_task_builds':5},'checks':checks,'models':{k:v['record'] for k,v in models.items()},'code':code,'cross_family':cross,'input_inventory':inv,'limits':['Shared generated schema parser and same infrastructure; not forensic or human independence.','No generator, Android build, emulator or inference run. No newly authenticated chronology.','Only final selected build outputs; initial attempts excluded. APK attribution owned by HA01/02.','Numerical and execution observations owned by HA04/05/06, not checked here.','Two computational serialization methods have method-specific hashes; JSON normalized object with hex ndarrays vs original FlatBuffer repack algorithm.']}
(OUT/'findings.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'denominators':result['denominators'],'failed':[x for x in checks if not x['passed']],'checks':len(checks),'cross_family':cross},indent=2))

sys.exit(0 if all(x["passed"] for x in checks) else 1)
