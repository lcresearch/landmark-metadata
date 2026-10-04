"""Predeclared synthetic CPU equivalence tests, with raw arrays preserved."""
from pathlib import Path
import hashlib
import json
import platform
import numpy as np
from tflite_runtime.interpreter import Interpreter
import tflite_runtime

ROOT=Path(__file__).resolve().parents[1]
VARIANTS=['original','swapped','description_control','swap_back_control']

def digest(a):
    return hashlib.sha256(a.tobytes()).hexdigest()

def main():
    rng=np.random.default_rng(20261003)
    first=Interpreter(model_path=str(ROOT/'artifacts/original.tflite'),num_threads=1)
    first.allocate_tensors()
    shape=tuple(first.get_input_details()[0]['shape'])
    inputs={'zeros':np.zeros(shape,np.float32),'ones':np.ones(shape,np.float32),'half':np.full(shape,.5,np.float32),'ramp':np.linspace(0,1,np.prod(shape),dtype=np.float32).reshape(shape)}
    inputs.update({f'random_{i}':rng.random(shape,dtype=np.float32) for i in range(8)})
    raw=ROOT/'results/runtime-arrays'
    raw.mkdir(exist_ok=True)
    np.savez_compressed(raw/'inputs.npz',**inputs)
    baseline={}
    report={'runtime':tflite_runtime.__version__,'numpy':np.__version__,'python':platform.python_version(),'platform':platform.platform(),
      'threads':1,'inputs':len(inputs),'input_shape':list(map(int,shape)),'scope':'Synthetic tensors; CPU interpreter. No Android or generated-wrapper inference. No task accuracy measurement.','variants':{}}
    for name in VARIANTS:
        interpreter=first if name=='original' else Interpreter(model_path=str(ROOT/f'artifacts/{name}.tflite'),num_threads=1)
        if name!='original': interpreter.allocate_tensors()
        inp=interpreter.get_input_details()[0]
        out=interpreter.get_output_details()
        assert inp['dtype']==np.float32
        rows=[]
        arrays={}
        for key,x in inputs.items():
            interpreter.set_tensor(inp['index'],x)
            interpreter.invoke()
            stats=[]
            for i,d in enumerate(out):
                y=interpreter.get_tensor(d['index'])
                assert np.isfinite(y).all()
                if name=='original': baseline[(key,i)]=y.copy()
                ref=baseline[(key,i)]
                equal=y.tobytes()==ref.tobytes()
                arrays[f'{key}_output_{i}']=y
                stats.append({'output_position':i,'shape':list(y.shape),'sha256':digest(y),'bitwise_equal_original':equal,
                  'max_abs_diff':float(np.max(np.abs(y-ref))),'min':float(y.min()),'max':float(y.max())})
                assert equal, (name,key,i)
            rows.append({'input':key,'input_sha256':digest(x),'outputs':stats})
        np.savez_compressed(raw/f'{name}-outputs.npz',**arrays)
        # Raw float files let the separately scoped Java decoder probe consume actual CPU results.
        for i in range(4): arrays[f'zeros_output_{i}'].astype('<f4').tofile(raw/f'{name}-zeros-output-{i}.f32')
        report['variants'][name]={'invocations':len(inputs),'all_outputs_bitwise_equal_original':True,'cases':rows}
        print(name,len(inputs),'CPU invocations; all 4 outputs bitwise equal to baseline',flush=True)
    report['total_invocations']=len(inputs)*len(VARIANTS)
    report['total_output_arrays']=report['total_invocations']*4
    (ROOT/'results/inference-results.json').write_text(json.dumps(report,indent=2))

if __name__=='__main__':
    main()
