#!/usr/bin/env python3
"""Fresh HA07 saved-byte pre-audit. No network/inference/input writes.
Independent comparisons; the historical analysis script is not imported.
Run with -B and PYTHONDONTWRITEBYTECODE=1 to protect input schema directory.
"""
import ast, collections, hashlib, io, json, pathlib, re, sys
import flatbuffers
import numpy as np

OUT = pathlib.Path(__file__).resolve().parent
BASE = pathlib.Path('/workspace/evidence-recovery-20261005T170453Z/package-v2/payload')
P3 = BASE / 'metadata-contract-p2p3-20261004T073824Z/P3'
E = BASE / 'metadata-contract-e2e-20261004T030536Z'
REPO = pathlib.Path('/workspace/landmark-agent-preaudit')
sys.dont_write_bytecode = True
sys.path.insert(0, str(BASE / 'SUPPLEMENTARY_SOURCE'))
import schema_py_generated as schema
import zipfile

inputs = {}
def sha(b): return hashlib.sha256(b).hexdigest()
def read(p):
    p = pathlib.Path(p); b = p.read_bytes()
    inputs[str(p)] = {'sha256': sha(b), 'bytes': len(b)}
    return b
def obj(p): return json.loads(read(p))
def body(k): return read(P3 / 'retrieved' / k / 'body')
def save(name, x): (OUT / name).write_text(json.dumps(x, indent=2) + '\n')
def norm(x):
    # Preserve numeric array representation; do not drop any schema object field.
    if isinstance(x, np.ndarray):
        return {'dtype': str(x.dtype), 'shape': list(x.shape), 'bytes_hex': x.tobytes().hex()}
    if isinstance(x, np.generic): return norm(x.item())
    if isinstance(x, bytes): return {'bytes_hex': x.hex()}
    if isinstance(x, float): return {'float_hex': x.hex()}
    if isinstance(x, (list, tuple)): return [norm(v) for v in x]
    if isinstance(x, dict): return {k:norm(v) for k,v in sorted(x.items())}
    if hasattr(x, '__dict__'): return {'schema_class': type(x).__name__, 'fields': norm(vars(x))}
    return x
def digest(x): return sha(json.dumps(x, sort_keys=True, separators=(',', ':')).encode())
def parse(p):
    b = read(p)
    if b[4:8] != b'TFL3': raise ValueError('not a TFL3 model')
    m = schema.ModelT.InitFromObj(schema.Model.GetRootAsModel(b, 0))
    meta = [x for x in m.metadata or [] if x.name == b'TFLITE_METADATA']
    if len(meta) != 1: raise ValueError('expected exactly one metadata entry')
    mi = meta[0].buffer
    refs = sorted({int(t.buffer) for sg in m.subgraphs for t in sg.tensors})
    if mi in refs: raise ValueError('metadata buffer is graph-referenced')
    desc = norm({k:v for k,v in vars(m).items() if k not in ('buffers', 'metadata')})
    buffers = [b'' if x.data is None else bytes(x.data) for x in m.buffers]
    other = norm([x for x in m.metadata or [] if x.name != b'TFLITE_METADATA'])
    outputs = [{'subgraph': i, 'ordered_output_indices': norm(sg.outputs),
                'ordered_output_tensors': [norm(sg.tensors[int(t)]) for t in sg.outputs]}
               for i,sg in enumerate(m.subgraphs)]
    return {'bytes': b, 'model':m, 'metadata_index':mi, 'refs':refs, 'desc':desc,
            'buffers':buffers, 'other_metadata':other, 'outputs':outputs}

