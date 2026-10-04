import json,io,tarfile
from common import ROOT,run,save,sha
adb=ROOT/'sdk/platform-tools/adb';prefix=[adb,'-s','emulator-5554'];builds=json.loads((ROOT/'build-results.json').read_text());statics={x['variant']:x for x in json.loads((ROOT/'static-results.json').read_text())};results=[]
dest=ROOT/'executions/primary';dest.mkdir(parents=True,exist_ok=False)
for build in builds:
 c=build['consumer'];v=build['variant'];folder=dest/c/v;folder.mkdir(parents=True);package=build['package'];record={'experiment_id':'P2','consumer':c,'variant':v,'static':statics[v],'build':build,'stages':{'installation':'NOT_REACHED','asset_identity':'NOT_REACHED','public_constructor':'NOT_REACHED','input_preparation':'NOT_REACHED','inference':'NOT_REACHED' if c=='wrapper' else 'ATOMIC_WITH_DECODING','generated_getter':'NOT_REACHED' if c=='wrapper' else 'INAPPLICABLE','classify_inference_and_decoding':'NOT_REACHED' if c=='task' else 'INAPPLICABLE'}}
 if build['package_status']!='PASS':record['earliest_failing_stage']=build.get('earliest_failing_stage');results.append(record);save(ROOT/'execution-results.json',results);continue
 stage='installation'
 try:
  p=run([*prefix,'install','-r',ROOT/'build'/c/v/'consumer.apk'],folder/'logs/install',timeout=180)
  if p.returncode:raise RuntimeError(p.stdout.decode(errors='replace')+p.stderr.decode(errors='replace'))
  record['stages']['installation']='PASS';run([*prefix,'shell','run-as',package,'rm','-rf','files/evidence'],folder/'logs/clear_previous_evidence');run([*prefix,'logcat','-c'],folder/'logs/clear_logcat')
  stage='instrumentation';p=run([*prefix,'shell','am','instrument','-w','-e','variant',v,package+'/org.example.contract.'+build['instrument']],folder/'logs/instrumentation',timeout=300);record['instrumentation_exit_code']=p.returncode
  run([*prefix,'logcat','-d','-v','threadtime','ContractEvidence:E','tflite:I','TensorFlowLite:I','AndroidRuntime:E','*:S'],folder/'logs/logcat')
  q=run([*prefix,'exec-out','run-as',package,'tar','-C','files/evidence','-cf','-','.'],folder/'logs/evidence-tar')
  if q.returncode:raise RuntimeError('Missing retrievable evidence:'+q.stderr.decode(errors='replace'))
  device=folder/'device';device.mkdir()
  with tarfile.open(fileobj=io.BytesIO(q.stdout)) as z:
   for member in z.getmembers():
    if member.isfile():
     name=member.name.removeprefix('./');assert '..' not in name.split('/');(device/name).write_bytes(z.extractfile(member).read())
  obs=json.loads((device/'result.json').read_text());record['observed']=obs;record['stages']['asset_identity']=obs.get('asset_identity_status','NOT_REACHED');record['stages']['public_constructor']=obs.get('model_loading_status' if c=='wrapper' else 'model_initialization_status','NOT_REACHED');observations=obs.get('observations',[])
  fields=['input_preparation','inference','generated_getter'] if c=='wrapper' else ['input_preparation','classify_inference_and_decoding']
  for field in fields:
   vals=[o.get(field+'_status','NOT_REACHED') for o in observations];record['stages'][field]='FAIL' if 'FAIL' in vals else 'PASS' if vals and all(x=='PASS' for x in vals) else 'NOT_REACHED'
  failures=[o for o in [obs,*observations] if 'earliest_failing_stage' in o];record['failures']=failures
  if failures:record['earliest_failing_stage']=failures[0]['earliest_failing_stage']
  record['artifact_directory']=str(folder.relative_to(ROOT))
 except Exception as exc:record['earliest_failing_stage']=stage;record['harness_exception']=repr(exc)
 results.append(record);save(ROOT/'execution-results.json',results);print(c,v,record['stages'],record.get('earliest_failing_stage',''),flush=True)
