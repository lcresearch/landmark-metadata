from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'MANIFEST.json').read_text())
for item in manifest['files']:
    p=ROOT/item['path']
    assert p.is_file(),f'Missing {p}'
    with p.open('rb') as f:actual=hashlib.file_digest(f,'sha256').hexdigest()
    assert actual==item['sha256'],f'Changed {p}'
print('Verified',len(manifest['files']),'archived files')
