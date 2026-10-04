import pathlib,json,hashlib,collections,re,sys
sys.dont_write_bytecode=True
from tflite_support import metadata
B=pathlib.Path('/workspace/metadata-contract-e2e-20261004T030536Z');P=pathlib.Path('/workspace/metadata-contract-paper');O=pathlib.Path(__file__).parent
inputs={}
def read(p):
 raw=pathlib.Path(p).read_bytes();inputs[str(p)]=hashlib.sha256(raw).hexdigest();return raw
def j(p):return json.loads(read(p))
s=j(P/'results/static-suite.json');vs=[v for r in s for v in r['variants']];ms=[r for r in s if r['variants']]
r=j(P/'results/runtime-suite.json');ds=j(P/'results/decoder-suite.json')
prior={'metadata_components':len(ms),'canonical_groups':len(set(c['canonical_sha256'] for c in ms)),'variants':len(vs),'structural_variants':dict(collections.Counter(v['variant'] for v in vs)),'structural_accept_count':sum(v['structural_validation']['accepted'] for v in vs),'reported_CPU_invocations':sum(v.get('invocations',0) for c in r for v in c['variants']),'reported_equal_variant_count':sum(v.get('bitwise_equal_original',False) for c in r for v in c['variants']),'isolated_decoder_probes':len(ds),'scope':'Recount from preserved per-component/per-variant reports; historical CPU inference and arrays not rerun in this supplementary audit.'}
assert [prior[k] for k in ['metadata_components','canonical_groups','variants','structural_accept_count','reported_CPU_invocations','reported_equal_variant_count','isolated_decoder_probes']]==[11,10,46,35,105,35,23]
roles={}
for v in ['original','metadata_exchange']:
 raw=read(B/'E7/variants'/v/'hand_landmarks_detector.tflite');md=json.loads(metadata.MetadataDisplayer.with_model_buffer(raw).get_metadata_json());names=[x['name'] for x in md['subgraph_metadata'][0]['output_tensor_metadata']]
 ref=j(B/'E7'/f'{v}-role-reference.json');actual=[ref['metadata_name_to_role'][n] for n in names];expected=ref['expected_roles'];roles[v]={'metadata_names':names,'mapped_roles':actual,'expected_roles':expected,'agreement':actual==expected}
assert not roles['original']['agreement'] and roles['metadata_exchange']['agreement']
for name in ['hand_landmarks_detector_graph.cc','external_files.bzl','hand_landmarker_test.py','BUILD']:
 read(B/'E7/sources'/name)
# Preserved javap has typed getters and Map.put output mapping. Read commands and stdout explicitly.
binding=[]
for v in ['original','swapped']:
 cmd=j(B/'E7/binding-audit'/v/'fresh-outputs-javap.command.json');text=read(B/'E7/binding-audit'/v/'fresh-outputs-javap.stdout').decode();assert cmd['exit_code']==0
 binding.append({'variant':v,'command':cmd,'getter_present':'getHandednessAsCategoryList' in text and 'getLandmarksAsTensorBuffer' in text,'output_map_instructions':text[text.index('getBuffer()'):text.index('getBuffer()')+2500]})
 assert binding[-1]['getter_present']
# Model slots 0/2 in printed getBuffer code, linked to field names, are manually reviewed in report.
for p in [B/'E3/sources/image_classifier.cc',B/'E3/sources/_pywrap_image_classifier.cc',B/'E3/task_one.py',B/'E3/implementation.json',B/'E5/preflight.py',pathlib.Path('/workspace/hand-contract-repro/sources/TensorLabel.java'),P/'sources/FileUtil.java']:
 read(p)
out={'historical_denominator_recount':prior,'hand_metadata_role_comparison':roles,'preserved_binding_disassembly':binding,'inputs':inputs}
(O/'supplemental.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:v for k,v in out.items() if k not in ['inputs','preserved_binding_disassembly']},indent=2))
