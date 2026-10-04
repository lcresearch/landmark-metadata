"""Archive current official repository XML and select the exact tested versions."""
import argparse,hashlib,json,pathlib,urllib.request,xml.etree.ElementTree as ET
VERSIONS={'platforms;android-30':'3','build-tools;35.0.0':'35.0.0','platform-tools':'37.0.1','emulator':'37.2.12','system-images;android-30;default;x86_64':'11'}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',required=True,type=pathlib.Path);args=ap.parse_args();pre=args.root/'prerequisites';pre.mkdir(parents=True,exist_ok=True)
    lock=json.loads(pathlib.Path(__file__).with_name('android-prerequisites.lock.json').read_text());packages={p['id']:p for p in lock['sdk']};records=[]
    for record in lock['repository_metadata']:
        with urllib.request.urlopen(record['url'],timeout=60) as response:data=response.read()
        (pre/record['filename']).write_bytes(data);rows=[]
        for node in ET.fromstring(data):
            name=node.attrib.get('path')
            if name not in VERSIONS or node.find('channelRef').attrib['ref']!='channel-0':continue
            revision='.'.join(c.text for c in node.find('revision'))
            if revision!=VERSIONS[name]:continue
            wanted=packages[name]
            archives=[a for a in node.findall('archives/archive') if a.findtext('host-os') in [None,'linux']]
            if len(archives)!=1:raise ValueError('Unexpected archive count: '+name)
            complete=archives[0].find('complete')
            if complete.findtext('checksum')!=wanted['sha1'] or int(complete.findtext('size'))!=wanted['expected_bytes'] or complete.findtext('url')!=wanted['url'].rsplit('/',1)[1]:raise ValueError('Official XML archive differs from pinned identity: '+name)
            rows.append({'path':name,'xml':ET.tostring(node,encoding='unicode')})
        (pre/(record['filename'].removesuffix('.xml')+'-selected.json')).write_text(json.dumps(rows,indent=2))
        records.append({'url':record['url'],'sha256':hashlib.sha256(data).hexdigest(),'selected':[r['path'] for r in rows]})
    found={p for row in records for p in row['selected']}
    if found!=set(VERSIONS):raise ValueError('Required version absent from current metadata; use separately pinned verified archives: '+str(set(VERSIONS)-found))
    (pre/'official-xml-selection.json').write_text(json.dumps(records,indent=2));print('PASS: 5 exact package versions and archive identities from official XML')
if __name__=='__main__':main()
