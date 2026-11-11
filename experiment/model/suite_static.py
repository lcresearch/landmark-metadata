from pathlib import Path
import copy
import hashlib
import io
import itertools
import json
import re
import struct
import subprocess
import sys
import zipfile
import flatbuffers
import numpy as np
from tflite_support import metadata
from tensorflow_lite_support.metadata import schema_py_generated as schema
from tensorflow_lite_support.metadata import metadata_schema_py_generated as ms
from inspect_suite import inspect

ROOT=Path(__file__).resolve().parents[1]

def sha(data):return hashlib.sha256(data).hexdigest()
def parse(data):return schema.Model.GetRootAsModel(data,0)

def md_bytes(data):
    model=parse(data)
    for i in range(model.MetadataLength()):
        if model.Metadata(i).Name()==b'TFLITE_METADATA':
            idx=model.Metadata(i).Buffer();return idx,model.Buffers(idx).DataAsNumpy().tobytes()
    return None,None

def canonical(data):
    model=schema.ModelT.InitFromObj(parse(data))
    for entry in model.metadata or []:
        if entry.name==b'TFLITE_METADATA':model.buffers[entry.buffer].data=None
    model.metadata=[entry for entry in model.metadata or [] if entry.name!=b'TFLITE_METADATA']
    builder=flatbuffers.Builder(0);builder.Finish(model.Pack(builder),file_identifier=b'TFL3')
    return bytes(builder.Output())

def associated(data):
    if not zipfile.is_zipfile(io.BytesIO(data)):return {}
    with zipfile.ZipFile(io.BytesIO(data)) as z:return {n:z.read(n) for n in z.namelist()}

def mutate_label(data,name):
    entries=associated(data)
    lines=entries[name].decode('utf-8').splitlines()
    assert len(lines)>=2
    entries[name]=('\n'.join(lines[:-1])+'\n').encode()
    with zipfile.ZipFile(io.BytesIO(data)) as z:start=min(x.header_offset for x in z.infolist())
    out=io.BytesIO(data[:start])
    with zipfile.ZipFile(out,'a',compression=zipfile.ZIP_STORED) as z:
        for filename,content in entries.items():
            info=zipfile.ZipInfo(filename,date_time=(1980,1,1,0,0,0))
            info.compress_type=zipfile.ZIP_STORED
            z.writestr(info,content)
    return out.getvalue()

def generate(path,folder):
    status=folder/'codegen-status.json'
    status.unlink(missing_ok=True)
    p=subprocess.run([sys.executable,str(ROOT/'scripts/codegen_one.py'),str(path),str(folder/'generated'),str(status)],capture_output=True,text=True,timeout=60)
    (folder/'codegen.log').write_text(p.stdout+p.stderr)
    result={'exit_code':p.returncode,'success':False}
    if status.exists():result.update(json.loads(status.read_text()))
    result['files']=[str(Path(f).relative_to(ROOT)) for f in result.get('files',[])]
    src=next((ROOT/f for f in result['files'] if f.endswith('.java')),None)
    result['field_output_indices']={};result['category_outputs']=[]
    if src:
        text=src.read_text()
        mapping={name:int(index) for name,index in re.findall(r'Tensor (\w+)Tensor = model.getOutputTensor\((\d+)\)',text)}
        result['field_output_indices']=mapping
        result['source_sha256']=sha(text.encode())
        for field in re.findall(r'new TensorLabel\((\w+)Labels, postprocess\w+\(\w+\)\)\.getCategoryList\(\)',text):
            result['category_outputs'].append({'field':field,'output_position':mapping[field]})
    return result

def decoder_predictions(data,info,generation):
    rows=[];attachments=associated(data)
    output_md=info.get('metadata',{}).get('subgraph_metadata',[{}])[0].get('output_tensor_metadata',[])
    for category in generation['category_outputs']:
        i=category['output_position'];shape=info['output_tensors'][i]['shape']
        files=[x for x in output_md[i].get('associated_files',[]) if x.get('type')=='TENSOR_AXIS_LABELS']
        if not files:
            rows.append(dict(category,status='ABSTAIN',reason='No TENSOR_AXIS_LABELS association'));continue
        name=files[0]['name']
        if name not in attachments:
            rows.append(dict(category,status='ABSTAIN',reason='Associated label bytes absent'));continue
        # Match FileUtil.loadLabels: ignore lines empty after Java String.trim().
        labels=[line for line in attachments[name].decode('utf-8').splitlines()
                if line.strip(''.join(chr(i) for i in range(33)))]
        axis=next((j for j,n in enumerate(shape) if n>1),None)
        if axis is None:status='FAIL';reason='NO_NONUNIT_AXIS'
        elif shape[axis]!=len(labels):status='FAIL';reason='LABEL_CARDINALITY'
        elif axis!=len(shape)-1:status='FAIL';reason='CATEGORY_AXIS_NOT_LAST'
        else:status='PASS';reason='DECODER_PRECONDITIONS_SATISFIED'
        rows.append(dict(category,status=status,reason=reason,shape=shape,label_file=name,label_count=len(labels),first_nonunit_axis=axis))
    return rows

