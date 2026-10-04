import io, json, pathlib, re, shutil, sys, zipfile
import numpy as np
from common import ROOT, HAND, JDK, sha, save, run
sys.dont_write_bytecode=True;sys.path.insert(0,str(ROOT.parent/'metadata-contract-paper/scripts'))
from suite_static import canonical, parse, md_bytes
from inspect_suite import inspect
base=ROOT/'E7';manifest=json.loads((HAND/'MANIFEST.json').read_text());checks=[]
for row in manifest['files']:
    file=HAND/row['path'];ok=file.is_file() and sha(file.read_bytes())==row['sha256'];checks.append({'path':str(file),'sha256':row['sha256'],'matches':ok})
assert all(x['matches'] for x in checks);save(base/'recovered-hand-manifest-audit.json',checks)
bundle=(HAND/'artifacts/official-v1.task').read_bytes();original=(HAND/'artifacts/original.tflite').read_bytes();swapped=(HAND/'artifacts/swapped.tflite').read_bytes()
assert sha(original)=='6acda74af3fbf40e68265c20c7394b2bad81a16a481dcd79ad7a081887c3d6b9'
assert sha(swapped)=='5c4a32919676d6645c082b4b2912ae4881862af967b5aa5b40e0ef6d616a3025'
with zipfile.ZipFile(io.BytesIO(bundle)) as z:payloads={name:z.read(name) for name in z.namelist()}
assert payloads['hand_landmarks_detector.tflite']==original
def pack(entries):
    out=io.BytesIO()
    with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_STORED) as z:
        for name,payload in entries.items():z.writestr(zipfile.ZipInfo(name,(1980,1,1,0,0,0)),payload)
    return out.getvalue()
control=pack(payloads);changed=dict(payloads);changed['hand_landmarks_detector.tflite']=swapped;restored=dict(changed);restored['hand_landmarks_detector.tflite']=original
variants={'original':bundle,'container_control':control,'metadata_exchange':pack(changed),'restoration':pack(restored)}
assert variants['restoration']==control
records=[]
for name,data in variants.items():
    folder=base/'variants'/name;folder.mkdir(parents=True,exist_ok=False);(folder/'hand_landmarker.task').write_bytes(data)
    with zipfile.ZipFile(io.BytesIO(data)) as z:entries={n:z.read(n) for n in z.namelist()}
    component=entries['hand_landmarks_detector.tflite'];(folder/'hand_landmarks_detector.tflite').write_bytes(component)
    m=parse(component);bm=parse(original);idx,md=md_bytes(original)
    nonmeta=all(np.array_equal(m.Buffers(i).DataAsNumpy(),bm.Buffers(i).DataAsNumpy()) for i in range(m.BuffersLength()) if i!=idx)
    assert canonical(component)==canonical(original) and nonmeta
    assert all(entries[n]==payloads[n] for n in payloads if n!='hand_landmarks_detector.tflite')
    record={'experiment_id':'E7','variant':name,'bundle_sha256':sha(data),'component_sha256':sha(component),'canonical_graph_sha256':sha(canonical(component)),
      'members':{n:sha(b) for n,b in entries.items()},'preservation_check':{'nonmetadata_buffers_equal':nonmeta,'canonical_equal':True,'other_components_equal':True,'changed_component_byte_offsets':[i for i,(a,b) in enumerate(zip(original,component)) if a!=b]},
      'inspection':inspect(component),'artifact_paths':{'bundle':str((folder/'hand_landmarker.task').relative_to(ROOT)),'component':str((folder/'hand_landmarks_detector.tflite').relative_to(ROOT))}}
    records.append(record)
save(base/'static-results.json',records)
old=json.loads((HAND/'results/compile-results.json').read_text());audit=[]
for name in ['original','swapped']:
    rec=old['variants'][name];src=pathlib.Path(rec['raw']['command'][-1]);patched=pathlib.Path(rec['repaired']['command'][-1]);a=src.read_text();b=patched.read_text()
    assert sha(src.read_bytes())==rec['source_sha256'] and sha(patched.read_bytes())==rec['patched_sha256']
    repaired=a;counts=[]
    for pattern,replacement in old['repair_rules']:repaired,n=re.subn(pattern,replacement,repaired);counts.append(n)
    assert repaired==b and counts==rec['repair_counts'];assert re.sub(r'[\s,]+','',a)==re.sub(r'[\s,]+','',b)
    folder=base/'binding-audit'/name;folder.mkdir(parents=True)
    shutil.copyfile(src,folder/'unmodified.java');shutil.copyfile(patched,folder/'separator-repaired.java')
    q=run([JDK/'bin/javap','-classpath',HAND/'build'/name/'classes','-c','-p','org.example.hand.HandModel$Outputs'],folder/'fresh-outputs-javap')
    assert q.returncode==0;bytecode=q.stdout.decode()
    match=re.search(r'java\.util\.Map<java\.lang\.Integer, java\.lang\.Object> getBuffer\(\);(.*?)(?:\n  private|\n})',bytecode,re.S);assert match
    pairs=re.findall(r'iconst_(\d).*?getfield\s+#\d+\s+// Field (\w+):',match.group(1),re.S)
    mapping={field:int(index) for index,field in pairs};assert mapping==rec['bytecode_field_output_mapping']
    audit.append({'variant':name,'fresh_disassembly_of_preserved_classes':True,'fresh_compilation':False,'recovered_raw_compile_exit':rec['raw']['exit_code'],'recovered_repaired_compile_exit':rec['repaired']['exit_code'],
      'source_sha256':sha(src.read_bytes()),'repaired_sha256':sha(patched.read_bytes()),'separator_rules_reapplied_to_in_memory_copy_match_preserved_patch':True,'changed_source_lines':rec['changed_source_lines'],'bytecode_field_output_mapping':mapping,'field_shapes':rec['field_shapes']})
save(base/'binding-audit.json',audit)
print(json.dumps(audit,indent=2))