schema_identity = read(BASE / 'SUPPLEMENTARY_SOURCE/schema_py_generated.py')
models = {
    'focal_original': E / 'E1/variants/original/model.tflite',
    'publisher_version1': P3 / 'retrieved/I01-publisher-model/body',
    'publisher_latest': P3 / 'retrieved/F02-publisher-latest-model/body',
    'tfhub_fp32_2': P3 / 'retrieved/I06-tfhub-lite-model/body',
    'permutation': E / 'E2/variants/label_permutation/model.tflite',
    'restoration': E / 'E2/variants/permutation_restoration/model.tflite',
}
parsed = {k:parse(p) for k,p in models.items()}
a = parsed['focal_original']
bridge = {}
for k,b in parsed.items():
    rows = [{'index':i, 'focal_bytes':len(x), 'other_bytes':len(y),
             'focal_sha256':sha(x), 'other_sha256':sha(y), 'byte_equal':x==y,
             'metadata_buffer':i==a['metadata_index']}
            for i,(x,y) in enumerate(zip(a['buffers'],b['buffers']))]
    bridge[k] = {
        'sha256':sha(b['bytes']), 'package_bytes_equal':a['bytes']==b['bytes'],
        'buffer_count':len(b['buffers']), 'metadata_index':b['metadata_index'],
        'complete_nonbuffer_nonmetadata_fields_equal': a['desc']==b['desc'],
        'fields_compared':sorted(a['desc']), 'fresh_descriptor_sha256':digest(b['desc']),
        'other_metadata_equal':a['other_metadata']==b['other_metadata'],
        'ordered_outputs_equal':a['outputs']==b['outputs'],
        'metadata_not_tensor_referenced':b['metadata_index'] not in b['refs'],
        'tensor_buffer_references':b['refs'],
        'equal_nonmetadata_buffers':sum(r['byte_equal'] and not r['metadata_buffer'] for r in rows),
        'different_buffer_indices':[r['index'] for r in rows if not r['byte_equal']],
        'buffers':rows,
    }
save('fresh-model-bridge.json', bridge)
save('fresh-computation-descriptor.json', a['desc'])
save('fresh-ordered-outputs.json', a['outputs'])

# Parse actual ZIP member bytes; no stored comparison table supplies the oracle.
def labels(b):
    with zipfile.ZipFile(io.BytesIO(b)) as z:
        if z.namelist() != ['labels_without_background.txt']: raise ValueError(z.namelist())
        raw = z.read(z.namelist()[0])
    text = raw.decode('utf-8', errors='strict')
    # All inspected resources use plain LF. This does not assume Python splitlines
    # implements Java parsing for arbitrary resources.
    if '\r' in text or any(ord(c)<32 and c!='\n' for c in text): raise ValueError('unexpected controls')
    lines = text.split('\n')
    if lines[-1] == '': lines.pop()
    return raw, lines
ref_raw=body('F11-explicit-class-order')
ref_all=ref_raw.decode('utf-8').split('\n')
if ref_all[-1]=='': ref_all.pop()
if len(ref_all)!=1001 or ref_all[0]!='background': raise ValueError('reference background/count')
ref=ref_all[1:]
resources={k:labels(v['bytes']) for k,v in parsed.items()}
label_rows=[{'output_position':i, 'external_line_1based':i+2, 'reference':ref[i],
             **{k:v[1][i] for k,v in resources.items()}} for i in range(1000)]
label_summary={k:{'count':len(v[1]),'resource_sha256':sha(v[0]),
                  'matches':sum(x==y for x,y in zip(v[1],ref)),
                  'mismatch_positions':[i for i,(x,y) in enumerate(zip(v[1],ref)) if x!=y]}
               for k,v in resources.items()}
dups={s:[i for i,x in enumerate(ref) if x==s] for s,n in collections.Counter(ref).items() if n>1}
label_summary['details']={'reference_total_lines':len(ref_all),'background_removed':ref_all[0],
                          'duplicate_display_names':dups,
                          'permutation_is_exact_left_rotation':resources['permutation'][1]==ref[1:]+ref[:1],
                          'permutation_unchanged_positions':[i for i,x in enumerate(resources['permutation'][1]) if x==ref[i]],
                          'witness_904':label_rows[904]}
save('fresh-label-rows.json',label_rows); save('fresh-label-summary.json',label_summary)

