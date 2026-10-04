#!/usr/bin/env python3
"""Read selected existing E1/E2/P2/P3 files; never execute a model.

This is a bounded readback, not a complete archive verifier. Comparisons are
reported as data, including false booleans; inspect the JSON rather than treating
process exit status as a universal evidence-validation result. The required
historical raw inputs remain outside the source-only repository.
"""
import argparse
import hashlib,json,struct
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--output-dir", required=True, type=Path,
                    help="New directory outside the repository; existing paths are rejected.")
parser.add_argument("--e2e-root", type=Path,
                    default=Path("/workspace/metadata-contract-e2e-20261004T030536Z"))
parser.add_argument("--p2p3-root", type=Path,
                    default=Path("/workspace/metadata-contract-p2p3-20261004T073824Z"))
args = parser.parse_args()
out = args.output_dir.resolve()
repository = Path(__file__).resolve().parents[3]
if out == repository or repository in out.parents:
    parser.error("Output must remain outside the source-only repository.")
if out.exists():
    parser.error("Output directory already exists; refusing to overwrite prior evidence.")
out.mkdir(parents=True, exist_ok=False)
seen={}
def read(p):
 p=Path(p); b=p.read_bytes(); seen[str(p)]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}; return b
def load(p):return json.loads(read(p))
e2e=args.e2e_root
phases={}; snapshots={}
for phase, variants in [('E1',['original','description_control','label_deletion','label_restoration']),('E2',['original','description_control','label_permutation','permutation_restoration'])]:
 rows=[]; base=e2e/phase/'executions/primary'; original={}
 for inp in ['gray127','rgb_pattern']:
  original[inp]={'raw':read(base/'original/device'/f'{inp}-output-0.f32'),'decoded':load(base/'original/device'/f'{inp}-decoded.json')}
 for variant in variants:
  d=base/variant/'device'; result=load(d/'result.json'); observations=[]
  if sorted(o['input'] for o in result['observations'])!=['gray127','rgb_pattern']:raise ValueError('input identities')
  for ob in result['observations']:
   inp=ob['input']; raw=read(d/f'{inp}-output-0.f32'); input_b=read(d/f'{inp}-input.rgb')
   rec={k:ob.get(k) for k in ['input','input_preparation_status','inference_status','raw_output_observation_status','generated_getter_status','earliest_failing_stage','exception_type','exception_message']}
   rec.update(raw_bytes=len(raw),raw_hash_matches_record=hashlib.sha256(raw).hexdigest()==ob['raw_output_sha256'],raw_equal_original=raw==original[inp]['raw'],input_hash_matches_record=hashlib.sha256(input_b).hexdigest()==ob['input_sha256'])
   if ob['generated_getter_status']=='PASS':
    decoded=load(d/f'{inp}-decoded.json'); ref=original[inp]['decoded']
    if [x['list_position'] for x in decoded]!=list(range(1000)):raise ValueError('decoded identities')
    rec.update(decoded_count=len(decoded),score_bits_equal_original=[x['score_float_bits'] for x in decoded]==[x['score_float_bits'] for x in ref],score_bits_equal_raw=[x['score_float_bits'] for x in decoded]==list(struct.unpack('<1000i',raw)),changed_label_positions=sum(x['label']!=y['label'] for x,y in zip(decoded,ref)),position904=decoded[904])
   else:rec['stack_contains_generated_getter']='ContractModel$Outputs.getProbabilityAsCategoryList' in ob['stack_trace']
   observations.append(rec)
  rows.append({'variant':variant,'model_loading_status':result['model_loading_status'],'observations':observations})
 phases[phase]=rows
p2=args.p2p3_root/'P2/executions/primary'; contrast={}
for consumer in ['wrapper','task']:
 j=load(p2/consumer/'label_deletion/device/result.json');contrast[consumer]=j
p3=args.p2p3_root/'P3/analysis'; reference=load(p3/'full-display-order-comparison.json')
if [x['output_position'] for x in reference]!=list(range(1000)):raise ValueError('reference identities')
reference_counts={variant:sum(row[key]==row['reference_display_label'] for row in reference) for variant,key in [('original','original_display_label'),('permutation','permutation_display_label'),('restoration','restored_display_label')]}
load(p3/'artifact-bridge.json');load(p3/'reference-chain.json')
result={'scope':'Read-only old primary E1/E2 result/input/raw/decoded bytes; P2 deletion stage records; P3 precomputed display comparison. No rerun or sealed-manifest authentication. P2/P3 preservation sources and model bytes not recomputed.','E1_E2':phases,'P2_deletion_records':contrast,'P3_recorded_strings_recounted':reference_counts,'source_files':seen}
with (out/'readback.json').open('x') as destination:
 destination.write(json.dumps(result,indent=2)+'\n')
print(json.dumps({'read_files':len(seen),'E1_E2':{k:[{'variant':x['variant'],'load':x['model_loading_status'],'observations':[{z:y[z] for z in ['input','inference_status','generated_getter_status','raw_equal_original','input_hash_matches_record','raw_hash_matches_record','changed_label_positions','score_bits_equal_original','score_bits_equal_raw'] if z in y} for y in x['observations']]} for x in v] for k,v in phases.items()},'P2_wrapper_earliest':[x.get('earliest_failing_stage') for x in contrast['wrapper']['observations']],'P2_task_earliest':contrast['task'].get('earliest_failing_stage'),'P3_reference_counts':reference_counts},indent=2))
