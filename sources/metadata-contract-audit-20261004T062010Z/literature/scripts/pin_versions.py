#!/usr/bin/env python3
import concurrent.futures, hashlib, json, pathlib, urllib.request
ROOT=pathlib.Path(__file__).resolve().parents[1]
versions={'mlguard':'2309.01379v1','docter':'2109.01002v4','acetest':'2305.17914v2'}
def one(pair):
 name,version=pair;url='https://arxiv.org/pdf/'+version;out=ROOT/'sources'/(name+'-version-pinned.pdf')
 r={'paper':name,'version':version,'url':url,'path':str(out)}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (research literature audit)'}),timeout=40) as f:data=f.read();r.update(final_url=f.geturl(),http_status=f.status)
  out.write_bytes(data);r.update(status='DOWNLOADED',sha256=hashlib.sha256(data).hexdigest(),bytes=len(data),identical_to_reviewed_pdf=data==(ROOT/'sources'/(name+'.pdf')).read_bytes())
 except Exception as e:r.update(status='UNAVAILABLE',exception_type=type(e).__name__,exception_message=str(e))
 return r
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:results=list(ex.map(one,versions.items()))
(ROOT/'version-pinning.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
