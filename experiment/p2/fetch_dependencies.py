from pathlib import Path
import urllib.request,hashlib,json,zipfile,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1];D=R/'dependencies';D.mkdir(exist_ok=True)
coordinates=[('org.tensorflow','tensorflow-lite-task-vision','0.4.4','aar'),('org.tensorflow','tensorflow-lite-task-base','0.4.4','aar'),('org.tensorflow','tensorflow-lite-support-api','0.4.4','aar'),('com.google.auto.value','auto-value-annotations','1.6','jar')]
records=[]
for group,artifact,version,ext in coordinates:
    record={'coordinate':f'{group}:{artifact}:{version}','artifacts':[]}
    for suffix in ['pom',ext]:
        name=f'{artifact}-{version}.{suffix}';url=f'https://repo.maven.apache.org/maven2/{group.replace(".","/")}/{artifact}/{version}/{name}';p=D/name
        data=urllib.request.urlopen(url).read();p.write_bytes(data);record['artifacts'].append({'url':url,'path':str(p.relative_to(R)),'sha256':hashlib.sha256(data).hexdigest()})
        if suffix=='aar':
            with zipfile.ZipFile(p) as z:z.extractall(D/artifact)
    records.append(record)
(R/'dependencies/downloads.json').write_text(json.dumps(records,indent=2))
