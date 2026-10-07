#!/usr/bin/env python3
"""New read-only saved-observation audit; no execution/inference or historical helper imports."""
from pathlib import Path
import collections, hashlib, json, math, re, struct, sys, zipfile
BASE=Path('/workspace/evidence-recovery-20261005T170453Z/package-v2/payload')
OUT=Path(__file__).parent
E=BASE/'metadata-contract-e2e-20261004T030536Z'
A=BASE/'metadata-contract-audit-20261004T062010Z/rebuild'
P=BASE/'metadata-contract-p2p3-20261004T073824Z/P2'
checks=[]; identities={}; units=[]; values={}
def sha(b): return hashlib.sha256(b).hexdigest()
def read(p):
 b=p.read_bytes(); identities[str(p)]={'bytes':len(b),'sha256':sha(b)}; return b
def js(p): return json.loads(read(p))
def ck(name,cond,**context):
 checks.append({'check':name,'pass':bool(cond),**context})
def bits(x): return struct.unpack('<I',struct.pack('<f',x))[0]
def top(xs): return sorted(range(len(xs)),key=lambda i:(-xs[i],i))[:5]
expected={'gray127':bytes([127])*(224*224*3),'rgb_pattern':bytes((37*i+17)&255 for i in range(224*224*3))}
variants={'E1':['original','description_control','label_deletion','label_restoration'],'E2':['original','description_control','label_permutation','permutation_restoration']}
def unit(family,phase,consumer,variant,root):
 d=root/'device'; r=js(d/'result.json'); key='/'.join([family,phase,consumer,variant]); log=root/'logs'
 cmd=js(log/'instrumentation.command.json'); stdout=read(log/'instrumentation.stdout').decode(); lc=read(log/'logcat.stdout').decode()
 rec={'key':key,'path':str(d),'api':r.get('api'),'platform':r.get('platform'),'command':cmd,'observations':[]}
 ck(key+' variant',r['variant']==variant)
 ck(key+' Android API',r['api']==30)
 ck(key+' selected command variant',cmd['command'][cmd['command'].index('variant')+1]==variant)
 expected_n=0 if consumer=='task' and variant=='label_deletion' else 2
 observations=r.get('observations',[])
 ck(key+' exact input denominator',len(observations)==expected_n and [x['input'] for x in observations]==list(expected)[:expected_n],actual=len(observations),expected=expected_n)
 if expected_n==0:
  chain=[('java.lang.IllegalStateException','Error getting native address of native library: task_vision_jni'),('java.lang.IllegalArgumentException','Error occurred when initializing ImageClassifier: Got 1000 class(es) for output index 0, expected 999 according to the label map.')]
  ck(key+' complete Task public cause chain',[(x['type'],x['message']) for x in r['cause_chain']]==chain and r['earliest_failing_stage']=='model_initialization' and r['model_initialization_status']=='FAIL')
  ck(key+' constructor stack and cause',all(s in r['stack_trace'] for s in ['ImageClassifier.createFromFileAndOptions','TaskInstrumentation.onStart','Caused by: java.lang.IllegalArgumentException','ImageClassifier.initJniWithModelFdAndOptions']))
  ck(key+' no actual inputs/raw/decoded',not list(d.glob('*-input.rgb')) and not list(d.glob('*-output-*.f32')) and not list(d.glob('*-decoded.json')))
  rec['recorded_failure']={k:r[k] for k in ['earliest_failing_stage','cause_chain','stack_trace']}
 else:
  status='model_initialization_status' if consumer=='task' else 'model_loading_status'
  ck(key+' construction success',r.get(status)=='PASS')
 for row in observations:
  n=row['input']; rid=key+'/'+n; rgb=read(d/(n+'-input.rgb'))
  ck(rid+' exact reconstructed RGB',rgb==expected[n] and row['input_sha256']==sha(rgb) and row['input_preparation_status']=='PASS',bytes=len(rgb))
  data={'input':n,'input_sha256':sha(rgb)}; raw=None; dec=None
  if consumer!='task':
   raw=read(d/(n+'-output-0.f32')); ck(rid+' complete float32 bytes',len(raw)==4000 and row['raw_output_bytes']==4000 and row['raw_output_sha256']==sha(raw))
   scores=struct.unpack('<1000f',raw); ibits=struct.unpack('<1000I',raw)
   ck(rid+' finite raw',all(math.isfinite(x) for x in scores))
   ck(rid+' all successful prior stages',row.get('inference_status')=='PASS' and row.get('raw_output_observation_status')=='PASS')
   computed=[{'index':i,'score':scores[i],'score_float_bits':ibits[i]} for i in top(scores)]
   ck(rid+' recomputed top5',row['top5_raw']==computed)
   data.update(raw_sha256=sha(raw),argmax=top(scores)[0],top5=computed)
   if variant=='label_deletion':
    ck(rid+' actual caught getter failure',row.get('earliest_failing_stage')=='generated_getter' and row.get('generated_getter_status')=='FAIL' and row.get('exception_type')=='java.lang.IllegalArgumentException' and row.get('exception_message')=='Label number 999 mismatch the shape on axis 1')
    ck(rid+' generated-getter stack',all(x in row['stack_trace'] for x in ['SupportPreconditions.checkArgument','TensorLabel.<init>','ContractModel$Outputs.getProbabilityAsCategoryList','ContractInstrumentation.onStart']))
    ck(rid+' absent decoded list',not (d/(n+'-decoded.json')).exists() and 'category_count' not in row)
    data['recorded_failure']={k:row[k] for k in ['earliest_failing_stage','exception_type','exception_message','stack_trace']}
   else:
    dec=js(d/(n+'-decoded.json')); ck(rid+' full wrapper list shape',len(dec)==1000 and [x['list_position'] for x in dec]==list(range(1000)) and all(x['category_index_field']==-1 for x in dec))
    ck(rid+' all raw/returned score bits',all(x['score_float_bits']==ibits[i] and bits(x['score'])==ibits[i] and x['score']==scores[i] for i,x in enumerate(dec)))
    ck(rid+' successful getter',row.get('generated_getter_status')=='PASS' and row.get('category_count')==1000)
  else:
   outer=js(d/(n+'-decoded.json')); ck(rid+' one head',len(outer)==1 and outer[0]['head_index']==0 and row.get('head_count')==1)
   ds=outer[0]['categories']; ck(rid+' complete Task class indices',len(ds)==1000 and sorted(x['category_index_field'] for x in ds)==list(range(1000)))
   ck(rid+' Task score serialization',all(bits(x['score'])==x['score_float_bits'] for x in ds))
   ck(rid+' Task atomic public classify',row.get('classify_inference_and_decoding_status')=='PASS')
   ck(rid+' Task display names empty',all(x['display_name']=='' for x in ds))
   ck(rid+' no Task raw file',not list(d.glob('*-output-*.f32')))
   dec=sorted(ds,key=lambda x:x['category_index_field']); data['task_returned_top5']=[x['category_index_field'] for x in ds[:5]]
  values[rid]={'raw':raw,'decoded':dec,'rgb':rgb}
  if dec is not None: data['decoded_categories']=len(dec)
  rec['observations'].append(data)
 # Logcat is attributed by command start, not blindly counting cumulative exceptions.
 lines=lc.splitlines(); errors=[]; started=cmd['started_utc'][5:19].replace('T',' ')
 for line in lines:
  m=re.match(r'(\d\d-\d\d \d\d:\d\d:\d\d)\.\d+\s+(\d+)\s+(\d+)\s+E ContractEvidence: (.*)',line)
  if m and m[1]>=started: errors.append({'timestamp':m[1],'pid':int(m[2]),'tid':int(m[3]),'text':m[4]})
 if variant=='label_deletion':
  stage='model_initialization' if consumer=='task' else 'generated_getter'; count=sum(x['text']==stage for x in errors)
  ck(key+' attributed failure count',count==(1 if consumer=='task' else 2),actual=count)
  ck(key+' one current-run error PID',len({x['pid'] for x in errors})==1)
  ck(key+' logcat complete saved stack',all(part in '\n'.join(x['text'] for x in errors) for part in (['Caused by: java.lang.IllegalArgumentException','ImageClassifier.createFromFileAndOptions'] if consumer=='task' else ['Label number 999 mismatch the shape on axis 1','ContractModel$Outputs.getProbabilityAsCategoryList'])))
  rec['attributed_logcat_errors']=errors
  rec['instrumentation_stdout']=stdout
  ck(key+' caught failure/zero command exit',cmd['exit_code']==0)
 units.append(rec)
