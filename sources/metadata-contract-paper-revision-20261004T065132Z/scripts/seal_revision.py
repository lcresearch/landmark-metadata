"""Create and verify the revision manifest once, excluding only itself."""
from pathlib import Path
import hashlib
import json

root = Path(__file__).resolve().parents[1]
manifest = root/'SHA256SUMS'

def sha(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()

files = sorted(p for p in root.rglob('*') if p.is_file() and p != manifest)
with manifest.open('x') as f:
    for path in files:
        f.write(f'{sha(path)}  {path.relative_to(root)}\n')
for line in manifest.read_text().splitlines():
    digest, name = line.split(maxsplit=1)
    assert sha(root/name) == digest, name
print(json.dumps({'status':'PASS', 'file_count':len(files), 'manifest_sha256':sha(manifest), 'manifest_path':str(manifest)}, indent=2))
