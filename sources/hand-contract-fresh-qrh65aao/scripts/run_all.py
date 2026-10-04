"""Execute from pinned existing inputs; each stage's stdout and stderr is preserved."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import platform
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]

def main():
    for name in ['artifacts','logs','results']: (ROOT/name).mkdir(exist_ok=True)
    steps=[]
    for name in ['static_experiment.py','compile_experiment.py','inference_experiment.py','decoder_experiment.py']:
        started=datetime.datetime.now(datetime.timezone.utc).isoformat()
        p=subprocess.run([sys.executable,str(ROOT/'scripts'/name)],cwd=ROOT,capture_output=True,text=True)
        log='logs/pipeline-'+name+'.log'
        (ROOT/log).write_text(p.stdout+p.stderr)
        print(name,p.returncode,flush=True)
        if p.returncode: print(p.stdout+p.stderr,flush=True)
        steps.append({'script':name,'started_utc':started,'exit_code':p.returncode,'log':log})
        (ROOT/'results/run-manifest.json').write_text(json.dumps({'python':sys.version,'platform':platform.platform(),'steps':steps},indent=2))
        if p.returncode: sys.exit(p.returncode)

if __name__=='__main__':
    main()
