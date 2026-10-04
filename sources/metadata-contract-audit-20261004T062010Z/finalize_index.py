#!/usr/bin/env python3
"""Build the final audit index from completed sub-audits; no experiment execution."""
import datetime, hashlib, json, pathlib
ROOT=pathlib.Path(__file__).resolve().parent
def read(name):return json.loads((ROOT/name).read_text())
def identity(name):
    p=ROOT/name
    return {'path':name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
fresh=read('verification/fresh-runtime-crosscheck.json')
build=read('rebuild/results.json')
preserved=read('preservation/results.json')
claims=read('claims/claim-audit.json')
before=read('verification/before.json');after=read('verification/after.json')
assert fresh['status']==preserved['status']==before['status']==after['status']=='PASS'
assert build['summary']['FAIL']==build['summary']['UNVERIFIABLE']==0
assert read('verification/manuscript-after.json')['status']=='PASS'
assert read('verification/baseline-crosscheck.json')['E5_additional_rejections_over_simple_baseline']==0
units=[]
for r in build['records']:
    units.append({k:r.get(k) for k in ['experiment_id','component_name','variant','model_sha256','canonical_graph_sha256','metadata_sha256','associated_file_sha256','apk_sha256','apk_asset_sha256','runtime_asset_sha256','consumer','generator_version','runtime_version','compiler_version','platform','structural_status','generation_status','compile_status','package_status','load_status','inference_status','decoder_status','earliest_failing_stage','semantic_check','artifact_paths']})
index={
    'audit_id':ROOT.name,
    'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'status':'COMPLETED_WITH_FINDINGS',
    'principal_result':'The preserved and freshly rebuilt E1/E2 evidence supports the bounded execution claims. E5 has no additional rejected core condition over the implementation-matched simple baseline or Task initialization. One manuscript implementation-scope statement requires correction.',
    'human_verification':'PENDING',
    'independent_human_replication':False,
    'same_installed_toolchain_reused':True,
    'fresh_output_and_AVD':True,
    'manuscript_modified':False,
    'historical_manifest_integrity':'PASS_BEFORE_AND_AFTER',
    'raw_observation_scope':{'new_phase_variant_execution_records':8,'unique_artifact_consumer_configurations':5,'canonical_graphs':1,'new_input_observations':16,'new_successful_category_lists':14,'new_caught_getter_exceptions':2,'historical_raw_observations_rechecked':32},
    'experimental_unit_definition':'component × variant × consumer/toolchain configuration; phase aliases and repeated inputs are not independent models',
    'subaudits':[
        {'id':'A01','status':'PASS','assertion':'Historical evidence and manuscript manifest-covered bytes remain unchanged','reports':['verification/before.json','verification/after.json','verification/manuscript-before.json','verification/manuscript-after.json']},
        {'id':'A02','status':'PASS','assertion':'Retained model/ZIP/APK/code/raw/decoded evidence supports preservation and interface claims','reports':['preservation/AUDIT_REPORT.md','preservation/results.json','preservation/bytecode/results.json']},
        {'id':'A03','status':'PASS','assertion':'Fresh generated builds and actual getter runs reproduce E1/E2 outcomes and recorded model identities','reports':['rebuild/AUDIT_REPORT.md','rebuild/results.json','verification/fresh-runtime-crosscheck.json']},
        {'id':'A04','status':'PASS','assertion':'Five-condition comparison yields identical incompatibility decisions for simple baseline, E5 and Task initialization','new_detection_increment_on_core_conditions':0,'reports':['baseline/RESULTS.md','baseline/results.json','verification/baseline-crosscheck.json']},
        {'id':'A05','status':'PASS','assertion':'E3/E4/E5 denominators and Hand bridge/decoded records support their explicitly bounded statements','reports':['claims/AUDIT_REPORT.md','claims/recomputed.json']},
        {'id':'A06','status':'FAIL','assertion':'The unqualified claim that E5 safely abstains on all unrecognized processing is supported by the implementation','finding':'Template regexes can miss getter/processor syntax; no current fixture outcome was shown incorrect','required_action':'Narrow manuscript lines 54–58 and 195; do not claim general dataflow analysis','reports':['claims/claim-audit.json','baseline/RESULTS.md','MANUSCRIPT_IMPACT.md']},
        {'id':'A07','status':'PASS','assertion':'Four specified full-text methods were retrieved/recovered, version-pinned and compared','novelty_established':False,'reports':['literature/AUDIT_REPORT.md','literature/results.json']},
        {'id':'A08','status':'UNVERIFIABLE','assertion':'EfficientNet original/permuted class order agrees/disagrees with an independent artifact-tied reference','reason':'No such reference established; I remains ABSTAIN'},
        {'id':'A09','status':'UNVERIFIABLE','assertion':'The initial historical E2 restoration replay attempt succeeded or failed','reason':'No complete recovered result; separate recovery and new execution do not assign an outcome to that attempt'},
    ],
    'claim_audit_status_counts':claims['status_counts'],
    'fresh_execution_records':units,
    'interpretation_limits':['Associated-label intervention is injected, not a natural EfficientNet defect.','No prediction accuracy or prevalence estimate.','No same-Android Task API comparison was added.','No new external model or natural-case search.','No independent class-order oracle or human audit.','Fresh harness pre-load asset hashing does not intercept native interpreter memory.','The installed SDK/JDK/Python were reused, not reinstalled from archive.','Full new DEX equality is checked within new builds; generated class bytes also match historical classes.'],
    'reports':[identity(n) for n in ['AUDIT_REPORT.md','AUDIT_PLAN.md','MANUSCRIPT_IMPACT.md','preservation/results.json','rebuild/results.json','baseline/results.json','claims/claim-audit.json','literature/results.json','verification/fresh-runtime-crosscheck.json']],
    'todo':'/workspace/metadata-contract-next/TODO.md',
    'todo_snapshot':'TODO.after.md',
}
(ROOT/'results.json').write_text(json.dumps(index,indent=2,ensure_ascii=False))
print(json.dumps({'status':index['status'],'principal_result':index['principal_result'],'human_verification':'PENDING'},indent=2))
