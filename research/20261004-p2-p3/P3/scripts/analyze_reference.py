#!/usr/bin/env python3
"""Compare archived bytes independently of the existing checker/mutation code.
No network calls. Display-order reference and stable-class-ID inquiry stay separate.
"""
import ast, collections, copy, hashlib, importlib.metadata, json, pathlib, platform, sys, zipfile
import flatbuffers
import numpy as np
from tensorflow_lite_support.metadata import schema_py_generated as schema
ROOT=pathlib.Path(__file__).resolve().parents[1]
OLD=pathlib.Path('/workspace/metadata-contract-e2e-20261004T030536Z')
FOCAL=OLD/'E1/variants/original/model.tflite'
def sha(data):return hashlib.sha256(data).hexdigest()
def save(name,value):
    p=ROOT/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(value,indent=2)+'\n')
def body(key):return (ROOT/'retrieved'/key/'body').read_bytes()
def normal(x):
    if isinstance(x,np.ndarray):return x.tolist()
    if isinstance(x,np.generic):return x.item()
    if isinstance(x,bytes):return {'bytes_hex':x.hex()}
    if isinstance(x,(list,tuple)):return [normal(y) for y in x]
    if isinstance(x,dict):return {k:normal(v) for k,v in x.items()}
    if hasattr(x,'__dict__'):return normal(vars(x))
    return x

def graph(data):
    obj=schema.ModelT.InitFromObj(schema.Model.GetRootAsModel(data,0))
    entries=[m for m in obj.metadata or [] if m.name==b'TFLITE_METADATA']
    assert len(entries)==1
    idx=entries[0].buffer
    buffers=[b'' if b.data is None else bytes(b.data) for b in obj.buffers]
    tensor_refs=sorted(set(int(t.buffer) for sg in obj.subgraphs for t in sg.tensors))
    assert idx not in tensor_refs,'Metadata buffer used by graph tensor'
    descriptor=normal({k:v for k,v in vars(obj).items() if k not in ['buffers','metadata']})
    other_metadata=normal([m for m in obj.metadata or [] if m.name!=b'TFLITE_METADATA'])
    canonical=copy.deepcopy(obj)
    canonical.buffers[idx].data=None
    canonical.metadata=[m for m in canonical.metadata or [] if m.name!=b'TFLITE_METADATA']
    builder=flatbuffers.Builder(0);builder.Finish(canonical.Pack(builder),file_identifier=b'TFL3')
    outputs=[]
    for sgi,sg in enumerate(obj.subgraphs):
        for pos,tid in enumerate(sg.outputs):
            outputs.append({'subgraph':sgi,'output_position':pos,'tensor_id':int(tid),'tensor':normal(sg.tensors[int(tid)])})
    return {'obj':obj,'idx':idx,'buffers':buffers,'tensor_buffer_references':tensor_refs,'graph_descriptor':descriptor,'other_metadata':other_metadata,'canonical_sha256':sha(bytes(builder.Output())),'outputs':outputs}
def label_resource(path):
    with zipfile.ZipFile(path) as z:
        names=z.namelist();assert names==['labels_without_background.txt']
        data=z.read(names[0]);return names[0],data,data.decode('utf8').splitlines()

focal=FOCAL.read_bytes(); assert sha(focal)=='6c7ab0a6e5dcbf38a8c33b960996a55a3b4300b36a018c4545801de3a3c8bde0'
assert body('I01-publisher-model')==focal==body('F02-publisher-latest-model')
a=graph(focal);b=graph(body('I06-tfhub-lite-model'))
assert a['idx']==b['idx']==165 and len(a['buffers'])==len(b['buffers'])==166
buffer_rows=[{'index':i,'focal_bytes':len(x),'tfhub_bytes':len(y),'focal_sha256':sha(x),'tfhub_sha256':sha(y),'equal':x==y,'metadata_buffer':i==a['idx']} for i,(x,y) in enumerate(zip(a['buffers'],b['buffers']))]
assert [r['index'] for r in buffer_rows if not r['equal']]==[165]
assert a['graph_descriptor']==b['graph_descriptor']
assert a['other_metadata']==b['other_metadata']
assert a['outputs']==b['outputs']
assert a['canonical_sha256']==b['canonical_sha256']=='73e57df01115600419abb72de4b2c3257200e12eb205d335bcbfc203a589bee8'
name,raw_labels,labels=label_resource(FOCAL)
assert label_resource(ROOT/'retrieved/I06-tfhub-lite-model/body')[1]==raw_labels
bridge={'focal_sha256':sha(focal),'tfhub_sha256':sha(body('I06-tfhub-lite-model')),'canonical_graph_sha256':a['canonical_sha256'],'buffers':buffer_rows,'equal_nonmetadata_buffers':sum(r['equal'] and not r['metadata_buffer'] for r in buffer_rows),'metadata_buffer_index':165,'metadata_buffer_not_tensor_referenced':True,'tensor_buffer_references':a['tensor_buffer_references'],'all_nonbuffer_nonmetadata_model_fields_equal':True,'other_metadata_equal':True,'ordered_outputs_equal':True,'outputs':a['outputs'],'associated_resource_bytes_equal':True,'associated_resource_sha256':sha(raw_labels),'scope':'Structural graph/weights equivalence with ordered outputs, not an inference replay or proof of undocumented conversion history.'}
save('analysis/artifact-bridge.json',bridge)
save('analysis/graph-descriptor.json',a['graph_descriptor'])

