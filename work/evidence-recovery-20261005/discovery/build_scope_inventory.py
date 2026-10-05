#!/usr/bin/env python3
"""Read saved trees, inventory proposed HA01-HA07 selection. Does not copy evidence."""
from pathlib import Path
import json,hashlib,collections,stat
out=Path('/workspace/evidence-recovery-20261005T170453Z/scope')
roots={
 'E':Path('/workspace/metadata-contract-e2e-20261004T030536Z'),
 'A':Path('/workspace/metadata-contract-audit-20261004T062010Z'),
 'F':Path('/workspace/metadata-contract-p2p3-20261004T073824Z')}
include_trees={'E':['E1','E2','phase0','scripts','verification'],
 'A':['preservation','rebuild','verification'],
 'F':['P2','P3','review','verification','scripts']}
excluded_parts={'sdk','venv','.venv','__pycache__','.git'}
excluded_binary_suffixes={'.aar','.jar','.so','.whl','.zip','.tar','.gz','.xz','.exe','.bin'}
rows=[]; omitted=[]
for key,root in roots.items():
 candidates=set(p for p in root.iterdir() if p.is_file())
 for rel in include_trees[key]:
  candidates.update(p for p in (root/rel).rglob('*') if p.is_file() or p.is_symlink())
 if key=='E':candidates.update(p for p in (root/'prerequisites').rglob('*') if p.is_file())
 for p in sorted(candidates):
  r=p.relative_to(root);parts=r.parts;reason=None
  if p.is_symlink():reason='symlink; do not follow outside selected scope'
  elif excluded_parts.intersection(parts):reason='SDK/AVD/installed environment/cache excluded'
  elif p.suffix in {'.keystore','.jks','.pem','.key'}:reason='signing key/credential excluded'
  elif p.name in {'unsigned.apk','aligned.apk'}:reason='redundant packaging intermediate; keep signed final APK and all build records'
  elif 'prerequisites' in parts or 'dependencies' in parts:
   if p.suffix in excluded_binary_suffixes or p.name=='R.txt' or 'headers' in parts:reason='dependency/toolchain payload excluded; retain identity/configuration records'
   if 'downloads' in parts or 'python-wheels' in parts or 'preserved-jars' in parts or 'extra-jars' in parts:reason='dependency/toolchain payload excluded; retain sibling identity/configuration records'
  if p.suffix=='.pyc':reason='cache excluded'
  entry={'family':key,'path':str(p),'relative_to_family':r.as_posix(),'bytes':p.lstat().st_size}
  if reason:entry['reason']=reason;omitted.append(entry)
  else:rows.append(entry)
selected={r['path'] for r in rows}
manifest_reports=[]
for key,root in roots.items():
 for m in sorted(root.rglob('SHA256SUMS')):
  if str(m) not in selected and m!=root/'SHA256SUMS':continue
  entries=[];outside=[];missing=[]
  for n,line in enumerate(m.read_text().splitlines(),1):
   expected,name=line.split(None,1);q=Path(name.lstrip('*'));q=q if q.is_absolute() else m.parent/q
   if not q.is_relative_to(root):outside.append(str(q))
   if not q.exists():missing.append(str(q))
   entries.append({'line':n,'path':str(q),'included':str(q) in selected})
  manifest_reports.append({'path':str(m),'sha256':hashlib.sha256(m.read_bytes()).hexdigest(),'bytes':m.stat().st_size,'entries':len(entries),'included_entries':sum(e['included'] for e in entries),'outside_family_root':outside,'missing_at_original_path':missing,'entry_byte_verification_performed':False,'excluded_entry_paths':[e['path'] for e in entries if not e['included']]})
summary={k:{'files':sum(x['family']==k for x in rows),'bytes':sum(x['bytes'] for x in rows if x['family']==k)} for k in roots}
obj={'scope':'Candidate exact HA01-HA07 saved-evidence selection, not a copied package or bulk byte verification. All keys/SDK/venv/dependency binaries excluded. Sign/keytool command records require the packager secret review before staging. Original artifacts are never modified.', 'roots':{k:str(v) for k,v in roots.items()},'summary':summary,'selected':rows,'excluded':omitted,'historical_manifests':manifest_reports,'interpretation':'All selected historical manifests remain byte-preserved but intentionally cover omitted entries; use a new complete relative-path package manifest. A manifest hash alone does not verify its entries.'}
(out/'focal-scope-inventory.json').write_text(json.dumps(obj,indent=2)+'\n')
(out/'focal-selected-paths.txt').write_text(''.join(x['path']+'\n' for x in rows))
(out/'focal-excluded-paths.json').write_text(json.dumps(omitted,indent=2)+'\n')
print(json.dumps({'summary':summary,'total_files':len(rows),'total_bytes':sum(x['bytes'] for x in rows),'excluded_candidates':len(omitted),'manifests':[{k:v for k,v in x.items() if k!='excluded_entry_paths'} for x in manifest_reports]},indent=2))
