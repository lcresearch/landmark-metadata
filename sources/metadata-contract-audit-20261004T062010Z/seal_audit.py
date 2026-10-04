#!/usr/bin/env python3
"""Seal completed audit files, excluding installed SDK/AVD and caches."""
import datetime, hashlib, json, os, pathlib
ROOT=pathlib.Path(__file__).resolve().parent
info={'sealed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'excluded':['rebuild/sdk/**','**/__pycache__/**','symlinks','root SHA256SUMS'],'human_verification':'PENDING','historical_evidence_modified':False,'current_todo':'/workspace/metadata-contract-next/TODO.md','todo_snapshot_sha256':hashlib.sha256((ROOT/'TODO.after.md').read_bytes()).hexdigest()}
assert pathlib.Path(info['current_todo']).read_bytes()==(ROOT/'TODO.after.md').read_bytes()
(ROOT/'SEAL_INFO.json').write_text(json.dumps(info,indent=2))
paths=[]
for folder,dirs,files in os.walk(ROOT,followlinks=False):
    base=pathlib.Path(folder)
    dirs[:]=[d for d in dirs if d!='__pycache__' and not (base/d).is_symlink() and (base/d).relative_to(ROOT).as_posix()!='rebuild/sdk']
    for name in files:
        p=base/name
        if p.is_symlink() or p==ROOT/'SHA256SUMS':continue
        paths.append(p)
rows=[]
for p in sorted(paths):
    with p.open('rb') as handle:h=hashlib.file_digest(handle,'sha256').hexdigest()
    rows.append(h+'  '+p.relative_to(ROOT).as_posix())
(ROOT/'SHA256SUMS').write_text('\n'.join(rows)+'\n')
print(json.dumps({'sealed_files':len(rows),'manifest_sha256':hashlib.sha256((ROOT/'SHA256SUMS').read_bytes()).hexdigest(),'excluded':info['excluded']}))
