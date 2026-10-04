import concurrent.futures
import datetime
import hashlib
import io
import json
from pathlib import Path
import urllib.request
import zipfile

ROOT=Path(__file__).resolve().parents[1]

def sha(data):return hashlib.sha256(data).hexdigest()

def main():
    protocol=json.loads((ROOT/'protocol.json').read_text())
    results=[]
    def fetch(target):
        row=dict(target,started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
        try:
            with urllib.request.urlopen(target['url'],timeout=60) as response:
                data=response.read();row.update(status=response.status,headers=dict(response.headers),resolved_url=response.url)
            path=ROOT/'models'/target['id']/target['url'].rsplit('/',1)[-1]
            path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
            row.update(sha256=sha(data),bytes=len(data),path=str(path.relative_to(ROOT)))
            row['components']=[]
            def unpack(content,member):
                if member.endswith('.tflite'):
                    digest=sha(content);dest=ROOT/'models/components'/f'{digest}.tflite'
                    dest.parent.mkdir(exist_ok=True);dest.write_bytes(content)
                    row['components'].append({'member':member,'sha256':digest,'bytes':len(content),'path':str(dest.relative_to(ROOT))})
                elif member.endswith('.task'):
                    with zipfile.ZipFile(io.BytesIO(content)) as z:
                        for n in sorted(z.namelist()):
                            if n.endswith(('.tflite','.task')):unpack(z.read(n),member+'!'+n)
            unpack(data,path.name)
        except Exception as exc:row['error']=repr(exc)
        print(target['id'],row.get('status'),len(row.get('components',[])),row.get('error',''),flush=True)
        return row
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        results=list(executor.map(fetch,protocol['targets']))
    (ROOT/'results/downloads.json').write_text(json.dumps(results,indent=2))
    unique={}
    for row in results:
        for component in row.get('components',[]):
            dest=unique.setdefault(component['sha256'],{'sha256':component['sha256'],'path':component['path'],'bytes':component['bytes'],'occurrences':[]})
            dest['occurrences'].append({'target':row['id'],'member':component['member']})
    (ROOT/'results/components.json').write_text(json.dumps(list(unique.values()),indent=2))
    print('Downloaded targets',sum('error' not in x for x in results),'component occurrences',sum(len(x.get('components',[])) for x in results),'unique components',len(unique))

if __name__=='__main__':main()
