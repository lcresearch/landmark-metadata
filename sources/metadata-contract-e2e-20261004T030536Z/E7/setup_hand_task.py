import json, pathlib, urllib.request
from common import ROOT, HAND, PYTHON, sha, save, run
base=ROOT/'E7';env=base/'venv'
requirements='''mediapipe==0.10.14
numpy==1.26.4
protobuf==4.25.3
opencv-contrib-python==4.10.0.84
jax==0.4.30
jaxlib==0.4.30
matplotlib==3.9.2
'''
(base/'requirements-selected.txt').write_text(requirements)
steps=[('venv',[PYTHON,'-m','venv',env]),
 ('download',[env/'bin/python','-m','pip','download','--only-binary=:all:','-r',base/'requirements-selected.txt','-d',base/'wheels']),
 ('install',[env/'bin/python','-m','pip','install','--no-index','--find-links',base/'wheels','-r',base/'requirements-selected.txt']),
 ('freeze',[env/'bin/python','-m','pip','freeze'])]
for name,command in steps:
    p=run(command,base/'setup-logs'/name,timeout=600)
    if p.returncode:save(base/'setup-status.json',{'status':'FAIL','stage':name,'exit_code':p.returncode});raise SystemExit(1)
    if name=='freeze':(base/'requirements.lock').write_bytes(p.stdout)
save(base/'wheels.json',[{'path':str(p.relative_to(ROOT)),'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size} for p in sorted((base/'wheels').glob('*.whl'))])
for name,url in [('thumb_up.jpg','https://storage.googleapis.com/mediapipe-assets/thumb_up.jpg'),('release-asset-hand_landmarker.task','https://storage.googleapis.com/mediapipe-assets/hand_landmarker.task')]:
    try:
        with urllib.request.urlopen(url,timeout=45) as response:data=response.read()
        (base/name).write_bytes(data);save(base/(name+'.provenance.json'),{'url':url,'sha256':sha(data),'bytes':len(data),'status':'DOWNLOADED'})
    except Exception as exc:
        save(base/(name+'.provenance.json'),{'url':url,'status':'FAIL','exception':repr(exc)})
        if name=='thumb_up.jpg':raise
save(base/'setup-status.json',{'status':'PASS'})
