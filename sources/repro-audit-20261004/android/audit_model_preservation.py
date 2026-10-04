"""Recompute model preservation without relying on stored PASS fields."""
import hashlib,io,json,pathlib,zipfile,datetime
import flatbuffers
from tensorflow_lite_support.metadata import schema_py_generated as schema
from tensorflow_lite_support.metadata import metadata_schema_py_generated as metadata_schema
ROOT=pathlib.Path(__file__).resolve().parents[1]
audit_started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
(ROOT/'model-preservation-audit.json').write_text(json.dumps({'status':'RUNNING','started_utc':audit_started_utc},indent=2))
def digest(b):return hashlib.sha256(b).hexdigest()
def read(path):
 b=path.read_bytes();m=schema.Model.GetRootAsModel(b,0)
 ids=[m.Metadata(i).Buffer() for i in range(m.MetadataLength()) if m.Metadata(i).Name()==b'TFLITE_METADATA']
 if len(ids)!=1:raise ValueError('Unexpected metadata buffers')
 buffers={i:bytes(m.Buffers(i).DataAsNumpy()) if m.Buffers(i).DataLength() else b'' for i in range(m.BuffersLength())}
 with zipfile.ZipFile(io.BytesIO(b)) as z:
  prefix=b[:min(i.header_offset for i in z.infolist())];associated={i.filename:z.read(i) for i in z.infolist()}
 return b,m,ids[0],buffers,prefix,associated
b0,m0,md0,buffers0,prefix0,assoc0=read(ROOT/'E1/variants/original/model.tflite');rows=[]
for exp in ['E1','E2']:
 for path in sorted((ROOT/exp/'variants').glob('*/model.tflite')):
  name=path.parent.name;b,m,md,buffers,prefix,assoc=read(path)
  checks={'metadata_buffer_index_equal':md==md0,'buffer_count_equal':len(buffers)==len(buffers0),'nonmetadata_buffers_equal':{i:v for i,v in buffers.items() if i!=md}=={i:v for i,v in buffers0.items() if i!=md0},'associated_filenames_equal':set(assoc)==set(assoc0)}
  if name=='description_control':
   differences=[i for i,(left,right) in enumerate(zip(b,b0)) if left!=right]
   checks['single_bit_description_intervention']=len(b)==len(b0) and len(differences)==1 and b[differences[0]]^b0[differences[0]]==32
   checks['associated_payloads_equal']=assoc==assoc0
   original_description=metadata_schema.ModelMetadata.GetRootAsModelMetadata(buffers0[md0],0).SubgraphMetadata(0).OutputTensorMetadata(0).Description()
   changed_description=metadata_schema.ModelMetadata.GetRootAsModelMetadata(buffers[md],0).SubgraphMetadata(0).OutputTensorMetadata(0).Description()
   checks['output_description_field_case_flip']=original_description==b'Probabilities of the 1000 labels respectively.' and changed_description==b'probabilities of the 1000 labels respectively.'
  else:
   checks['prezip_prefix_equal']=prefix==prefix0;checks['embedded_metadata_equal']=buffers[md]==buffers0[md0]
  if not all(checks.values()):raise ValueError(str(path)+': '+str(checks))
  normalized=schema.ModelT.InitFromObj(m)
  for entry in normalized.metadata or []:
   if entry.name==b'TFLITE_METADATA':normalized.buffers[entry.buffer].data=None
  normalized.metadata=[entry for entry in normalized.metadata or [] if entry.name!=b'TFLITE_METADATA']
  builder=flatbuffers.Builder(0);builder.Finish(normalized.Pack(builder),file_identifier=b'TFL3')
  rows.append({'canonical_graph_sha256':digest(bytes(builder.Output())),'experiment':exp,'variant':name,'sha256':digest(b),'nonmetadata_buffer_count':len(buffers)-1,'checks':checks})
source_files=[p for exp in ['E1','E2'] for p in (ROOT/exp/'variants').glob('*/generated/src/main/java/org/example/contract/ContractModel.java')]
if len(rows)!=8 or len({r['sha256'] for r in rows})!=5 or len({r['canonical_graph_sha256'] for r in rows})!=1:raise ValueError('Unexpected model/graph cardinality')
if len(source_files)!=8 or len({digest(p.read_bytes()) for p in source_files})!=1:raise ValueError('Missing or unequal generated Java sources')
(ROOT/'model-preservation-audit.json').write_text(json.dumps({'status':'PASS','started_utc':audit_started_utc,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'rows':rows,'distinct_model_bytes':len({r['sha256'] for r in rows}),'distinct_canonical_graphs':len({r['canonical_graph_sha256'] for r in rows}),'all_generated_java_equal':len({digest(p.read_bytes()) for exp in ['E1','E2'] for p in (ROOT/exp/'variants').glob('*/generated/src/main/java/org/example/contract/ContractModel.java')})==1},indent=2))
print('PASS:',len(rows),'model conditions;',len(buffers0)-1,'nonmetadata buffers preserved')