# Reconstruct every Git tree from the saved complete recursive tree response.
tree=obj(P3/'retrieved/F05-source-tree/body')
commit=obj(P3/'retrieved/F03-tfhub-repo-head/body')[0]
if tree['truncated']: raise ValueError('truncated catalog tree')
entries={x['path']:x for x in tree['tree']}
children=collections.defaultdict(list)
for path,x in entries.items():
    parent,_,name=path.rpartition('/')
    children[parent].append((name,x))
def git_hash(kind,b): return hashlib.sha1(kind.encode()+b' '+str(len(b)).encode()+b'\0'+b).hexdigest()
tree_checks=[]
for parent,items in children.items():
    items.sort(key=lambda item:(item[0]+('/' if item[1]['type']=='tree' else '')).encode())
    blob=b''.join((x['mode'].lstrip('0')+' '+name).encode()+b'\0'+bytes.fromhex(x['sha']) for name,x in items)
    expected=commit['commit']['tree']['sha'] if parent=='' else entries[parent]['sha']
    actual=git_hash('tree',blob)
    tree_checks.append({'path':parent,'expected':expected,'recomputed':actual,'equal':expected==actual})
pin=commit['sha']
card_paths={'F07-pinned-lite-card':'assets/docs/tensorflow/models/efficientnet/lite0/fp32/lite/2.md',
            'F10-pinned-parent-card':'assets/docs/tensorflow/models/efficientnet/lite0/classification/1.md'}
card_checks={}
for key,path in card_paths.items():
    b=body(key); record=obj(P3/'retrieved'/key/'retrieval.json')
    card_checks[key]={'path':path,'blob_id':git_hash('blob',b), 'tree_blob_id':entries[path]['sha'],
                     'blob_matches_tree':git_hash('blob',b)==entries[path]['sha'],
                     'url_is_exact_pinned_path':record['url']==f'https://raw.githubusercontent.com/tensorflow/tfhub.dev/{pin}/{path}'}
verification=commit['commit']['verification']
headers,message=verification['payload'].split('\n\n',1)
sig=verification['signature'].replace('\n','\n ')
commit_bytes=(headers+'\ngpgsig '+sig+'\n\n'+message).encode()
authority={'catalog_commit':pin,'commit_date':commit['commit']['committer']['date'],
           'reconstructed_commit_sha1':git_hash('commit',commit_bytes),
           'reconstructed_commit_matches':git_hash('commit',commit_bytes)==pin,
           'signature_cryptographically_verified_this_audit':False,
           'recorded_github_verification':verification['verified'],
           'tree_response_header_sha':tree['sha'],'commit_root_tree_sha':commit['commit']['tree']['sha'],
           'tree_checks':tree_checks,'all_trees_match':all(x['equal'] for x in tree_checks),
           'cards':card_checks}
lite=body('F07-pinned-lite-card').decode(); parent=body('F10-pinned-parent-card').decode()
authority['explicit_links']={
    'lite_identifies_fp32_2':lite.startswith('# Lite tensorflow/efficientnet/lite0/fp32/2'),
    'lite_identifies_classification_1_parent':'<!-- parent-model: tensorflow/efficientnet/lite0/classification/1 -->' in lite,
    'parent_identifies_classification_1':parent.startswith('# Module tensorflow/efficientnet/lite0/classification/1'),
    'parent_links_exact_external_reference':'https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt' in parent,
    'parent_prescribes_background_omission':'please ignore the first background class, ie. index 0 corresponds to\n"tench"' in parent,
    'parent_specifies_1000_classes':'`num_classes` = 1000' in parent}
