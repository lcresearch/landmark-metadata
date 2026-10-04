"""Exploratory probe, prompted by observing two labels for a scalar score."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import zipfile
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
JDK=Path(os.environ.get('REPRO_JDK',str(ROOT/'toolchains/jdk-17.0.12+7')))

def run(args,log):
    p=subprocess.run([str(x) for x in args],cwd=ROOT,capture_output=True,text=True)
    (ROOT/'logs'/log).write_text(p.stdout+p.stderr)
    assert p.returncode==0, p.stdout+p.stderr
    return p.stdout

def main():
    labels=ROOT/'artifacts/handedness.txt'
    with zipfile.ZipFile(ROOT/'artifacts/original.tflite') as z: labels.write_bytes(z.read('handedness.txt'))
    run([JDK/'bin/javac','--release','8','-cp','deps/*','-d','build/decoder','scripts/DecoderProbe.java'],'decoder-javac.log')
    report={'status':'exploratory, planned after metadata and generated source inspection',
      'scope':'Execute official TensorLabel category decoder and generated DequantizeOp(0,0) expression on actual CPU output buffers in a host JVM. Does not execute a generated wrapper, Android app, or Java TFLite interpreter.',
      'labels':labels.read_text().splitlines(),'cases':[]}
    for name,size,index in [('original',63,0),('swapped',1,2)]:
        f=ROOT/f'results/runtime-arrays/{name}-zeros-output-{index}.f32'
        stdout=run([JDK/'bin/java','-cp','deps/*:build/decoder','DecoderProbe',name,str(size),f,labels],name+'-decoder-probe.log')
        report['cases'].append({'variant':name,'shape':[1,size],'output_position':index,'input':'zeros','raw_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'stdout':stdout})
        print(stdout,flush=True)
    # Positive control isolates the API cardinality requirement with an explicit two-score tensor.
    # This synthetic vector is not claimed to implement MediaPipe handedness semantics.
    positive=ROOT/'results/runtime-arrays/decoder-positive-two-scores.f32'
    np.array([.25,.75],dtype='<f4').tofile(positive)
    stdout=run([JDK/'bin/java','-cp','deps/*:build/decoder','DecoderProbe','two_score_api_control','2',positive,labels],'positive-decoder-probe.log')
    report['cases'].append({'variant':'two_score_api_control','shape':[1,2],'synthetic_scores':[.25,.75],'stdout':stdout})
    assert 'status=ok categories=2' in stdout
    print(stdout,flush=True)
    assert 'Label number 2 mismatch the shape on axis 1' in report['cases'][0]['stdout']
    assert 'Cannot find an axis to label' in report['cases'][1]['stdout']
    (ROOT/'results/decoder-results.json').write_text(json.dumps(report,indent=2))

if __name__=='__main__':
    main()
