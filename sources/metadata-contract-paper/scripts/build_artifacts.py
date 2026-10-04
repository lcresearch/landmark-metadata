from pathlib import Path
import datetime
import hashlib
import json
import zipfile

ROOT=Path(__file__).resolve().parents[1]

def digest(path):
    with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def main():
    files=[]
    for folder in ['models','runs','scripts','results','logs','sources','hand-evidence','manuscript']:
        for p in (ROOT/folder).rglob('*'):
            if not p.is_file() or '__pycache__' in p.parts or 'preview' in p.parts:continue
            if folder=='manuscript' and p.suffix in ['.aux','.fls','.fdb_latexmk','.out']:continue
            files.append(p)
    files.extend(ROOT/f for f in ['protocol.json','protocol-freeze.json','contracts.json','requirements.lock','REPRODUCE.txt','研究说明.txt'])
    files=sorted(set(files));stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
    entries=[{'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':digest(p)} for p in files]
    manifest={'created_utc':stamp,'scope':'Preserved claim-relevant workspace evidence, including large model and numerical files. Generated checker demonstration directories and page-preview images are not study evidence. This manifest does not imply all payloads are included in the lightweight archive.','files':entries}
    (ROOT/'WORKSPACE-EVIDENCE-MANIFEST.json').write_text(json.dumps(manifest,indent=2))
    selected=[]
    for p in files:
        if p.suffix in ['.tflite','.task','.npz','.f32']:continue
        if p.suffix=='.pdf' and p!=ROOT/'manuscript/paper.pdf':continue
        if p.name in ['dara-paper.txt','aibom-paper.txt','tflite-support-tree.json']:continue
        if '-reference.' in p.name:continue
        selected.append(p)
    selected.append(ROOT/'WORKSPACE-EVIDENCE-MANIFEST.json')
    light={'created_utc':stamp,'scope':'Files actually contained in the lightweight paper/source archive; see REPRODUCE.txt for omitted raw payloads and restore requirements.',
      'files':[{'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':digest(p)} for p in selected]}
    (ROOT/'ARCHIVE-MANIFEST.json').write_text(json.dumps(light,indent=2))
    selected.append(ROOT/'ARCHIVE-MANIFEST.json')
    archive=ROOT.parent/'metadata-contract-paper-sources.zip'
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in selected:z.write(p,arcname='metadata-contract-paper/'+str(p.relative_to(ROOT)))
    checksum=digest(archive)
    (ROOT.parent/'metadata-contract-paper-sources.sha256').write_text(checksum+'  '+archive.name+'\n')
    print(json.dumps({'archive':str(archive),'bytes':archive.stat().st_size,'sha256':checksum,'archived_files':len(selected),'workspace_evidence_files':len(files)},indent=2))

if __name__=='__main__':main()
