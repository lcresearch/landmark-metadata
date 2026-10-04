from common import ROOT,PYTHON,JDK,run,save,sha
import pathlib,platform,json
for name,command in [('python',[PYTHON,'--version']),('python-freeze',[PYTHON,'-m','pip','freeze']),('java',[JDK/'bin/java','-version']),('javac',[JDK/'bin/javac','-version']),('adb',[ROOT/'sdk/platform-tools/adb','version']),('emulator',[ROOT/'sdk/emulator/emulator','-version']),('d8',[ROOT/'sdk/build-tools/35.0.0/d8','--version']),('aapt2',[ROOT/'sdk/build-tools/35.0.0/aapt2','version'])]:
    run(command,ROOT/'versions'/name)
files=[ROOT/'sdk/platforms/android-30/android.jar',ROOT/'sdk/system-images/android-30/default/x86_64/source.properties',ROOT/'sdk/build-tools/35.0.0/source.properties',ROOT/'sdk/emulator/source.properties',JDK/'release']
save(ROOT/'versions/files.json',[{'path':str(p),'resolved_path':str(p.resolve()),'sha256':sha(p.read_bytes()),'text':p.read_text() if p.suffix=='.properties' or p.name=='release' else None} for p in files])
