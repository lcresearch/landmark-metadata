import json, shutil
from common import ROOT, sha, save, run
OLD=ROOT.parent/'metadata-contract-paper';protocol=ROOT/'E4/protocol';protocol.mkdir(parents=True,exist_ok=False)
specs=[
 ('image_classifier','efficientnet_lite0','int8','efficientnet_lite0.tflite'),
 ('image_classifier','efficientnet_lite0','float16','efficientnet_lite0.tflite'),
 ('image_classifier','efficientnet_lite2','float32','efficientnet_lite2.tflite'),
 ('image_classifier','efficientnet_lite2','int8','efficientnet_lite2.tflite'),
 ('image_classifier','efficientnet_lite2','float16','efficientnet_lite2.tflite'),
 ('object_detector','efficientdet_lite0','int8','efficientdet_lite0.tflite'),
 ('object_detector','efficientdet_lite2','float32','efficientdet_lite2.tflite'),
 ('object_detector','efficientdet_lite2','int8','efficientdet_lite2.tflite'),
 ('object_detector','efficientdet_lite2','float16','efficientdet_lite2.tflite'),
 ('object_detector','ssd_mobilenet_v2','float32','ssd_mobilenet_v2.tflite'),
 ('object_detector','ssd_mobilenet_v2','int8','ssd_mobilenet_v2.tflite'),
 ('face_detector','blaze_face_short_range','float16','blaze_face_short_range.tflite'),
 ('face_detector','blaze_face_full_range_sparse','float16','blaze_face_full_range_sparse.tflite'),
 ('image_segmenter','selfie_segmenter','float16','selfie_segmenter.tflite'),
 ('image_segmenter','selfie_segmenter_landscape','float16','selfie_segmenter_landscape.tflite'),
 ('image_segmenter','hair_segmenter','float32','hair_segmenter.tflite'),
 ('image_segmenter','selfie_multiclass_256x256','float32','selfie_multiclass_256x256.tflite'),
 ('pose_landmarker','pose_landmarker_full','float16','pose_landmarker_full.task'),
 ('pose_landmarker','pose_landmarker_heavy','float16','pose_landmarker_heavy.task'),
 ('audio_classifier','yamnet','float32','yamnet.tflite'),
]
candidates=[{'id':f'C{i+1:02d}','url':'https://storage.googleapis.com/mediapipe-models/'+'/'.join([task,name,dtype,'1',file]),'task_family':task,'model_name':name,'declared_precision_in_url':dtype} for i,(task,name,dtype,file) in enumerate(specs)]
save(protocol/'candidates.json',candidates)
prior=json.loads((OLD/'results/static-suite.json').read_text())
save(protocol/'prior-exclusions.json',[{'component_sha256':c['sha256'],'canonical_graph_sha256':c['canonical_sha256']} for c in prior])
(protocol/'scripts').mkdir()
for name in ['check_model.py','inspect_suite.py','suite_static.py','codegen_one.py']:shutil.copyfile(OLD/'scripts'/name,protocol/'scripts'/name)
shutil.copyfile(OLD/'contracts.json',protocol/'contracts.json')
shutil.copyfile(ROOT/'PREVALIDATION_PROTOCOL.md',protocol/'PREVALIDATION_PROTOCOL.md')
shutil.copyfile(ROOT/'EXPERIMENT_E4_PLAN.md',protocol/'EXPERIMENT_E4_PLAN.md')
shutil.copyfile(ROOT/'scripts/prepare_e1.py',protocol/'existing-associated-file-procedure.py')
shutil.copyfile(ROOT/'scripts/prepare_e2.py',protocol/'existing-permutation-procedure.py')
shutil.copyfile(OLD/'requirements.lock',protocol/'requirements.lock')
save(protocol/'mutation-rules.json',{'description':'One same-size ASCII letter case change in first available output/model description.','metadata_count':'Reduce populated output tensor metadata vector count by one in-place.','index_exchange':'First lexicographic populated output pair with differing graph shapes; exchange only metadata vector relative offsets.','label_deletion':'Remove final label line using preserved suite_static.mutate_label; deterministic ZIP timestamps.','label_permutation':'Cyclic left one label line, preserve count/multiset/filename/line-ending convention; preserve TFLite prefix and metadata.','restoration':'Inverse operation, require original associated payloads.','external_observations':'Originals only. Mutations evaluated later on preserved controls, never counted as natural defects.'})
(protocol/'.gitignore').write_text('checks/\n__pycache__/\n*.pyc\n')
hashes={str(p.relative_to(protocol)):sha(p.read_bytes()) for p in sorted(protocol.rglob('*')) if p.is_file()}
save(protocol/'FROZEN_FILES.json',hashes)
for name,command in [('init',['git','init']),('add',['git','add','.']),('commit',['git','-c','user.name=Protocol automation','-c','user.email=protocol@local.invalid','commit','-m','Freeze E4 rules, eligibility, references and 20 candidates before inspection'])]:
    p=run(command,ROOT/'E4/freeze-logs'/name,cwd=protocol)
    if p.returncode:raise SystemExit('Protocol freeze failed')
p=run(['git','rev-parse','HEAD'],ROOT/'E4/freeze-logs/head',cwd=protocol)
save(ROOT/'E4/prevalidation-freeze.json',{'git_commit':p.stdout.decode().strip(),'frozen_files_sha256':sha((protocol/'FROZEN_FILES.json').read_bytes()),'protocol_sha256':sha((protocol/'PREVALIDATION_PROTOCOL.md').read_bytes()),'candidate_sha256':sha((protocol/'candidates.json').read_bytes()),'external_downloads_started':False,'status':'LOCAL_SAME_SESSION_FREEZE_NOT_THIRD_PARTY_PREREGISTRATION'})
print(p.stdout.decode().strip())
