import argparse, io, json, tarfile
from common import ROOT, sha, save, run
ap=argparse.ArgumentParser();ap.add_argument('--experiment',required=True);ap.add_argument('--run',required=True);ap.add_argument('--variants',nargs='+');args=ap.parse_args()
adb=ROOT/'sdk/platform-tools/adb';prefix=[adb,'-s','emulator-5554'];package='org.example.contract.consumer'
rows=json.loads((ROOT/args.experiment/'static-results.json').read_text());builds=json.loads((ROOT/args.experiment/'build-results.json').read_text())
if args.variants:rows=[r for r in rows if r['variant'] in args.variants]
dest=ROOT/args.experiment/'executions'/args.run;dest.mkdir(parents=True,exist_ok=False);results=[]
for static in rows:
    name=static['variant'];build=next(b for b in builds if b['variant']==name);folder=dest/name;folder.mkdir();record=dict(static)
    record['execution_run']=args.run;record['build']=build
    record['compile_status']=build['stages'].get('compile',{}).get('status','NOT_REACHED');record['package_status']=build['package_status']
    for field in ['load_status','input_preparation_status','inference_status','decoder_status']:record[field]='NOT_REACHED'
    if build['package_status']!='PASS':
        record['earliest_failing_stage']=build.get('earliest_failing_stage');results.append(record);continue
    stage='installation'
    try:
        p=run([*prefix,'install','-r',ROOT/args.experiment/'variants'/name/'build/consumer.apk'],folder/'logs/install',timeout=180)
        if p.returncode:raise RuntimeError(p.stdout.decode(errors='replace')+p.stderr.decode(errors='replace'))
        record['install_status']='PASS'
        run([*prefix,'shell','run-as',package,'rm','-rf','files/evidence'],folder/'logs/clear_previous_evidence')
        stage='instrumentation'
        p=run([*prefix,'shell','am','instrument','-w','-e','variant',name,package+'/org.example.contract.ContractInstrumentation'],folder/'logs/instrumentation',timeout=300)
        record['instrumentation_exit_code']=p.returncode
        run([*prefix,'logcat','-d','-v','threadtime','ContractEvidence:E','tflite:I','TensorFlowLite:I','AndroidRuntime:E','*:S'],folder/'logs/logcat')
        q=run([*prefix,'exec-out','run-as',package,'tar','-C','files/evidence','-cf','-','.'],folder/'logs/evidence-tar',binary=True)
        if q.returncode:raise RuntimeError('No retrievable instrumentation evidence: '+q.stderr.decode(errors='replace'))
        raw=folder/'device';raw.mkdir()
        with tarfile.open(fileobj=io.BytesIO(q.stdout)) as archive:
            for member in archive.getmembers():
                if not member.isfile():continue
                relative=member.name.removeprefix('./')
                if '..' in relative.split('/'):raise ValueError('Unsafe evidence path')
                (raw/relative).write_bytes(archive.extractfile(member).read())
        observed=json.loads((raw/'result.json').read_text());record['observed']=observed
        record['load_status']=observed.get('model_loading_status','NOT_REACHED')
        observations=observed.get('observations',[])
        for target,source in [('input_preparation_status','input_preparation_status'),('inference_status','inference_status'),('decoder_status','generated_getter_status')]:
            states=[o.get(source,'NOT_REACHED') for o in observations]
            record[target]='FAIL' if 'FAIL' in states else 'PASS' if states and all(s=='PASS' for s in states) else 'NOT_REACHED'
        failure=next((o for o in [observed,*observations] if 'earliest_failing_stage' in o),None)
        if failure:
            for k in ['earliest_failing_stage','exception_type','exception_message','stack_trace']:record[k]=failure.get(k)
        record['raw_output_hashes']={p.name:sha(p.read_bytes()) for p in raw.glob('*.f32')}
        record['artifact_paths']['execution']=str(folder.relative_to(ROOT))
    except Exception as exc:
        record.update(earliest_failing_stage=stage,harness_exception=repr(exc))
    results.append(record);save(dest/'results.json',results)
    print(name,record['load_status'],record['inference_status'],record['decoder_status'],record.get('earliest_failing_stage',''),flush=True)
save(dest/'results.json',results)
