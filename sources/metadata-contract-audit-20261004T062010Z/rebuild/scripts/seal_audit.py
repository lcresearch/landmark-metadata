from pathlib import Path
from hashlib import sha256
import json
root=Path(__file__).resolve().parents[1]
# SDK installation is reused read-only; mutable AVD disk images are not durable experimental records.
# Preserve the final new AVD configuration separately, while omitting image/runtime scratch state.
items=[]
for p in sorted(root.rglob('*')):
    rel=p.relative_to(root)
    if not p.is_file() or p.is_symlink() or rel.parts[0]=='sdk' or p.name in ['SHA256SUMS','SEAL.json'] or '__pycache__' in rel.parts:continue
    items.append((sha256(p.read_bytes()).hexdigest(),rel.as_posix()))
(root/'SHA256SUMS').write_text(''.join(h+'  '+p+'\n' for h,p in items))
(root/'SEAL.json').write_text(json.dumps({'files':len(items),'sha256sums_sha256':sha256((root/'SHA256SUMS').read_bytes()).hexdigest(),'excluded':'sdk/ reused symlink installation and new mutable AVD; Python caches; manifest and seal itself','human_audit':'PENDING'},indent=2))
print(len(items))
