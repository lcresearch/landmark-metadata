import concurrent.futures, hashlib, io, json, pathlib, sys, urllib.error, urllib.request, zipfile
import numpy as np
from common import ROOT, HAND, JDK, PYTHON, sha, save, run
BASE=ROOT/'E4';PROTOCOL=BASE/'protocol';sys.dont_write_bytecode=True;sys.path.insert(0,str(PROTOCOL/'scripts'))
from suite_static import canonical, parse
from inspect_suite import inspect

def download(candidate):
    row=dict(candidate);dest=BASE/'downloads'/candidate['id'];dest.mkdir(parents=True,exist_ok=False)
    for attempt in range(2):
        try:
            with urllib.request.urlopen(candidate['url'],timeout=90) as response:
                data=response.read(128*1024*1024+1);row['http_status']=response.status;row['response_headers']=dict(response.headers)
            if len(data)>128*1024*1024:raise ValueError('Predeclared 128 MiB size limit exceeded')
            file=dest/candidate['url'].rsplit('/',1)[1];file.write_bytes(data)
            row.update(status='DOWNLOADED',bytes=len(data),sha256=sha(data),path=str(file.relative_to(ROOT)),attempts=attempt+1)
            break
        except Exception as exc:
            row.update(status='UNAVAILABLE' if isinstance(exc,urllib.error.HTTPError) else 'DOWNLOAD_ERROR',error=repr(exc),attempts=attempt+1)
            if isinstance(exc,urllib.error.HTTPError):row['http_status']=exc.code
            retry=(not isinstance(exc,urllib.error.HTTPError) or exc.code>=500) and not isinstance(exc,ValueError)
            if not retry or attempt==1:break
    save(dest/'record.json',row);return row

def members(data,name):
    if name.endswith('.tflite'):yield name,data;return
    if not zipfile.is_zipfile(io.BytesIO(data)):raise ValueError('Expected readable task ZIP')
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        for entry in sorted(z.infolist(),key=lambda e:e.filename):
            if '..' in pathlib.PurePosixPath(entry.filename).parts or entry.filename.startswith('/'):raise ValueError('Unsafe archive member')
            if entry.filename.endswith(('.tflite','.task')):
                if entry.file_size>128*1024*1024:raise ValueError('Member exceeds size limit')
                for child,payload in members(z.read(entry),entry.filename):yield name+'!'+child,payload

def graph_details(raw):
    m=parse(raw);g=m.Subgraphs(0);result={}
    for direction,count,at in [('inputs',g.InputsLength,g.Inputs),('outputs',g.OutputsLength,g.Outputs)]:
        tensors=[]
        for i in range(count()):
            t=g.Tensors(at(i));signature=t.ShapeSignatureAsNumpy()
            tensors.append({'index':int(at(i)),'shape':t.ShapeAsNumpy().tolist(),'shape_signature':signature.tolist() if isinstance(signature,np.ndarray) else [],'type':int(t.Type())})
        result[direction]=tensors
    return result

