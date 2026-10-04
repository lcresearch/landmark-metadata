#!/usr/bin/env python3
"""Independently inspect saved P3 bytes; no network, inference, or P3 writes."""
import base64
import collections
import hashlib
import io
import json
from pathlib import Path
import re
import sys
import zipfile
import numpy as np
from tensorflow_lite_support.metadata import schema_py_generated as schema

BASE = Path('/workspace/metadata-contract-p2p3-20261004T073824Z')
P3 = BASE / 'P3'
OUT = BASE / 'review/reference-audit'
FOCAL = Path('/workspace/metadata-contract-e2e-20261004T030536Z/E1/variants/original/model.tflite')
PERM = Path('/workspace/metadata-contract-e2e-20261004T030536Z/E2/variants/label_permutation/model.tflite')
RESTORE = Path('/workspace/metadata-contract-e2e-20261004T030536Z/E2/variants/permutation_restoration/model.tflite')
checks = []
inventory = {}

def sha(data): return hashlib.sha256(data).hexdigest()
def read(path):
    data = Path(path).read_bytes()
    inventory[str(path)] = {'bytes': len(data), 'sha256': sha(data)}
    return data
def check(name, value, **details):
    checks.append({'name': name, 'status': 'PASS' if value else 'FAIL', **details})
def normalize(obj):
    if isinstance(obj, bytes): return {'bytes': base64.b64encode(obj).decode()}
    if isinstance(obj, np.ndarray):
        return {'dtype':str(obj.dtype), 'shape':list(obj.shape), 'bytes':base64.b64encode(obj.tobytes()).decode()}
    if isinstance(obj, np.generic): return obj.item()
    if isinstance(obj, (tuple,list)): return [normalize(x) for x in obj]
    if isinstance(obj, dict): return {str(k):normalize(v) for k,v in sorted(obj.items())}
    if hasattr(obj,'__dict__'): return {'type':type(obj).__name__, 'fields':normalize(vars(obj))}
    return obj
def parsed(raw):
    m = schema.Model.GetRootAsModel(raw,0)
    obj = schema.ModelT.InitFromObj(m)
    ids = [i.buffer for i in obj.metadata if i.name == b'TFLITE_METADATA']
    assert len(ids)==1
    mid=ids[0]
    buffers=[b'' if b.data is None else b.data.tobytes() for b in obj.buffers]
    outputs=[]
    tensor_metadata_refs=[]
    for si,sg in enumerate(obj.subgraphs):
        outputs.append({'subgraph':si, 'output_tensor_indices':[int(i) for i in sg.outputs],
                        'output_tensor_fields':[normalize(sg.tensors[int(i)]) for i in sg.outputs]})
        tensor_metadata_refs += [(si,ti) for ti,t in enumerate(sg.tensors) if t.buffer==mid]
    obj.metadata=[i for i in obj.metadata if i.name!=b'TFLITE_METADATA']
    obj.buffers[mid].data=None
    computational=json.dumps(normalize(obj),sort_keys=True,separators=(',',':')).encode()
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        names=z.namelist()
        files={n:z.read(n) for n in names}
    return {'raw_sha256':sha(raw), 'metadata_index':mid, 'buffers':buffers,
            'metadata_sha256':sha(buffers[mid]), 'parsed_computation':computational,
            'parsed_computation_sha256':sha(computational), 'outputs':outputs,
            'tensor_metadata_refs':tensor_metadata_refs,'associated':files}

selected=['I01-publisher-model','I06-tfhub-lite-model','F03-tfhub-repo-head',
          'F05-source-tree','F07-pinned-lite-card','F10-pinned-parent-card',
          'F11-explicit-class-order','F01-publisher-labels']
