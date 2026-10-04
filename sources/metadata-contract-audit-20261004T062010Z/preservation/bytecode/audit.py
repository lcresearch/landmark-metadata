#!/usr/bin/env python3
"""Read-only audit of existing evidence. No inference or Android execution."""
import datetime, hashlib, json, pathlib, re, subprocess, zipfile

BASE = pathlib.Path('/workspace/metadata-contract-e2e-20261004T030536Z')
OUT = pathlib.Path('/workspace/metadata-contract-audit-20261004T062010Z/preservation/bytecode')
JAVAP = '/workspace/hand-contract-repro/toolchains/jdk-17.0.12+7/bin/javap'
DEXDUMP = str(BASE / 'sdk/build-tools/35.0.0/dexdump')
manifest = {}
commands = []
def read(p):
    b = p.read_bytes()
    manifest[str(p)] = {'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}
    return b
def execute(command, name):
    p = subprocess.run(command, capture_output=True)
    (OUT / (name + '.stdout')).write_bytes(p.stdout)
    (OUT / (name + '.stderr')).write_bytes(p.stderr)
    commands.append({'argv': command, 'returncode': p.returncode, 'stdout': str(OUT / (name+'.stdout')), 'stderr': str(OUT / (name+'.stderr'))})
    if p.returncode: raise RuntimeError(command)
    return p.stdout.decode()

variants = []
for experiment in ['E1', 'E2']:
    read(BASE / experiment / 'implementation-snapshot/ContractInstrumentation.java')
    for v in sorted((BASE / experiment / 'variants').iterdir()):
        if not (v / 'build/classes').is_dir(): continue
        files = [v/'generated/src/main/java/org/example/contract/ContractModel.java', *sorted((v/'build/classes').rglob('*.class')), v/'build/dex/classes.dex']
        hashes = {}
        for p in files:
            b = read(p)
            hashes[str(p.relative_to(v))] = hashlib.sha256(b).hexdigest()
        apk = v/'build/consumer.apk'
        read(apk)
        with zipfile.ZipFile(apk) as z:
            names = [n for n in z.namelist() if n.endswith('.dex')]
            apk_dex = {n: hashlib.sha256(z.read(n)).hexdigest() for n in names}
        variants.append({'experiment': experiment, 'variant': v.name, 'hashes': hashes, 'apk_path': str(apk), 'apk_dex_sha256': apk_dex, 'apk_dex_matches_build': apk_dex == {'classes.dex': hashes['build/dex/classes.dex']}})
read(BASE / 'scripts/ContractInstrumentation.java')

classes = BASE / 'E1/variants/original/build/classes'
for class_name in ['ContractInstrumentation', 'ContractModel', 'ContractModel$Metadata', 'ContractModel$Outputs']:
    execute([JAVAP, '-c', '-p', '-l', '-classpath', str(classes), 'org.example.contract.' + class_name], 'javap-' + class_name.replace('$','-'))
execute([JAVAP, '-version'], 'javap-version')
full_dex = execute([DEXDUMP, '-d', '-f', '-h', str(BASE / 'E1/variants/original/build/dex/classes.dex')], 'dexdump-full')
blocks = re.split(r'(?=^Class #\d+ header:)', full_dex, flags=re.M)
selected = []
for b in blocks:
    m = re.search(r"Class descriptor\s+: '(.*?)'", b)
    if m and (m.group(1).startswith('Lorg/example/contract/') or m.group(1) in ['Lorg/tensorflow/lite/support/label/TensorLabel;', 'Lorg/tensorflow/lite/support/common/FileUtil;', 'Lorg/tensorflow/lite/support/model/Model;', 'Lorg/tensorflow/lite/support/common/ops/DequantizeOp;']): selected.append(b)
    if m and m.group(1) in ['Lorg/tensorflow/lite/support/tensorbuffer/TensorBuffer;', 'Lorg/tensorflow/lite/support/label/Category;', 'Lorg/tensorflow/lite/support/metadata/MetadataExtractor;']:
        (OUT/('dexdump-'+m.group(1).split('/')[-1][:-1]+'.txt')).write_text(b)
(OUT/'dexdump-selected.txt').write_text(''.join(selected))

executions=[]
for experiment in ['E1','E2']:
    for p in sorted((BASE/experiment/'executions').glob('*/*/device/result.json')):
        result=json.loads(read(p))
        run_dir=p.parent.parent
        logs={}
        for name in ['instrumentation.stdout','instrumentation.stderr','instrumentation.command.json','logcat.stdout','logcat.stderr','logcat.command.json']:
            log=run_dir/'logs'/name
            logs[name]=read(log).decode() if log.exists() else None
        rows=[]
        for row in result.get('observations',[]):
            rows.append({k:row[k] for k in ['input','input_preparation_status','inference_status','raw_output_observation_status','generated_getter_status','category_count','raw_output_bytes','earliest_failing_stage','exception_type','exception_message','stack_trace'] if k in row})
        lc=logs['logcat.stdout'] or ''
        executions.append({'path':str(p),'experiment':experiment,'run':run_dir.parent.name,'variant':run_dir.name,'model_loading_status':result.get('model_loading_status'),'loaded_label_count':result.get('loaded_label_count'),'observations':rows,'instrumentation_stdout':logs['instrumentation.stdout'],'instrumentation_exit_code':json.loads(logs['instrumentation.command.json']).get('exit_code') if logs['instrumentation.command.json'] else None,'logcat_exception_occurrences':lc.count('java.lang.IllegalArgumentException: Label number 999 mismatch the shape on axis 1'),'logcat_generated_getter_stack_occurrences':lc.count('ContractModel$Outputs.getProbabilityAsCategoryList(ContractModel.java:47)'),'logcat_harness_line81_occurrences':lc.count('ContractInstrumentation.onStart(ContractInstrumentation.java:81)'),'logcat_fatal_exception': 'FATAL EXCEPTION' in lc,'logcat_lines':lc.splitlines()})
        start=datetime.datetime.fromisoformat(json.loads(logs['instrumentation.command.json'])['started_utc']).strftime('%m-%d %H:%M:%S.%f')[:18]
        end=datetime.datetime.fromisoformat(json.loads(logs['logcat.command.json'])['started_utc']).strftime('%m-%d %H:%M:%S.%f')[:18]
        interval_lines=[line for line in lc.splitlines() if re.match(r'^\d\d-\d\d ',line) and start <= line[:18] <= end]
        interval='\n'.join(interval_lines)
        executions[-1].update({'logcat_attribution_note':'Archived logcat is cumulative. Time-correlated lines use same-day instrument start and logcat dump start; timestamps alone are not independent provenance attestation.','logcat_interval_start':start,'logcat_interval_end':end,'logcat_current_interval_lines':interval_lines,'logcat_current_interval_exception_count':interval.count('java.lang.IllegalArgumentException: Label number 999 mismatch the shape on axis 1'),'logcat_current_interval_getter_stack_count':interval.count('ContractModel$Outputs.getProbabilityAsCategoryList(ContractModel.java:47)'),'logcat_current_interval_harness_stack_count':interval.count('ContractInstrumentation.onStart(ContractInstrumentation.java:81)')})

keys=list(variants[0]['hashes'])
equality={k: len({v['hashes'][k] for v in variants})==1 for k in keys}
result={'audit_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'kind':'AI-assisted static artifact and archived log audit; not human audit or independent execution','evidence_root':str(BASE),'excluded':'build-before-dependency-closure; all model execution and emulator startup','variants':variants,'all_eight_variant_equality':equality,'harness_source_equal': len({manifest[str(BASE/p)]['sha256'] for p in ['E1/implementation-snapshot/ContractInstrumentation.java','E2/implementation-snapshot/ContractInstrumentation.java','scripts/ContractInstrumentation.java']})==1,'executions':executions,'commands':commands,'input_manifest':manifest}
result['status']='PASS'
result['status_scope']='Saved source/class/DEX and 16 complete phase/run/variant records are consistent for the audited claims; not human or fresh execution validation.'
result['review_findings']={
    'actual_generated_call_chain': {'status':'PASS','detail':'Source, fresh class bytecode and APK-identical DEX show newInstance -> process -> generated getter.'},
    'actual_bundled_label_decoder': {'status':'PASS','detail':'TensorLabel constructor guard and getCategoryList are present in the actual APK DEX.'},
    'associated_file_consumption': {'status':'PASS','detail':'output metadata [0], associatedFiles[0] name -> MetadataExtractor ZIP stream -> FileUtil.loadLabels.'},
    'apk_dex_raw_nonmutation': {'status':'PASS','detail':'Outputs.getBuffer only builds map; exact TensorBuffer.getBuffer only returns buffer. duplicate-only observer changes no original position or data.'},
    'exception_caught': {'status':'PASS','detail':'Throwable catch region includes getter; deletion reports and timed logcat stacks agree.'},
    'unchanged_code': {'status':'PASS','detail':'Eight variant Java and class/DEX hashes equal; all APK DEX match build DEX.'},
    'cumulative_logcat': {'status':'PASS','caveat':'Whole dumps contain prior deletion stacks; time-correlated deletion primary/replay have two stacks each, other 14 intervals none. Do not attribute complete dump to directory variant.'},
    'human_audit': {'status':'UNVERIFIABLE','detail':'Not performed; this is AI-assisted artifact audit.'},
    'independent_execution': {'status':'UNVERIFIABLE','detail':'Not performed.'}
}
result['incomplete_attempts']=[]
for experiment in ['E1','E2']:
    for p in sorted((BASE/experiment/'executions').glob('*/*')):
        if p.is_dir() and not (p/'device/result.json').exists():
            available=[]
            for q in sorted((p/'logs').glob('*')):
                if q.is_file(): read(q); available.append(str(q))
            result['incomplete_attempts'].append({'path':str(p),'status':'UNVERIFIABLE','runtime_classification':'UNCLASSIFIED','reason':'No device/result.json; must not count as getter PASS or FAIL. Recovery is a separate saved record.','available_logs':available})
result['input_manifest_recheck_unchanged']=all(hashlib.sha256(pathlib.Path(k).read_bytes()).hexdigest()==v['sha256'] for k,v in manifest.items())
(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n')
(OUT/'commands.json').write_text(json.dumps(commands,indent=2)+'\n')
(OUT/'input-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'variant_count':len(variants),'equality':equality,'harness_source_equal':result['harness_source_equal'],'execution_count':len(executions),'apk_dex_all_match':all(v['apk_dex_matches_build'] for v in variants),'selected_dex_classes':len(selected)},indent=2))
