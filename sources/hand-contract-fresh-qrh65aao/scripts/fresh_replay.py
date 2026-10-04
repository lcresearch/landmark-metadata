"""Fresh generated sources/classes/results, same operator and pinned dependency set."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]

def load(root,name):
    return json.loads((root/'results'/name).read_text())

def normalized(root):
    s=load(root,'static-results.json')
    c=load(root,'compile-results.json')
    i=load(root,'inference-results.json')
    d=load(root,'decoder-results.json')
    return {
        'static':s,
        'compilation':{k:{kk:vv for kk,vv in v.items() if kk not in ['raw','repaired','consumer']} | {'exit_codes':[v[t]['exit_code'] for t in ['raw','repaired','consumer']]} for k,v in c['variants'].items()},
        'inference':i,
        'decoder':d,
    }

def main():
    dest=Path(tempfile.mkdtemp(prefix='hand-contract-fresh-',dir='/workspace'))
    for name in ['artifacts','logs','results']: (dest/name).mkdir()
    shutil.copytree(ROOT/'scripts',dest/'scripts',ignore=shutil.ignore_patterns('__pycache__'))
    shutil.copy2(ROOT/'artifacts/original.tflite',dest/'artifacts/original.tflite')
    # Dependency jars are reused as pinned toolchain inputs; no generated artifact is reused.
    shutil.copytree(ROOT/'deps',dest/'deps')
    env=os.environ.copy()
    env['REPRO_JDK']=str(ROOT/'toolchains/jdk-17.0.12+7')
    p=subprocess.run([sys.executable,str(dest/'scripts/run_all.py')],cwd=dest,env=env,capture_output=True,text=True)
    (ROOT/'logs/fresh-replay.log').write_text(p.stdout+p.stderr)
    assert p.returncode==0,p.stdout+p.stderr
    original=normalized(ROOT)
    replay=normalized(dest)
    assert original==replay
    digest=hashlib.sha256(json.dumps(original,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    report={'fresh_directory':str(dest),'replayed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
      'exit_code':p.returncode,'normalized_results_equal':True,'normalized_result_sha256':digest,
      'scope':'Fresh source generation, patched files, classes, and inference outputs. Same session/operator, same installed Python environment, JDK, and copied dependency jars. Not independent human reproduction.',
      'fresh_model_artifacts_copied':['original.tflite'],'fresh_invocations':replay['inference']['total_invocations']}
    (ROOT/'results/fresh-replay.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':
    main()
