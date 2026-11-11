import pathlib,json,sys,importlib.metadata,platform
from common import ROOT,HAND,JDK,run,save,sha,PYTHON
versions={'python':sys.version,'host':platform.platform(),'packages':{n:importlib.metadata.version(n) for n in ['tflite-support','numpy','flatbuffers']},'task_native_interpreter_version':'UNKNOWN; official Task0.4.4 .so pinned, no assertion of equality to standalone TFLite2.13.0'}
for name,cmd in [('java',[JDK/'bin/java','-version']),('javac',[JDK/'bin/javac','-version']),('adb',[ROOT/'sdk/platform-tools/adb','version']),('emulator',[ROOT/'sdk/emulator/emulator','-version']),('aapt2',[ROOT/'sdk/build-tools/35.0.0/aapt2','version']),('d8',[ROOT/'sdk/build-tools/35.0.0/d8','--version'])]:
 p=run(cmd,ROOT/'versions'/name);versions[name]={'stdout':p.stdout.decode(errors='replace'),'stderr':p.stderr.decode(errors='replace'),'exit_code':p.returncode}
versions['sdk_source_properties']={str(p.relative_to(ROOT/'sdk')):p.read_text() for p in [ROOT/'sdk/emulator/source.properties',ROOT/'sdk/platform-tools/source.properties',ROOT/'sdk/build-tools/35.0.0/source.properties',ROOT/'sdk/system-images/android-30/default/x86_64/source.properties'] if p.exists()}
save(ROOT/'versions/versions.json',versions)