retrievals={}
bodies={}
for name in selected:
    record=json.loads(read(P3/'retrieved'/name/'retrieval.json'))
    body=read(P3/'retrieved'/name/'body')
    check(name+': saved body matches retrieval hash/size/status',
          sha(body)==record['sha256'] and len(body)==record['bytes'] and record['status']==200)
    retrievals[name]={'url':record['url'],'final_url':record['final_url'],'status':record['status'],
      'bytes':len(body),'sha256':sha(body),'started_utc':record['started_utc'],
      'finished_utc':record['finished_utc'], 'object_generation':record.get('headers',{}).get('x-goog-generation')}
    bodies[name]=body

focal=read(FOCAL)
check('focal exact SHA-256',sha(focal)=='6c7ab0a6e5dcbf38a8c33b960996a55a3b4300b36a018c4545801de3a3c8bde0')
check('fresh publisher exact-version download equals focal',focal==bodies['I01-publisher-model'])
a=parsed(focal);b=parsed(bodies['I06-tfhub-lite-model'])
check('bridge is not whole-file identity',a['raw_sha256']!=b['raw_sha256'])
check('same buffer count and metadata buffer index',len(a['buffers'])==len(b['buffers']) and a['metadata_index']==b['metadata_index'])
changed=[i for i in range(len(a['buffers'])) if a['buffers'][i]!=b['buffers'][i]]
check('all non-metadata buffer bytes identical',changed==[a['metadata_index']],changed_indices=changed)
check('metadata buffer is not used as tensor data',not a['tensor_metadata_refs'] and not b['tensor_metadata_refs'])
check('all parsed schema computation and weight fields identical',a['parsed_computation']==b['parsed_computation'])
check('full output tensor order and fields identical',a['outputs']==b['outputs'])

commit=json.loads(bodies['F03-tfhub-repo-head'])[0]
tree=json.loads(bodies['F05-source-tree'])
# The saved commit-addressed GitTrees response reports the requested commit SHA
# in its header, not the root tree object's SHA. Verify the actual Git objects
# instead of accepting either identifier as a substitute for this proof.
directories={'':commit['commit']['tree']['sha']}
directories.update({e['path']:e['sha'] for e in tree['tree'] if e['type']=='tree'})
children={path:[] for path in directories}
for entry in tree['tree']:
    parent_path, _, basename=entry['path'].rpartition('/')
    children[parent_path].append({**entry,'basename':basename})
tree_objects=[]
for directory, expected_sha in sorted(directories.items()):
    entries=sorted(children[directory],key=lambda e:(e['basename']+('/' if e['type']=='tree' else '')).encode())
    payload=b''.join(e['mode'].lstrip('0').encode()+b' '+e['basename'].encode()+b'\0'+bytes.fromhex(e['sha']) for e in entries)
    actual_sha=hashlib.sha1(b'tree '+str(len(payload)).encode()+b'\0'+payload).hexdigest()
    tree_objects.append({'path':directory,'expected_git_tree_sha1':expected_sha,
                         'recomputed_git_tree_sha1':actual_sha,'equal':expected_sha==actual_sha,
                         'direct_entry_count':len(entries)})
check('reconstructed root Git tree belongs to resolved commit',tree_objects[0]['equal'] and not tree.get('truncated',False))
check('all saved recursive Git tree objects independently reconstruct',all(t['equal'] for t in tree_objects),
      directory_count=len(tree_objects),mismatches=[t for t in tree_objects if not t['equal']])
git_blobs=[]
for name in ['F07-pinned-lite-card','F10-pinned-parent-card']:
    record=retrievals[name]
    prefix='https://raw.githubusercontent.com/tensorflow/tfhub.dev/'+commit['sha']+'/'
    check(name+': retrieved by immutable resolved commit',record['url'].startswith(prefix))
    path=record['url'][len(prefix):]
    entries=[x for x in tree['tree'] if x['path']==path]
    blob=hashlib.sha1(b'blob '+str(len(bodies[name])).encode()+b'\0'+bodies[name]).hexdigest()
    check(name+': raw Markdown bytes match git-tree blob',len(entries)==1 and entries[0]['sha']==blob)
    git_blobs.append({'candidate':name,'path':path,'git_blob_sha1':blob})