card=body('F10-pinned-parent-card').decode()
assert 'num_classes` = 1000' in card
assert 'please ignore the first background class, ie. index 0 corresponds to' in card
assert '"tench"' in card
external_bytes=body('F11-explicit-class-order'); external_all=external_bytes.decode().splitlines()
assert len(external_all)==1001 and external_all[0]=='background'
# The only offset applied is explicitly required by the pinned parent card.
reference=external_all[1:]
assert len(labels)==len(reference)==1000
assert body('F01-publisher-labels')==external_bytes
assert labels==reference
mutant_path=OLD/'E2/variants/label_permutation/model.tflite';restore_path=OLD/'E2/variants/permutation_restoration/model.tflite'
_,_,permuted=label_resource(mutant_path);_,_,restored=label_resource(restore_path)
assert permuted==labels[1:]+labels[:1] and restored==labels
assert graph(mutant_path.read_bytes())['canonical_sha256']==a['canonical_sha256']
assert graph(restore_path.read_bytes())['canonical_sha256']==a['canonical_sha256']
positions=[{'output_position':i,'external_file_line_1based':i+2,'reference_display_label':reference[i],'original_display_label':labels[i],'permutation_display_label':permuted[i],'restored_display_label':restored[i],'original_matches_reference':labels[i]==reference[i],'permutation_matches_reference':permuted[i]==reference[i],'restoration_matches_reference':restored[i]==reference[i]} for i in range(1000)]
assert sum(not x['permutation_matches_reference'] for x in positions)==999
save('analysis/full-display-order-comparison.json',positions)
duplicates=[{'display_label':k,'output_positions':v} for k,v in sorted((k,[i for i,x in enumerate(labels) if x==k]) for k in set(labels)) if len(v)>1]

