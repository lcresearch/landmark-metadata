#!/usr/bin/env python3
"""Archive bounded P3 requests; never interpret a model name as artifact identity."""
import concurrent.futures, datetime, hashlib, json, pathlib, platform, sys, urllib.error, urllib.request
ROOT=pathlib.Path(__file__).resolve().parents[1]
def sha(b): return hashlib.sha256(b).hexdigest()
def fetch(t):
    out=ROOT/'retrieved'/t['id']; out.mkdir(exist_ok=False)
    row=dict(t,started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
    redirects=[]
    class Redirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self,req,fp,code,msg,headers,newurl):
            redirects.append({'from':req.full_url,'status':code,'to':newurl})
            return super().redirect_request(req,fp,code,msg,headers,newurl)
    opener=urllib.request.build_opener(Redirect())
    try:
        try: response=opener.open(urllib.request.Request(t['url'],headers={'User-Agent':'MetadataContractResearch/1.0'}),timeout=45)
        except urllib.error.HTTPError as exc: response=exc
        with response:
            body=response.read(150*1024*1024+1)
            row.update(status=response.status,final_url=response.url,headers=dict(response.headers))
        if len(body)>150*1024*1024: raise ValueError('Response exceeds predeclared operational 150 MiB cap')
        (out/'body').write_bytes(body)
        row.update(bytes=len(body),sha256=sha(body),body_path=str((out/'body').relative_to(ROOT)))
    except Exception as exc: row.update(error=repr(exc))
    row.update(redirects=redirects,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
    (out/'retrieval.json').write_text(json.dumps(row,indent=2)+'\n')
    print(t['id'],row.get('status'),row.get('bytes'),row.get('sha256'),row.get('error',''),flush=True)
    return row
if __name__=='__main__':
    plan=pathlib.Path(sys.argv[1]); targets=json.loads(plan.read_text())
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: results=list(pool.map(fetch,targets))
    (ROOT/'analysis'/f'{plan.stem}-results.json').write_text(json.dumps({'python':sys.version,'platform':platform.platform(),'request_plan':str(plan),'request_plan_sha256':sha(plan.read_bytes()),'results':results},indent=2)+'\n')