lite=bodies['F07-pinned-lite-card'].decode()
parent=bodies['F10-pinned-parent-card'].decode()
check('exact lite fp32/2 identity in card',lite.startswith('# Lite tensorflow/efficientnet/lite0/fp32/2\n'))
check('explicit parent is classification/1',
      '<!-- parent-model: tensorflow/efficientnet/lite0/classification/1 -->' in lite)
check('exact parent card identifies classification/1',parent.startswith('# Module tensorflow/efficientnet/lite0/classification/1\n'))
check('parent independently declares 1000 classes', '`num_classes` = 1000' in parent)
check('parent independently links external label object',retrievals['F11-explicit-class-order']['url'] in parent)
check('background offset explicitly declared before comparison',
      'please ignore the first background class, ie. index 0 corresponds to\n"tench".' in parent)

all_lines=bodies['F11-explicit-class-order'].decode('utf-8').splitlines()
check('external list is 1001 entries with leading background',len(all_lines)==1001 and all_lines[0]=='background')
check('external standalone object also matches publisher-linked list',bodies['F11-explicit-class-order']==bodies['F01-publisher-labels'])
# The sole offset is declared by the parent card, not selected by agreement with focal.
reference=all_lines[1:]
focal_labels=a['associated']['labels_without_background.txt'].decode('utf-8').splitlines()
mutant=parsed(read(PERM))
mutant_labels=mutant['associated']['labels_without_background.txt'].decode('utf-8').splitlines()
restored=parsed(read(RESTORE))
restored_labels=restored['associated']['labels_without_background.txt'].decode('utf-8').splitlines()
check('focal list exactly matches all 1000 external positions',focal_labels==reference)
check('permutation graph/weights same as bridge',mutant['parsed_computation']==a['parsed_computation'])
check('mutant is predeclared full cyclic mapping',mutant_labels==focal_labels[1:]+focal_labels[:1])
mismatches=[i for i,(x,y) in enumerate(zip(mutant_labels,reference)) if x!=y]
check('exact 999 mutant display-order mismatches',len(mutant_labels)==1000 and mismatches==[i for i in range(1000) if i!=638])
check('restoration recovers all 1000 reference display positions',restored_labels==reference)
check('restoration preserves graph/weights and exact original label payload',
      restored['parsed_computation']==a['parsed_computation'] and restored['associated']==a['associated'])
duplicate_names={label:[i for i,x in enumerate(reference) if x==label]
                 for label,count in collections.Counter(reference).items() if count>1}
check('display labels are not unique stable class IDs',duplicate_names.get('maillot')==[638,639])
check('no synset ID is supplied by reference object',not any(re.fullmatch(r'n\d{8}',x) for x in reference))

