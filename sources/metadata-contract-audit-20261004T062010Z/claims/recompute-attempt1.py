"""Read-only audit of preserved records; no generation, compilation, inference or emulator run."""
import collections, hashlib, io, json, pathlib, re, struct, sys, zipfile
sys.dont_write_bytecode=True
import flatbuffers
from tensorflow_lite_support.metadata import schema_py_generated as schema
B=pathlib.Path('/workspace/metadata-contract-e2e-20261004T030536Z')
O=pathlib.Path(__file__).parent
files={}
def read(p):
 p=pathlib.Path(p);raw=p.read_bytes();files[str(p)]={'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)};return raw
def j(p):return json.loads(read(p))
def digest(b):return hashlib.sha256(b).hexdigest()
def canonical(raw):
 m=schema.ModelT.InitFromObj(schema.Model.GetRootAsModel(raw,0))
 for e in m.metadata or []:
  if e.name==b'TFLITE_METADATA':m.buffers[e.buffer].data=None
 m.metadata=[e for e in m.metadata or [] if e.name!=b'TFLITE_METADATA']
 builder=flatbuffers.Builder(0);builder.Finish(m.Pack(builder),file_identifier=b'TFL3');return bytes(builder.Output())
def model_buffers(raw):
 m=schema.Model.GetRootAsModel(raw,0)
 return [bytes(m.Buffers(i).Data(j) for j in range(m.Buffers(i).DataLength())) for i in range(m.BuffersLength())]
# Every Task unit, directly from per-execution report and category payloads.
e3=[];e3comp=[]
for round_ in ['primary','replay']:
 decoded={}
 for v in ['original','description_control','label_deletion','label_permutation']:
  d=B/'E3/executions'/round_/v/'outputs';r=j(d/'result.json')
  e3.append(dict(round=round_,variant=v,**r))
  if v=='label_deletion':
   assert r['initialization_status']=='FAIL' and r['inference_status']==r['decoder_status']=='NOT_REACHED'
   assert r['exception_message']=='Got 1000 class(es) for output index 0, expected 999 according to the label map.'
  else:
   assert r['initialization_status']==r['classify_status']=='PASS'
   for inp in ['gray127','rgb_pattern']:
    h=j(d/(inp+'-decoded.json'));assert len(h)==1
    cats=h[0]['categories'];assert len(cats)==1000
    by={x['index']:x for x in cats};assert set(by)==set(range(1000))
    assert all(struct.unpack('<I',struct.pack('<f',x['score']))[0]==x['score_float_bits'] for x in cats)
    decoded[v,inp]=by
 for inp in ['gray127','rgb_pattern']:
  a,c,p=(decoded[v,inp] for v in ['original','description_control','label_permutation'])
  result={'round':round_,'input':inp,'control_equal':a==c,'permutation_score_bits_equal':all(a[i]['score_float_bits']==p[i]['score_float_bits'] for i in range(1000)),'labels_changed':sum(a[i]['label']!=p[i]['label'] for i in range(1000))}
  assert result['control_equal'] and result['permutation_score_bits_equal'] and result['labels_changed']==999;e3comp.append(result)
# E4 from independent downloads/component records and command logs, not summary.
e4=j(B/'E4/results.json');cands=j(B/'E4/protocol/candidates.json');dl=[]
for c in cands:
 r=j(B/'E4/downloads'/c['id']/'record.json');assert r['id']==c['id'] and r['url']==c['url'];dl.append(r)
 if r['status']=='DOWNLOADED':assert digest(read(B/r['path']))==r['sha256']
counts=collections.Counter(r['status'] for r in dl);assert counts=={'DOWNLOADED':16,'UNAVAILABLE':4};assert all(r['http_status']==404 for r in dl if r['status']=='UNAVAILABLE')
occ=e4['component_occurrences'];checked=[r for r in occ if r['status']=='CHECKED'];assert len(occ)==18 and len(checked)==15
assert collections.Counter(r['status'] for r in occ)=={'CHECKED':15,'EXCLUDED_PRIOR_GRAPH':2,'EXCLUDED_PRIOR_COMPONENT':1}
decount=collections.Counter();compilecount=collections.Counter();warningrows=[];e4raw=[]
for r in checked:
 raw=read(B/r['artifact_paths']['model']);assert digest(raw)==r['component_sha256'];assert digest(canonical(raw))==r['canonical_graph_sha256']
 folder=B/'E4/components'/r['component_sha256'];cmd=j(folder/'logs/javac.command.json');code=cmd['exit_code'];compilecount['PASS' if code==0 else 'FAIL']+=1
 check=j(folder/'logs/checker.stdout');assert check==r['checker']
 assert check['structural_check']=='PASS' and check['index_check'].startswith('ABSTAIN')
 ds=r['decoder_check'];status='INAPPLICABLE' if isinstance(ds,str) and ds.startswith('INAPPLICABLE') else 'INCOMPATIBLE' if any(x['status']=='FAIL' for x in ds) else 'COMPATIBLE'
 decount[status]+=1
 diag=check['generation']['diagnostics'];read(folder/'logs/javac.stderr')
 for p in r['artifact_paths']['generated_sources']:read(B/p)
 if status=='INCOMPATIBLE':warningrows.append({'component_sha256':r['component_sha256'],'javac_exit':code,'generator_diagnostic':diag})
 e4raw.append({'component_sha256':r['component_sha256'],'canonical_graph_sha256':r['canonical_graph_sha256'],'compile_exit':code,'D':status})
assert len(set(r['canonical_graph_sha256'] for r in checked))==15
assert compilecount=={'PASS':8,'FAIL':7} and decount=={'COMPATIBLE':4,'INCOMPATIBLE':9,'INAPPLICABLE':2}
assert sum(r['javac_exit']!=0 for r in warningrows)==5
assert all('not supported' in r['generator_diagnostic'] for r in warningrows if r['javac_exit']==0)
frozen=j(B/'E4/protocol/FROZEN_FILES.json');assert all(digest(read(B/'E4/protocol'/p))==h for p,h in frozen.items())
# E5 from each per-fixture report, inspect persisted artifact hash and compare combined report.
e5=j(B/'E5/results.json');fs=e5['fixtures'];assert len(fs)==len(set(x['model_sha256'] for x in fs))==65
s=collections.Counter();d=collections.Counter();i=collections.Counter();dynamic=[]
for f in fs:
 r=j(B/'E5/checks'/f['model_sha256']/'result.json');assert r==f['report'];assert digest(read(f['path']))==f['model_sha256']
 s[r['STRUCTURAL']['status']]+=1;d[r['DECODER_COMPATIBILITY']['status']]+=1;i[r['REFERENCE_BACKED_SEMANTIC']['status']]+=1
 if r['DECODER_COMPATIBILITY']['status']=='ABSTAIN':dynamic.append({'sha256':f['model_sha256'],'aliases':f['aliases'],'findings':r['DECODER_COMPATIBILITY']['findings'],'outputs':r['STRUCTURAL']['facts']['graph_outputs']})
assert s=={'ACCEPTED_BY_METADATA_POPULATOR_0_4_4':52,'REJECTED_BY_METADATA_POPULATOR_0_4_4':11,'ABSTAIN_NO_METADATA':2}
assert d=={'INCOMPATIBLE':27,'NOT_REACHED':11,'INAPPLICABLE_NO_SELECTED_GETTER':14,'ABSTAIN_NO_METADATA':2,'ABSTAIN':3,'COMPATIBLE_PRECONDITIONS':8} and i=={'ABSTAIN':65}
# Hand source artifact bridge re-derived directly from pinned bundle and focal artifact.
pinned=read(B/'E7/source-pinned-hand_landmarker.task');focal=read(B/'E7/variants/original/hand_landmarks_detector.tflite');mutant=read(B/'E7/variants/metadata_exchange/hand_landmarks_detector.tflite')
with zipfile.ZipFile(io.BytesIO(pinned)) as z:source=z.read('hand_landmarks_detector.tflite')
external=read(B/'E7/sources/external_files.bzl').decode();pinnedsha=digest(pinned);assert pinnedsha in external and 'generation=1677051718270846' in external
assert digest(source)=='11c272b891e1a99ab034208e23937a8008388cf11ed2a9d776ed3d01d0ba00e3';assert digest(focal)=='6acda74af3fbf40e68265c20c7394b2bad81a16a481dcd79ad7a081887c3d6b9'
bs,bf=model_buffers(source),model_buffers(focal);assert len(bs)==len(bf)==173
changed=[x for x in range(173) if bs[x]!=bf[x]];assert changed==[172]
cs,cf,cm=map(canonical,[source,focal,mutant]);assert cs==cf==cm
byte_offsets=[x for x in range(len(focal)) if focal[x]!=mutant[x]];assert len(focal)==len(mutant) and len(byte_offsets)==4
outs=[]
for raw in [source,focal,mutant]:
 m=schema.Model.GetRootAsModel(raw,0);g=m.Subgraphs(0);outs.append([(g.Outputs(i),g.Tensors(g.Outputs(i)).ShapeAsNumpy().tolist()) for i in range(g.OutputsLength())])
assert outs[0]==outs[1]==outs[2]
tag=j(B/'E7/sources/tag.json');assert tag['object']['sha']=='4cf89a70942ca3252e46ace7e4552f53be9bef2e'
for row in j(B/'E7/sources/immutable-commit-source-verification.json'):assert digest(read(B/'E7/sources'/row['url'].rsplit('/',1)[1]))==row['sha256']
img=read(B/'E7/source-pinned-thumb_up.jpg');assert digest(img) in external and img==read(B/'E7/thumb_up.jpg')
handruns=[];hand_decoded=[];handbits=[]
for round_ in ['primary','replay']:
 for v in ['original','container_control','metadata_exchange','restoration']:
  p=B/'E7/executions'/round_/v/'outputs';r=j(p/'result.json');dec=j(p/'decoded.json');bits=read(p/'decoded-float-bits.bin');computed=[]
  def visit(x):
   if isinstance(x,float):computed.append(struct.pack('<f',x))
   elif isinstance(x,list):
    for y in x:visit(y)
   elif isinstance(x,dict):
    for k in sorted(x):visit(x[k])
  visit(dec);assert b''.join(computed)==bits and digest(bits)==r['decoded_float_bits_sha256']
  assert r['detect_status']=='PASS' and r['detected_hands']==1 and r['landmarks_per_hand']==r['world_landmarks_per_hand']==[21]
  assert r['image_sha256']==digest(img)
  bundle=read(B/'E7/variants'/v/'hand_landmarker.task');assert digest(bundle)==r['bundle_sha256']
  with zipfile.ZipFile(io.BytesIO(bundle)) as z:
   assert z.read('hand_landmarks_detector.tflite')==read(B/'E7/variants'/v/'hand_landmarks_detector.tflite')
  handruns.append({'round':round_,'variant':v,'image_sha256':r['image_sha256'],'decoded_bits_sha256':digest(bits),'model_bundle_sha256':digest(bundle)})
  hand_decoded.append(dec);handbits.append(bits)
assert all(x==hand_decoded[0] for x in hand_decoded) and len(set(handbits))==1
# Source-extraction limitation examples; pure regex audit, not consumer execution or natural model finding.
pf=read(B/'E5/preflight.py').decode();getter_pattern=re.search(r"getters=re.findall\(r'(.+)',text\)",pf).group(1)
normal='public List<Category> getX() { return new TensorLabel(xLabels, postprocessX(x)).getCategoryList();'
qualified='public java.util.List<Category> getX() { return new TensorLabel(xLabels, postprocessX(x)).getCategoryList();'
assert re.findall(getter_pattern,normal) and not re.findall(getter_pattern,qualified)
ops_pattern=re.search(r"ops=re.findall\(r'(.+)',body",pf).group(1)
ops=[re.findall(ops_pattern,t) for t in ['return new TensorProcessor.Builder().add(factory()).build();','return new TensorProcessor.Builder().add(new custom.ShapeChangingOp()).build();']]
assert ops==[[],[]]
result={'audit_kind':'Fresh read-only recomputation from preserved bytes and unit records; no new generation/compilation/inference','E3':{'unit_records':e3,'score_comparisons':e3comp},'E4':{'download_counts':counts,'occurrence_counts':dict(collections.Counter(r['status'] for r in occ)),'compile_counts':compilecount,'decoder_counts':decount,'units':e4raw,'incompatibility_qualification':warningrows,'frozen_file_hashes_match':True},'E5':{'fixture_count':len(fs),'structural_counts':s,'decoder_counts':d,'semantic_counts':i,'dynamic_abstentions':dynamic},'Hand':{'source_bundle_sha256':pinnedsha,'source_component_sha256':digest(source),'focal_component_sha256':digest(focal),'buffer_count':len(bs),'changed_source_focal_buffers':changed,'canonical_graph_sha256':digest(cf),'exchange_byte_offsets':byte_offsets,'graph_output_order_shape':outs[0],'task_runs':handruns,'all_decoded_JSON_and_float32_bits_equal':True},'E5_extraction_limitations':{'same_call_qualified_return_type_unmatched':True,'factory_add_ops_extracted':ops[0],'fullyqualified_constructor_ops_extracted':ops[1],'scope':'Illustrative parser snippets only; not produced by pinned generator, compiled, executed, or presented as an observed fixture misclassification.'},'inputs':files,'assertions':'PASS'}
(O/'recomputed.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k not in ['inputs','E3','Hand','E4']},indent=2));print('Read input files:',len(files))
