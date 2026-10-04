"""Seal and package this manuscript revision; do not touch experiment evidence."""
import hashlib
import json
import pathlib
import zipfile

root = pathlib.Path(__file__).resolve().parents[1]
manifest = root/'SHA256SUMS'
archive = root.with_suffix('.zip')
if manifest.exists() or archive.exists():
    raise SystemExit('Revision already sealed; create a new revision rather than overwrite.')
paths = sorted(p for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts)
lines = []
for p in paths:
    digest = hashlib.sha256(p.read_bytes()).hexdigest()
    lines.append(f'{digest}  {p.relative_to(root)}')
manifest.write_text('\n'.join(lines)+'\n')
with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED) as z:
    for p in paths+[manifest]:
        info = zipfile.ZipInfo(str(pathlib.Path(root.name)/p.relative_to(root)),(2026,10,4,0,0,0))
        info.compress_type=zipfile.ZIP_DEFLATED
        z.writestr(info,p.read_bytes())
digest=hashlib.sha256(archive.read_bytes()).hexdigest()
archive.with_suffix('.zip.sha256').write_text(f'{digest}  {archive.name}\n')
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    for p in paths+[manifest]:
        assert z.read(str(pathlib.Path(root.name)/p.relative_to(root)))==p.read_bytes()
print(json.dumps({'manifest_entries':len(paths),'archive':str(archive),
                  'archive_bytes':archive.stat().st_size,'archive_sha256':digest,
                  'scope':'Manuscript/source/reviews/claim map only; underlying experiment package is separately preserved.'},indent=2))
