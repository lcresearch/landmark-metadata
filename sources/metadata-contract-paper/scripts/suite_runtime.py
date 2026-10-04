from pathlib import Path
import json
import subprocess
import sys
import numpy as np
from tflite_runtime.interpreter import Interpreter

ROOT=Path(__file__).resolve().parents[1]

def main():
    report=[]
    for component in json.loads((ROOT/'results/static-suite.json').read_text()):
        row={'id':component['id'],'variants':[]}
        if not component['variants']:
            row['skipped']=component['status'];report.append(row);continue
        folder=ROOT/'runs'/component['id'];input_path=folder/'inputs.npz'
        try:
            base=Interpreter(model_path=str(ROOT/component['path']),num_threads=1)
            rng=np.random.default_rng(20261003);arrays={}
            for i,detail in enumerate(base.get_input_details()):
                shape=tuple(detail['shape']);dtype=detail['dtype']
                if any(x<1 for x in shape):raise ValueError('Dynamic input not handled')
                for name,values in [('zeros',np.zeros(shape,np.float32)),('half',np.full(shape,.5,np.float32)),('random',rng.random(shape,dtype=np.float32))]:
                    if np.issubdtype(dtype,np.integer):
                        scale,zero=detail['quantization']
                        if scale<=0:raise ValueError('Missing input quantization')
                        values=np.clip(np.rint(values/scale)+zero,np.iinfo(dtype).min,np.iinfo(dtype).max)
                    arrays[f'{name}_input_{i}']=values.astype(dtype)
            np.savez_compressed(input_path,**arrays)
        except Exception as exc:
            row['setup_error']=repr(exc);report.append(row);continue
        baseline=None
        for variant in component['variants']:
            rec={'variant':variant['variant']}
            if not variant['structural_validation']['accepted']:
                rec['skipped']='structural rejection';row['variants'].append(rec);continue
            path=ROOT/variant['path'];dest=path.parent/'runtime'
            try:
                p=subprocess.run([sys.executable,str(ROOT/'scripts/runtime_one.py'),str(path),str(input_path),str(dest)],capture_output=True,text=True,timeout=90)
                (path.parent/'runtime.log').write_text(p.stdout+p.stderr)
                rec['exit_code']=p.returncode
                if p.returncode==0:
                    rec.update(json.loads((dest/'result.json').read_text()))
                    digests=[[x['sha256'] for x in case['outputs']] for case in rec['cases']]
                    if variant['variant']=='original':baseline=digests
                    rec['bitwise_equal_original']=digests==baseline if baseline is not None else None
                    if baseline is not None:assert rec['bitwise_equal_original']
                else:rec['error_tail']=(p.stdout+p.stderr)[-2000:]
            except subprocess.TimeoutExpired as exc:rec['error']='timeout after 90s'
            row['variants'].append(rec)
            print(component['id'],variant['variant'],'runtime',rec.get('exit_code',rec.get('error')),'equal',rec.get('bitwise_equal_original'),flush=True)
        report.append(row)
        (ROOT/'results/runtime-suite.json').write_text(json.dumps(report,indent=2))

if __name__=='__main__':main()
