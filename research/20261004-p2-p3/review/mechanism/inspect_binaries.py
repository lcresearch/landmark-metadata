#!/usr/bin/env python3
"""Inspect actual resolved P2 Java/native dependencies without running inference."""
import hashlib, json, pathlib, subprocess
ROOT = pathlib.Path(__file__).resolve().parent
P2 = ROOT.parents[1] / 'P2'
JDK = pathlib.Path('/workspace/hand-contract-repro/toolchains/jdk-17.0.12+7/bin')
JAVA = {
    'task_image_classifier': ('tensorflow-lite-task-vision', [
        'org.tensorflow.lite.task.vision.classifier.ImageClassifier',
        'org.tensorflow.lite.task.vision.classifier.ImageClassifier$1',
        'org.tensorflow.lite.task.vision.classifier.ImageClassifier$4']),
    'task_jni_utils': ('tensorflow-lite-task-base', ['org.tensorflow.lite.task.core.TaskJniUtils']),
    'task_support_tensorlabel': ('tensorflow-lite-support-api', ['org.tensorflow.lite.support.label.TensorLabel']),
}
def record(p):
    b=p.read_bytes(); return {'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def main():
    out=ROOT/'binary'; out.mkdir(exist_ok=True)
    commands=[]; artifacts=[]
    for name,(dep,classes) in JAVA.items():
        p=P2/'dependencies'/dep/'classes.jar'; artifacts.append(record(p))
        cmd=[str(JDK/'javap'),'-c','-p','-classpath',str(p),*classes]
        res=subprocess.run(cmd,capture_output=True)
        (out/(name+'.javap.txt')).write_bytes(res.stdout)
        (out/(name+'.stderr')).write_bytes(res.stderr)
        commands.append({'name':name,'argv':cmd,'exit_code':res.returncode})
        if res.returncode: raise RuntimeError(f'javap failed: {name}')
    support=pathlib.Path('/workspace/hand-contract-repro/deps/tensorflow-lite-support-api-0.4.4.jar')
    artifacts.append(record(support))
    cmd=[str(JDK/'javap'),'-c','-p','-classpath',str(support),'org.tensorflow.lite.support.label.TensorLabel']
    res=subprocess.run(cmd,capture_output=True)
    (out/'wrapper_support_tensorlabel.javap.txt').write_bytes(res.stdout)
    commands.append({'name':'wrapper_support_tensorlabel','argv':cmd,'exit_code':res.returncode})
    native=P2/'dependencies/tensorflow-lite-task-vision/jni/x86_64/libtask_vision_jni.so'
    artifacts.append(record(native))
    for name,cmd in [('native_symbols',['nm','-D','-C',str(native)]),('native_strings',['strings',str(native)])]:
        res=subprocess.run(cmd,capture_output=True)
        (out/(name+'.txt')).write_bytes(res.stdout)
        (out/(name+'.stderr')).write_bytes(res.stderr)
        commands.append({'name':name,'argv':cmd,'exit_code':res.returncode})
    (ROOT/'binary-provenance.json').write_text(json.dumps({'artifacts':artifacts,'commands':commands},indent=2)+'\n')
    print(json.dumps({'artifact_count':len(artifacts),'exit_codes':[c['exit_code'] for c in commands],
      'wrapper_and_task_support_jar_identical':support.read_bytes()==(P2/'dependencies/tensorflow-lite-support-api/classes.jar').read_bytes()}))
if __name__=='__main__': main()