chain_links=[
 {'link':'Focal -> exact publisher object','status':'PASS','basis':'Fresh retrieved version-1 model bytes equal exact focal SHA-256.'},
 {'link':'Publisher/versioned TFHub artifact provenance','status':'PASS','basis':'Saved successful official TFHub versioned request, publisher redirects and remote-url metadata; artifact bytes/hash and storage generation retained. This is publisher provenance, not a verified build attestation.'},
 {'link':'TFHub artifact -> focal computational identity','status':'PASS','basis':'All 165 non-metadata buffers, complete parsed computation fields, output tensor indices/order and tensor fields agree. Whole files and metadata differ.'},
 {'link':'Version-pinned Lite card -> exact parent card','status':'PASS','basis':'Immutable-commit raw Markdown matches resolved commit tree blob hashes; Lite fp32/2 explicitly declares classification/1.'},
 {'link':'Parent card -> external display mapping and offset','status':'PASS','basis':'Exact parent card states 1000 classes, points to separate external ImageNetLabels object, and explicitly says ignore leading background; no fitted offset.'},
 {'link':'External mapping -> full original/mutant display agreement','status':'PASS','basis':'All 1000 original positions match; cyclic permutation mismatches 999 positions, with duplicate maillot at 638/639.'},
 {'link':'Output index -> stable synset/class ID -> display name','status':'UNVERIFIABLE','basis':'The graph-linked mapping retrieved here contains display strings, not unique stable IDs; duplicate names prevent recovering a unique ID chain from those strings alone. Ancillary generic dataset resources need their own model-specific bridge.'},
 {'link':'Prediction correctness or task accuracy','status':'UNVERIFIABLE','basis':'Reference agreement is an output-association property. No independently ground-truthed image accuracy test is supplied.'},
 {'link':'Independent human audit','status':'UNVERIFIABLE','basis':'This is an AI-agent read-only evidence audit.'}
]
result={'scope':'AI independent re-computation from saved P3 bytes only; no network, inference, or source evidence mutation.',
 'status':'FAIL' if any(c['status']=='FAIL' for c in checks) else 'PASS_DISPLAY_REFERENCE_ONLY',
 'plan_question_outcome':'PARTIAL: graph-linked display-order reference supported; complete stable-ID semantics not established.',
 'checks':checks,'chain_links':chain_links,'retrievals':retrievals,'source_commit':commit['sha'], 'git_blobs':git_blobs,
 'git_tree_objects':tree_objects,'git_tree_response_header_sha':tree['sha'],
 'git_tree_commit_declared_root_sha':commit['commit']['tree']['sha'],
 'audit_deviation':'Initial strict tree-response-header comparison failed because saved commit-addressed response header echoes commit SHA. Initial script/results/stdout retained in attempt-1-header-assumption. Revised check reconstructs the root and every recursive Git tree object and verifies committed object hashes; evidence unchanged.',
 'focal_sha256':a['raw_sha256'],'tfhub_sha256':b['raw_sha256'],
 'computational_fingerprint_method':'Fresh deterministic parsed-schema serialization, metadata entry removed and metadata payload cleared; not the P3/study canonicalizer.',
 'computational_fingerprint_sha256':a['parsed_computation_sha256'],
 'buffers':[{'index':i,'focal_sha256':sha(x),'tfhub_sha256':sha(b['buffers'][i]),'equal':x==b['buffers'][i], 'bytes':len(x)} for i,x in enumerate(a['buffers'])],
 'outputs':a['outputs'], 'external_reference_lines':len(all_lines), 'offset_rule':'Drop exactly first line, as required by exact parent card.',
 'original_display_matches':sum(x==y for x,y in zip(focal_labels,reference)),
 'restored_display_matches':sum(x==y for x,y in zip(restored_labels,reference)),
 'mutant_display_mismatches':mismatches,'duplicate_names':duplicate_names,
 'full_display_mapping':[{'output_position':i,'external_reference_line_1_based':i+2,'reference_label':x,
                           'focal_label':focal_labels[i],'permuted_label':mutant_labels[i],
                           'restored_label':restored_labels[i]}
                        for i,x in enumerate(reference)],
 'input_inventory':inventory,'schema_path':schema.__file__,'schema_sha256':sha(Path(schema.__file__).read_bytes()),
 'audit_script_sha256':sha(Path(__file__).read_bytes()),'command_argv':[sys.executable]+sys.argv}
OUT.mkdir(parents=True,exist_ok=True)
(OUT/'results.json').write_text(json.dumps(result,indent=2))
print(json.dumps({'status':result['status'],'checks':collections.Counter(c['status'] for c in checks),
 'changed_buffers':changed,'original_matches':result['original_display_matches'],'mutant_mismatches':len(mismatches),
 'duplicate_names':duplicate_names,'failures':[x for x in checks if x['status']=='FAIL']},indent=2))
