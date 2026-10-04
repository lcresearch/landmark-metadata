from pathlib import Path
import hashlib
import json
import os
import subprocess

ROOT=Path(__file__).resolve().parents[1]
BASE=Path(os.environ.get('HAND_REPRO_ROOT','/workspace/hand-contract-repro'))
JDK=BASE/'toolchains/jdk-17.0.12+7'

def main():
    results=[]
    for component in json.loads((ROOT/'results/static-suite.json').read_text()):
        row={'id':component['id'],'variants':[]}
        for variant in component['variants']:
            rec={'variant':variant['variant'],'repair_applied':False}
            generation=variant.get('generation',{})
            files=[ROOT/path for path in generation.get('files',[]) if path.endswith('.java')]
            if not files:rec['skipped']='No generated Java';row['variants'].append(rec);continue
            folder=(ROOT/variant['path']).parent;output=folder/'classes'
            command=[str(JDK/'bin/javac'),'--release','8','-cp',str(BASE/'deps/*'),'-d',str(output),*map(str,files)]
            p=subprocess.run(command,capture_output=True,text=True,timeout=60)
            (folder/'raw-javac.log').write_text(p.stdout+p.stderr)
            rec.update(exit_code=p.returncode,command=command)
            if p.returncode==0:
                rec['class_hashes']={str(f.relative_to(output)):hashlib.sha256(f.read_bytes()).hexdigest() for f in output.rglob('*.class')}
                q=subprocess.run([str(JDK/'bin/javap'),'-classpath',str(output),'-c','-p','org.example.contract.ContractModel$Outputs'],capture_output=True,text=True)
                (folder/'outputs-javap.txt').write_text(q.stdout+q.stderr)
            row['variants'].append(rec)
            print(component['id'],variant['variant'],'raw javac',p.returncode,flush=True)
        results.append(row)
        (ROOT/'results/compile-suite.json').write_text(json.dumps(results,indent=2))

if __name__=='__main__':main()
