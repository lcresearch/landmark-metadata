"""Replay the byte-preserved preflight checker with a catalog of real recovered files.

Only catalog/summarization orchestration is new. Existing evidence is reused after
SHA-256 validation; new core fixtures are added when --include-core is requested.
No synthetic outcomes or historical run records are imported.
"""
import argparse
import collections
import json
import pathlib
import sys
ROOT=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts'))
from common import sha,save
from preflight import check
parser=argparse.ArgumentParser();parser.add_argument('--include-core',action='store_true');parser.add_argument('--core-models',type=pathlib.Path);args=parser.parse_args()
OLD=ROOT.parent/'metadata-contract-paper';ANDROID=ROOT.parent/'repro-android';base=ROOT/'E5';base.mkdir(exist_ok=True)
fixtures={};known={}
def add(path,alias,baseline=None):
    digest=sha(path.read_bytes())
    if digest not in fixtures: fixtures[digest]={'model_sha256':digest,'path':str(path),'aliases':[],'baseline':str(baseline) if baseline else None}
    fixtures[digest]['aliases'].append(alias)
    if baseline and not fixtures[digest]['baseline']:fixtures[digest]['baseline']=str(baseline)
for component in json.loads((OLD/'results/static-suite.json').read_text()):
    if not component['variants']:
        add(OLD/component['path'],{'phase':'prior','component':component['id'],'variant':'no_metadata_original'});continue
    original=OLD/next(v for v in component['variants'] if v['variant']=='original')['path']
    for variant in component['variants']:
        add(OLD/variant['path'],{'phase':'prior','component':component['id'],'variant':variant['variant']},original if variant['variant']!='original' else None)
if args.include_core:
    for experiment in ['E1','E2']:
        original=ANDROID/experiment/'variants/original/model.tflite'
        variants=sorted((ANDROID/experiment/'variants').glob('*/model.tflite'))
        if not variants or not original.is_file():raise RuntimeError(f'{experiment} real variants unavailable')
        for path in variants:
            variant=path.parent.name
            add(path,{'phase':experiment,'component':'efficientnet','variant':variant},original if variant!='original' else None)
        results_path=ANDROID/experiment/'results.json'
        if results_path.is_file():
            for unit in json.loads(results_path.read_text())['units']:
                path=ANDROID/unit['artifact_paths']['model'];digest=sha(path.read_bytes())
                outcome=unit['decoder_status']
                if digest in known and known[digest]!=outcome:raise RuntimeError('Contradictory observed decoder outcomes')
                known[digest]=outcome
if args.core_models:
    original=args.core_models/'original.tflite'
    for variant in ['original','description_control','label_deletion','label_permutation','label_restoration']:
        path=args.core_models/f'{variant}.tflite'
        add(path,{'phase':'core_reconstructed_for_Task','component':'efficientnet','variant':variant,'Android_outcome_not_inferred':True},original if variant!='original' else None)
for row in json.loads((ROOT/'E4/results.json').read_text())['component_occurrences']:
    if row['status']=='CHECKED':
        add(ROOT/row['artifact_paths']['model'],{'phase':'E4_external','component':row['component_sha256'],'variant':'original','frozen_D':row['decoder_check']})
save(base/'evaluation-fixtures-before-run.json',list(fixtures.values()))
previous={}
if (base/'results.json').exists():previous={x['model_sha256']:x['report'] for x in json.loads((base/'results.json').read_text())['fixtures']}
results=[]
for digest,fixture in fixtures.items():
    if digest in previous:
        report=previous[digest]
        if report['artifact_sha256']!=digest or sha(pathlib.Path(report['model_path']).read_bytes())!=digest:raise RuntimeError('Saved fixture evidence digest mismatch')
    else:
        report=check(pathlib.Path(fixture['path']),base/'checks'/digest,baseline=pathlib.Path(fixture['baseline']) if fixture['baseline'] else None)
        print(digest[:12],report['STRUCTURAL']['status'],report['DECODER_COMPATIBILITY']['status'],report.get('controller_error',''),flush=True)
    record=dict(fixture,report=report)
    if digest in known:
        record['known_actual_Android_getter_outcome']=known[digest]
        record['preflight_flags_known_getter_failure']=report['DECODER_COMPATIBILITY']['status']=='INCOMPATIBLE' if known[digest]=='FAIL' else None
        record['incorrect_rejection_of_successfully_executed_path']=known[digest]=='PASS' and (report['STRUCTURAL']['status'].startswith('REJECTED') or report['DECODER_COMPATIBILITY']['status']=='INCOMPATIBLE')
    results.append(record)
    save(base/'results.json',{'experimental_unit':'distinct artifact bytes x unchanged historical preflight; aliases are not independent models','orchestration':'run_e5_incremental.py: new catalog and incremental reuse; check() is byte-preserved','includes_core_variants':bool(args.include_core or args.core_models),'uses_reconstructed_Task_models':bool(args.core_models),'fixtures':results})
summary={'distinct_fixtures':len(results),'includes_core_variants':bool(args.include_core or args.core_models),'uses_reconstructed_Task_models':bool(args.core_models),'structural_counts':dict(collections.Counter(x['report']['STRUCTURAL']['status'] for x in results)),'decoder_counts':dict(collections.Counter(x['report']['DECODER_COMPATIBILITY']['status'] for x in results)),'semantic_counts':dict(collections.Counter(x['report']['REFERENCE_BACKED_SEMANTIC']['status'] for x in results)),'controller_errors':sum('controller_error' in x['report'] for x in results),'known_Android_artifacts':len(known),'known_Android_getter_failures':sum(v=='FAIL' for v in known.values()),'known_failure_detection':None if 'FAIL' not in known.values() else all(x.get('preflight_flags_known_getter_failure') for x in results if x.get('known_actual_Android_getter_outcome')=='FAIL'),'incorrect_rejections_of_observed_successes':sum(x.get('incorrect_rejection_of_successfully_executed_path',False) for x in results)}
save(base/'replay-summary.json',summary);print(json.dumps(summary,indent=2))
