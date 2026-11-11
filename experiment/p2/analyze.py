import json,pathlib,hashlib,struct
from common import ROOT,sha,save
rows=json.loads((ROOT/'execution-results.json').read_text());statics=json.loads((ROOT/'static-results.json').read_text());builds=json.loads((ROOT/'build-results.json').read_text());assert len(rows)==10
checks=[];numeric=[]
for row in rows:
 c=row['consumer'];v=row['variant'];static=row['static'];obs=row.get('observed',{});d=ROOT/row.get('artifact_directory','MISSING')/'device'
 identity={'consumer':c,'variant':v,'source_copy_apk_preload_equal':static['variant_sha256']==row['build'].get('apk_model_sha256')==obs.get('loaded_asset_sha256'),'inputs':[]}
 for item in obs.get('observations',[]):
  name=item['input'];rawrgb=(d/(name+'-input.rgb')).read_bytes();expected=bytes([127])*(224*224*3) if name=='gray127' else bytes((37*k+17)%256 for k in range(224*224*3));identity['inputs'].append({'name':name,'predeclared_bytes_equal':rawrgb==expected,'reported_hash_equal':sha(rawrgb)==item['input_sha256']})
 checks.append(identity)
 for name in ['gray127','rgb_pattern']:
  p=d/(name+'-decoded.json');base=ROOT/'executions/primary'/c/'original/device'/(name+'-decoded.json');n={'consumer':c,'variant':v,'input':name,'decoded_available':p.exists()}
  if c=='wrapper':
   raw=d/(name+'-output-0.f32');rawbase=base.parent/(name+'-output-0.f32');n['raw_available']=raw.exists()
   if raw.exists():n['raw_equal_original']=raw.read_bytes()==rawbase.read_bytes();n['raw_sha256']=sha(raw.read_bytes())
  if p.exists():
   decoded=json.loads(p.read_text());original=json.loads(base.read_text());cats=decoded if c=='wrapper' else decoded[0]['categories'];bcats=original if c=='wrapper' else original[0]['categories'];key='list_position' if c=='wrapper' else 'category_index_field';indexed={x[key]:x for x in cats};bi={x[key]:x for x in bcats};n['categories']=len(cats);n['indices_complete']=sorted(indexed)==list(range(1000));n['score_bits_equal_original']=all(indexed[k]['score_float_bits']==bi[k]['score_float_bits'] for k in bi if k in indexed) and set(indexed)==set(bi);n['changed_label_count']=sum(indexed[k]['label']!=bi[k]['label'] for k in bi if k in indexed);n['decoded_equal_original']=decoded==original;n['top5_indices']=sorted(indexed,key=lambda k:(-indexed[k]['score'],k))[:5]
   n['witness904']={'index':904,'original_label':bi[904]['label'],'label':indexed[904]['label'],'score':indexed[904]['score'],'score_float_bits':indexed[904]['score_float_bits']}
   if c=='wrapper':
    floats=struct.unpack('<1000f',(d/(name+'-output-0.f32')).read_bytes());bits=struct.unpack('<1000i',(d/(name+'-output-0.f32')).read_bytes());n['decoded_score_bits_equal_raw']=all(indexed[k]['score_float_bits']==bits[k] for k in indexed)
  numeric.append(n)
cross=[]
for v in [r['variant'] for r in statics]:
 for name in ['gray127','rgb_pattern']:
  wp=ROOT/'executions/primary/wrapper'/v/'device'/(name+'-decoded.json');tp=ROOT/'executions/primary/task'/v/'device'/(name+'-decoded.json')
  if not(wp.exists() and tp.exists()):continue
  w={x['list_position']:x for x in json.loads(wp.read_text())};t={x['category_index_field']:x for x in json.loads(tp.read_text())[0]['categories']};common=set(w)&set(t);cross.append({'variant':v,'input':name,'compared_indices':len(common),'equal_score_bit_count':sum(w[k]['score_float_bits']==t[k]['score_float_bits'] for k in common),'equal_label_count':sum(w[k]['label']==t[k]['label'] for k in common),'max_abs_returned_score_difference':max(abs(w[k]['score']-t[k]['score']) for k in common),'note':'Task public returned scores, not native raw tensors; no cross-consumer raw-tensor equivalence claim'})
summary={'primary_units':10,'unique_graphs':1,'variants':5,'consumers':2,'observed_input_runs':sum(len(x.get('observed',{}).get('observations',[])) for x in rows),'stage_matrix':[{'consumer':x['consumer'],'variant':x['variant'],'stages':x['stages'],'earliest_failing_stage':x.get('earliest_failing_stage')} for x in rows],'identity_checks':checks,'numeric_comparisons':numeric,'cross_consumer_returned_score_comparisons':cross,'source_classes_dex':{'all_generated_source_equal':all(x['generated_source_equal_original'] for x in statics),'all_classes_equal_within_consumer':all(x['classes_equal_original'] for x in builds),'all_dex_equal_within_consumer':all(x['dex_equal_original'] for x in builds)},'records':rows}
save(ROOT/'results.json',summary);print(json.dumps({k:v for k,v in summary.items() if k not in ['records','numeric_comparisons']},indent=2))
