import hashlib,json,pathlib,struct,zipfile,sys
from common import ROOT,save,sha
OLD=pathlib.Path('/workspace/metadata-contract-e2e-20261004T030536Z')
records=[];checks=[]
def check(name,value,detail=None):
    checks.append({'check':name,'status':'PASS' if value is True else 'FAIL' if value is False else 'UNVERIFIABLE','detail':detail})
def load(p):return json.loads(p.read_text())
for ex in ['E1','E2']:
    path=ROOT/ex/'executions/primary/results.json'
    if not path.exists():
        check(ex+' fresh execution records available',None,'Missing results.json');continue
    rows=load(path);base=next(r for r in rows if r['variant']=='original');basedir=ROOT/base['artifact_paths']['execution']/'device'
    priorrows=load(OLD/ex/'executions/primary/results.json')
    for r in rows:
        variant=r['variant'];unit=ex+'/'+variant;folder=ROOT/ex/'variants'/variant
        model=(folder/'model.tflite').read_bytes();workspace_hash=sha(model)
        with zipfile.ZipFile(folder/'build/consumer.apk') as apk: apk_bytes=apk.read('assets/model.tflite')
        device_hash=r.get('observed',{}).get('loaded_asset_sha256')
        check(unit+' workspace/APK/runtime asset identity',workspace_hash==sha(apk_bytes)==device_hash,{'workspace':workspace_hash,'apk_asset':sha(apk_bytes),'runtime_asset':device_hash})
        prior=next(p for p in priorrows if p['variant']==variant)
        source=(folder/'generated/src/main/java/org/example/contract/ContractModel.java').read_bytes()
        oldsource=(OLD/ex/'variants'/variant/'generated/src/main/java/org/example/contract/ContractModel.java').read_bytes()
        check(unit+' unmodified generated source matches historical',source==oldsource,{'fresh_sha256':sha(source),'historical_sha256':sha(oldsource)})
        classroot=folder/'build/classes';oldclassroot=OLD/ex/'variants'/variant/'build/classes'
        actualclasses={str(p.relative_to(classroot)):sha(p.read_bytes()) for p in sorted(classroot.rglob('ContractModel*.class'))}
        historicalclasses={str(p.relative_to(oldclassroot)):sha(p.read_bytes()) for p in sorted(oldclassroot.rglob('ContractModel*.class'))}
        actualdex={p.name:sha(p.read_bytes()) for p in (folder/'build/dex').glob('*.dex')}
        check(unit+' class and DEX records recomputed from actual files',actualclasses==r['build'].get('generated_class_hashes') and actualdex==r['build'].get('dex_hashes'))
        check(unit+' generated classes match historical actual files',actualclasses==historicalclasses and bool(actualclasses))
        check(unit+' generated source/classes/DEX equal fresh original',r['source_sha256']==base['source_sha256'] and r['build'].get('generated_class_hashes')==base['build'].get('generated_class_hashes') and r['build'].get('dex_hashes')==base['build'].get('dex_hashes'))
        check(unit+' canonical/nonmetadata preservation',r['preservation_check']['canonical_equal'] and r['preservation_check']['nonmetadata_buffers_equal'])
        if variant!='description_control':check(unit+' embedded metadata/preZIP preservation',r['preservation_check']['embedded_metadata_equal'] and r['preservation_check']['flatbuffer_prefix_equal'])
        freshdir=ROOT/r['artifact_paths']['execution']/'device';priordir=OLD/prior['artifact_paths']['execution']/'device'
        observations=[]
        for name in ['gray127','rgb_pattern']:
            obs=next((o for o in r.get('observed',{}).get('observations',[]) if o.get('input')==name),{})
            raw=freshdir/(name+'-output-0.f32');refraw=basedir/raw.name;oldraw=priordir/raw.name
            if not raw.exists():check(unit+'/'+name+' raw output available',None);continue
            payload=raw.read_bytes();scores=list(struct.unpack('<'+str(len(payload)//4)+'f',payload));top=sorted(range(len(scores)),key=lambda i:(-scores[i],i))[:5]
            check(unit+'/'+name+' input equal original', (freshdir/(name+'-input.rgb')).read_bytes()==(basedir/(name+'-input.rgb')).read_bytes())
            check(unit+'/'+name+' all raw output bytes equal original',payload==refraw.read_bytes(),{'sha256':sha(payload)})
            check(unit+'/'+name+' all raw output bytes equal historical',payload==oldraw.read_bytes(),{'historical_sha256':sha(oldraw.read_bytes())})
            check(unit+'/'+name+' independently recomputed top5 matches logged',top==[t['index'] for t in obs.get('top5_raw',[])])
            decoded=freshdir/(name+'-decoded.json');basedec=basedir/decoded.name;olddec=priordir/decoded.name
            dr={'input':name,'raw_output_sha256':sha(payload),'raw_value_count':len(scores),'argmax_index':top[0],'top5_indices':top,'inference_status':obs.get('inference_status'),'generated_getter_status':obs.get('generated_getter_status'),'earliest_failing_stage':obs.get('earliest_failing_stage'),'exception_type':obs.get('exception_type'),'exception_message':obs.get('exception_message'),'stack_trace':obs.get('stack_trace')}
            if decoded.exists():
                a=load(decoded);b=load(basedec);dr['decoded_count']=len(a)
                bits=[struct.unpack('<i',struct.pack('<f',s))[0] for s in scores]
                check(unit+'/'+name+' all returned score bits match raw positions',[x['score_float_bits'] for x in a]==bits)
                check(unit+'/'+name+' all returned score bits match original',[x['score_float_bits'] for x in a]==[x['score_float_bits'] for x in b])
                check(unit+'/'+name+' decoded result matches historical',a==load(olddec))
                changed=[i for i,(x,y) in enumerate(zip(a,b)) if x['label']!=y['label']];dr['changed_label_count']=len(changed);dr['changed_label_positions']=changed
                dr['argmax_association']={'position':top[0],'score':scores[top[0]],'original_label':b[top[0]]['label'],'variant_label':a[top[0]]['label']}
                dr['category_index_field_values']=sorted(set(x['category_index_field'] for x in a))
                if variant=='label_permutation':
                    check(unit+'/'+name+' cyclic shift association',len(a)==len(b) and all(a[i]['label']==b[(i+1)%len(b)]['label'] for i in range(len(a))))
                    check(unit+'/'+name+' historical label change count 999 independently recovered',len(changed)==999)
                else:check(unit+'/'+name+' decoded association unchanged/restored',a==b)
            else:
                dr['decoded_result']='NOT_RETURNED';dr['decoded_equality']='NOT_APPLICABLE'
                check(unit+'/'+name+' expected deletion failure at real getter',variant=='label_deletion' and obs.get('inference_status')=='PASS' and obs.get('generated_getter_status')=='FAIL' and obs.get('earliest_failing_stage')=='generated_getter' and obs.get('exception_type')=='java.lang.IllegalArgumentException' and obs.get('exception_message')=='Label number 999 mismatch the shape on axis 1' and 'ContractModel$Outputs.getProbabilityAsCategoryList(ContractModel.java:47)' in obs.get('stack_trace',''))
            observations.append(dr)
        records.append({'experiment_id':ex,'component_name':r['component_name'],'variant':variant,'model_sha256':workspace_hash,'canonical_graph_sha256':r['canonical_graph_sha256'],'metadata_sha256':r['metadata_sha256'],'associated_file_sha256':r['associated_file_sha256'],'apk_sha256':r['build'].get('apk_sha256'),'apk_asset_sha256':sha(apk_bytes),'runtime_asset_sha256':device_hash,'structural_consumer':'tflite_support.metadata.MetadataPopulator.with_model_buffer/load_metadata_buffer/populate','preservation_check':r['preservation_check'],'raw_output_hashes':r['raw_output_hashes'],'structural_status':r['structural_status'],'generation_status':r['generation_status'],'compile_status':r['compile_status'],'package_status':r['package_status'],'load_status':r['load_status'],'inference_status':r['inference_status'],'decoder_status':r['decoder_status'],'earliest_failing_stage':r.get('earliest_failing_stage'),'source_sha256':sha(source),'generated_classes':r['build'].get('generated_class_hashes'),'dex_hashes':r['build'].get('dex_hashes'),'observations':observations,'artifact_paths':r['artifact_paths'],'reference_source':None,'semantic_check':'ABSTAIN_NO_INDEPENDENT_CLASS_ORDER_REFERENCE','consumer':r['consumer'],'runtime_version':r['runtime_version'],'generator_version':r['generator_version'],'compiler_version':r['compiler_version'],'platform':r['observed'].get('platform'),'notes':['Fresh output and AVD using same installed toolchain; one primary per variant with two repeated input observations.','AssetManager byte hash is obtained before newInstance from the same Context and asset name; generated Model.createModel path unchanged.','Instrumented harness catches getter exceptions; no application crash claim.']})
check('eight phase/variant execution records completed',len(records)==8)
check('all fresh generated source/classes/DEX identical across phase records', bool(records) and all(r['source_sha256']==records[0]['source_sha256'] and r['generated_classes']==records[0]['generated_classes'] and r['dex_hashes']==records[0]['dex_hashes'] for r in records))
result={'scope':'Agent fresh-output/AVD construction audit; no independent human verification','records':records,'checks':checks,'summary':{s:sum(c['status']==s for c in checks) for s in ['PASS','FAIL','UNVERIFIABLE']},'denominators':{'phase_variant_execution_records':len(records),'unique_artifact_consumer_configurations':len(set((r['model_sha256'],r['consumer'],r['runtime_version'],r['generator_version'],r['compiler_version'],r['platform']) for r in records)),'byte_distinct_models':len(set(r['model_sha256'] for r in records)),'canonical_graphs':len(set(r['canonical_graph_sha256'] for r in records)),'input_observations':sum(len(r['observations']) for r in records)},'human_audit_status':'PENDING','unverified_claims':['Independent class-order semantic correctness','Independent human verification','SDK-from-archive clean installation','Untouched generated Gradle project build','Prediction accuracy or generalization']}
save(ROOT/'results.json',result)
lines=['# E1/E2 fresh construction audit','','This agent audit freshly regenerated and built the same eight phase/variant execution records, then executed the actual generated Android interface on two predetermined synthetic inputs per record. The SDK/JDK/Python installation was reused; the output directories, debug signing key and Android AVD were new. This is not an independent human reproduction or SDK-from-archive reconstruction.','','## Observed phase/variant records','','| Experiment | Variant | Structure | Generation | Compile/package | Load | Inference | Actual getter |','|---|---|---|---|---|---|---|---|']
for r in records:lines.append('| '+' | '.join([r['experiment_id'],r['variant'],r['structural_status'],r['generation_status'],r['compile_status']+'/'+r['package_status'],r['load_status'],r['inference_status'],r['decoder_status']])+' |')
lines+=['','## Audit checks','',str(result['summary']),'', 'Denominators: '+str(result['denominators']),'','These are correlated software assertions over five artifact-by-consumer configurations, not 180 independent experiments or an accuracy metric. Unverified semantic/human claims are listed separately in results.json. Per-check results and exact hashes: `results.json`. Source snapshots and patches preserve the sole instrumentation addition (asset identity) and orchestration gate change (fresh primary sufficient before E2). Every subprocess command and stdout/stderr are preserved under each unit and `commands-executed.sh`.','','| Check | Status |','|---|---|']
for c in checks:lines.append('| '+c['check']+' | '+c['status']+' |')
lines+=['','## Interpretation and remaining boundaries','','The fresh E1 deletion reproduces java.lang.IllegalArgumentException: Label number 999 mismatch the shape on axis 1, reached through the actual unmodified generated getter after successful inference on both tested inputs. Original, description and restoration complete successfully. The fresh E2 permutation completes successfully, preserves all raw/returned score bits and changes 999 displayed labels on each input; inverse restoration recovers the original decoded lists. At RGB position 904, score 0.23542051017284393 remains fixed while window screen changes to window shade. Raw outputs are compared byte-for-byte on the tested inputs; no inference accuracy or universal-input numerical claim is made. E2 label permutation changes exposed association relative to the original, without an independently tied class-order reference. A successful decoder is not semantic validation.','','A new harness hashes the installed AssetManager resource immediately before generated newInstance uses the identical asset name and Context. It does not intercept or replace the native interpreter buffer. Generated-source inspection and library tracing therefore remain part of the load-identity chain. Whole APK byte equality is intentionally not assessed; the embedded model and signing key differ. Generated classes are compared against historical classes, whereas full DEX is compared across fresh variants only because the harness changed.','','The build compiles unmodified generated Java inside the disclosed custom minimal instrumentation harness; it does not claim that the untouched generated Gradle project builds. Fresh results are compared to preserved historical primary outputs. No new independent model or blinded held-out validation is implied. New same-APK replay was not required by this construction audit. Human verification, standalone archived-toolchain installation and independent class-order reference remain pending.']
(ROOT/'AUDIT_REPORT.md').write_text('\n'.join(lines)+'\n')
print(json.dumps(result['summary']));sys.exit(1 if result['summary']['FAIL'] else 0)
