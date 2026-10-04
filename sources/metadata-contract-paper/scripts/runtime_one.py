from pathlib import Path
import hashlib
import json
import sys
import numpy as np
from tflite_runtime.interpreter import Interpreter

model,inputs_path,dest=map(Path,sys.argv[1:4]);dest.mkdir(parents=True,exist_ok=True)
runtime=Interpreter(model_path=str(model),num_threads=1);runtime.allocate_tensors()
inputs=runtime.get_input_details();outputs=runtime.get_output_details()
arrays={};records=[]
with np.load(inputs_path) as cases:
    for case in ['zeros','half','random']:
        for i,detail in enumerate(inputs):runtime.set_tensor(detail['index'],cases[f'{case}_input_{i}'])
        runtime.invoke();row={'input':case,'outputs':[]}
        for j,detail in enumerate(outputs):
            array=runtime.get_tensor(detail['index']);arrays[f'{case}_output_{j}']=array
            if not np.isfinite(array).all():raise RuntimeError('Nonfinite output')
            row['outputs'].append({'position':j,'shape':list(array.shape),'dtype':str(array.dtype),'sha256':hashlib.sha256(array.tobytes()).hexdigest(),
              'quantization':detail['quantization'],'min':float(array.min()),'max':float(array.max())})
            if case=='zeros':array.astype('<f4').tofile(dest/f'zeros-output-{j}.f32')
        records.append(row)
np.savez_compressed(dest/'outputs.npz',**arrays)
(dest/'result.json').write_text(json.dumps({'success':True,'invocations':3,'cases':records},indent=2))