def main():
    report=[]
    components=json.loads((ROOT/'results/inspection.json').read_text())
    for component in components:
        raw=(ROOT/component['path']).read_bytes();cid=component['sha256'][:12]
        record={k:v for k,v in component.items() if k!='inspection'}
        record['id']=cid;record['canonical_sha256']=sha(canonical(raw));record['variants']=[]
        idx,md=md_bytes(raw)
        if md is None:
            record['status']='ABSTAIN_NO_METADATA';report.append(record)
            (ROOT/'results/static-suite.json').write_text(json.dumps(report,indent=2));continue
        s=ms.ModelMetadata.GetRootAsModelMetadata(md,0).SubgraphMetadata(0)
        n=s.OutputTensorMetadataLength()
        if not n:
            record['status']='ABSTAIN_NO_OUTPUT_METADATA';report.append(record);continue
        start=raw.find(md);assert start>=0 and raw.count(md)==1
        vector=s._tab.Vector(s._tab.Offset(10));variants=[('original',raw,{'kind':'natural'})]
        # Choose an existing description. Changing ASCII letter case preserves length.
        mdjson=component['inspection']['metadata'];description=None
        for entry in mdjson.get('subgraph_metadata',[{}])[0].get('output_tensor_metadata',[])+[mdjson]:
            desc=entry.get('description','')
            if desc and any(c.isascii() and c.isalpha() for c in desc):description=desc;break
        if description:
            b=description.encode();where=raw.find(b,start,start+len(md));assert where>=start
            delta=next(i for i,v in enumerate(b) if 65<=v<=90 or 97<=v<=122)
            changed=bytearray(raw);changed[where+delta]^=32
            variants.append(('description_control',bytes(changed),{'kind':'negative_control'}))
        changed=bytearray(raw);struct.pack_into('<I',changed,start+vector-4,n-1)
        variants.append(('count_minus_one',bytes(changed),{'kind':'structural_positive_control','old_count':n,'new_count':n-1}))
        shapes=[t['shape'] for t in component['inspection']['output_tensors']]
        pairs=[(i,j) for i,j in itertools.combinations(range(n),2) if shapes[i]!=shapes[j]]
        if pairs:
            i,j=pairs[0];changed=bytearray(raw)
            for dest,src in [(i,j),(j,i)]:
                pos=vector+dest*4;struct.pack_into('<I',changed,start+pos,s.OutputTensorMetadata(src)._tab.Pos-pos)
            variants.append(('swap_first_different_shape',bytes(changed),{'kind':'seeded_association_exchange','indices':[i,j]}))
        category_label_files=[]
        for name,data,intervention in variants:
            folder=ROOT/'runs'/cid/name;folder.mkdir(parents=True,exist_ok=True)
            path=folder/'model.tflite';path.write_bytes(data)
            model=parse(data);base=parse(raw)
            changed_buffers=[i for i in range(model.BuffersLength()) if not np.array_equal(model.Buffers(i).DataAsNumpy(),base.Buffers(i).DataAsNumpy())]
            assert all(i==idx for i in changed_buffers)
            assert canonical(data)==canonical(raw)
            if intervention['kind']!='associated_label_mutation':
                assert len(data)==len(raw)
                assert all(start<=i<start+len(md) for i,(a,b) in enumerate(zip(raw,data)) if a!=b)
                assert associated(data)==associated(raw)
            row={'variant':name,'path':str(path.relative_to(ROOT)),'sha256':sha(data),'intervention':intervention,'changed_buffers':changed_buffers,
                'non_metadata_buffers_equal':True,'canonical_sha256':sha(canonical(data))}
            try:
                pop=metadata.MetadataPopulator.with_model_buffer(data);pop.load_metadata_buffer(md_bytes(data)[1]);pop.populate()
                row['structural_validation']={'accepted':True}
            except Exception as exc:row['structural_validation']={'accepted':False,'error':repr(exc)}
            info=inspect(data);row['inspection']=info
            if row['structural_validation']['accepted']:
                row['generation']=generate(path,folder)
                row['decoder_checks']=decoder_predictions(data,info,row['generation'])
            else:
                row['generation']={'success':False,'skipped':'structural rejection'};row['decoder_checks']=[]
            if name=='original':
                for check in row['decoder_checks']:
                    label=check.get('label_file')
                    if check.get('label_count',0)>=2 and label not in category_label_files:
                        category_label_files.append(label)
                        variants.append(('label_drop_'+str(len(category_label_files)),mutate_label(raw,label),{'kind':'associated_label_mutation','label_file':label}))
            record['variants'].append(row)
            print(cid,name,'structural',row['structural_validation']['accepted'],'generator',row['generation'].get('success'),[(x['field'],x['status'],x.get('reason')) for x in row['decoder_checks']],flush=True)
        record['status']='INSPECTED';report.append(record)
        (ROOT/'results/static-suite.json').write_text(json.dumps(report,indent=2))

if __name__=='__main__':main()
