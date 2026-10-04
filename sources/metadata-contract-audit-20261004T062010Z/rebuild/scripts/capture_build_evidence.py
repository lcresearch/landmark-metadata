from common import ROOT,JDK,HAND,run,save,sha
files=[]
for base,pattern in [(ROOT/'prerequisites/aar','*/jni/x86_64/*.so'),(ROOT/'prerequisites/extra-jars','*.jar'),(HAND/'deps','*.jar')]:
    for p in sorted(base.glob(pattern)):
        if p.name.startswith('android-'):continue
        files.append({'path':str(p),'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size})
save(ROOT/'versions/native-and-java-dependencies.json',files)
classes=ROOT/'E1/variants/original/build/classes'
for cls in ['ContractModel','ContractModel$Outputs','ContractInstrumentation']:
    run([JDK/'bin/javap','-classpath',classes,'-c','-p','org.example.contract.'+cls],ROOT/'bytecode'/cls)
