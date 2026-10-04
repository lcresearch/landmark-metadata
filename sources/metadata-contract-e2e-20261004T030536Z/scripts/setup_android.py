"""Archive and install exactly selected Android prerequisites (no model execution)."""
import concurrent.futures, hashlib, json, os, pathlib, shutil, urllib.request, xml.etree.ElementTree as E, zipfile
ROOT=pathlib.Path(__file__).resolve().parents[1]
PRE=ROOT/'prerequisites'; SDK=ROOT/'sdk'
PRE.mkdir(exist_ok=True); SDK.mkdir(exist_ok=True)
downloads=PRE/'downloads'; downloads.mkdir(exist_ok=True)
tasks=[]
for key,base in [('repository','https://dl.google.com/android/repository/'),('system-images','https://dl.google.com/android/repository/sys-img/android/')]:
    for row in json.loads((PRE/(key+'-selected.json')).read_text()):
        x=E.fromstring(row['xml'])
        if x.find('channelRef').attrib['ref']!='channel-0': continue
        for archive in x.findall('archives/archive'):
            if archive.findtext('host-os') not in [None,'linux']: continue
            c=archive.find('complete')
            target={'platforms;android-30':'platforms/android-30','build-tools;35.0.0':'build-tools/35.0.0','platform-tools':'platform-tools','emulator':'emulator','system-images;android-30;default;x86_64':'system-images/android-30/default/x86_64'}[row['path']]
            tasks.append({'id':row['path'],'url':base+c.findtext('url'),'sha1':c.findtext('checksum'),'expected_bytes':int(c.findtext('size')),'target':target,'kind':'sdk'})
for artifact,version in [('tensorflow-lite','2.13.0'),('tensorflow-lite-api','2.13.0'),('tensorflow-lite-support','0.4.4'),('tensorflow-lite-support-api','0.4.4')]:
    base=f'https://repo.maven.apache.org/maven2/org/tensorflow/{artifact}/{version}/{artifact}-{version}'
    tasks.append({'id':f'{artifact}:{version}','url':base+'.aar','kind':'aar','target':artifact})
    tasks.append({'id':f'{artifact}:{version}:pom','url':base+'.pom','kind':'pom'})

def download(t):
    record=dict(t); p=downloads/t['url'].rsplit('/',1)[1]
    try:
        if not p.exists():
            with urllib.request.urlopen(t['url'],timeout=90) as r, p.with_suffix(p.suffix+'.partial').open('wb') as out:
                shutil.copyfileobj(r,out)
            p.with_suffix(p.suffix+'.partial').rename(p)
        data=p.read_bytes();record.update(path=str(p.relative_to(ROOT)),bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
        if 'sha1' in t: assert hashlib.sha1(data).hexdigest()==t['sha1'] and len(data)==t['expected_bytes']
        record['status']='DOWNLOADED'
        if t['kind']=='sdk':
            dest=SDK/t['target'];dest.mkdir(parents=True,exist_ok=True)
            with zipfile.ZipFile(p) as z:
                prefix=z.namelist()[0].split('/')[0]+'/'
                for info in z.infolist():
                    if not info.filename.startswith(prefix):raise ValueError('Unexpected ZIP root')
                    rel=info.filename[len(prefix):]
                    if not rel:continue
                    file=dest/rel
                    if '..' in pathlib.Path(rel).parts:raise ValueError('unsafe ZIP path')
                    if info.is_dir():file.mkdir(parents=True,exist_ok=True)
                    else:
                        file.parent.mkdir(parents=True,exist_ok=True);file.write_bytes(z.read(info))
                        mode=(info.external_attr>>16)&0o777
                        if mode: file.chmod(mode)
        elif t['kind']=='aar':
            dest=PRE/'aar'/t['target'];dest.mkdir(parents=True,exist_ok=True)
            with zipfile.ZipFile(p) as z:z.extractall(dest)
            old=pathlib.Path('/workspace/hand-contract-repro/deps')/(p.stem+'.jar')
            if old.exists():
                record['classes_match_preserved_jar']=(dest/'classes.jar').read_bytes()==old.read_bytes()
                assert record['classes_match_preserved_jar']
        print(t['id'],record['status'],record['sha256'],flush=True)
    except Exception as exc:
        record.update(status='FAIL',error=repr(exc));print(t['id'],'FAIL',repr(exc),flush=True)
    return record

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(download,tasks))
(PRE/'downloads.json').write_text(json.dumps(results,indent=2))
if any(x['status']=='FAIL' for x in results):raise SystemExit(1)