publisher_doc=body('I02-publisher-doc').decode()
authority['explicit_links']['publisher_doc_links_exact_latest_model']='https://storage.googleapis.com/mediapipe-models/image_classifier/efficientnet_lite0/float32/latest/efficientnet_lite0.tflite' in publisher_doc
authority['explicit_links']['publisher_doc_links_F01_labels']='https://storage.googleapis.com/mediapipe-tasks/image_classifier/labels.txt' in publisher_doc
authority['publisher_labels_equal_prescribed_reference']=body('F01-publisher-labels')==ref_raw
tfhub_record=obj(P3/'retrieved/I06-tfhub-lite-model/retrieval.json')
authority['tfhub_redirects']=[{'from_host':r['from'].split('/')[2], 'status':r['status'],
                             'to_host':r['to'].split('/')[2]} for r in tfhub_record['redirects']]
authority['tfhub_storage_remoteurl']=tfhub_record['headers']['x-goog-meta-kaggle-remoteurl']
authority['tfhub_storage_generation']=tfhub_record['headers']['x-goog-generation']
retrieval_checks=[]
for record_path in sorted((P3/'retrieved').glob('*/retrieval.json')):
    r=obj(record_path); b=read(record_path.parent/'body')
    retrieval_checks.append({'id':r['id'],'status':r.get('status'),'url':r['url'],
                             'started_utc':r.get('started_utc'),'body_sha256':sha(b),
                             'recorded_sha256':r.get('sha256'),'hash_equal':sha(b)==r.get('sha256'),
                             'size_equal':len(b)==r.get('bytes'),
                             'storage_generation':r.get('headers',{}).get('x-goog-generation')})
authority['retrieval_checks']=retrieval_checks
save('fresh-source-authority.json',authority)

# Ancillary candidate ID correspondence does not establish artifact training lineage.
synsets=body('F17-synset-order').decode().splitlines()
names=dict(line.split('\t',1) for line in body('F18-synset-names').decode().splitlines())
checkpoint=ast.literal_eval(body('F15-tpu-labelmap').decode())
candidate={'synset_count':len(synsets),'unique_synsets':len(set(synsets)),
           'checkpoint_name_matches':sum(names[s]==checkpoint[i] for i,s in enumerate(synsets)),
           'first_synonym_display_matches':sum(names[s].split(',')[0]==ref[i] for i,s in enumerate(synsets)),
           'stable_class_id_authority':'ABSTAIN; name agreement does not bind exact artifact training lineage'}
save('fresh-candidate-id-summary.json',candidate)

# Stored rows are compared only after fresh derivation above.
old_rows=obj(P3/'analysis/full-display-order-comparison.json')
stored_rows_equal=len(old_rows)==len(label_rows) and all(
    x['output_position']==y['output_position'] and x['external_file_line_1based']==y['external_line_1based']
    and x['reference_display_label']==y['reference'] and x['original_display_label']==y['focal_original']
    and x['permutation_display_label']==y['permutation'] and x['restored_display_label']==y['restoration']
    for x,y in zip(old_rows,label_rows))
old_bridge=obj(P3/'analysis/artifact-bridge.json')
comparison={'all_1000_stored_rows_match_fresh':stored_rows_equal,
            'bridge_recorded_equal_nonmetadata':old_bridge['equal_nonmetadata_buffers'],
            'bridge_fresh_equal_nonmetadata':bridge['tfhub_fp32_2']['equal_nonmetadata_buffers'],
            'recorded_canonical_sha256':old_bridge['canonical_graph_sha256'],
            'fresh_descriptor_sha256':bridge['tfhub_fp32_2']['fresh_descriptor_sha256'],
            'normalization_note':'Fresh descriptor serializes every known schema field, preserving numeric array bytes. It is not the historical FlatBuffer repack; cross-algorithm digest equality is not expected.'}
save('new-vs-recorded.json',comparison)
for relative in ['AGENTS.md','MEMORY.md','TODO.md','docs/DECISIONS.md','docs/human-audit/CHECKLIST.md',
                 'work/agent-preaudit-20261007/PROTOCOL.md','work/workshop-convergence-20261007/manuscript/paper.tex',
                 'work/workshop-convergence-20261007/CLAIM_EVIDENCE.md']:
    read(REPO/relative)
