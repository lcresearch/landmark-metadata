import argparse, hashlib, json, pathlib, shutil
from common import ROOT, save
ap=argparse.ArgumentParser();ap.add_argument('--experiment',required=True);args=ap.parse_args()
folder=ROOT/args.experiment
if (folder/'SHA256SUMS').exists():raise SystemExit('Already sealed; do not overwrite')
snapshot=folder/'implementation-snapshot';snapshot.mkdir()
for name in ['common.py','prepare_e1.py','codegen_one.py','build_android.py','run_android.py','ContractInstrumentation.java','summarize_android.py','prepare_e2.py']:
    src=ROOT/'scripts'/name
    if src.exists():shutil.copyfile(src,snapshot/name)
for suffix in ['PLAN','RESULTS']:
    src=ROOT/f'EXPERIMENT_{args.experiment}_{suffix}.md'
    if src.exists():shutil.copyfile(src,folder/src.name)
lines=[];records=[]
for p in sorted(folder.rglob('*')):
    if not p.is_file() or any(part in p.parts for part in ['__pycache__','venv','.venv']):continue
    h=hashlib.file_digest(p.open('rb'),'sha256').hexdigest();rel=str(p.relative_to(folder))
    lines.append(f'{h}  {rel}');records.append({'path':rel,'bytes':p.stat().st_size,'sha256':h})
(folder/'SHA256SUMS').write_text('\n'.join(lines)+'\n')
print(args.experiment,'sealed files',len(records),'manifest sha256',hashlib.sha256((folder/'SHA256SUMS').read_bytes()).hexdigest())
