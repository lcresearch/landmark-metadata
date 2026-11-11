import argparse, json, pathlib, shutil, sys, zipfile
from common import ROOT, HAND, JDK, sha, save, run

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--experiment',required=True);args=ap.parse_args()
    sdk=ROOT/'sdk';bt=sdk/'build-tools/35.0.0';platform=sdk/'platforms/android-30/android.jar'
    deps=[p for p in sorted((HAND/'deps').glob('*.jar')) if not p.name.startswith('android-')]
    # Include declared image API dependency when present; this harness uses TensorImage(Bitmap).
    deps+=list((ROOT/'prerequisites/extra-jars').glob('*.jar'))
    rows=json.loads((ROOT/args.experiment/'static-results.json').read_text());results=[]
    keystore=ROOT/'prerequisites/research-debug.keystore'
    if not keystore.exists():
        p=run([JDK/'bin/keytool','-genkeypair','-keystore',keystore,'-storepass','android','-alias','research','-keypass','android','-keyalg','RSA','-keysize','2048','-validity','3650','-dname','CN=Local Research Instrumentation'],ROOT/'prerequisites/keytool')
        if p.returncode:raise SystemExit('Failed to create disposable test signing key')
    for row in rows:
        folder=ROOT/args.experiment/'variants'/row['variant'];build=folder/'build';build.mkdir(exist_ok=False)
        record={'variant':row['variant'],'source_modified':False,'dependencies':{str(p):sha(p.read_bytes()) for p in deps},'stages':{}}
        def stage(name,command,timeout=180):
            p=run(command,build/'logs'/name,timeout=timeout)
            record['stages'][name]={'status':'PASS' if p.returncode==0 else 'FAIL','exit_code':p.returncode}
            if p.returncode!=0:
                record['earliest_failing_stage']=name
                raise RuntimeError(name)
            return p
        try:
            source=folder/'generated/src/main/java/org/example/contract/ContractModel.java'
            classes=build/'classes';classes.mkdir();classpath=':'.join(map(str,[platform,*deps]))
            stage('compile',[JDK/'bin/javac','--release','8','-cp',classpath,'-d',classes,source,ROOT/'scripts/ContractInstrumentation.java'])
            record['generated_class_hashes']={str(p.relative_to(classes)):sha(p.read_bytes()) for p in sorted(classes.rglob('ContractModel*.class'))}
            record['harness_class_sha256']=sha((classes/'org/example/contract/ContractInstrumentation.class').read_bytes())
            program=build/'program.jar'
            with zipfile.ZipFile(program,'w') as z:
                for p in sorted(classes.rglob('*.class')):
                    z.writestr(zipfile.ZipInfo(str(p.relative_to(classes)),(1980,1,1,0,0,0)),p.read_bytes())
            dex=build/'dex';dex.mkdir()
            stage('dex',[bt/'d8','--release','--min-api','23','--lib',platform,'--output',dex,program,*deps])
            record['dex_hashes']={p.name:sha(p.read_bytes()) for p in dex.glob('*.dex')}
            assets=build/'assets';assets.mkdir();shutil.copyfile(folder/'model.tflite',assets/'model.tflite')
            manifest=build/'AndroidManifest.xml'
            manifest.write_text('''<manifest xmlns:android="http://schemas.android.com/apk/res/android" package="org.example.contract.consumer" android:versionCode="1" android:versionName="1.0">
 <uses-sdk android:minSdkVersion="23" android:targetSdkVersion="30" />
 <application android:label="Contract evidence" android:debuggable="true" android:extractNativeLibs="true" android:hasCode="true" />
 <instrumentation android:name="org.example.contract.ContractInstrumentation" android:targetPackage="org.example.contract.consumer" android:functionalTest="true" />
</manifest>''')
            unsigned=build/'unsigned.apk'
            stage('package_resources',[bt/'aapt2','link','-o',unsigned,'--manifest',manifest,'-I',platform,'-A',assets,'-0','tflite'])
            with zipfile.ZipFile(unsigned,'a',compression=zipfile.ZIP_STORED) as z:
                for p in sorted(dex.glob('*.dex')):z.writestr(zipfile.ZipInfo(p.name,(1980,1,1,0,0,0)),p.read_bytes())
                for p in sorted((ROOT/'prerequisites/aar').glob('*/jni/x86_64/*.so')):
                    z.writestr(zipfile.ZipInfo('lib/x86_64/'+p.name,(1980,1,1,0,0,0)),p.read_bytes())
            stage('zipalign',[bt/'zipalign','-f','4',unsigned,build/'aligned.apk'])
            stage('sign',[bt/'apksigner','sign','--ks',keystore,'--ks-key-alias','research','--ks-pass','pass:android','--key-pass','pass:android','--out',build/'consumer.apk',build/'aligned.apk'])
            stage('verify_apk',[bt/'apksigner','verify','--verbose',build/'consumer.apk'])
            record['apk_sha256']=sha((build/'consumer.apk').read_bytes());record['package_status']='PASS'
        except Exception as exc:
            record['package_status']='FAIL';record['error']=repr(exc)
        results.append(record);save(ROOT/args.experiment/'build-results.json',results)
        print(row['variant'],record['package_status'],record.get('earliest_failing_stage',''),flush=True)
    if results:
        base=results[0]
        for r in results:
            r['generated_classes_equal_original']=bool(r.get('generated_class_hashes')) and r.get('generated_class_hashes')==base.get('generated_class_hashes')
            r['dex_equal_original']=bool(r.get('dex_hashes')) and r.get('dex_hashes')==base.get('dex_hashes')
    save(ROOT/args.experiment/'build-results.json',results)
    if any(r['package_status']!='PASS' for r in results):raise SystemExit(1)
if __name__=='__main__':main()
