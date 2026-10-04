"""Compare maintained checker judgments with fresh retained fixtures and Java counterexamples."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
sys.dont_write_bytecode = True

from preflight import check
from evidence_validation import (required_fixture_digests, require_exact_identities,
                                 require_fixture_digest)

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--catalog',type=Path,default=Path('/workspace/repro-external/E5/results.json'))
parser.add_argument('--counterexamples',type=Path,default=Path('/workspace/repro-audit/independent-audit/label-parser'))
parser.add_argument('--output-dir',required=True,type=Path)
# Frozen catalog digest recorded by claims/claim-map.json, claim C32, in 3809a71.
parser.add_argument('--required-manifest',type=Path,
                    default=Path('/workspace/repro-external/E5/results.json'),
                    help='Frozen original catalog, or JSON with the 65 original artifact_sha256s')
parser.add_argument('--required-manifest-sha256',
                    default='bf49a475696eec4b38fb17587f6541a8393da14297e5dca1d433a051ba166e79',
                    help='Previously recorded digest; default pins claim C32 original E5 catalog')
args=parser.parse_args()
out=args.output_dir.resolve()
repo=Path(__file__).resolve().parents[3]
if out.is_relative_to(repo):raise ValueError('Evidence must stay outside the repository')
out.mkdir(parents=True,exist_ok=False)
rows=[]
fixtures=json.loads(args.catalog.read_text())['fixtures']
required=required_fixture_digests(args.required_manifest,args.required_manifest_sha256)
require_exact_identities((f['model_sha256'] for f in fixtures),required,'Original fixtures')
for fixture in fixtures:
    require_fixture_digest(fixture)
for fixture in fixtures:
    path=Path(fixture['path']);baseline=Path(fixture['baseline']) if fixture.get('baseline') else None
    current=check(path,out/'fixtures'/fixture['model_sha256'],baseline=baseline)
    require_fixture_digest(fixture,current)
    previous=fixture['report']
    same=all(current[key]['status']==previous[key]['status'] for key in ['STRUCTURAL','REFERENCE_BACKED_SEMANTIC','DECODER_COMPATIBILITY','PRESERVATION'])
    same=same and current['DECODER_COMPATIBILITY']['findings']==previous['DECODER_COMPATIBILITY']['findings']
    rows.append({'fixture':fixture['model_sha256'],'passed':same and 'controller_error' not in current,'kind':'retained-fixture'})
for name,expected,count in [('original','COMPATIBLE_PRECONDITIONS',1000),('lf_replaced_by_vertical_tab','INCOMPATIBLE',999),('unicode_separator_inside_first_label','COMPATIBLE_PRECONDITIONS',1000)]:
    model=args.counterexamples/name/'model.tflite'
    report=check(model,out/'counterexamples'/name/'preflight')
    findings=report['DECODER_COMPATIBILITY']['findings']
    passed=report['DECODER_COMPATIBILITY']['status']==expected and len(findings)==1 and findings[0]['label_count']==count
    rows.append({'fixture':name,'passed':passed,'kind':'actual-Java-counterexample'})
    dest=out/'counterexamples'/name/'baseline'
    worker=subprocess.run([sys.executable,str(Path(__file__).with_name('baseline.py')),'simple_baseline',str(model),str(dest)],capture_output=True)
    (dest/'stdout.txt').write_bytes(worker.stdout);(dest/'stderr.txt').write_bytes(worker.stderr)
    baseline=json.loads((dest/'result.json').read_text())
    rows.append({'fixture':name,'passed':baseline['status']==expected and worker.returncode==(2 if expected=='INCOMPATIBLE' else 0),'kind':'baseline-counterexample'})
result={'retained_fixtures':len(fixtures),'counterexamples':3,'passed':sum(r['passed'] for r in rows),'failed':sum(not r['passed'] for r in rows),'checks':rows}
(out/'result.json').write_text(json.dumps(result,indent=2))
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
if any(not r['passed'] for r in rows):raise SystemExit(1)