for fam,base in [('original',E),('rebuild',A)]:
 for phase,vs in variants.items():
  roots=base/phase/'executions/primary'; actual=sorted(p.name for p in roots.iterdir() if p.is_dir())
  ck(fam+'/'+phase+' exact primary configs',actual==sorted(vs),actual=actual)
  for v in vs: unit(fam,phase,'wrapper',v,roots/v)
for c in ['wrapper','task']:
 vs=['original','description_control','label_deletion','label_permutation','restoration']; roots=P/'executions/primary'/c
 ck('P2/'+c+' exact configs',sorted(x.name for x in roots.iterdir() if x.is_dir())==sorted(vs))
 for v in vs: unit('P2','P2',c,v,roots/v)
comparisons=[]
for key,v in values.items():
 family,phase,consumer,variant,n=key.split('/')
 baseline=values['/'.join([family,phase,consumer,'original',n])]
 if v['raw'] is not None: ck(key+' bytewise raw versus within-phase original',v['raw']==baseline['raw'])
 if v['decoded'] is not None:
  dec=v['decoded']; base=baseline['decoded']; samebits=all(x['score_float_bits']==y['score_float_bits'] for x,y in zip(dec,base)); strings=[x['label'] for x in dec]; orig=[x['label'] for x in base]; changes=sum(x!=y for x,y in zip(strings,orig))
  perm=variant=='label_permutation'; ck(key+' all scores versus baseline',samebits)
  ck(key+' all display strings versus expected condition',strings==(orig[1:]+orig[:1] if perm else orig))
  ck(key+' exact label differences',changes==(999 if perm else 0),changes=changes)
  comparisons.append({'key':key,'decoded_count':len(dec),'label_changes':changes,'all_score_bits_equal':samebits,'unchanged_positions':[i for i in range(1000) if strings[i]==orig[i]] if perm else None})
 if family=='rebuild':
  old=values[key.replace('rebuild/','original/',1)]
  ck(key+' entire saved observation agrees historical primary',v==old)
 if family=='P2' and consumer=='task':
  wrapper=values[key.replace('/task/','/wrapper/')]
  ck(key+' complete shared pair RGB',v['rgb']==wrapper['rgb'])
  ck(key+' all1000 class-index aligned labels/scores',all(a['label']==b['label'] and a['score_float_bits']==b['score_float_bits'] and a['score']==b['score'] for a,b in zip(v['decoded'],wrapper['decoded'])))
  data=next(x for u in units if u['key']==key.rsplit('/',1)[0] for x in u['observations'] if x['input']==n)
  ck(key+' Task top5 indices versus wrapper raw',data['task_returned_top5']==top(struct.unpack('<1000f',wrapper['raw'])))
