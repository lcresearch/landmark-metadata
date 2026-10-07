#!/usr/bin/env python3
"""Read-only saved-byte pre-audit; no generation, compilation or inference."""
import collections, hashlib, io, json, pathlib, re, sys, zipfile
sys.dont_write_bytecode=True
from tensorflow_lite_support.metadata import schema_py_generated as schema
import numpy as np
O=pathlib.Path('/workspace/agent-preaudit-20261007T0749Z/secondary')
E=pathlib.Path('/workspace/metadata-contract-e2e-20261004T030536Z')
A=pathlib.Path('/workspace/metadata-contract-audit-20261004T062010Z/baseline')
R=pathlib.Path('/workspace/landmark-agent-preaudit')
files={}; checks={}; gaps=[]
def read(p,ha):
 p=pathlib.Path(p); b=p.read_bytes(); files[str(p)]={'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b),'ha':ha};return b
def js(p,ha):return json.loads(read(p,ha))
def digest(b):return hashlib.sha256(b).hexdigest()
def normalize(v):
 if isinstance(v,np.ndarray):return {'dtype':str(v.dtype),'shape':list(v.shape),'bytes':v.tobytes().hex()}
 if isinstance(v,bytes):return {'bytes':v.hex()}
 if isinstance(v,list):return [normalize(x) for x in v]
 if hasattr(v,'__dict__'):return {k:normalize(x) for k,x in vars(v).items()}
 return v
# HA08 independent buffer/computational object comparison
ha='HA08'; h=E/'E7'
focal=read(h/'variants/original/hand_landmarks_detector.tflite',ha)
pinned_bundle=read(h/'source-pinned-hand_landmarker.task',ha)
with zipfile.ZipFile(io.BytesIO(pinned_bundle)) as z:pinned=z.read('hand_landmarks_detector.tflite')
f=schema.ModelT.InitFromObj(schema.Model.GetRootAsModel(focal,0)); p=schema.ModelT.InitFromObj(schema.Model.GetRootAsModel(pinned,0))
fields=['version','operatorCodes','subgraphs','signatureDefs']
checks[ha]={'focal_sha256':digest(focal),'pinned_component_sha256':digest(pinned),'different_component_bytes':focal!=pinned,'computational_fields_equal':{k:normalize(getattr(f,k))==normalize(getattr(p,k)) for k in fields},'buffers_focal':len(f.buffers),'buffers_pinned':len(p.buffers),'different_buffer_indices':[i for i,(x,y) in enumerate(zip(f.buffers,p.buffers)) if normalize(x)!=normalize(y)],'source_scope':'Direct saved source read; no wheel/source equivalence validation'}
for path in ['source-component-equivalence.json','source-pinned-assets.json','sources/immutable-commit-source-verification.json','sources/tag.json','sources/hand_landmarks_detector_graph.cc','sources/external_files.bzl','sources/provenance.json','static-results.json','binding-audit.json']:
 read(h/path,ha)
checks[ha]['source_pinned_bundle_sha256']=digest(pinned_bundle)
checks[ha]['fixed_image_sha256']=digest(read(h/'thumb_up.jpg',ha))
checks[ha]['source_pinned_image_equal']=read(h/'thumb_up.jpg',ha)==read(h/'source-pinned-thumb_up.jpg',ha)
variants=['original','container_control','metadata_exchange','restoration']; bytebase=None; runtime=[]
for phase in ['primary','replay']:
 for v in variants:
  d=js(h/f'executions/{phase}/{v}/outputs/result.json',ha); b=read(h/f'executions/{phase}/{v}/outputs/decoded.json',ha)
  read(h/f'executions/{phase}/{v}/logs/task.command.json',ha)
  floatbits=read(h/f'executions/{phase}/{v}/outputs/decoded-float-bits.bin',ha)
  if digest(floatbits)!=d['decoded_float_bits_sha256']: raise ValueError('Float bits digest mismatch')
  bundle=read(h/f'variants/{v}/hand_landmarker.task',ha)
  if bytebase is None:bytebase=b
  runtime.append({'phase':phase,'variant':v,'decoded_equal_original_primary':b==bytebase,'canonical_decoded_hash_matches_record':digest(json.dumps(json.loads(b),sort_keys=True,separators=(',',':')).encode())==d['decoded_sha256'],'bundle_hash_matches_record':digest(bundle)==d['bundle_sha256'],'image_hash_matches':d['image_sha256']==checks[ha]['fixed_image_sha256'],'statuses':{k:d[k] for k in ['initialization_status','input_preparation_status','detect_status']},'version':d['mediapipe_version'],'detected_hands':d['detected_hands']})
checks[ha]['runtime_units']=runtime
compile_path=pathlib.Path('/workspace/hand-contract-repro/results/compile-results.json')
if compile_path.exists():
 comp=js(compile_path,ha);checks[ha]['compile_records']=[]
 for v in ['original','swapped']:
  a=read(h/f'binding-audit/{v}/unmodified.java',ha).decode(); b=read(h/f'binding-audit/{v}/separator-repaired.java',ha).decode(); repaired=a
  for pattern,repl in comp['repair_rules']:repaired=re.sub(pattern,repl,repaired)
  rec=comp['variants'][v]
  for mode in ['raw','repaired']: read(pathlib.Path('/workspace/hand-contract-repro')/rec[mode]['log'],ha)
  dis=read(h/f'binding-audit/{v}/fresh-outputs-javap.stdout',ha).decode()
  match=re.search(r'java\.util\.Map<java\.lang\.Integer, java\.lang\.Object> getBuffer\(\);(.*?)(?:\n  private|\n})',dis,re.S)
  mapping={field:int(i) for i,field in re.findall(r'iconst_(\d).*?getfield\s+#\d+\s+// Field (\w+):',match.group(1),re.S)}
  checks[ha]['compile_records'].append({'variant':v,'raw_exit':rec['raw']['exit_code'],'repaired_exit':rec['repaired']['exit_code'],'same_rules_reproduce_repair':repaired==b,'only_whitespace_comma_changes':re.sub(r'[\s,]+','',a)==re.sub(r'[\s,]+','',b),'saved_disassembly_mapping':mapping,'raw_compile':rec['raw']})
# HA09a full saved E4 denominator and byte checks
ha='HA09a'; r=E/'E4'; d=js(r/'results.json',ha); ds=js(r/'downloads.json',ha);candidates=js(r/'protocol/candidates.json',ha);freeze=js(r/'prevalidation-freeze.json',ha);freeze_files=js(r/'protocol/FROZEN_FILES.json',ha)
frozen=[{'path':n,'matches':digest(read(r/'protocol'/n,ha))==s} for n,s in freeze_files.items()]
checked=[x for x in d['component_occurrences'] if x['status']=='CHECKED']; rows=[]
for x in d['component_occurrences']:
 if x['status']!='CHECKED':continue
 mp=E/x['artifact_paths']['model'];base=mp.parent; cc=js(base/'logs/javac.command.json',ha);stderr=read(base/'logs/javac.stderr',ha).decode()
 read(base/'logs/checker.command.json',ha);read(base/'logs/checker.stdout',ha)
 dec=x['decoder_check'];status=('INAPPLICABLE' if isinstance(dec,str) else ('INCOMPATIBLE' if any(z['status']=='FAIL' for z in dec) else 'COMPATIBLE'))
 rows.append({'candidate':x['candidate'],'model_sha_matches':digest(read(mp,ha))==x['component_sha256'],'canonical_graph_saved':x['canonical_graph_sha256'],'compile_status':x['compile_status'],'compile_exit':cc['exit_code'],'compile_exit_matches':cc['exit_code']==x['compile_exit_code'],'stderr_has_error':'error:' in stderr,'D':status,'structural':x['structural_status'],'I':x['semantic_check'],'generation_warnings':x['checker']['generation']['diagnostics']})
for x in ds:
 read(r/f'downloads/{x["id"]}/record.json',ha)
 if x['status']=='DOWNLOADED': x['fresh_sha_matches']=digest(read(E/x['path'],ha))==x['sha256']
checks[ha]={'candidate_count':len(candidates),'candidate_digest_matches_freeze':digest(read(r/'protocol/candidates.json',ha))==freeze['candidate_sha256'],'frozen_file_checks':frozen,'downloads':dict(collections.Counter(x['status'] for x in ds)),'download_bytes_all_match':all(x.get('fresh_sha_matches',True) for x in ds),'component_occurrences':len(d['component_occurrences']),'occurrence_statuses':dict(collections.Counter(x['status'] for x in d['component_occurrences'])),'new_graph_count_recorded_hashes':len(set(x['canonical_graph_sha256'] for x in checked)),'rows':rows,'compile_counts':dict(collections.Counter(x['compile_status'] for x in rows)),'D_counts':dict(collections.Counter(x['D'] for x in rows)),'independent_graph_recomputation':'NOT_CHECKED','development_46_105_23':'NOT_CHECKED: omitted from short claim; bounded review prioritizes retained E4 claim','historical_chronology':'candidate/file identities checked; external timestamp authenticity NOT_CHECKED'}
# HA09b all 65 fixture identities + per-fixture saved report equality, baseline raw units
ha='HA09b';r=E/'E5';frozen=js(r/'evaluation-fixtures-before-run.json',ha);d=js(r/'results.json',ha)['fixtures'];rows=[]
for x in d:
 report=js(r/f'checks/{x["model_sha256"]}/result.json',ha);p=pathlib.Path(x['path'])
 rows.append({'sha256':x['model_sha256'],'exists':p.exists(),'artifact_sha_matches':digest(read(p,ha))==x['model_sha256'] if p.exists() else None,'report_matches_aggregate':report==x['report'],'D':report['DECODER_COMPATIBILITY']['status'],'I':report['REFERENCE_BACKED_SEMANTIC']['status'],'D_detail':report['DECODER_COMPATIBILITY'] if 'ABSTAIN' in report['DECODER_COMPATIBILITY']['status'] else None})
baseline=[]
for v in ['original','description_control','label_deletion','label_permutation','label_restoration']:
 row={'variant':v}
 for consumer in ['displayer','populator','simple_baseline','task_init','e5']:
  q=js(A/f'conditions/{v}/{consumer}/result.json',ha);row[consumer]=q['DECODER_COMPATIBILITY']['status'] if consumer=='e5' else q['status'];row[consumer+'_artifact_sha']=q.get('artifact_sha256',q.get('model_sha256'))
 baseline.append(row)
structural=js(A/'conditions/structural_count_minus_one/populator/result.json',ha)
checks[ha]={'frozen_count':len(frozen),'result_count':len(d),'frozen_sha_set_matches':{x['model_sha256'] for x in frozen}=={x['model_sha256'] for x in d},'frozen_sha_unique':len({x['model_sha256'] for x in frozen}),'D_counts':dict(collections.Counter(x['D'] for x in rows)),'I_counts':dict(collections.Counter(x['I'] for x in rows)),'fixtures':rows,'baseline_units':baseline,'extra_e5_rejections_over_simple':[x['variant'] for x in baseline if x['e5']=='INCOMPATIBLE' and x['simple_baseline']!='INCOMPATIBLE'],'extra_e5_rejections_over_task':[x['variant'] for x in baseline if x['e5']=='INCOMPATIBLE' and x['task_init']!='FAIL'],'structural_count_reduction':{'status':structural['status'],'exception':structural['exception_message']}}
# HA09c missing reconstruction raw; source inspection is separate
ha='HA09c';paths=['/workspace/repro-audit/independent-audit/label-parser/results.json','/workspace/repro-audit/independent-audit/label-parser/baseline-task-comparison.json','/workspace/repro-external/E5/evaluation-fixtures-before-run.json']
checks[ha]={'raw_paths':[{'path':p,'exists':pathlib.Path(p).exists()} for p in paths]}
for path in ['sources/repro-audit-20261004/reports/CHECKER_AUDIT.md','sources/metadata-contract-e2e-20261004T030536Z/scripts/preflight.py','sources/metadata-contract-audit-20261004T062010Z/baseline/audit_one.py']:
 read(R/path,ha)
# HA10 actual issue/comment bodies, count denominator only
ha='HA10';pub=pathlib.Path('/workspace/significance-review-20261004/public-reports');issue=js(pub/'issue-01.json',ha);comments=js(pub/'issue-01-comments.json',ha);member=[x for x in comments if x['id']==1108777779][0]
checks[ha]={'issue_number':issue['number'],'issue_created':issue['created_at'],'issue_url':issue['html_url'],'body_has_generated_getter_stack':'LiteModelDeeplabv31Metadata2$Outputs.getSegmentationMasksAsCategoryList' in issue['body'],'body_has_mismatch':'Label number 21 mismatch the shape on axis 1' in issue['body'],'member_reply':{'id':member['id'],'association':member['author_association'],'author':member['user']['login'],'created':member['created_at'],'body':member['body']},'natural_artifact_reproduction':'NOT_CHECKED; no model fetched or executed','full_text_overlap':'NOT_CHECKED; source/report scope reviewed only'}
for path in ['research/20261004-significance-review/PUBLIC_REPORTS.md','research/20261004-contribution-review/CONTRIBUTION_COMPARISON.md','research/20261004-significance-review/SIGNIFICANCE_ASSESSMENT.md','work/workshop-convergence-20261007/CLAIM_EVIDENCE.md','work/workshop-convergence-20261007/manuscript/paper.tex']:
 read(R/path,ha)
read(E/'scripts/hand_task_one.py','HA08')
read(pathlib.Path(schema.__file__),'HA08')
(O/'observations.json').write_text(json.dumps({'method':'Saved byte readback and static computation; no inference, generation or compilation','checks':checks,'files':files},indent=2)+'\n')
print(json.dumps({k:{a:b for a,b in v.items() if a not in ['fixtures','rows','runtime_units','compile_records','frozen_file_checks']} for k,v in checks.items()},indent=2))