synsets=body('F17-synset-order').decode().splitlines()
assert len(synsets)==len(set(synsets))==1000
human={x.split('\t',1)[0]:x.split('\t',1)[1] for x in body('F18-synset-names').decode().splitlines()}
checkpoint_names=ast.literal_eval(body('F15-tpu-labelmap').decode())
assert set(checkpoint_names)==set(range(1000))
synrows=[{'candidate_index':i,'candidate_synset':sid,'candidate_full_name':human[sid],'checkpoint_full_name':checkpoint_names[i],'checkpoint_full_name_matches':human[sid]==checkpoint_names[i],'candidate_first_synonym':human[sid].split(',')[0],'external_display_label':reference[i],'candidate_first_synonym_matches':human[sid].split(',')[0]==reference[i],'artifact_tied_stable_id':False} for i,sid in enumerate(synsets)]
save('analysis/candidate-synset-comparison.json',synrows)
requests=[json.loads(p.read_text()) for p in sorted((ROOT/'retrieved').glob('*/retrieval.json'))]
assert sum(x['id'].startswith('I') for x in requests)==12
assert sum(x['id'].startswith('F') for x in requests)==18
versions={'python':sys.version,'platform':platform.platform(),'tflite_support':importlib.metadata.version('tflite-support'),'flatbuffers':importlib.metadata.version('flatbuffers'),'numpy':np.__version__,'tensorflow_tpu_head_observed':json.loads(body('F13-tpu-head'))[0]['sha'],'tensorflow_models_pinned_synset_revision':json.loads(body('F14-tensorflow-models-head'))[0]['sha'],'tensorflow_tfhub_card_revision':'81fdea8ffa53b5acbd66a012d17fb8f9602c714b'}
results={'experiment_id':'P3','status':'COMPLETE_WITH_QUALIFIED_DISPLAY_REFERENCE','focal_component_sha256':sha(focal),'canonical_graph_sha256':a['canonical_sha256'],'plan_sha256':sha((ROOT/'EXPERIMENT_P3_PLAN.md').read_bytes()),'primary_result':{'display_order_reference':'ESTABLISHED_BY_PUBLISHER_CARD_AND_GRAPH_EQUIVALENT_BRIDGE','stable_class_id_reference':'ABSTAIN','prediction_correctness':'NOT_EVALUATED','original_display_agreement':'PASS','permutation_display_agreement':'FAIL','restoration_display_agreement':'PASS','original_position_matches':1000,'permutation_position_mismatches':999,'restoration_position_matches':1000,'background_rule':'Ignore first reference-file entry as explicitly specified by classification/1 card; output index 0 maps to tench','reference_total_lines':1001,'evaluated_output_positions':1000,'duplicate_display_labels':duplicates,'unchanged_permutation_positions':[x['output_position'] for x in positions if x['permutation_matches_reference']],'witness_904':positions[904]},'bridge':{k:v for k,v in bridge.items() if k not in ['buffers','tensor_buffer_references']},'candidate_stable_ids':{'count':1000,'checkpoint_full_name_matches':sum(x['checkpoint_full_name_matches'] for x in synrows),'first_synonym_display_matches':sum(x['candidate_first_synonym_matches'] for x in synrows),'result':'Candidate generic ImageNet synset order agrees with the separately linked checkpoint names, but exact artifact-to-synset training lineage is not established. Matching display strings do not identify duplicate classes.'},'bounded_search':{'initial_candidates':12,'followups':18,'max_initial':12,'max_followups':18,'status_counts':dict(collections.Counter(str(x.get('status')) for x in requests)),'stop_reason':'All predeclared source families examined; request bounds reached. Display-order chain obtained; no further expansion for stable IDs.'},'versions':versions,'retrieval_records':[str((ROOT/'retrieved'/x['id']/'retrieval.json').relative_to(ROOT)) for x in requests],'fresh_vs_recovered':{'fresh':['30 bounded network requests and archived bodies','independent graph/buffer/order equality analysis','all 1000 original/permuted/restored display labels compared with external publisher mapping'],'recovered':['E1 original artifact and E2 permutation/restoration bytes'],'new_inference':False,'human_verification':False},'limitations':['Frozen catalog commit records publisher documentation retrieved now; it is not asserted to be the original model-release-time document revision.','The original display strings are not used as the oracle; comparison uses the external file explicitly prescribed by the parent card.','External label-file bytes are archived and hashed; historical lifetime immutability of its unversioned URL is not established.','Graph/weights equality establishes exact output ordering across the model bridge; no independent training, numerical task accuracy, or prediction correctness was evaluated.','No stable synset ID can be asserted for the focal artifact solely from this chain.','E2 permutation is injected, not a natural EfficientNet defect.'],'artifacts':['analysis/artifact-bridge.json','analysis/graph-descriptor.json','analysis/full-display-order-comparison.json','analysis/candidate-synset-comparison.json']}
reference_records=[]
for variant,path,strings in [('original',FOCAL,labels),('label_permutation',mutant_path,permuted),('permutation_restoration',restore_path,restored)]:
    g=graph(path.read_bytes()); resource_name,resource_data,_=label_resource(path)
    disagreements=[i for i,(actual,expected) in enumerate(zip(strings,reference)) if actual!=expected]
    reference_records.append({'experiment_id':'P3','component_name':'efficientnet_lite0','variant':variant,'component_sha256':sha(path.read_bytes()),'canonical_graph_sha256':g['canonical_sha256'],'associated_file':resource_name,'associated_file_sha256':sha(resource_data),'metadata_sha256':sha(g['buffers'][g['idx']]),'consumer':'offline published display-order comparison','consumer_version':'scripts/analyze_reference.py','reference_source':'analysis/reference-chain.json','reference_sha256':sha(external_bytes),'semantic_check':{'I_display':'FAIL' if disagreements else 'PASS','I_stable_class_id':'ABSTAIN','positions':1000,'disagreement_count':len(disagreements)},'decoder_check':'NOT_EVALUATED_IN_P3','inference_status':'NOT_RUN_IN_P3','preservation_check':'CANONICAL_GRAPH_MATCH','artifact_paths':{'model':str(path),'comparison':'analysis/full-display-order-comparison.json'}})
results['experimental_units']=reference_records
save('results.json',results)
print(json.dumps({'status':results['status'],'display_order':results['primary_result'],'stable_ids':results['candidate_stable_ids'],'search':results['bounded_search']},indent=2))