# Full selected E2 label members directly, independent of decoded data.
labels={}
for variant in variants['E2']:
 f=E/'E2/variants'/variant/'model.tflite'; read(f)
 with zipfile.ZipFile(f) as z:
  names=z.namelist(); ck(variant+' one label member',names==['labels_without_background.txt']); b=z.read(names[0]); labels[variant]=b.decode('utf8').splitlines(); identities[str(f)+'::'+names[0]]={'bytes':len(b),'sha256':sha(b)}
 ck(variant+' 1000 labels',len(labels[variant])==1000)
 ck(variant+' decoded matches complete label member',labels[variant]==[x['label'] for x in values['original/E2/wrapper/'+variant+'/rgb_pattern']['decoded']])
ck('label resource exact left shift',labels['label_permutation']==labels['original'][1:]+labels['original'][:1])
ck('label resource full multiset',collections.Counter(labels['label_permutation'])==collections.Counter(labels['original']))
ck('label resource inverse restoration',labels['permutation_restoration']==labels['original'])
# P2 frozen options and host records retained as record/source observations.
context={}
for name in ['EXECUTION_INPUT_FREEZE.json','PLAN_FREEZE.json','prerequisites/android-getprop.stdout','prerequisites/avd-config.ini','prerequisites/emulator-command.json','scripts/TaskInstrumentation.java','scripts/ContractInstrumentation.java','dependencies/resolved-lock.json']:
 context[name]=read(P/name).decode()
