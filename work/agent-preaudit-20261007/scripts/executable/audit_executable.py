#!/usr/bin/env python3
"""Read-only HA01/HA02 audit of selected saved primary executions, no inference."""
from pathlib import Path
import hashlib,json,subprocess,re,zipfile
B=Path('/workspace/evidence-recovery-20261005T170453Z/package-v2/payload')
O=Path('/workspace/agent-preaudit-20261007T0749Z/executable')
E=B/'metadata-contract-e2e-20261004T030536Z';A=B/'metadata-contract-audit-20261004T062010Z/rebuild';P=B/'metadata-contract-p2p3-20261004T073824Z/P2'
J=Path('/workspace/hand-contract-repro/toolchains/jdk-17.0.12+7/bin/javap');D=Path('/workspace/metadata-contract-e2e-20261004T030536Z/sdk/build-tools/35.0.0/dexdump')
inv={};commands=[]
def sha(b): return hashlib.sha256(b).hexdigest()
def read(p):
 b=p.read_bytes();inv[str(p)]={'sha256':sha(b),'bytes':len(b)};return b
def digest(p):read(p);return inv[str(p)]['sha256']
def js(p):return json.loads(read(p))
def run(argv,out):
 r=subprocess.run([str(x) for x in argv],capture_output=True);out.write_bytes(r.stdout);out.with_suffix('.stderr').write_bytes(r.stderr)
 commands.append({'argv':[str(x) for x in argv],'exit_code':r.returncode,'stdout':str(out),'stdout_sha256':sha(r.stdout),'stderr':r.stderr.decode(errors='replace')});return r.stdout.decode(errors='replace')
units=[];unique_classes={};unique_dex={}
for family,root in [('original',E),('construction_audit',A)]:
 for phase in ['E1','E2']:
  for v in sorted((root/phase/'variants').iterdir()):
   units.append({'family':family,'phase':phase,'consumer':'wrapper','variant':v.name,'variant_dir':v,'build':v/'build','run':root/phase/'executions/primary'/v.name})
for consumer in ['wrapper','task']:
 for v in sorted((P/'variants').iterdir()):units.append({'family':'P2','phase':'P2','consumer':consumer,'variant':v.name,'variant_dir':v,'build':P/'build'/consumer/v.name,'run':P/'executions/primary'/consumer/v.name})
rows=[]
for u in units:
 v,b,r=u['variant_dir'],u['build'],u['run'];row={k:x for k,x in u.items() if not isinstance(x,Path)};row['paths']={k:str(x) for k,x in u.items() if isinstance(x,Path)}
 mh=digest(v/'model.tflite');sh=digest(b/'assets/model.tflite');apk=read(b/'consumer.apk');row['model_sha256']=mh;row['apk_sha256']=sha(apk)
 with zipfile.ZipFile(b/'consumer.apk') as z:
  row['apk_model_sha256']=sha(z.read('assets/model.tflite'));row['apk_dex_sha256']={n:sha(z.read(n)) for n in z.namelist() if re.fullmatch(r'classes\d*\.dex',n)}
 row['working_staged_apk_model_equal']=mh==sh==row['apk_model_sha256'];row['dex_sha256']={p.name:digest(p) for p in (b/'dex').glob('*.dex')};row['staged_apk_dex_equal']=row['dex_sha256']==row['apk_dex_sha256']
 for p in (b/'dex').glob('*.dex'):unique_dex.setdefault(digest(p),p)
 row['classes']={str(p.relative_to(b/'classes')):digest(p) for p in (b/'classes').rglob('*.class')}
 for p in (b/'classes').rglob('*.class'):unique_classes.setdefault(digest(p),p)
 gen=v/'generated/src/main/java/org/example/contract/ContractModel.java';row['generated_source_sha256']=digest(gen)
 rec=js(r/'device/result.json');row['record_variant']=rec.get('variant');row['runtime_asset_sha256']=rec.get('loaded_asset_sha256');row['runtime_asset_matches']=None if not row['runtime_asset_sha256'] else mh==row['runtime_asset_sha256'];row['recorded_input_observations']=len(rec.get('observations',[]));row['recorded_platform']=rec.get('platform');row['recorded_api']=rec.get('api')
 ic=js(r/'logs/install.command.json');it=read(r/'logs/install.stdout').decode();ins=js(r/'logs/instrumentation.command.json');manifest=read(b/'AndroidManifest.xml').decode()
 installed=next((x for x in ic['command'] if x.endswith('.apk')),None);expected='/workspace/'+str((b/'consumer.apk').relative_to(B))
 row['install_target']=installed;row['install_target_matches_selected_apk']=installed==expected;row['install_exit_code']=ic['exit_code'];row['install_stdout']=it.strip();row['instrumentation_command']=ins['command'];row['instrumentation_exit_code']=ins['exit_code'];row['install_started_utc']=ic.get('started_utc');row['instrumentation_started_utc']=ins.get('started_utc')
 package=re.search(r'package="([^"]+)"',manifest).group(1);inst=re.search(r'<instrumentation[^>]*android:name="([^"]+)"',manifest).group(1);target=ins['command'][-1];row['manifest_instrumentation_matches_command']=target==package+'/'+inst;row['instrumentation_variant_matches']=ins['command'][ins['command'].index('variant')+1]==u['variant']
 row['build_commands']={}
 for stage in ['compile','dex','package_resources','sign','verify_apk']:
  q=js(b/'logs'/f'{stage}.command.json');row['build_commands'][stage]={'exit_code':q['exit_code'],'command':q['command']}
 rows.append(row)
