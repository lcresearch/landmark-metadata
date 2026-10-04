import io, json, pathlib, shutil, sys, zipfile
import numpy as np
from common import ROOT, PYTHON, sha, save, run
OLD=pathlib.Path('/workspace/metadata-contract-paper')
sys.dont_write_bytecode=True
sys.path.insert(0,str(OLD/'scripts'))
from suite_static import canonical, md_bytes, associated, parse, mutate_label
from tflite_support import metadata

def rewrite_associated(raw, entries):
    with zipfile.ZipFile(io.BytesIO(raw)) as z:start=min(x.header_offset for x in z.infolist())
    out=io.BytesIO(raw[:start])
    with zipfile.ZipFile(out,'a',compression=zipfile.ZIP_STORED) as z:
        for name,data in entries.items():
            info=zipfile.ZipInfo(name,(1980,1,1,0,0,0));info.compress_type=zipfile.ZIP_STORED;z.writestr(info,data)
    return out.getvalue()

def prepare(experiment, variants, original, provenance):
    base=parse(original);idx,md=md_bytes(original);base_canonical=canonical(original)
    with zipfile.ZipFile(io.BytesIO(original)) as z:prefix_len=min(x.header_offset for x in z.infolist())
    records=[]
    for name,data in variants.items():
        folder=ROOT/experiment/'variants'/name;folder.mkdir(parents=True,exist_ok=False)
        path=folder/'model.tflite';path.write_bytes(data)
        model=parse(data);metadata_data=md_bytes(data)[1]
        entries=associated(data)
        for filename,payload in entries.items():
            dest=folder/'associated'/filename;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(payload)
        checks={'canonical_equal':canonical(data)==base_canonical,
            'nonmetadata_buffers_equal':model.BuffersLength()==base.BuffersLength() and all(np.array_equal(model.Buffers(i).DataAsNumpy(),base.Buffers(i).DataAsNumpy()) for i in range(base.BuffersLength()) if i!=idx),
            'embedded_metadata_equal':metadata_data==md,
            'flatbuffer_prefix_equal':data[:prefix_len]==original[:prefix_len],
            'whole_model_equal':data==original,
            'associated_filenames_equal':set(entries)==set(associated(original))}
        assert checks['canonical_equal'] and checks['nonmetadata_buffers_equal']
        if name!='description_control':assert checks['embedded_metadata_equal'] and checks['flatbuffer_prefix_equal']
        row={'experiment_id':experiment,'component_name':'efficientnet_lite0','component_sha256':sha(original),
          'variant_sha256':sha(data),'canonical_graph_sha256':sha(canonical(data)),'source_bundle':provenance,'variant':name,
          'metadata_sha256':sha(metadata_data),'associated_file_sha256':{n:sha(b) for n,b in entries.items()},
          'label_counts':{n:len([line for line in b.decode().splitlines() if line.strip()]) for n,b in entries.items()},
          'preservation_check':checks,'generator_version':'tflite-support==0.4.4','consumer':'unmodified generated ContractModel; pinned Android instrumentation harness',
          'runtime_version':'tensorflow-lite Java/native 2.13.0','compiler_version':'Temurin JDK 17.0.12+7 --release 8',
          'platform':'Android API 30 default x86_64 emulator, software CPU','semantic_check':'ABSTAIN_NO_INDEPENDENT_CLASS_ORDER_REFERENCE',
          'artifact_paths':{'model':str(path.relative_to(ROOT))},'notes':[]}
        try:
            pop=metadata.MetadataPopulator.with_model_buffer(data);pop.load_metadata_buffer(metadata_data);pop.populate()
            row['structural_status']='PASS'
        except Exception as exc:
            row.update(structural_status='FAIL',structural_exception=repr(exc))
        if row['structural_status']=='PASS':
            p=run([PYTHON,ROOT/'scripts/codegen_one.py',path,folder/'generated',folder/'codegen-status.json'],folder/'logs/codegen')
            row['generation_status']='PASS' if p.returncode==0 and (folder/'codegen-status.json').exists() else 'FAIL'
            source=folder/'generated/src/main/java/org/example/contract/ContractModel.java'
            if source.exists():
                row['source_sha256']=sha(source.read_bytes());row['artifact_paths']['source']=str(source.relative_to(ROOT))
        records.append(row);save(ROOT/experiment/'static-results.json',records)
    base_source=records[0].get('source_sha256')
    for row in records:row['preservation_check']['generated_source_equal']=row.get('source_sha256')==base_source
    save(ROOT/experiment/'static-results.json',records)
    print(json.dumps([{k:r[k] for k in ['variant','variant_sha256','structural_status','generation_status','preservation_check']} for r in records],indent=2))

def main():
    old=OLD/'runs/6c7ab0a6e5dc';original=(old/'original/model.tflite').read_bytes();assert sha(original)=='6c7ab0a6e5dcbf38a8c33b960996a55a3b4300b36a018c4545801de3a3c8bde0'
    desc=(old/'description_control/model.tflite').read_bytes()
    # Replay the same one-character, same-size description edit rather than assuming the saved mutant.
    md=md_bytes(original)[1];text=b'Probabilities of the 1000 labels respectively.';pos=original.find(text,original.find(md));assert pos>=0
    changed=bytearray(original);changed[pos]^=32;assert bytes(changed)==desc
    drop=mutate_label(original,'labels_without_background.txt');assert drop==(old/'label_drop_1/model.tflite').read_bytes()
    restored=rewrite_associated(drop,associated(original));assert associated(restored)==associated(original)
    shutil.copyfile(OLD/'scripts/codegen_one.py',ROOT/'scripts/codegen_one.py')
    prepare('E1',dict(original=original,description_control=desc,label_deletion=drop,label_restoration=restored),original,
        'https://storage.googleapis.com/mediapipe-models/image_classifier/efficientnet_lite0/float32/1/efficientnet_lite0.tflite; exact bytes recovered from frozen local evidence')
if __name__=='__main__':main()
