import argparse, json, pathlib, struct
from common import ROOT, sha, save
ap=argparse.ArgumentParser();ap.add_argument('--experiment',required=True);args=ap.parse_args();base=ROOT/args.experiment
primary=json.loads((base/'executions/primary/results.json').read_text())
replay_path=base/'executions/replay/results.json';replay=json.loads(replay_path.read_text()) if replay_path.exists() else []
original=base/'executions/primary/original/device';checks=[]
for row in primary:
    name=row['variant'];folder=base/'executions/primary'/name/'device';comparison={'variant':name,'inputs':[]}
    for case in ['gray127','rgb_pattern']:
        item={'input':case}
        raw=folder/(case+'-output-0.f32');raw0=original/(case+'-output-0.f32')
        if raw.exists() and raw0.exists():
            item['raw_output_equal_original']=raw.read_bytes()==raw0.read_bytes()
            item['input_equal_original']=(folder/(case+'-input.rgb')).read_bytes()==(original/(case+'-input.rgb')).read_bytes()
        else:item['raw_output_equal_original']=None
        dec=folder/(case+'-decoded.json');dec0=original/(case+'-decoded.json')
        if dec.exists() and dec0.exists():
            decoded=json.loads(dec.read_text());decoded0=json.loads(dec0.read_text())
            item['decoded_equal_original']=decoded==decoded0
            item['score_bits_equal_original']=[d['score_float_bits'] for d in decoded]==[d['score_float_bits'] for d in decoded0]
            item['changed_label_positions']=[i for i,(a,b) in enumerate(zip(decoded,decoded0)) if a['label']!=b['label']]
            item['cyclic_association_mapping_holds']=len(decoded)==len(decoded0) and all(d['label']==decoded0[(i+1)%len(decoded0)]['label'] for i,d in enumerate(decoded))
            observed=next(o for o in row.get('observed',{}).get('observations',[]) if o['input']==case)
            item['top5']=[dict(d,label=decoded[d['index']]['label'],original_label=decoded0[d['index']]['label']) for d in observed['top5_raw']]
            item['returned_scores_match_raw_position']=all(d['score_float_bits']==struct.unpack_from('<I',raw.read_bytes(),4*i)[0] for i,d in enumerate(decoded))
        comparison['inputs'].append(item)
    again=next((r for r in replay if r['variant']==name),None)
    if again:
        comparison['replay_same_stage_outcomes']=all(row.get(k)==again.get(k) for k in ['load_status','inference_status','decoder_status','earliest_failing_stage','exception_type','exception_message'])
        comparison['replay_raw_outputs_equal']=row.get('raw_output_hashes')==again.get('raw_output_hashes')
        re_dir=base/'executions/replay'/name/'device'
        comparison['replay_decoded_equal']=all((re_dir/p.name).exists() and (re_dir/p.name).read_bytes()==p.read_bytes() for p in folder.glob('*-decoded.json'))
    row['comparisons']=comparison;row['replay_record']=again;checks.append(comparison)
save(base/'results.json',{'experiment_id':args.experiment,'experimental_unit':'component × variant × consumer/toolchain configuration','units':primary,'unit_count':len(primary),'primary_inputs_per_unit':2,'replay_is_independent':False,'comparison_checks':checks})
lines=[f'# {args.experiment} results','', 'Fresh Android instrumentation execution of the byte-unmodified generated public interface. Recovered host-JVM probes are not pooled into these results. Same-environment replay is separate from the primary observations.','', '| Variant | S | Generate | Compile | Package | Load | Inference | Actual getter | Earliest failure |','|---|---|---|---|---|---|---|---|---|']
for r in primary:lines.append('| '+' | '.join(str(r.get(k,'—' if k=='earliest_failing_stage' else 'NOT_REACHED')) for k in ['variant','structural_status','generation_status','compile_status','package_status','load_status','inference_status','decoder_status','earliest_failing_stage'])+' |')
lines+=['','## Preservation and actual observations','']
for r in primary:
    c=r['comparisons'];lines.append(f"- {r['variant']}: canonical graph preserved={r['preservation_check']['canonical_equal']}; embedded metadata equal={r['preservation_check']['embedded_metadata_equal']}; source equal={r['preservation_check']['generated_source_equal']}; generated classes equal={r['build']['generated_classes_equal_original']}; DEX equal={r['build']['dex_equal_original']}.")
    for i in c['inputs']:
        lines.append(f"  - {i['input']}: raw equality={i['raw_output_equal_original']}; score-bit equality={i.get('score_bits_equal_original','NOT_REACHED')}; changed label positions={len(i.get('changed_label_positions',[])) if 'changed_label_positions' in i else 'NOT_REACHED'}.")
    if r.get('exception_type'):lines.append(f"  - Exact failure: `{r['exception_type']}: {r.get('exception_message')}`.")
    lines.append(f"  - Replay: stage outcomes={c.get('replay_same_stage_outcomes','NOT_RUN')}; raw equality={c.get('replay_raw_outputs_equal','NOT_RUN')}; decoded equality={c.get('replay_decoded_equal','NOT_RUN')}.")
lines+=['','## Evidence paths and boundaries','', f'`{args.experiment}/results.json` contains one record per variant/configuration with nested primary and replay evidence. See `variants/<variant>/generated`, `variants/<variant>/build`, and `executions/<run>/<variant>/device` plus `logs`. Exact subprocesses are in `commands-executed.sh` and each `.command.json`. Full dependencies and downloads: `prerequisites/`.', '', 'The generated historical Gradle project was not used. The pinned minimal Android APK harness compiles the unmodified Java with official Java/native dependencies. Whole-APK byte differences are not treated as code differences. No deployment, real-user impact, task-accuracy, prevalence, semantic-truth or general detector-accuracy claim follows. Class-order semantics remain ABSTAIN absent an independent artifact-tied reference.','', 'The restored associated payload matches the original; archive container bytes need not match the publisher ZIP. A successful label-order intervention changes association relative to original only. If a stage is NOT_REACHED, no later-stage outcome is inferred.','']
if (base/'deviations.json').exists():lines+=['## Deviations','', '```json',(base/'deviations.json').read_text(),'```','']
(ROOT/f'EXPERIMENT_{args.experiment}_RESULTS.md').write_text('\n'.join(lines))
print(json.dumps([{k:r.get(k) for k in ['variant','load_status','inference_status','decoder_status','earliest_failing_stage','exception_message']} for r in primary],indent=2))
