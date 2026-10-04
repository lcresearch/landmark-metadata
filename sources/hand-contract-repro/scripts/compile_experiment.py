"""Record raw failures, audit one shared separator repair, compile and inspect bytecode."""
from pathlib import Path
import difflib
import hashlib
import json
import os
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
JDK = Path(os.environ.get('REPRO_JDK', str(ROOT / 'toolchains/jdk-17.0.12+7')))
VARIANTS = ['original', 'swapped', 'description_control', 'swap_back_control']
RULES = [
    (r'(Outputs\(Metadata metadata), ,', r'\1,'),
    (r'(new Outputs\(metadata), ,', r'\1,'),
    (r'([a-zA-Z]+Postprocessor)(TensorProcessor worldLandmarksPostprocessor)', r'\1, \2'),
    (r'([a-zA-Z]+Postprocessor)(worldLandmarksPostprocessor\);)', r'\1, \2'),
]

def sha(data):
    return hashlib.sha256(data).hexdigest()

def run(args, log):
    p = subprocess.run([str(x) for x in args], cwd=ROOT, capture_output=True, text=True)
    (ROOT / 'logs' / log).write_text(p.stdout + p.stderr)
    return {'command': [str(x) for x in args], 'exit_code': p.returncode, 'log': 'logs/' + log}, p.stdout

def main():
    report = {'repair_rules': RULES, 'java_version': subprocess.run([str(JDK/'bin/java'), '-version'],capture_output=True,text=True).stderr, 'variants': {}}
    consumer = ROOT / 'scripts/BindingConsumer.java'
    consumer.write_text('''import org.example.hand.HandModel;
public final class BindingConsumer {
  public static int inspect(HandModel.Outputs out) {
    return out.getHandednessAsCategoryList().size()
        + out.getLandmarksAsTensorBuffer().getFloatArray().length;
  }
}
''')
    static = json.loads((ROOT/'results/static-results.json').read_text())
    for name in VARIANTS:
        src = ROOT / f'generated/{name}/src/main/java/org/example/hand/HandModel.java'
        raw = src.read_text()
        raw_result, _ = run([JDK/'bin/javac', '--release','8','-cp','deps/*','-d',f'build/{name}/raw',src], name+'-raw-javac.log')
        repaired = raw
        counts=[]
        for pattern,repl in RULES:
            repaired,n = re.subn(pattern,repl,repaired)
            counts.append(n)
        assert counts == [1,1,1,1]
        assert re.sub(r'[,\s]','',raw) == re.sub(r'[,\s]','',repaired)
        changed_lines = [i for i,(a,b) in enumerate(zip(raw.splitlines(),repaired.splitlines()),1) if a != b]
        assert len(changed_lines) == 2 and len(raw.splitlines()) == len(repaired.splitlines())
        # Every method except constructor and process retains exact source text.
        for pattern in [r'Map<Integer, Object> getBuffer\(\) \{.*?\n    \}', r'public Metadata\(.*?\n    \}', r'public List<Category> getHandednessAsCategoryList\(\) \{.*?\n    \}', r'public TensorBuffer getLandmarksAsTensorBuffer\(\) \{.*?\n    \}']:
            assert re.search(pattern,raw,re.S).group(0) == re.search(pattern,repaired,re.S).group(0)
        patched = ROOT/f'patched/{name}/org/example/hand/HandModel.java'
        patched.parent.mkdir(parents=True,exist_ok=True)
        patched.write_text(repaired)
        patch=''.join(difflib.unified_diff(raw.splitlines(True),repaired.splitlines(True),fromfile='generated/HandModel.java',tofile='patched/HandModel.java'))
        (ROOT/'logs'/f'{name}-syntax.patch').write_text(patch)
        out=f'build/{name}/classes'
        fixed_result,_ = run([JDK/'bin/javac','--release','8','-cp','deps/*','-d',out,patched],name+'-repaired-javac.log')
        assert fixed_result['exit_code'] == 0, (ROOT/f"logs/{name}-repaired-javac.log").read_text()
        consumer_result,_ = run([JDK/'bin/javac','--release','8','-cp',f'deps/*:{out}','-d',f'build/{name}/consumer',consumer],name+'-consumer-javac.log')
        assert consumer_result['exit_code'] == 0
        _,bytecode=run([JDK/'bin/javap','-classpath',out,'-c','-p','org.example.hand.HandModel$Outputs'],name+'-outputs-javap.txt')
        _,mdbytecode=run([JDK/'bin/javap','-classpath',out,'-c','-p','org.example.hand.HandModel$Metadata'],name+'-metadata-javap.txt')
        get_buffer=bytecode.split('java.util.Map<java.lang.Integer, java.lang.Object> getBuffer();')[1].split('private ')[0]
        pairs=re.findall(r'iconst_([0-3])\n\s+\d+: invokestatic[^\n]*\n\s+\d+: aload_0\n\s+\d+: getfield[^\n]*// Field (\w+):Lorg/tensorflow/lite/support/tensorbuffer/TensorBuffer;',get_buffer)
        mapping={field:int(index) for index,field in pairs}
        expected={'handedness':2,'presenseScore':1,'landmarks':0,'worldLandmarks':3} if name=='swapped' else {'handedness':0,'presenseScore':1,'landmarks':2,'worldLandmarks':3}
        assert mapping == expected, mapping
        source_map={field:int(index) for index,field in re.findall(r'outputs.put\((\d+), (\w+)\.getBuffer\(\)\)',raw)}
        assert source_map == mapping
        metadata_map={field:int(index) for field,index in re.findall(r'Tensor (\w+)Tensor = model.getOutputTensor\((\d+)\)',raw)}
        assert metadata_map == mapping
        shape_map={field:static['variants'][name]['model']['outputs'][index]['shape'] for field,index in mapping.items()}
        hashes={p.name:sha(p.read_bytes()) for p in (ROOT/out).rglob('*.class')}
        report['variants'][name]={'raw':raw_result,'repaired':fixed_result,'consumer':consumer_result,'repair_counts':counts,'changed_source_lines':changed_lines,
          'source_sha256':sha(raw.encode()),'patched_sha256':sha(repaired.encode()),'source_equal_after_stripping_only_commas_and_whitespace':True,
          'binding_methods_unchanged_by_repair':True,'bytecode_field_output_mapping':mapping,'field_shapes':shape_map,
          'consumer_class_sha256':sha((ROOT/f'build/{name}/consumer/BindingConsumer.class').read_bytes()),'wrapper_class_hashes':hashes}
        print(name,'exit codes',raw_result['exit_code'],fixed_result['exit_code'],consumer_result['exit_code'],'bytecode bindings',mapping,flush=True)
    assert len({r['consumer_class_sha256'] for r in report['variants'].values()})==1
    assert report['variants']['original']['wrapper_class_hashes'] == report['variants']['description_control']['wrapper_class_hashes'] == report['variants']['swap_back_control']['wrapper_class_hashes']
    report['all_consumer_class_hashes_equal']=True
    report['negative_control_wrapper_class_hashes_equal']=True
    (ROOT/'results/compile-results.json').write_text(json.dumps(report,indent=2))

if __name__ == '__main__':
    main()
