import json, pathlib
from common import ROOT, sha, save
from preflight import check
OLD=ROOT.parent/'metadata-contract-paper';base=ROOT/'E5';base.mkdir(exist_ok=True)
fixtures={}
def add(path,alias,baseline=None):
    data=path.read_bytes();digest=sha(data)
    if digest not in fixtures:fixtures[digest]={'model_sha256':digest,'path':str(path),'aliases':[],'baseline':str(baseline) if baseline else None}
    fixtures[digest]['aliases'].append(alias)
    if baseline and not fixtures[digest]['baseline']:fixtures[digest]['baseline']=str(baseline)
for component in json.loads((OLD/'results/static-suite.json').read_text()):
    if not component['variants']:add(OLD/component['path'],{'phase':'prior','component':component['id'],'variant':'no_metadata_original'});continue
    original=OLD/next(v for v in component['variants'] if v['variant']=='original')['path']
    for v in component['variants']:add(OLD/v['path'],{'phase':'prior','component':component['id'],'variant':v['variant']},original if v['variant']!='original' else None)
known={}
for experiment in ['E1','E2']:
    for unit in json.loads((ROOT/experiment/'results.json').read_text())['units']:
        p=ROOT/unit['artifact_paths']['model'];add(p,{'phase':experiment,'component':'efficientnet','variant':unit['variant']},ROOT/experiment/'variants/original/model.tflite' if unit['variant']!='original' else None)
        known[sha(p.read_bytes())]=unit['decoder_status']
for row in json.loads((ROOT/'E4/results.json').read_text())['component_occurrences']:
    if row['status']=='CHECKED':add(ROOT/row['artifact_paths']['model'],{'phase':'E4_external','component':row['component_sha256'],'variant':'original','frozen_D':row['decoder_check']})
save(base/'evaluation-fixtures-before-run.json',list(fixtures.values()))
results=[]
for digest,fixture in fixtures.items():
    evidence=base/'checks'/digest;report=check(pathlib.Path(fixture['path']),evidence,baseline=pathlib.Path(fixture['baseline']) if fixture['baseline'] else None)
    record=dict(fixture,report=report)
    if digest in known:
        record['known_actual_Android_getter_outcome']=known[digest]
        record['preflight_flags_known_getter_failure']=report['DECODER_COMPATIBILITY']['status']=='INCOMPATIBLE' if known[digest]=='FAIL' else None
        record['incorrect_rejection_of_successfully_executed_path']=known[digest]=='PASS' and (report['STRUCTURAL']['status'].startswith('REJECTED') or report['DECODER_COMPATIBILITY']['status']=='INCOMPATIBLE')
    results.append(record);save(base/'results.json',{'experimental_unit':'distinct artifact bytes × selected static preflight configuration; aliases retained, not independent models','fixtures':results})
    print(digest[:12],report['STRUCTURAL']['status'],report['DECODER_COMPATIBILITY']['status'],report.get('controller_error',''),flush=True)
