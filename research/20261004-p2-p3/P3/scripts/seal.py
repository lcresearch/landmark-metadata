#!/usr/bin/env python3
import hashlib,pathlib
root=pathlib.Path(__file__).resolve().parents[1]
manifest=root/'SHA256SUMS'
assert not manifest.exists(),'Refuse to reseal an existing evidence manifest'
files=sorted(p for p in root.rglob('*') if p.is_file() and p!=manifest)
manifest.write_text(''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(root)}\n' for p in files))
print(len(files),'files; SHA256SUMS',hashlib.sha256(manifest.read_bytes()).hexdigest())
