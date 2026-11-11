"""Independent, strict evidence checks for fresh E1/E2 Android executions."""
import hashlib,json,pathlib,struct,zipfile,subprocess,sys,datetime
ROOT=pathlib.Path(__file__).resolve().parents[1]
audit_started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
(ROOT/'audit-results.json').write_text(json.dumps({'status':'RUNNING','started_utc':audit_started_utc},indent=2))
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def require(ok,msg):
 if not ok:raise ValueError(msg)
subprocess.run([sys.executable,str(ROOT/'scripts/audit_model_preservation.py')],check=True)
preservation=json.loads((ROOT/'model-preservation-audit.json').read_text())
require(len(preservation['rows'])==8,'complete independently recomputed preservation set')
require(preservation['distinct_canonical_graphs']==1,'canonical graph identity')
require(preservation['distinct_model_bytes']==5,'five distinct model byte conditions')
checks=[]
code_checks=[]
global_generated_classes=None
global_all_classes=None
global_dex=None
global_source=None
global_native=None
for exp,expected_variants in [('E1',{'original','description_control','label_deletion','label_restoration'}),('E2',{'original','description_control','label_permutation','permutation_restoration'})]:
 base=ROOT/exp; static={r['variant']:r for r in json.loads((base/'static-results.json').read_text())};builds={r['variant']:r for r in json.loads((base/'build-results.json').read_text())}
 require(set(static)==expected_variants,exp+' static variants')
 require(set(builds)==expected_variants,exp+' build variants')
 for name in sorted(expected_variants):
  folder=base/'variants'/name;build=folder/'build';classes=build/'classes';apk=build/'consumer.apk';record=builds[name]
  source=folder/'generated/src/main/java/org/example/contract/ContractModel.java'
  source_hash=digest(source);actual_generated={str(p.relative_to(classes)):digest(p) for p in sorted(classes.rglob('ContractModel*.class'))};actual_all_classes={str(p.relative_to(classes)):digest(p) for p in sorted(classes.rglob('*.class'))};actual_dex={p.name:digest(p) for p in sorted((build/'dex').glob('*.dex'))}
  require(bool(actual_generated) and bool(actual_all_classes) and bool(actual_dex),'nonempty generated classes/all classes/DEX')
  require(actual_generated==record['generated_class_hashes'],'record versus actual generated class hashes')
  require(actual_dex==record['dex_hashes'],'record versus actual DEX hashes')
  require(digest(classes/'org/example/contract/ContractInstrumentation.class')==record['harness_class_sha256'],'actual harness class hash')
  require(digest(apk)==record['apk_sha256'],'actual APK hash')
  require(source_hash==static[name]['source_sha256'],'actual generated source hash')
  with zipfile.ZipFile(apk) as z:
   apk_dex={n:hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if n.startswith('classes') and n.endswith('.dex') and '/' not in n}
   require(apk_dex==actual_dex,'APK DEX bytes versus actual build DEX')
   natives={n:hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if n.startswith('lib/x86_64/') and n.endswith('.so')}
   require(bool(natives),'native libraries present in APK')
  if global_source is None:global_source=source_hash;global_generated_classes=actual_generated;global_all_classes=actual_all_classes;global_dex=actual_dex;global_native=natives
  require(source_hash==global_source and actual_generated==global_generated_classes and actual_all_classes==global_all_classes and actual_dex==global_dex and natives==global_native,'actual source/classes/DEX/native equality across all E1/E2 variants')
  code_checks.append({'experiment':exp,'variant':name,'source_sha256':source_hash,'generated_class_hashes':actual_generated,'all_class_hashes':actual_all_classes,'dex_hashes':actual_dex,'native_hashes':natives,'apk_sha256':digest(apk),'status':'PASS'})
 allrows={}
 for run in ['primary','replay']:
  rows=json.loads((base/'executions'/run/'results.json').read_text());require({r['variant'] for r in rows}==expected_variants and len(rows)==4,exp+'/'+run+' execution variants')
  for r in rows:
   name=r['variant'];folder=base/'executions'/run/name/'device';model=base/'variants'/name/'model.tflite';source=base/'variants'/name/'generated/src/main/java/org/example/contract/ContractModel.java';apk=base/'variants'/name/'build/consumer.apk'
   observed=json.loads((folder/'result.json').read_text());obs=observed['observations'];require(len(obs)==2 and {x['input'] for x in obs}=={'gray127','rgb_pattern'},'input set')
   require(observed['model_loading_status']=='PASS','load')
   require(observed['variant']==name and observed['api']==30,'observed variant and API')
   require(observed['loaded_label_count']==(999 if name=='label_deletion' else 1000),'loaded label cardinality')
   require(r.get('observed')==observed,'runner observation equals retrieved device JSON')
   require(r['build']==builds[name],'executed build snapshot matches actual audited APK/build')
   install_command=json.loads((folder.parent/'logs/install.command.json').read_text())
   require(install_command['exit_code']==0 and pathlib.Path(install_command['command'][-1]).resolve()==apk.resolve(),'successful recorded install targets the audited APK')
   require(r.get('install_status')=='PASS' and r.get('instrumentation_exit_code')==0,'installation and instrumentation transport')
   require(observed['loaded_asset_sha256']==digest(model)==static[name]['variant_sha256'],'working and AssetManager model hashes')
   require(digest(source)==static[name]['source_sha256'],'source hash')
   with zipfile.ZipFile(apk) as z:require(z.read('assets/model.tflite')==model.read_bytes(),'APK asset')
   for x in obs:
    case=x['input'];input_bytes=(folder/(case+'-input.rgb')).read_bytes();raw=(folder/(case+'-output-0.f32')).read_bytes();require(x['inference_status']=='PASS' and x['input_preparation_status']=='PASS','input/inference')
    require(len(raw)==4000 and x['raw_output_bytes']==4000 and x['raw_output_observation_status']=='PASS' and x['raw_output_sha256']==hashlib.sha256(raw).hexdigest(),'raw identity and observation stage')
    expected_input=bytes([127])*224*224*3 if case=='gray127' else bytes((37*i+17)&255 for i in range(224*224*3));require(input_bytes==expected_input,'input construction');require(x['input_sha256']==hashlib.sha256(input_bytes).hexdigest(),'recorded input hash versus actual bytes')
    baseline=ROOT/'E1'/'executions'/'primary'/'original'/'device';require(raw==(baseline/(case+'-output-0.f32')).read_bytes(),'cross-variant raw equality')
    if name=='label_deletion':
     require(not (folder/(case+'-decoded.json')).exists(),'failed getter has no stale decoded payload')
     require(x['generated_getter_status']=='FAIL' and x['earliest_failing_stage']=='generated_getter','deletion failure stage')
     require(x['exception_type']=='java.lang.IllegalArgumentException' and x['exception_message']=='Label number 999 mismatch the shape on axis 1','deletion diagnosis')
     require('ContractModel$Outputs.getProbabilityAsCategoryList' in x['stack_trace'],'actual generated getter stack')
    else:
     require(x['generated_getter_status']=='PASS','getter')
     decoded=json.loads((folder/(case+'-decoded.json')).read_text());original=json.loads((baseline/(case+'-decoded.json')).read_text());require(len(decoded)==1000,'category count')
     require([d['score_float_bits']&0xffffffff for d in decoded]==list(struct.unpack('<1000I',raw)),'returned score bits')
     if name=='label_permutation':
      require(all(d['label']==original[(i+1)%1000]['label'] for i,d in enumerate(decoded)),'permutation mapping')
      require(sum(d['label']!=o['label'] for d,o in zip(decoded,original))==999,'changed-label count')
     else:require(decoded==original,'controls decode equality')
    if run=='replay':
     prior=base/'executions'/'primary'/name/'device';require(raw==(prior/(case+'-output-0.f32')).read_bytes(),'replay raw')
     if name!='label_deletion':require((folder/(case+'-decoded.json')).read_bytes()==(prior/(case+'-decoded.json')).read_bytes(),'replay decoded')
   require(builds[name]['generated_class_hashes']==builds['original']['generated_class_hashes'],'generated classes')
   require(builds[name]['dex_hashes']==builds['original']['dex_hashes'],'DEX')
   expected_decoder='FAIL' if name=='label_deletion' else 'PASS'
   require(r.get('load_status')=='PASS' and r.get('inference_status')=='PASS' and r.get('decoder_status')==expected_decoder,'summary outcomes agree with device stages')
   checks.append({'experiment':exp,'run':run,'variant':name,'input_observations':len(obs),'getter':r['decoder_status'],'loaded_model_sha256':observed['loaded_asset_sha256'],'status':'PASS'})
(ROOT/'audit-results.json').write_text(json.dumps({'status':'PASS','started_utc':audit_started_utc,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks,'input_observations':sum(x['input_observations'] for x in checks),'code_checks':code_checks,'distinct_model_bytes':preservation['distinct_model_bytes'],'distinct_model_graphs':preservation['distinct_canonical_graphs'],'canonical_graph_sha256':sorted({r['canonical_graph_sha256'] for r in preservation['rows']}),'human_audit':False},indent=2))
print('PASS:',len(checks),'variant/run records;',sum(x['input_observations'] for x in checks),'input observations')
