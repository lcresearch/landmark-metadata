"""Keep public-stage observation separate from atomic-call granularity."""
import json
from common import ROOT,save
p=ROOT/'results.json';data=json.loads(p.read_text());data['normalization']={'source':'execution-results.json retained unchanged','reason':'Collector uses ATOMIC_WITH_DECODING as Task inference marker. This is granularity, not evidence of reaching inference; final units separate these.'}
for row in data['records']:
 row.update(experiment_id='P2',component_name='efficientnet_lite0',component_sha256=row['static']['component_sha256'],variant_sha256=row['static']['variant_sha256'],canonical_graph_sha256=row['static']['canonical_graph_sha256'],metadata_sha256=row['static']['metadata_sha256'],associated_file_sha256=row['static']['associated_sha256'],consumer_version='Support0.4.4 generated wrapper' if row['consumer']=='wrapper' else 'Task Vision0.4.4 Android Java',runtime_version='standalone Java/native TFLite2.13.0' if row['consumer']=='wrapper' else 'published Task0.4.4 native library; bundled TFLite version UNKNOWN',generator_version='tflite-support0.4.4' if row['consumer']=='wrapper' else 'INAPPLICABLE',compiler_version='Temurin17.0.12+7 --release8; D8 build-tools35.0.0',platform='same fresh Android API30 default x86_64 emulator',semantic_check='ABSTAIN_NO_ARTIFACT_TIED_INDEPENDENT_CLASS_ORDER_REFERENCE_WITHIN_P2',preservation_check=row['static']['preservation'])
 device=ROOT/row.get('artifact_directory','MISSING')/'device'
 row['raw_output_hashes']={p.name:__import__('hashlib').sha256(p.read_bytes()).hexdigest() for p in device.glob('*.f32')}
 row['decoded_result']={p.stem:str(p.relative_to(ROOT)) for p in device.glob('*-decoded.json')}
 row['artifact_paths']={'model':str(ROOT/'variants'/row['variant']/'model.tflite'),'build':str(ROOT/'build'/row['consumer']/row['variant']),'execution':str(device)}
 row['reference_source']=None;row['decoder_check']='Observed actual public consumer behavior; no separate preflight invocation in P2'
 row['exception_type']=row.get('failures',[{}])[0].get('exception_type') if row.get('failures') else None
 row['exception_message']=row.get('failures',[{}])[0].get('exception_message') if row.get('failures') else None
 row['structural_status']=row['static']['metadata_population_status'];row['generation_status']=row['static']['generation_status'] if row['consumer']=='wrapper' else 'INAPPLICABLE';row['compile_status']=row['build']['stages'].get('compile',{}).get('status','NOT_REACHED')
 if row['consumer']=='task':
  atomic=row['stages']['classify_inference_and_decoding'];row['stage_granularity']={'classify_inference_and_decoding':'ATOMIC_PUBLIC_CALL'};row['stages']['inference']='NOT_REACHED' if atomic=='NOT_REACHED' else 'NOT_SEPARATELY_OBSERVED';row['stages']['decoder']='NOT_REACHED' if atomic=='NOT_REACHED' else 'NOT_SEPARATELY_OBSERVED'
data['stage_matrix']=[{'consumer':x['consumer'],'variant':x['variant'],'stages':x['stages'],'earliest_failing_stage':x.get('earliest_failing_stage')} for x in data['records']]
save(p,data)
