import pathlib,hashlib,json,datetime
ROOT=pathlib.Path(__file__).resolve().parents[1]
summary={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'P2 files except SDK links and writable emulator state; effective AVD config and getprop preserved under prerequisites; no build/model/library binary for source-only GitHub','excluded_top_level':['sdk'],'human_verification':'PENDING','frozen_input_verification':'all hashes recomputed before seal'}
frozen=json.loads((ROOT/'EXECUTION_INPUT_FREEZE.json').read_text());mismatch=[]
for row in frozen['files']:
 p=ROOT/row['path']
 if hashlib.sha256(p.read_bytes()).hexdigest()!=row['sha256']:mismatch.append(row['path'])
assert not mismatch,mismatch
(ROOT/'SEAL.json').write_text(json.dumps(summary,indent=2))
rows=[]
for p in sorted(ROOT.rglob('*')):
 relative=p.relative_to(ROOT)
 if relative.parts[0]=='sdk' or p.is_symlink() or not p.is_file() or relative.as_posix()=='SHA256SUMS':continue
 digest=hashlib.sha256(p.read_bytes()).hexdigest();rows.append(f'{digest}  {relative.as_posix()}\n')
(ROOT/'SHA256SUMS').write_text(''.join(rows))
print(json.dumps({'count':len(rows),'manifest_sha256':hashlib.sha256((ROOT/'SHA256SUMS').read_bytes()).hexdigest()},indent=2))
