import hashlib,json,pathlib,sys
sys.dont_write_bytecode=True
from tensorflow_lite_support.metadata import schema_py_generated as s, metadata_schema_py_generated as ms
O=pathlib.Path('/workspace/agent-preaudit-20261007T0749Z/secondary'); p=O/'observations.json';d=json.loads(p.read_text()); files=d['files'];c=d['checks'];R=pathlib.Path('/workspace/landmark-agent-preaudit');E=pathlib.Path('/workspace/metadata-contract-e2e-20261004T030536Z')
def read(p,ha):
 p=pathlib.Path(p);b=p.read_bytes();files[str(p)]={'ha':ha,'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)};return b
for p0 in ['sources/repro-audit-20261004/maintained/java_labels.py','sources/repro-audit-20261004/maintained/verify_fixture_regression.py','sources/repro-audit-20261004/probes/probe_label_parser.py']:read(R/p0,'HA09c')
path='/workspace/repro-external/E5/results.json';c['HA09c']['raw_paths'].append({'path':path,'exists':pathlib.Path(path).exists(),'expected_sha256':'bf49a475696eec4b38fb17587f6541a8393da14297e5dca1d433a051ba166e79'})
for filename in ['FileUtil.java','../label/TensorLabel.java']:
 p0=pathlib.Path('/workspace/contribution-review-20261004/official/tensorflow_lite_support/java/src/java/org/tensorflow/lite/support/common')/filename
 if p0.exists():read(p0.resolve(),'HA09b/HA09c')
idx=json.loads(read(R/'research/20261004-significance-review/public-report-sources.json','HA10'))
def walk(x):
 if isinstance(x,dict):
  if x.get('response_path','').endswith(('issue-01.json','issue-01-comments.json')):
   b=read(x['response_path'],'HA10');c['HA10'].setdefault('source_index_checks',[]).append({'path':x['response_path'],'sha256_matches_index':hashlib.sha256(b).hexdigest()==x['response_sha256'],'bytes_match_index':len(b)==x['response_bytes']})
  for y in x.values():walk(y)
 elif isinstance(x,list):
  for y in x:walk(y)
walk(idx)
md=[]
for v in ['original','metadata_exchange']:
 b=read(E/f'E7/variants/{v}/hand_landmarks_detector.tflite','HA08');m=s.Model.GetRootAsModel(b,0);i=next(m.Metadata(i).Buffer() for i in range(m.MetadataLength()) if m.Metadata(i).Name()==b'TFLITE_METADATA');meta=ms.ModelMetadata.GetRootAsModelMetadata(m.Buffers(i).DataAsNumpy().tobytes(),0).SubgraphMetadata(0)
 md.append({'variant':v,'metadata_buffer':i,'output_names':[meta.OutputTensorMetadata(j).Name().decode() for j in range(meta.OutputTensorMetadataLength())],'ordered_shapes':[m.Subgraphs(0).Tensors(m.Subgraphs(0).Outputs(j)).ShapeAsNumpy().tolist() for j in range(m.Subgraphs(0).OutputsLength())]})
c['HA08']['metadata_direct_parse']=md
for v in ['original','swapped']:
 for p0 in (pathlib.Path('/workspace/hand-contract-repro/build')/v/'classes').rglob('*.class'):read(p0,'HA08')
c['HA08']['fresh_disassembly']='NOT_CHECKED: inspected saved javap mapping and hashed available classes; no independent fresh disassembly in this bounded review'
c['HA09b']['independent_execution']='NOT_CHECKED: saved static and initialization records only'
p.write_text(json.dumps(d,indent=2)+'\n')
print(json.dumps({'files':len(files),'source_index_checks':c['HA10']['source_index_checks'],'metadata':md},indent=2))
