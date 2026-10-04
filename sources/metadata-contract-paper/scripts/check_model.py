"""Static, consumer-specific check of one TFLite model; no inference required.

Usage: python scripts/check_model.py model.tflite
Semantic index checking requires an exact digest present in contracts.json.
"""
from pathlib import Path
import argparse
import hashlib
import json
import tempfile
from tflite_support import metadata
from inspect_suite import inspect
from suite_static import md_bytes, generate, decoder_predictions

ROOT=Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser();parser.add_argument('model',type=Path);args=parser.parse_args()
    data=args.model.read_bytes();digest=hashlib.sha256(data).hexdigest();info=inspect(data)
    report={'model_sha256':digest,'consumer':'tflite-support 0.4.4 AndroidJavaGenerator / TensorLabel(List, TensorBuffer).getCategoryList',
      'scope':'Static checks of this consumer path; passing does not prove semantic correctness or successful Android execution.'}
    _,md=md_bytes(data)
    if md is None:
        report['status']='ABSTAIN_NO_METADATA';print(json.dumps(report,indent=2));return
    try:
        p=metadata.MetadataPopulator.with_model_buffer(data);p.load_metadata_buffer(md);p.populate()
        report['structural_check']='PASS'
    except Exception as exc:
        report.update(structural_check='FAIL',diagnostic=repr(exc));print(json.dumps(report,indent=2));return
    (ROOT/'checks').mkdir(exist_ok=True)
    folder=Path(tempfile.mkdtemp(prefix=digest[:12]+'-',dir=ROOT/'checks'))
    path=folder/'model.tflite';path.write_bytes(data)
    g=generate(path,folder);report['generation']=g
    if any(any(d<=0 for d in t['shape']) for t in info['output_tensors']):
        report['decoder_check']='ABSTAIN_DYNAMIC_SHAPE'
    else:report['decoder_checks']=decoder_predictions(data,info,g)
    report['index_check']='ABSTAIN_NO_SEMANTIC_REFERENCE'
    for key,contract in json.loads((ROOT/'contracts.json').read_text())['contracts'].items():
        if digest==key:
            names=info['metadata']['subgraph_metadata'][0]['output_tensor_metadata']
            roles=[contract['name_to_role'].get(n.get('name')) for n in names]
            report['index_check']='FAIL' if roles!=contract['expected_roles'] else 'PASS'
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
