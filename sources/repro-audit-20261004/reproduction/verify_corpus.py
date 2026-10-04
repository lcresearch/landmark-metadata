"""Independently require complete fresh arrays and verify their recorded digests."""
from pathlib import Path
import hashlib, json
import numpy as np
from tensorflow_lite_support.metadata import schema_py_generated as schema

ROOT=Path('/workspace/metadata-contract-paper')
checks=[]
def check(name,passed,**facts): checks.append(dict(name=name,passed=bool(passed),**facts))
def sha(data):return hashlib.sha256(data).hexdigest()
static=json.loads((ROOT/'results/static-suite.json').read_text())
runtime=json.loads((ROOT/'results/runtime-suite.json').read_text())
runtime_map={(c['id'],v['variant']):v for c in runtime for v in c['variants']}
observations=0;arrays=0;accepted=0;rejected=0
for component in static:
    original=(ROOT/component['path']).read_bytes()
    check(component['id']+'/publisher_digest',sha(original)==component['sha256'])
    m=schema.Model.GetRootAsModel(original,0)
    metadata_indices={m.Metadata(i).Buffer() for i in range(m.MetadataLength()) if m.Metadata(i).Name()==b'TFLITE_METADATA'}
    baseline_folder=ROOT/'runs'/component['id']/'original/runtime'
    for variant in component['variants']:
        name=component['id']+'/'+variant['variant']
        data=(ROOT/variant['path']).read_bytes();mut=schema.Model.GetRootAsModel(data,0)
        check(name+'/model_digest',sha(data)==variant['sha256'])
        check(name+'/all_nonmetadata_buffers',m.BuffersLength()==mut.BuffersLength() and all(np.array_equal(m.Buffers(i).DataAsNumpy(),mut.Buffers(i).DataAsNumpy()) for i in range(m.BuffersLength()) if i not in metadata_indices))
        record=runtime_map.get((component['id'],variant['variant']))
        if not variant['structural_validation']['accepted']:
            rejected+=1;check(name+'/structural_rejection_recorded',record is not None and record.get('skipped')=='structural rejection');continue
        accepted+=1
        check(name+'/runtime_completed',record is not None and record.get('exit_code')==0 and record.get('success') is True and record.get('invocations')==3)
        dest=(ROOT/variant['path']).parent/'runtime'
        if not (dest/'outputs.npz').exists() or not (baseline_folder/'outputs.npz').exists():
            check(name+'/required_arrays',False);continue
        with np.load(dest/'outputs.npz') as actual,np.load(baseline_folder/'outputs.npz') as baseline:
            expected={f'{case}_output_{i}' for case in ['zeros','half','random'] for i in range(m.Subgraphs(0).OutputsLength())}
            check(name+'/complete_array_keys',set(actual.files)==expected and set(baseline.files)==expected)
            observed_cases=record.get('cases',[])
            check(name+'/complete_case_records',{c['input'] for c in observed_cases}=={'zeros','half','random'} and len(observed_cases)==3)
            for case in observed_cases:
                observations+=1
                check(name+'/'+case['input']+'/complete_output_records',len(case['outputs'])==m.Subgraphs(0).OutputsLength())
                for output in case['outputs']:
                    key=f"{case['input']}_output_{output['position']}"; a=actual[key];b=baseline[key];arrays+=1
                    check(name+'/'+key,np.isfinite(a).all() and a.shape==b.shape and a.dtype==b.dtype and a.tobytes()==b.tobytes() and sha(a.tobytes())==output['sha256'])
decoder=json.loads((ROOT/'results/decoder-suite.json').read_text())
check('decoder_expected_fixture_count',len(decoder)==23)
for i,r in enumerate(decoder):
    check('decoder/'+str(i),r.get('exit_code')==0 and 'skipped' not in r and 'probe_error' not in r and r.get('observed',{}).get('status')==r['prediction']['status'] and r['observed']['labels']==r['prediction']['label_count'])
check('nonempty_required_design',len(static)==13 and accepted==35 and rejected==11 and observations==105)
report={'components':len(static),'accepted_variants':accepted,'structurally_rejected':rejected,'cpu_observations_verified':observations,'raw_arrays_verified':arrays,'decoder_probes_verified':len(decoder),'passed':sum(c['passed'] for c in checks),'failed':sum(not c['passed'] for c in checks),'checks':checks}
Path('/workspace/repro-control/corpus-verification.json').write_text(json.dumps(report,indent=2))
print(json.dumps({k:v for k,v in report.items() if k!='checks'},indent=2))
if not checks or any(not c['passed'] for c in checks):raise SystemExit(1)