auditroot=P3.parent/'review/reference-audit'
for p in sorted((auditroot/'attempt-1-header-assumption').iterdir()):
    if p.is_file(): read(p)
read(P3/'analysis/reference-chain.json');read(P3/'analysis/candidate-synset-comparison.json')
original_copies=[]
for path,identity in list(inputs.items()):
    p=pathlib.Path(path)
    if not p.is_relative_to(BASE): continue
    rel=p.relative_to(BASE)
    if rel.parts[0]=='SUPPLEMENTARY_SOURCE': continue
    source=pathlib.Path('/workspace')/rel
    if source.exists():
        b=read(source)
        original_copies.append({'package_path':path,'original_path':str(source),
                                'sha256':sha(b),'matches_package':sha(b)==identity['sha256']})
    else:
        original_copies.append({'package_path':path,'original_path':str(source),'missing':True})
save('package-vs-originals.json',original_copies)
save('input-identities.json',inputs)
summary={'scope':'HA07/C5 agent pre-audit; saved-byte/static recomputation only',
         'human_status':'PENDING','new_inference':False,
         'versions':{'python':sys.version,'flatbuffers':flatbuffers.__version__,'numpy':np.__version__},
         'model_artifacts':len(models),'independent_computational_graphs':1,'evaluated_display_positions':1000,
         'equal_nonmetadata_buffers':bridge['tfhub_fp32_2']['equal_nonmetadata_buffers'],
         'all_computation_fields_equal':all(x['complete_nonbuffer_nonmetadata_fields_equal'] for x in bridge.values()),
         'ordered_outputs_equal':all(x['ordered_outputs_equal'] for x in bridge.values()),
         'original_matches':label_summary['focal_original']['matches'],
         'permutation_disagreements':len(label_summary['permutation']['mismatch_positions']),
         'restoration_matches':label_summary['restoration']['matches'],
         'all_retrieval_hashes_match':all(x['hash_equal'] and x['size_equal'] for x in retrieval_checks),
         'tree_count':len(tree_checks),'all_tree_objects_match':authority['all_trees_match'],
         'commit_reconstructed':authority['reconstructed_commit_matches'],
         'all_card_blob_ids_match':all(x['blob_matches_tree'] for x in card_checks.values()),
         'all_explicit_authority_links_present':all(authority['explicit_links'].values()),
         'stored_rows_match_fresh':stored_rows_equal,'candidate_ids':candidate}
required = {
    'all_computation_fields_equal':summary['all_computation_fields_equal'],
    'ordered_outputs_equal':summary['ordered_outputs_equal'],
    'six_models_166_buffers_metadata_165':all(v['buffer_count']==166 and v['metadata_index']==165 for v in bridge.values()),
    'six_models_165_nonmetadata_equal':all(v['equal_nonmetadata_buffers']==165 for v in bridge.values()),
    'all_six_resource_counts_1000':all(label_summary[k]['count']==1000 for k in models),
    'original_and_restoration_1000_permutation_999':summary['original_matches']==summary['restoration_matches']==1000 and summary['permutation_disagreements']==999,
    'retrieval_hashes_and_sizes':summary['all_retrieval_hashes_match'],
    'trees_and_commit':summary['all_tree_objects_match'] and summary['commit_reconstructed'],
    'pinned_card_blobs_and_links':summary['all_card_blob_ids_match'] and summary['all_explicit_authority_links_present'],
    'all_1000_recorded_rows':summary['stored_rows_match_fresh'],
    'all_72_selected_original_copies_match':len(original_copies)==72 and all(x.get('matches_package',False) for x in original_copies),
}
summary['required_computed_checks']=required
summary['agent_verdict']='SUPPORTED_WITHIN_INSPECTED_SCOPE' if all(required.values()) else 'DISCREPANCY_FOUND'
save('computation-summary.json',summary)
print(json.dumps(summary,indent=2))
if not all(required.values()): raise SystemExit('One or more HA07 computations disagreed; inspect summary')