def main():
    freeze=json.loads((BASE/'prevalidation-freeze.json').read_text());assert freeze['external_downloads_started'] is False
    frozen=json.loads((PROTOCOL/'FROZEN_FILES.json').read_text())
    assert all(sha((PROTOCOL/f).read_bytes())==h for f,h in frozen.items())
    candidates=json.loads((PROTOCOL/'candidates.json').read_text());prior=json.loads((PROTOCOL/'prior-exclusions.json').read_text())
    prior_hashes={r['component_sha256'] for r in prior};prior_graphs={r['canonical_graph_sha256'] for r in prior}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:downloads=list(pool.map(download,candidates))
    save(BASE/'downloads.json',downloads)
    seen_bytes={};seen_graphs={};records=[]
    for candidate in downloads:
        print(candidate['id'],candidate['status'],flush=True)
        if candidate['status']!='DOWNLOADED':continue
        raw=(ROOT/candidate['path']).read_bytes()
        try:components=list(members(raw,pathlib.Path(candidate['path']).name))
        except Exception as exc:
            records.append({'candidate':candidate['id'],'status':'ARCHIVE_ERROR','error':repr(exc)});continue
        for member,data in components:
            digest=sha(data);row={'experiment_id':'E4','candidate':candidate['id'],'source_bundle':candidate['url'],'member':member,'component_sha256':digest,'variant':'unmodified_published_bytes','consumer':'frozen Support 0.4.4 generator / TensorLabel default path','status':'PENDING'}
            folder=BASE/'components'/digest;folder.mkdir(parents=True,exist_ok=True);model=folder/'model.tflite'
            if not model.exists():model.write_bytes(data)
            row['artifact_paths']={'model':str(model.relative_to(ROOT))}
            try:
                row['canonical_graph_sha256']=sha(canonical(data));graph=row['canonical_graph_sha256'];row['tensors']=graph_details(data)
                if digest in prior_hashes:row['status']='EXCLUDED_PRIOR_COMPONENT'
                elif graph in prior_graphs:row['status']='EXCLUDED_PRIOR_GRAPH'
                elif digest in seen_bytes:row.update(status='EXCLUDED_DUPLICATE_COMPONENT',first_occurrence=seen_bytes[digest])
                elif graph in seen_graphs:row.update(status='EXCLUDED_DUPLICATE_GRAPH',first_occurrence=seen_graphs[graph])
                else:
                    seen_bytes[digest]=candidate['id']+'!'+member;seen_graphs[graph]=candidate['id']+'!'+member
                    p=run([PYTHON,PROTOCOL/'scripts/check_model.py',model],folder/'logs/checker',timeout=90)
                    row['checker_exit_code']=p.returncode
                    try:check=json.loads(p.stdout);row['checker']=check
                    except Exception as exc:row.update(status='CHECKER_ERROR',parse_error=repr(exc));check={}
                    if check:
                        if check.get('status')=='ABSTAIN_NO_METADATA':row.update(status='ABSTAIN_NO_METADATA',structural_status='NOT_APPLICABLE',semantic_check='ABSTAIN_NO_REFERENCE',decoder_check='ABSTAIN_NO_METADATA')
                        else:
                            row['structural_status']=check.get('structural_check','UNKNOWN');row['semantic_check']=check.get('index_check','ABSTAIN_NO_REFERENCE')
                            generation=check.get('generation',{});row['generation_status']='PASS' if generation.get('success') else 'FAIL_OR_NOT_REACHED'
                            dynamic=any(any(d<=0 for d in t['shape']+t['shape_signature']) for t in row['tensors']['outputs'])
                            row['decoder_check']='ABSTAIN_DYNAMIC_OUTPUT' if dynamic else check.get('decoder_checks',check.get('decoder_check','INAPPLICABLE_NO_GENERATED_CATEGORY_PATH'))
                            if row['decoder_check']==[]:row['decoder_check']='INAPPLICABLE_NO_GENERATED_CATEGORY_PATH'
                            row['status']='CHECKED' if p.returncode==0 else 'CHECKER_ERROR'
                            sources=[PROTOCOL/f for f in generation.get('files',[]) if f.endswith('.java')]
                            if sources:
                                row['artifact_paths']['generated_sources']=[str(s.relative_to(ROOT)) for s in sources]
                                q=run([JDK/'bin/javac','--release','8','-cp',str(HAND/'deps/*'),'-d',folder/'classes',*sources],folder/'logs/javac',timeout=90)
                                row['compile_status']='PASS' if q.returncode==0 else 'FAIL';row['compile_exit_code']=q.returncode
                                row['generated_class_hashes']={str(f.relative_to(folder)):sha(f.read_bytes()) for f in (folder/'classes').rglob('*.class')}
                            else:row['compile_status']='NOT_REACHED'
            except Exception as exc:row.update(status='INSPECTION_OR_CONTROLLER_ERROR',error=repr(exc))
            records.append(row);save(BASE/'results.json',{'protocol_commit':freeze['git_commit'],'downloads':downloads,'component_occurrences':records})
            print(candidate['id'],member,row['status'],row.get('compile_status',''),row.get('decoder_check',''),flush=True)
    assert all(sha((PROTOCOL/f).read_bytes())==h for f,h in frozen.items())
    save(BASE/'results.json',{'protocol_commit':freeze['git_commit'],'downloads':downloads,'component_occurrences':records,'frozen_rule_files_unchanged':True})
if __name__=='__main__':main()
