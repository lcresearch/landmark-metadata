from pathlib import Path
import argparse, hashlib, io, json, shutil, subprocess, sys, zipfile

parser=argparse.ArgumentParser(description='Fresh Task classification, replay and baseline comparison.')
parser.add_argument('--output-dir',required=True,type=Path)
parser.add_argument('--python',type=Path,default=Path('/workspace/hand-contract-repro/.venv/bin/python'))
parser.add_argument('--corpus',type=Path,default=Path('/workspace/metadata-contract-paper/runs/6c7ab0a6e5dc'))
args=parser.parse_args()
ROOT=args.output_dir.resolve();PYTHON=args.python.absolute();CORPUS=args.corpus.resolve()
REPO=Path(__file__).resolve().parents[3]
if ROOT.is_relative_to(REPO):raise ValueError('Evidence must be outside the source-only repository')
ROOT.mkdir(parents=True,exist_ok=False)
for name in ['scripts','inputs','models','logs']:(ROOT/name).mkdir()
shutil.copy2(REPO/'sources/metadata-contract-e2e-20261004T030536Z/scripts/task_one.py',ROOT/'scripts/task_one.py')
shutil.copy2(REPO/'sources/metadata-contract-audit-20261004T062010Z/baseline/audit_one.py',ROOT/'scripts/audit_one.py')
(ROOT/'scripts/common.py').write_text("import json\ndef save(path,value):\n    path.parent.mkdir(parents=True,exist_ok=True)\n    path.write_text(json.dumps(value,indent=2))\n")
def sha(data): return hashlib.sha256(data).hexdigest()
def pack(raw, payloads):
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        prefix=min(x.header_offset for x in z.infolist())
    out=io.BytesIO(raw[:prefix])
    with zipfile.ZipFile(out,'a',compression=zipfile.ZIP_STORED) as z:
        for name,data in payloads.items():
            info=zipfile.ZipInfo(name,(1980,1,1,0,0,0)); info.compress_type=zipfile.ZIP_STORED
            z.writestr(info,data)
    return out.getvalue()
original=(CORPUS/'original/model.tflite').read_bytes()
if sha(original)!='6c7ab0a6e5dcbf38a8c33b960996a55a3b4300b36a018c4545801de3a3c8bde0':
    raise RuntimeError('Original artifact mismatch')
with zipfile.ZipFile(io.BytesIO(original)) as z:
    files={name:z.read(name) for name in z.namelist()}
name='labels_without_background.txt'; labels=files[name].decode().splitlines()
shifted=dict(files); shifted[name]=('\n'.join(labels[1:]+labels[:1])+ ('\n' if files[name].endswith(b'\n') else '')).encode()
models={'original':original,'description_control':(CORPUS/'description_control/model.tflite').read_bytes(),
        'label_deletion':(CORPUS/'label_drop_1/model.tflite').read_bytes(),
        'label_permutation':pack(original,shifted),'label_restoration':pack(original,files)}
for name,data in models.items(): (ROOT/'models'/f'{name}.tflite').write_bytes(data)
count=224*224*3
inputs={'gray127':bytes([127])*count,'rgb_pattern':bytes((37*i+17)%256 for i in range(count))}
for name,data in inputs.items(): (ROOT/'inputs'/f'{name}-input.rgb').write_bytes(data)
(ROOT/'inputs/manifest.json').write_text(json.dumps({k:sha(v) for k,v in inputs.items()},indent=2))
records=[]
for repeat in ['primary','replay']:
    for name in models:
        dest=ROOT/repeat/name
        p=subprocess.run([str(PYTHON),str(ROOT/'scripts/task_one.py'),str(ROOT/'models'/f'{name}.tflite'),str(ROOT/'inputs'),str(dest)],capture_output=True)
        (ROOT/'logs'/f'{repeat}-{name}.stdout').write_bytes(p.stdout)
        (ROOT/'logs'/f'{repeat}-{name}.stderr').write_bytes(p.stderr)
        result=json.loads((dest/'result.json').read_text()) if (dest/'result.json').exists() else {'controller_error':'missing result'}
        records.append({'run':repeat,'variant':name,'exit_code':p.returncode,'result':result})
        print(repeat,name,result.get('initialization_status'),result.get('classify_status'),flush=True)
(ROOT/'task-results.json').write_text(json.dumps(records,indent=2))
checks=[]
for repeat in ['primary','replay']:
    for name in models:
        row=next(r for r in records if r['run']==repeat and r['variant']==name)
        result=row['result']
        ok=row['exit_code']==0 and (result.get('initialization_status')=='FAIL' and result.get('earliest_failing_stage')=='task_initialization' and 'expected 999' in result.get('exception_message','') if name=='label_deletion' else result.get('classify_status')=='PASS' and len(result.get('observations',[]))==2 and all(x['returned_categories']==1000 for x in result['observations']))
        checks.append({'name':repeat+'/'+name+'/stages','pass':ok})
        if name=='label_deletion': continue
        for case in inputs:
            actual=json.loads((ROOT/repeat/name/f'{case}-decoded.json').read_text())[0]['categories']
            baseline=json.loads((ROOT/repeat/'original'/f'{case}-decoded.json').read_text())[0]['categories']
            indexed={c['index']:c for c in actual}; reference={c['index']:c for c in baseline}
            scores=set(indexed)==set(reference) and all(indexed[i]['score_float_bits']==reference[i]['score_float_bits'] for i in reference)
            changed=sum(indexed[i]['label']!=reference[i]['label'] for i in reference)
            expected=999 if name=='label_permutation' else 0
            checks.append({'name':repeat+'/'+name+'/'+case,'pass':scores and changed==expected,'score_bits_equal':scores,'changed_labels':changed})
            if repeat=='replay':
                checks.append({'name':'replay/'+name+'/'+case+'/decoded_bytes','pass':(ROOT/repeat/name/f'{case}-decoded.json').read_bytes()==(ROOT/'primary'/name/f'{case}-decoded.json').read_bytes()})
baseline_records=[]
for name in models:
    for mode in ['displayer','populator','simple_baseline','task_init']:
        dest=ROOT/'baseline'/name/mode
        p=subprocess.run([str(PYTHON),str(ROOT/'scripts/audit_one.py'),mode,str(ROOT/'models'/f'{name}.tflite'),str(dest)],capture_output=True)
        (ROOT/'logs'/f'baseline-{name}-{mode}.stdout').write_bytes(p.stdout)
        (ROOT/'logs'/f'baseline-{name}-{mode}.stderr').write_bytes(p.stderr)
        result=json.loads((dest/'result.json').read_text())
        baseline_records.append({'variant':name,'mode':mode,'exit_code':p.returncode,'result':result})
        expected={'displayer':'READABLE','populator':'ACCEPTED','simple_baseline':'INCOMPATIBLE' if name=='label_deletion' else 'COMPATIBLE_PRECONDITIONS','task_init':'FAIL' if name=='label_deletion' else 'PASS'}[mode]
        checks.append({'name':'baseline/'+name+'/'+mode,'pass':result['status']==expected and p.returncode==(2 if expected in ['FAIL','INCOMPATIBLE'] else 0)})
(ROOT/'baseline-results.json').write_text(json.dumps(baseline_records,indent=2))
(ROOT/'checks.json').write_text(json.dumps({'checks':checks,'passed':sum(x['pass'] for x in checks),'failed':sum(not x['pass'] for x in checks)},indent=2))
if not checks or any(not x['pass'] for x in checks): raise SystemExit(1)
