"""Recalculate P2 observable facts directly from device files and packaged assets.

This is a separate implementation from the execution controller/analyzer. It
does not execute an interpreter or read raw outputs through the tested APIs.
"""
from pathlib import Path
import collections
import hashlib
import json
import struct
import zipfile

ROOT = Path(__file__).resolve().parents[1]
P2 = ROOT/'P2'
VARIANTS = ['original','description_control','label_deletion','label_permutation','restoration']
CASES = ['gray127','rgb_pattern']

def sha(data):
    return hashlib.sha256(data).hexdigest()

def load(p):
    return json.loads(p.read_text())

def main():
    out=ROOT/'verification/runtime-record-review.json'
    if out.exists():
        raise FileExistsError('Preserve previous reviews; use a new output path after changes.')
    inputs={row['variant']:row for row in load(ROOT/'INPUTS.json')['input_models']}
    frozen=load(P2/'EXECUTION_INPUT_FREEZE.json')
    checks=[]
    def check(name, ok, **detail):
        checks.append({'name':name,'status':'PASS' if ok else 'FAIL',**detail})
    with zipfile.ZipFile(inputs['original']['path']) as archive:
        base_names=archive.namelist()
        base_payload=archive.read('labels_without_background.txt')
    base_label_lines=base_payload.decode('utf-8').splitlines()
    for variant, row in inputs.items():
        path=Path(row['path'])
        check(f'{variant}: original source model digest',sha(path.read_bytes())==row['sha256'])
        with zipfile.ZipFile(path) as archive:
            check(f'{variant}: associated filenames preserved',archive.namelist()==base_names)
            payload=archive.read('labels_without_background.txt')
        expected=base_label_lines
        if variant=='label_deletion':expected=base_label_lines[:-1]
        if variant=='label_permutation':expected=base_label_lines[1:]+base_label_lines[:1]
        check(f'{variant}: exact declared resource order',payload.decode('utf-8').splitlines()==expected)
        if variant in ['original','description_control','restoration']:
            check(f'{variant}: original resource bytes',payload==base_payload)
    for row in frozen['files']:
        check('frozen execution input '+row['path'],sha((P2/row['path']).read_bytes())==row['sha256'])
    expected_inputs={'gray127':bytes([127])*(224*224*3),
                     'rgb_pattern':bytes((37*i+17)%256 for i in range(224*224*3))}
    units=[];decoded={};raw={};platforms=set();fingerprints=[]
    builds=load(P2/'build-results.json')
    for consumer in ['wrapper','task']:
        for variant in VARIANTS:
            folder=P2/'executions/primary'/consumer/variant/'device'
            report=load(folder/'result.json')
            platforms.add((report['platform'],report['api']))
            check(f'{consumer}/{variant}: device identifies variant',report['variant']==variant)
            build=next(x for x in builds if x['consumer']==consumer and x['variant']==variant)
            apk=P2/'build'/consumer/variant/'consumer.apk'
            with zipfile.ZipFile(apk) as archive:
                asset=archive.read('assets/model.tflite')
            check(f'{consumer}/{variant}: APK/device/source asset identity',
                  sha(asset)==report['loaded_asset_sha256']==inputs[variant]['sha256'])
            ctor=report.get('model_loading_status' if consumer=='wrapper' else 'model_initialization_status','NOT_REACHED')
            unit={'consumer':consumer,'variant':variant,'constructor':ctor,
                  'exception_type':report.get('exception_type'),'exception_message':report.get('exception_message'),
                  'cause_chain':report.get('cause_chain'), 'observations':[]}
            obs=report.get('observations',[])
            check(f'{consumer}/{variant}: observed input count follows constructor',len(obs)==(2 if ctor=='PASS' else 0))
            for case in obs:
                name=case['input'];pixels=(folder/f'{name}-input.rgb').read_bytes()
                check(f'{consumer}/{variant}/{name}: fixed RGB input',pixels==expected_inputs[name] and sha(pixels)==case['input_sha256'])
                record={'input':name,'input_sha256':sha(pixels),'inference':case.get('inference_status'),
                        'getter':case.get('generated_getter_status'),
                        'classify_atomic':case.get('classify_inference_and_decoding_status'),
                        'earliest_failure':case.get('earliest_failing_stage'),
                        'exception_type':case.get('exception_type'),'exception_message':case.get('exception_message')}
                if consumer=='wrapper' and (folder/f'{name}-output-0.f32').exists():
                    content=(folder/f'{name}-output-0.f32').read_bytes()
                    check(f'wrapper/{variant}/{name}: raw tensor length and digest',len(content)==4000 and sha(content)==case['raw_output_sha256'])
                    raw[(variant,name)]=content
                path=folder/f'{name}-decoded.json'
                if path.exists():
                    values=load(path)
                    if consumer=='task':
                        check(f'task/{variant}/{name}: one category head',len(values)==1 and values[0]['head_index']==0)
                        values=values[0]['categories']
                        by_index={v['category_index_field']:v for v in values}
                    else:
                        by_index={v['list_position']:v for v in values}
                    check(f'{consumer}/{variant}/{name}: complete category indices',len(values)==1000 and set(by_index)==set(range(1000)))
                    decoded[(consumer,variant,name)]=[by_index[i] for i in range(1000)]
                    if consumer=='wrapper':
                        words=struct.unpack('<1000I',raw[(variant,name)])
                        check(f'wrapper/{variant}/{name}: every returned score equals raw bits',
                              all((v['score_float_bits']&0xffffffff)==words[i] for i,v in enumerate(decoded[(consumer,variant,name)])))
                    record['category_count']=len(values)
                unit['observations'].append(record)
            units.append(unit)
    check('all units use the same platform fingerprint and API',len(platforms)==1,platforms=sorted(platforms))
    comparisons=[]
    for consumer in ['wrapper','task']:
        for name in CASES:
            base=decoded.get((consumer,'original',name))
            if base is None:
                check(f'{consumer}/{name}: original successful decoded result available',False)
                continue
            for variant in VARIANTS:
                vals=decoded.get((consumer,variant,name))
                if vals is None:continue
                changed=[i for i in range(1000) if vals[i]['label']!=base[i]['label']]
                same_scores=all(vals[i]['score_float_bits']==base[i]['score_float_bits'] for i in range(1000))
                expected_labels=[v['label'] for v in base]
                if variant=='label_permutation':expected_labels=expected_labels[1:]+expected_labels[:1]
                check(f'{consumer}/{variant}/{name}: planned label transformation', [v['label'] for v in vals]==expected_labels)
                comparisons.append({'consumer':consumer,'variant':variant,'input':name,'same_score_bits':same_scores,'changed_label_count':len(changed),'changed_positions':changed})
    raw_comparisons=[{'variant':v,'input':n,'equal_original':b==raw[('original',n)]} for (v,n),b in raw.items()]
    cross=[]
    for variant in VARIANTS:
        for name in CASES:
            a=decoded.get(('wrapper',variant,name));b=decoded.get(('task',variant,name))
            if a is None or b is None:continue
            mismatched=[i for i in range(1000) if a[i]['score_float_bits']!=b[i]['score_float_bits']]
            av=[struct.unpack('<f',struct.pack('<I',v['score_float_bits']&0xffffffff))[0] for v in a]
            bv=[struct.unpack('<f',struct.pack('<I',v['score_float_bits']&0xffffffff))[0] for v in b]
            cross.append({'variant':variant,'input':name,'bitwise_differing_scores':len(mismatched),
                          'max_absolute_score_difference':max(abs(x-y) for x,y in zip(av,bv)),
                          'label_disagreements':sum(x['label']!=y['label'] for x,y in zip(a,b)),
                          'comparison_scope':'Returned scores aligned by output/class index, not native raw Task tensors.'})
    result={'status':'PASS' if all(c['status']=='PASS' for c in checks) else 'FAIL',
            'checks':checks,'unit_count':len(units),'completed_input_observations':sum(len(u['observations']) for u in units),
            'decoded_lists':len(decoded),'wrapper_raw_tensors':len(raw),'units':units,
            'within_consumer_comparisons':comparisons,'wrapper_raw_comparisons':raw_comparisons,
            'cross_consumer_returned_score_comparisons':cross,
            'model_experiments_run_by_review':False,'human_verification':False}
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','unit_count','completed_input_observations','decoded_lists','wrapper_raw_tensors']},indent=2))
    print(json.dumps({'check_counts':dict(collections.Counter(c['status'] for c in checks)),
                      'within_score_invariance':all(c['same_score_bits'] for c in comparisons),
                      'wrapper_raw_invariance':all(c['equal_original'] for c in raw_comparisons),
                      'cross_consumer_comparisons':cross},indent=2))
    raise SystemExit(result['status']!='PASS')

if __name__=='__main__':main()