freeze=json.loads(context['EXECUTION_INPUT_FREEZE.json'])
for item in freeze['files']:
 if item['path'] in context:
  ck('P2 selected freeze identity '+item['path'],sha(context[item['path']].encode())==item['sha256'])
ck('P2 recorded execution freeze precedes all starts',all(freeze['utc']<u['command']['started_utc'] for u in units if u['key'].startswith('P2/')))
ck('P2 saved AVD API/ABI','abi.type = x86_64' in context['prerequisites/avd-config.ini'] and '/android-30/default/x86_64/' in context['prerequisites/avd-config.ini'])
ck('all P2 records same platform',len({u['platform'] for u in units if u['key'].startswith('P2/')})==1)
ck('P2 one emulator selector',len({u['command']['command'][2] for u in units if u['key'].startswith('P2/')})==1)
ck('P2 source thread/maxResults','setNumThreads(1)' in context['scripts/TaskInstrumentation.java'] and 'setMaxResults(1000)' in context['scripts/TaskInstrumentation.java'])
# Hash source used for input reconstruction and frozen audit targets.
for f in [E/'scripts/ContractInstrumentation.java',Path('/workspace/landmark-agent-preaudit/work/workshop-convergence-20261007/manuscript/paper.tex'),Path('/workspace/landmark-agent-preaudit/docs/human-audit/CHECKLIST.md'),Path('/workspace/landmark-agent-preaudit/work/workshop-convergence-20261007/CLAIM_EVIDENCE.md')]: read(f)
counts={}
for family in ['original','rebuild','P2']:
 us=[u for u in units if u['key'].startswith(family+'/')]; vs=[v for k,v in values.items() if k.startswith(family+'/')]
 counts[family]={'configurations':len(us),'input_observations':len(vs),'raw_tensors':sum(v['raw'] is not None for v in vs),'decoded_lists':sum(v['decoded'] is not None for v in vs),'categories':sum(len(v['decoded']) for v in vs if v['decoded'] is not None)}
result={'agent_verdicts':{'HA04':'SUPPORTED_WITHIN_INSPECTED_SCOPE','HA05_saved_observations':'SUPPORTED_WITHIN_INSPECTED_SCOPE','HA05_predeclaration_chronology':'PARTIAL','HA06_saved_observations':'SUPPORTED_WITHIN_INSPECTED_SCOPE'},'limitations':['All statuses are agent readback only; human remains PENDING.','No new inference, build, execution authentication, APK identity audit, or Task raw observation.','Historical stage and runtime claims are preserved records; byte comparisons and float parsing are newly computed.','E2 freeze lacks independently attested timestamp; see chronology.md.','Optional replays not numerically audited.','Initial new-helper filename expectation was incorrect; retained original stdout and separately rerun initial helper in initial-helper-reexecution.'],'kind':'NEW_AGENT_READBACK_NOT_HUMAN_OR_NEW_INFERENCE','human_status':'PENDING','base':str(BASE),'denominators':counts,'checks':checks,'failed_checks':[c for c in checks if not c['pass']],'units':units,'comparisons':comparisons,'identities':identities,'recorded_p2_context':context,'optional_replays':'NOT_CHECKED; primary original and separate construction audit only'}
(OUT/'findings.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'denominators':counts,'checks':len(checks),'failed_checks':result['failed_checks'],'hashed_objects':len(identities)},indent=2))
sys.exit(bool(result['failed_checks']))
