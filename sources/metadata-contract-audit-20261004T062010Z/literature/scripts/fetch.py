#!/usr/bin/env python3
import concurrent.futures, datetime, hashlib, json, pathlib, shutil, subprocess, urllib.request
ROOT=pathlib.Path(__file__).resolve().parents[1]
SOURCES=ROOT/'sources'
papers={
 'mlguard': ('2309.01379','10.1145/3617574.3617859'),
 'docter': ('2109.01002','10.1145/3533767.3534220'),
 'acetest': ('2305.17914','10.1145/3597926.3598088'),
 'dara': (None,'10.1007/s10664-025-10711-4'),
}
def get(url,path):
 r={'url':url,'path':str(path),'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (research literature audit)'}),timeout=50) as f:
   data=f.read(); r.update(final_url=f.geturl(),http_status=f.status,content_type=f.headers.get('Content-Type'))
  path.write_bytes(data);r.update(status='DOWNLOADED',bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
 except Exception as e:r.update(status='UNAVAILABLE',exception_type=type(e).__name__,exception_message=str(e))
 return r
jobs=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
 for name,(arxiv,doi) in papers.items():
  jobs.append(ex.submit(get,'https://api.crossref.org/works/'+doi,SOURCES/(name+'-crossref.json')))
  if arxiv:
   jobs.append(ex.submit(get,'https://arxiv.org/pdf/'+arxiv,SOURCES/(name+'.pdf')))
   jobs.append(ex.submit(get,'https://arxiv.org/abs/'+arxiv,SOURCES/(name+'-abstract.html')))
 records=[j.result() for j in jobs]
old=pathlib.Path('/workspace/metadata-contract-paper/sources/dara-paper.pdf')
new=SOURCES/'dara.pdf';shutil.copyfile(old,new)
records.append({'status':'COPIED_PRESERVED_EVIDENCE','source_path':str(old),'path':str(new),'sha256':hashlib.sha256(new.read_bytes()).hexdigest(),'bytes':new.stat().st_size})
for pdf in sorted(SOURCES.glob('*.pdf')):
 if pdf.read_bytes().startswith(b'%PDF'):
  for mode in ['reading','layout']:
   out=pdf.with_name(pdf.stem+'-'+mode+'.txt');cmd=['pdftotext']+(['-layout'] if mode=='layout' else [])+[str(pdf),str(out)]
   p=subprocess.run(cmd,capture_output=True,text=True);records.append({'command':cmd,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'path':str(out)})
  p=subprocess.run(['pdfinfo',str(pdf)],capture_output=True,text=True);pdf.with_suffix('.pdfinfo.txt').write_text(p.stdout+p.stderr)
(ROOT/'retrieval-results.json').write_text(json.dumps(records,indent=2)+'\n')
print(json.dumps(records,indent=2))
