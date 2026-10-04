"""Restore fixed Android prerequisites, preserving TLS and artifact verification.

Run with --verify-cache to independently validate a retained download cache.
No secrets, model assets, generated output or installed dependencies belong in Git.
"""
import argparse,hashlib,json,pathlib,shutil,tarfile,urllib.request,xml.etree.ElementTree as ET,zipfile,datetime

def checked_download(url,path,sha256,sha1=None,size=None,verify_only=False):
    if not path.exists():
        if verify_only: raise FileNotFoundError(path)
        partial=path.with_name(path.name+'.partial')
        with urllib.request.urlopen(url,timeout=180) as response,partial.open('wb') as out:
            shutil.copyfileobj(response,out)
        partial.replace(path)
    data=path.read_bytes()
    if hashlib.sha256(data).hexdigest()!=sha256: raise ValueError('SHA256 mismatch: '+path.name)
    if sha1 and hashlib.sha1(data).hexdigest()!=sha1: raise ValueError('SHA1 mismatch: '+path.name)
    if size is not None and len(data)!=size: raise ValueError('Size mismatch: '+path.name)
    return data

def unpack_zip(path,destination,strip_root=False):
    destination.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(path) as archive:
        prefix=archive.namelist()[0].split('/')[0]+'/' if strip_root else ''
        for info in archive.infolist():
            if not info.filename.startswith(prefix): raise ValueError('Unexpected ZIP root')
            relative=pathlib.PurePosixPath(info.filename[len(prefix):])
            if relative.is_absolute() or '..' in relative.parts: raise ValueError('Unsafe ZIP path')
            if str(relative)=='.': continue
            target=destination/pathlib.Path(relative)
            if info.is_dir(): target.mkdir(parents=True,exist_ok=True)
            else:
                target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(archive.read(info))
                mode=(info.external_attr>>16)&0o777
                if mode: target.chmod(mode)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=pathlib.Path,required=True);ap.add_argument('--hand',type=pathlib.Path,required=True);ap.add_argument('--verify-cache',action='store_true');ap.add_argument('--repo',type=pathlib.Path,default=next((p for p in pathlib.Path(__file__).resolve().parents if (p/'.git').is_file() or (p/'.git/HEAD').is_file()),pathlib.Path('/workspace/landmark-metadata')));args=ap.parse_args()
    repo=args.repo.resolve()
    for label,path in [('root',args.root),('hand',args.hand)]:
        target=path.resolve()
        if target.is_relative_to(repo) or repo.is_relative_to(target):raise ValueError(f'{label} must be outside the repository and cannot contain it: {target}')
    lock=json.loads(pathlib.Path(__file__).with_name('android-prerequisites.lock.json').read_text());pre=args.root/'prerequisites';downloads=pre/'downloads';downloads.mkdir(parents=True,exist_ok=True)
    started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
    (pre/'prerequisite-integrity-check.json').write_text(json.dumps({'status':'RUNNING','started_utc':started_utc},indent=2))
    checks=[]
    for row in lock['sdk']:
        archive=downloads/row['url'].rsplit('/',1)[1]
        checked_download(row['url'],archive,row['sha256'],row['sha1'],row['expected_bytes'],args.verify_cache)
        if not args.verify_cache: unpack_zip(archive,args.root/'sdk'/row['target'],True)
        checks.append({'artifact':row['id'],'sha256':row['sha256'],'status':'PASS'})
    jdk=lock['jdk'];archive=downloads/jdk['url'].rsplit('/',1)[1]
    checked_download(jdk['url'],archive,jdk['sha256'],verify_only=args.verify_cache)
    if not args.verify_cache:
        target=args.hand/'toolchains';target.mkdir(parents=True,exist_ok=True)
        with tarfile.open(archive) as bundle:
            for member in bundle.getmembers():
                if not (target/member.name).resolve().is_relative_to(target.resolve()):raise ValueError('Unsafe JDK tar member')
            bundle.extractall(target,filter='data')
    checks.append({'artifact':'Temurin '+jdk['directory'],'sha256':jdk['sha256'],'status':'PASS'})
    for row in lock['java_dependencies']:
        archive=downloads/row['url'].rsplit('/',1)[1]
        data=checked_download(row['url'],archive,row['sha256'],row['sha1'],verify_only=args.verify_cache)
        jar=zipfile.ZipFile(archive).read('classes.jar') if archive.suffix=='.aar' else data
        if hashlib.sha256(jar).hexdigest()!=row['jar_sha256']:raise ValueError('Java classes mismatch: '+archive.name)
        if not args.verify_cache:
            target=pre/'extra-jars' if row['destination']=='extra-jars' else args.hand/'deps';target.mkdir(parents=True,exist_ok=True);(target/row['jar_filename']).write_bytes(jar)
            if archive.suffix=='.aar' and row['destination']=='hand-deps':
                artifact=row['jar_filename'].rsplit('-',1)[0];unpack_zip(archive,pre/'aar'/artifact)
        checks.append({'artifact':row['jar_filename'],'sha256':row['sha256'],'status':'PASS'})
    (pre/'prerequisite-integrity-check.json').write_text(json.dumps({'status':'PASS','started_utc':started_utc,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'mode':'verify-cache' if args.verify_cache else 'restore','checks':checks},indent=2))
    print('PASS:',len(checks),'fixed SDK/JDK/Java archives; SHA256, available official SHA1, SDK size and extracted Java classes verified')

if __name__=='__main__':main()
