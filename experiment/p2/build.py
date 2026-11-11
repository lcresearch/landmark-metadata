import json,pathlib,zipfile,shutil
from common import ROOT,HAND,JDK,sha,save,run
sdk=ROOT/'sdk';bt=sdk/'build-tools/35.0.0';platform=sdk/'platforms/android-30/android.jar';old=pathlib.Path('/workspace/metadata-contract-e2e-20261004T030536Z');dep=ROOT/'dependencies';extra=old/'prerequisites/extra-jars'
wrapper=[p for p in sorted((HAND/'deps').glob('*.jar')) if not p.name.startswith('android-')]+sorted(extra.glob('*.jar'))
task=[dep/'tensorflow-lite-task-vision/classes.jar',dep/'tensorflow-lite-task-base/classes.jar',dep/'tensorflow-lite-support-api/classes.jar',HAND/'deps/tensorflow-lite-api-2.13.0.jar',HAND/'deps/annotation-1.3.0.jar',extra/'checker-qual-2.5.8.jar',extra/'image-1.0.0-beta1.jar',dep/'auto-value-annotations-1.6.jar']
configs={'wrapper':{'deps':wrapper,'natives':list((old/'prerequisites/aar').glob('*/jni/x86_64/*.so')),'package':'org.example.contract.consumer','instrument':'ContractInstrumentation'},'task':{'deps':task,'natives':list((dep/'tensorflow-lite-task-vision/jni/x86_64').glob('*.so')),'package':'org.example.task.consumer','instrument':'TaskInstrumentation'}}
lock={k:{'classpaths':[{'path':str(p),'sha256':sha(p.read_bytes())} for p in v['deps']],'natives':[{'path':str(p),'sha256':sha(p.read_bytes())} for p in v['natives']],'declarations':'Maven POMs saved in dependencies; shared Support API transitive versions reused from old sealed setup. AndroidX annotation selected1.3.0 vs provideddeclared1.1.0. No Gradle resolver.'} for k,v in configs.items()};save(dep/'resolved-lock.json',lock)
key=ROOT/'prerequisites/research.keystore'
if not key.exists():
 p=run([JDK/'bin/keytool','-genkeypair','-keystore',key,'-storepass','android','-alias','research','-keypass','android','-keyalg','RSA','-keysize','2048','-validity','3650','-dname','CN=P2 Research'],ROOT/'logs/keytool');assert p.returncode==0
rows=json.loads((ROOT/'static-results.json').read_text());results=[]
for consumer,cfg in configs.items():
 for row in rows:
  v=row['variant'];folder=ROOT/'variants'/v;build=ROOT/'build'/consumer/v;build.mkdir(parents=True,exist_ok=False);record={'consumer':consumer,'variant':v,'stages':{},'generated_source_modified':False if consumer=='wrapper' else 'INAPPLICABLE','package':cfg['package'],'instrument':cfg['instrument']}
  def stage(name,cmd):
   p=run(cmd,build/'logs'/name,timeout=300);record['stages'][name]={'status':'PASS' if p.returncode==0 else 'FAIL','exit_code':p.returncode}
   if p.returncode:record['earliest_failing_stage']=name;raise RuntimeError(name)
  try:
   classes=build/'classes';classes.mkdir();sources=[ROOT/'scripts'/(cfg['instrument']+'.java')]
   if consumer=='wrapper':sources.insert(0,folder/'generated/src/main/java/org/example/contract/ContractModel.java')
   stage('compile',[JDK/'bin/javac','--release','8','-cp',':'.join(map(str,[platform,*cfg['deps']])),'-d',classes,*sources]);record['generated_class_hashes']={str(p.relative_to(classes)):sha(p.read_bytes()) for p in classes.rglob('ContractModel*.class')};record['all_class_hashes']={str(p.relative_to(classes)):sha(p.read_bytes()) for p in classes.rglob('*.class')}
   program=build/'program.jar'
   with zipfile.ZipFile(program,'w') as z:
    for p in sorted(classes.rglob('*.class')):z.writestr(zipfile.ZipInfo(str(p.relative_to(classes)),(1980,1,1,0,0,0)),p.read_bytes())
   dex=build/'dex';dex.mkdir();stage('dex',[bt/'d8','--release','--min-api','23','--lib',platform,'--output',dex,program,*cfg['deps']]);record['dex_hashes']={p.name:sha(p.read_bytes()) for p in dex.glob('*.dex')}
   assets=build/'assets';assets.mkdir();shutil.copyfile(folder/'model.tflite',assets/'model.tflite');manifest=build/'AndroidManifest.xml';manifest.write_text(f'<manifest xmlns:android="http://schemas.android.com/apk/res/android" package="{cfg["package"]}" android:versionCode="1" android:versionName="1.0"><uses-sdk android:minSdkVersion="23" android:targetSdkVersion="30"/><application android:label="P2 evidence" android:debuggable="true" android:extractNativeLibs="true" android:hasCode="true"/><instrumentation android:name="org.example.contract.{cfg["instrument"]}" android:targetPackage="{cfg["package"]}" android:functionalTest="true"/></manifest>');unsigned=build/'unsigned.apk';stage('package_resources',[bt/'aapt2','link','-o',unsigned,'--manifest',manifest,'-I',platform,'-A',assets,'-0','tflite'])
   with zipfile.ZipFile(unsigned,'a',compression=zipfile.ZIP_STORED) as z:
    for p in sorted(dex.glob('*.dex')):z.writestr(zipfile.ZipInfo(p.name,(1980,1,1,0,0,0)),p.read_bytes())
    for p in cfg['natives']:z.writestr(zipfile.ZipInfo('lib/x86_64/'+p.name,(1980,1,1,0,0,0)),p.read_bytes())
   stage('zipalign',[bt/'zipalign','-f','4',unsigned,build/'aligned.apk']);stage('sign',[bt/'apksigner','sign','--ks',key,'--ks-key-alias','research','--ks-pass','pass:android','--key-pass','pass:android','--out',build/'consumer.apk',build/'aligned.apk']);stage('verify_apk',[bt/'apksigner','verify','--verbose',build/'consumer.apk']);record['package_status']='PASS';record['apk_sha256']=sha((build/'consumer.apk').read_bytes())
   with zipfile.ZipFile(build/'consumer.apk') as z:record['apk_model_sha256']=sha(z.read('assets/model.tflite'))
  except Exception as exc:record['package_status']='FAIL';record['error']=repr(exc)
  results.append(record);save(ROOT/'build-results.json',results);print(consumer,v,record['package_status'],record.get('earliest_failing_stage',''),flush=True)
for c in configs:
 group=[x for x in results if x['consumer']==c];base=group[0]
 for row in group:
  row['classes_equal_original']=row.get('all_class_hashes')==base.get('all_class_hashes');row['dex_equal_original']=row.get('dex_hashes')==base.get('dex_hashes')
save(ROOT/'build-results.json',results)
