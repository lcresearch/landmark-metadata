"""Read-only verification of frozen evidence; never invokes an old suite writer."""
import hashlib, json, os, pathlib, subprocess, sys, zipfile
import importlib.metadata
import numpy as np

ROOT=pathlib.Path(__file__).resolve().parents[1]
OLD=pathlib.Path('/workspace/metadata-contract-paper')
HAND=pathlib.Path('/workspace/hand-contract-repro')
sys.dont_write_bytecode=True
sys.path.insert(0,str(OLD/'scripts'))
from suite_static import canonical, md_bytes, associated, parse

def digest(data): return hashlib.sha256(data).hexdigest()
def entry(p): return {'path':str(p),'bytes':p.stat().st_size,'sha256':digest(p.read_bytes())}
def load(name): return json.loads((OLD/'results'/f'{name}.json').read_text())

manifest=json.loads((OLD/'WORKSPACE-EVIDENCE-MANIFEST.json').read_text())
checks=[]
for row in manifest['files']:
    p=OLD/row['path']
    actual=entry(p) if p.is_file() else {'path':str(p),'missing':True}
    actual['matches_frozen_hash']=actual.get('sha256')==row['sha256']
    checks.append(actual)
assert all(c['matches_frozen_hash'] for c in checks)
(ROOT/'phase0/frozen-manifest-verification.json').write_text(json.dumps(checks,indent=2))

inventory=[]
for base in [OLD,HAND]:
    for p in sorted(base.rglob('*')):
        if not p.is_file() or any(x in p.relative_to(base).parts for x in ['.venv','toolchains','__pycache__']): continue
        inventory.append(entry(p))
(ROOT/'phase0/inventory.json').write_text(json.dumps(inventory,indent=2))

static=load('static-suite'); comp=load('compile-suite'); runtime=load('runtime-suite'); dec=load('decoder-suite')
allvariants=[v for c in static for v in c['variants']]
summary={
 'metadata_components':sum(c['status']=='INSPECTED' for c in static),
 'metadata_graph_groups':len({c['canonical_sha256'] for c in static if c['status']=='INSPECTED'}),
 'variants':len(allvariants),
 'count_reductions_rejected':sum(v['variant']=='count_minus_one' and not v['structural_validation']['accepted'] for v in allvariants),
 'accepted_variants':sum(v['structural_validation']['accepted'] for v in allvariants),
 'recovered_cpu_invocations':sum(v.get('invocations',0) for c in runtime for v in c['variants']),
 'isolated_decoder_probes':len(dec),
 'unmodified_original_compile_success_ids':[c['id'] for c in comp if next((v for v in c['variants'] if v['variant']=='original'),{}).get('exit_code')==0],
}
focused=[]
for cid in ['6c7ab0a6e5dc','62a87ded76da']:
    c=next(c for c in static if c['id']==cid)
    base=(OLD/next(v for v in c['variants'] if v['variant']=='original')['path']).read_bytes()
    bmodel=parse(base); idx,bmd=md_bytes(base)
    reference=OLD/'runs'/cid/'original'
    base_java=(reference/'generated/src/main/java/org/example/contract/ContractModel.java').read_bytes()
    base_classes={str(p.relative_to(reference/'classes')):digest(p.read_bytes()) for p in (reference/'classes').rglob('*.class')}
    arrays0=np.load(reference/'runtime/outputs.npz')
    rows=[]
    for v in c['variants']:
        folder=(OLD/v['path']).parent; data=(folder/'model.tflite').read_bytes(); model=parse(data)
        row={'variant':v['variant'],'model':entry(folder/'model.tflite'),'canonical_graph_sha256':digest(canonical(data)),
             'canonical_equal':canonical(data)==canonical(base),'metadata_sha256':digest(md_bytes(data)[1]),
             'embedded_metadata_equal':md_bytes(data)[1]==bmd,
             'nonmetadata_buffers_equal':all(np.array_equal(model.Buffers(i).DataAsNumpy(),bmodel.Buffers(i).DataAsNumpy()) for i in range(model.BuffersLength()) if i!=idx),
             'associated_files':{name:{'sha256':digest(content),'nonempty_lines':len([s for s in content.decode().splitlines() if s.strip()])} for name,content in associated(data).items()},
             'recovered_structural_result':v['structural_validation']}
        if v['structural_validation']['accepted']:
            source=folder/'generated/src/main/java/org/example/contract/ContractModel.java'
            row['source']=entry(source); row['source_equal']=source.read_bytes()==base_java
            row['class_hashes']={str(p.relative_to(folder/'classes')):digest(p.read_bytes()) for p in (folder/'classes').rglob('*.class')}
            row['compiled_classes_equal']=row['class_hashes']==base_classes
            arrays=np.load(folder/'runtime/outputs.npz')
            row['recovered_arrays_equal']=all(arrays[k].tobytes()==arrays0[k].tobytes() for k in arrays0.files)
            row['raw_output_hashes']={k:digest(arrays[k].tobytes()) for k in arrays.files}
            row['decoder_log']=(folder/'decoder-probability.log').read_text() if (folder/'decoder-probability.log').exists() else None
            row['recovered_decoder_records']=[d for d in dec if d['id']==cid and d['variant']==v['variant']]
            row['recovered_compile_result']=next(vv for cc in comp if cc['id']==cid for vv in cc['variants'] if vv['variant']==v['variant'])
            assert row['source_equal'] and row['compiled_classes_equal'] and row['recovered_arrays_equal']
        assert row['canonical_equal'] and row['nonmetadata_buffers_equal']
        rows.append(row)
    focused.append({'id':cid,'source_occurrences':c['occurrences'],'variants':rows})

versions={'python':sys.version,'python_executable':sys.executable,'packages':{name:importlib.metadata.version(name) for name in ['tflite-support','tflite-runtime','numpy','flatbuffers','protobuf']},
 'jdk':subprocess.run([str(HAND/'toolchains/jdk-17.0.12+7/bin/java'),'-version'],capture_output=True,text=True).stderr,
 'jars':[entry(p) for p in sorted((HAND/'deps').glob('*.jar'))]}
archives=[entry(pathlib.Path('/workspace')/name) for name in ['hand-contract-evidence.zip','metadata-contract-paper-sources.zip']]
result={'evidence_status':'Fresh byte/hash/array audit of recovered evidence; no new generation, compilation, inference, or decoder execution in phase 0.',
 'frozen_manifest_entries_verified':len(checks),'inventory_entries':len(inventory),'summary_recomputed_from_records':summary,'focused':focused,'versions':versions,'archives':archives,
 'important_files':[entry(OLD/p) for p in ['manuscript/paper.tex','manuscript/paper.pdf','WORKSPACE-EVIDENCE-MANIFEST.json','results/summary.json','scripts/suite_static.py','scripts/codegen_one.py','scripts/suite_compile.py','scripts/DecoderProbe.java']]}
(ROOT/'phase0/results.json').write_text(json.dumps(result,indent=2))
print(json.dumps({'manifest_verified':len(checks),'inventory_entries':len(inventory),'summary':summary,'efficientnet':[{'variant':v['variant'],'sha256':v['model']['sha256'],'canonical':v['canonical_graph_sha256'],'source_equal':v.get('source_equal'),'classes_equal':v.get('compiled_classes_equal'),'arrays_equal':v.get('recovered_arrays_equal')} for v in focused[0]['variants']]},indent=2))
