from pathlib import Path
import json
import os
import subprocess
import zipfile

ROOT=Path(__file__).resolve().parents[1]
BASE=Path(os.environ.get('HAND_REPRO_ROOT','/workspace/hand-contract-repro'))
JDK=BASE/'toolchains/jdk-17.0.12+7'

def main():
    output=ROOT/'build/decoder';output.mkdir(parents=True,exist_ok=True)
    p=subprocess.run([str(JDK/'bin/javac'),'--release','8','-cp',str(BASE/'deps/*'),'-d',str(output),str(ROOT/'scripts/DecoderProbe.java')],capture_output=True,text=True)
    (ROOT/'logs/decoder-javac.log').write_text(p.stdout+p.stderr);assert p.returncode==0,p.stderr
    runtime={c['id']:c for c in json.loads((ROOT/'results/runtime-suite.json').read_text())}
    results=[]
    for component in json.loads((ROOT/'results/static-suite.json').read_text()):
        rt={v['variant']:v for v in runtime[component['id']]['variants']}
        for variant in component['variants']:
            folder=(ROOT/variant['path']).parent
            for check in variant['decoder_checks']:
                row={'id':component['id'],'variant':variant['variant'],'prediction':check}
                if not rt.get(variant['variant'],{}).get('success'):
                    row['skipped']='No successful CPU outputs';results.append(row);continue
                with zipfile.ZipFile(ROOT/variant['path']) as z:labels=z.read(check['label_file'])
                path=folder/f"probe-{check['field']}-labels.txt";path.write_bytes(labels)
                raw=folder/'runtime'/f"zeros-output-{check['output_position']}.f32"
                args=[str(JDK/'bin/java'),'-cp',str(BASE/'deps/*')+':'+str(output),'DecoderProbe',','.join(map(str,check['shape'])),str(raw),str(path)]
                p=subprocess.run(args,capture_output=True,text=True,timeout=30)
                (folder/f"decoder-{check['field']}.log").write_text(p.stdout+p.stderr)
                row['exit_code']=p.returncode
                if p.returncode==0:
                    row['observed']=json.loads(p.stdout);row['prediction_matches']=row['observed']['status']==check['status']
                    assert row['prediction_matches'],row
                    assert row['observed']['labels']==check['label_count']
                else:row['probe_error']=p.stderr[-2000:]
                results.append(row)
                print(component['id'],variant['variant'],check['field'],row.get('observed',row.get('probe_error')),flush=True)
    (ROOT/'results/decoder-suite.json').write_text(json.dumps(results,indent=2))

if __name__=='__main__':main()
