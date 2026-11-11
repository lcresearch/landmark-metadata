"""Check observed Android service readiness; a boot property alone is insufficient."""
import argparse,datetime,json,pathlib,subprocess,time

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--adb',type=pathlib.Path,required=True);ap.add_argument('--serial',required=True);ap.add_argument('--evidence',type=pathlib.Path,required=True);ap.add_argument('--timeout',type=float,default=90);args=ap.parse_args()
    started=time.monotonic();deadline=started+args.timeout;observations=[];consecutive=0;previous_pid=None;ready=False
    result={'status':'FAIL','serial':args.serial,'observations':observations,'reason':'No successful functional readiness observation'}
    while time.monotonic()<deadline:
        record={'elapsed_seconds':round(time.monotonic()-started,2),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'probes':{}}
        for name,command in [('boot',['getprop','sys.boot_completed']),('package',['cmd','package','path','android']),('activity',['cmd','activity','get-config']),('system_server',['pidof','system_server'])]:
            budget=min(15,max(0.01,deadline-time.monotonic()))
            try:
                p=subprocess.run([str(args.adb),'-s',args.serial,'shell',*command],capture_output=True,text=True,timeout=budget)
                record['probes'][name]={'exit_code':p.returncode,'stdout':p.stdout.strip(),'stderr':p.stderr.strip()}
            except subprocess.TimeoutExpired:record['probes'][name]={'exit_code':None,'error':'TIMEOUT'}
        probes=record['probes'];pid=probes['system_server'].get('stdout','')
        passed=all(p['exit_code']==0 for p in probes.values()) and probes['boot'].get('stdout')=='1' and probes['package'].get('stdout','').startswith('package:') and probes['activity'].get('stdout','').startswith('config:') and pid.isdigit()
        consecutive=consecutive+1 if passed and pid==previous_pid else 1 if passed else 0;previous_pid=pid
        record.update(functional_probes_passed=passed,stable_observations=consecutive);observations.append(record)
        ready=consecutive>=3
        result={'status':'PASS' if ready else 'WAITING','serial':args.serial,'required_stable_observations':3,'observations':observations,'scope':'Observed boot, package and activity service responsiveness with stable system_server PID; does not guarantee future stability.'}
        args.evidence.parent.mkdir(parents=True,exist_ok=True);args.evidence.write_text(json.dumps(result,indent=2))
        if ready:break
        time.sleep(min(5,max(0,deadline-time.monotonic())))
    if not ready:result['status']='FAIL';args.evidence.write_text(json.dumps(result,indent=2))
    print(result['status'],args.serial,'functional service readiness')
    raise SystemExit(0 if ready else 1)
if __name__=='__main__':main()
