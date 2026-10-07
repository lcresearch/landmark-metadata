#!/usr/bin/env python3
"""Compare freshly hashed primary-unit artifacts with historical recorded identities."""
from pathlib import Path
import json,hashlib,subprocess,re
O=Path('/workspace/agent-preaudit-20261007T0749Z/executable');B=Path('/workspace/evidence-recovery-20261005T170453Z/package-v2/payload');R=Path('/workspace/landmark-agent-preaudit')
x=json.loads((O/'raw-checks.json').read_text());inv=json.loads((O/'inspected-inputs.json').read_text())
def get(p):
 b=p.read_bytes();inv[str(p)]={'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)};return b
def load(p):return json.loads(get(p))
checks=[]
for u in x['units']:
 fam=u['family'];phase=u['phase'];v=u['variant'];c=u['consumer']
 if fam=='original':
  p=B/'metadata-contract-e2e-20261004T030536Z'/phase/'build-results.json';a=next(r for r in load(p) if r['variant']==v)
 elif fam=='construction_audit':
  p=B/'metadata-contract-audit-20261004T062010Z/rebuild/results.json';a=next(r for r in load(p)['records'] if r['variant']==v and r['experiment_id']==phase)
 else:
  p=B/'metadata-contract-p2p3-20261004T073824Z/P2/build-results.json';a=next(r for r in load(p) if r['variant']==v and r['consumer']==c)
 keys={'apk_sha256':'apk_sha256','apk_model_sha256':'apk_model_sha256','apk_asset_sha256':'apk_model_sha256','model_sha256':'model_sha256','dex_hashes':'dex_sha256'}
 row={'family':fam,'phase':phase,'consumer':c,'variant':v,'record':str(p),'checks':{k:a[k]==u[z] for k,z in keys.items() if k in a}}
 row['checks']['generated_classes']=all(u['classes'].get(k)==v for k,v in a.get('generated_class_hashes',a.get('generated_classes',{})).items())
 if fam=='P2':
  p=B/'metadata-contract-p2p3-20261004T073824Z/P2/static-results.json';a=next(r for r in load(p) if r['variant']==v);row['checks']['static_model']=a['variant_sha256']==u['model_sha256']
 checks.append(row)
# Preserve honest dependency scope: hash available files designated by final DEX commands, never infer missing files.
deps={}
for u in x['units']:
 for raw in u['build_commands']['dex']['command']:
  if not raw.endswith('.jar') or raw.endswith('/program.jar') or raw.endswith('/android.jar'):continue
  candidates=[B/raw.removeprefix('/workspace/'),Path(raw)]
  p=next((p for p in candidates if p.exists()),None)
  deps[raw]={'inspected_path':str(p) if p else None,'sha256':hashlib.sha256(get(p)).hexdigest() if p else None,'provenance':'selected package' if p and p.is_relative_to(B) else 'secondary original absolute path' if p else 'missing at checked paths'}
# Read historical locator reports without adopting their PASS.
for rel in ['metadata-contract-audit-20261004T062010Z/preservation/bytecode/input-manifest.json','metadata-contract-audit-20261004T062010Z/preservation/bytecode/results.json','metadata-contract-audit-20261004T062010Z/preservation/bytecode/report.md','metadata-contract-audit-20261004T062010Z/rebuild/AUDIT_REPORT.md']:
 p=B/rel
 if p.exists():get(p)
for rel in ['AGENTS.md','MEMORY.md','TODO.md','docs/DECISIONS.md','docs/human-audit/CHECKLIST.md','work/agent-preaudit-20261007/PROTOCOL.md','work/workshop-convergence-20261007/CLAIM_EVIDENCE.md','work/workshop-convergence-20261007/manuscript/paper.tex']:
 get(R/rel)
res={'target_sha256':inv[str(R/'work/workshop-convergence-20261007/manuscript/paper.tex')]['sha256'],'git_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'record_checks':checks,'dependencies':deps,'scope_note':'Dependency digests freshly computed at named locations. This does not resolve Task embedded native interpreter identity or independently attest historical execution.'}
(O/'record-comparisons.json').write_text(json.dumps(res,indent=2)+'\n');(O/'inspected-inputs.json').write_text(json.dumps(inv,indent=2)+'\n')
print('historical artifact record comparisons:',sum(all(v['checks'].values()) for v in checks),'/',len(checks));print('dependency files:',len(deps),'missing:',sum(v['inspected_path'] is None for v in deps.values()));print('target',res['target_sha256'],'head',res['git_head'])
for c in checks:
 if not all(c['checks'].values()):print('MISMATCH',c)
print('inspected files',len(inv))
# Parse the actual binary manifests inside final APKs; staged XML alone is insufficient.
aapt=Path('/workspace/metadata-contract-e2e-20261004T030536Z/sdk/build-tools/35.0.0/aapt');get(aapt);manifest_checks=[];manifest_commands=[]
for u in x['units']:
 apk=Path(u['paths']['build'])/'consumer.apk';argv=[str(aapt),'dump','xmltree',str(apk),'AndroidManifest.xml'];r=subprocess.run(argv,capture_output=True,text=True)
 out=O/'disassembly'/('manifest-'+u['apk_sha256']+'.txt');out.write_text(r.stdout)
 package=re.search(r'A: package="([^"]+)"',r.stdout).group(1);section=r.stdout.split('E: instrumentation ',1)[1]
 name=re.search(r'A: android:name[^=]*="([^"]+)"',section).group(1);target=re.search(r'A: android:targetPackage[^=]*="([^"]+)"',section).group(1)
 manifest_checks.append({'apk':str(apk),'package':package,'instrumentation':name,'target_package':target,'matches_run_command':u['instrumentation_command'][-1]==package+'/'+name and target==package,'exit_code':r.returncode})
 manifest_commands.append({'argv':argv,'exit_code':r.returncode,'stdout':str(out),'stdout_sha256':hashlib.sha256(r.stdout.encode()).hexdigest(),'stderr':r.stderr})
res['actual_apk_manifest_checks']=manifest_checks;(O/'record-comparisons.json').write_text(json.dumps(res,indent=2)+'\n');(O/'commands-manifest.json').write_text(json.dumps(manifest_commands,indent=2)+'\n');(O/'inspected-inputs.json').write_text(json.dumps(inv,indent=2)+'\n');print('actual APK manifests match',sum(v['matches_run_command'] for v in manifest_checks),'/',len(manifest_checks))
