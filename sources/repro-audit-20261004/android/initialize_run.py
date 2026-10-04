"""Copy preserved experiment sources into a fresh external evidence directory."""
import argparse,difflib,hashlib,json,pathlib,shutil
E2E='metadata-contract-e2e-20261004T030536Z';AUDIT='metadata-contract-audit-20261004T062010Z'
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=pathlib.Path,required=True);ap.add_argument('--root',type=pathlib.Path,required=True);ap.add_argument('--port',type=int,default=5554);args=ap.parse_args()
    if args.root.resolve().is_relative_to(args.repo.resolve()):raise ValueError('Evidence root must stay outside source-only repository')
    if args.root.exists():raise FileExistsError('Use a fresh evidence root: '+str(args.root))
    old=args.repo/'sources'/E2E;audit=args.repo/'sources'/AUDIT/'rebuild/scripts';scripts=args.root/'scripts';scripts.mkdir(parents=True);(args.root/'prerequisites').mkdir();(args.root/'logs').mkdir()
    for p in (old/'scripts').iterdir():
        if p.suffix in ['.py','.java']:shutil.copyfile(p,scripts/p.name)
    for name in ['EXPERIMENT_E1_PLAN.md','EXPERIMENT_E2_PLAN.md']:shutil.copyfile(old/name,args.root/name)
    provenance=[]
    for name in ['ContractInstrumentation.java','prepare_e2.py']:
        shutil.copyfile(audit/name,scripts/name);provenance.append({'source':str(audit/name),'sha256':hashlib.sha256((audit/name).read_bytes()).hexdigest()})
    changes=[('prepare_e1.py','exact bytes recovered from frozen local evidence','fresh HTTPS publisher download; SHA-256 matches historical identifier')]
    if args.port!=5554:changes.extend([('run_android.py','emulator-5554',f'emulator-{args.port}'),('start_emulator.py','emulator-5554',f'emulator-{args.port}'),('start_emulator.py',"'5554'",repr(str(args.port)))])
    for name,before,after in changes:
        p=scripts/name;text=p.read_text()
        if before not in text:raise ValueError('Expected adapter anchor missing: '+name)
        p.write_text(text.replace(before,after))
    for name in ['audit_android_results.py','audit_model_preservation.py','check_android_ready.py']:
        own=pathlib.Path(__file__).with_name(name);shutil.copyfile(own,scripts/own.name)
    startup=scripts/'start_emulator.py';text=startup.read_text().replace('import json, os, pathlib, subprocess, time','import json, os, pathlib, subprocess, time, sys')
    text=text.replace("        if q.stdout.strip()=='1':\n","        if q.stdout.strip()=='1':\n            readiness_log=pre/('functional-readiness-'+str(len(observations)))\n            functional=run([sys.executable,ROOT/'scripts/check_android_ready.py','--adb',adb,'--serial','emulator-"+str(args.port)+"','--evidence',readiness_log.with_suffix('.json'),'--timeout','60'],readiness_log,timeout=70)\n            if functional.returncode!=0: continue\n")
    startup.write_text(text)
    (args.root/'SOURCE_PROVENANCE.json').write_text(json.dumps({'base_source':str(old/'scripts'),'audit_sources':provenance,'adaptations':['Audit harness adds pre-initialization AssetManager hash; generated model source remains unmodified.','Audit prepare_e2 gates on completed E1 primary. E1 replay may run concurrently; all replays remain required.','Model provenance text describes fresh publisher retrieval instead of excluded old evidence.','Readiness now additionally checks real package/activity service responses and three stable system_server PID observations; boot property alone proved insufficient in the failed secondary AVD attempt.','Default path dependencies remain /workspace/{hand-contract-repro,metadata-contract-paper}; use supplied parent restoration first.'], 'scripts':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in scripts.iterdir() if p.is_file()}},indent=2))
    print('Initialized fresh external run:',args.root)
if __name__=='__main__':main()