# Fresh disassembly of every unique saved application class, with equality extending it to all primary units.
for h,p in unique_classes.items():run([J,'-c','-p','-s',p],O/'disassembly'/f'class-{h}.txt')
# One fresh disassembly per unique final DEX; selected entire class bodies retained.
selected=['Lorg/example/contract/','Lorg/tensorflow/lite/support/tensorbuffer/TensorBuffer;','Lorg/tensorflow/lite/support/label/TensorLabel;','Lorg/tensorflow/lite/support/common/ops/DequantizeOp;','Lorg/tensorflow/lite/support/common/ops/NormalizeOp;','Lorg/tensorflow/lite/support/common/SequentialProcessor;','Lorg/tensorflow/lite/support/model/Model;','Lorg/tensorflow/lite/support/common/FileUtil;','Lorg/tensorflow/lite/support/metadata/MetadataExtractor;']
for h,p in unique_dex.items():
 dest=O/'disassembly'/f'dex-{h}.txt';txt=run([D,'-d',p],dest)
 parts=re.split(r'(?=^Class #\d+\s+-)',txt,flags=re.M);out=[]
 for part in parts:
  m=re.search(r"Class descriptor\s*:\s*'([^']+)'",part)
  if m and any(m.group(1).startswith(s) for s in selected):out.append(part)
 if not out: raise RuntimeError('No selected DEX classes found')
 (O/'disassembly'/f'dex-{h}-selected.txt').write_text('\n'.join(out))
for p in [J,D,E/'scripts/ContractInstrumentation.java',A/'scripts/ContractInstrumentation.java',P/'scripts/ContractInstrumentation.java',P/'scripts/TaskInstrumentation.java',A/'results.json',P/'static-results.json',P/'build-results.json',E/'E1/build-results.json',E/'E2/build-results.json']:
 digest(p)
summary={'agent_status':'SUPPORTED_WITHIN_INSPECTED_SCOPE','human_status':'PENDING','scope':'26 primary units, no replay or initial unexecuted builds; saved bytes and command/record attribution, no inference or device-pulled APK','unit_count':len(rows),'unique_model_hashes':len(set(x['model_sha256'] for x in rows)),'unique_generated_sources':len(set(x['generated_source_sha256'] for x in rows)),'unique_application_classes':len(unique_classes),'unique_final_dex':len(unique_dex),'units':rows,'fresh_disassembly_input_by_hash':{'classes':{h:str(p) for h,p in unique_classes.items()},'dex':{h:str(p) for h,p in unique_dex.items()}},'commands':commands}
(O/'raw-checks.json').write_text(json.dumps(summary,indent=2)+'\n');(O/'inspected-inputs.json').write_text(json.dumps(inv,indent=2)+'\n');(O/'commands.json').write_text(json.dumps(commands,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k not in ['units','commands','fresh_disassembly_input_by_hash']},indent=2))
for key in ['working_staged_apk_model_equal','staged_apk_dex_equal','install_target_matches_selected_apk','manifest_instrumentation_matches_command','instrumentation_variant_matches']:
 print(key,sum(x[key] for x in rows),'/',len(rows))
print('runtime asset matches',sum(x['runtime_asset_matches'] is True for x in rows),'absent',sum(x['runtime_asset_matches'] is None for x in rows))
print('disassembly returns',[x['exit_code'] for x in commands])
