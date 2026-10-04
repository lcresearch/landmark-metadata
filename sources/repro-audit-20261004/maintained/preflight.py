"""Pre-flight for Support 0.4.4's actual generated default Java category path.

Reports separate evidence scopes; never a universal model-validity judgment.
"""
import argparse, hashlib, json, pathlib, re, subprocess, sys, tempfile, traceback
sys.dont_write_bytecode=True
import numpy as np
from tflite_support import metadata
from tensorflow_lite_support.metadata import schema_py_generated as schema
from runtime import PYTHON, SOURCE_SCRIPTS, sha, save, run, require_external
from java_labels import LabelEncodingUnsupported, load_java_utf8_labels
sys.dont_write_bytecode=True
sys.path.insert(0,str(SOURCE_SCRIPTS))
from suite_static import canonical, md_bytes, associated, parse
from inspect_suite import inspect

def reference_check(data,info,reference_path):
    if reference_path is None:return {'status':'ABSTAIN','reason':'No independently supplied artifact-tied semantic reference.'}
    ref=json.loads(reference_path.read_text())
    required=['artifact_sha256','origin','source_path','source_sha256','source_uri','artifact_binding_explanation','kind']
    if any(k not in ref for k in required) or ref.get('origin')!='externally_supplied_contract':return {'status':'ABSTAIN','reason':'Reference lacks required external provenance or artifact binding.'}
    source=(reference_path.parent/ref['source_path']).resolve()
    if not source.is_file() or sha(source.read_bytes())!=ref['source_sha256']:return {'status':'ABSTAIN','reason':'Reference source bytes unavailable or hash mismatch.'}
    if ref['artifact_sha256']!=sha(data):return {'status':'ABSTAIN','reason':'Reference is not tied to this exact artifact digest; no implicit transfer to a mutant.'}
    if ref['source_sha256']==sha(data):return {'status':'ABSTAIN','reason':'The model itself is not an independent semantic reference.'}
    result={'reference_path':str(reference_path),'source_uri':ref['source_uri'],'source_sha256':ref['source_sha256'],
      'qualification':'Comparison against the supplied external contract. Source interpretation and claimed artifact binding still require human verification; this tool does not certify them.'}
    output_md=info['metadata']['subgraph_metadata'][0]['output_tensor_metadata']
    if ref['kind']=='output_roles':
        mapping=ref['metadata_name_to_role'];names=[x.get('name') for x in output_md]
        if any(n not in mapping for n in names):return dict(result,status='ABSTAIN',reason='Unmapped metadata name; roles are not inferred.')
        actual=[mapping[n] for n in names];result.update(actual_roles=actual,expected_roles=ref['expected_roles'],status='REFERENCE_AGREEMENT' if actual==ref['expected_roles'] else 'REFERENCE_DISAGREEMENT')
    elif ref['kind']=='class_order':
        files=associated(data);filename=ref['label_file']
        if filename not in files:return dict(result,status='ABSTAIN',reason='Referenced label payload missing.')
        try:
            labels=load_java_utf8_labels(files[filename])
        except LabelEncodingUnsupported as error:
            return dict(result,status='ABSTAIN',reason=str(error))
        result.update(status='REFERENCE_AGREEMENT' if labels==ref['expected_labels'] else 'REFERENCE_DISAGREEMENT',label_file=filename)
    else:result.update(status='ABSTAIN',reason='Unknown reference kind.')
    return result

def check(model_path,evidence,reference=None,baseline=None):
    evidence=require_external(evidence)
    data=model_path.read_bytes();evidence.mkdir(parents=True,exist_ok=False)
    report={'artifact_sha256':sha(data),'model_path':str(model_path.resolve()),'selected_consumer':'tflite-support 0.4.4 generated Java, default TensorProcessor, TensorLabel(List<String>, TensorBuffer).getCategoryList()',
      'STRUCTURAL':{'status':'UNKNOWN'},'REFERENCE_BACKED_SEMANTIC':{'status':'ABSTAIN','reason':'No independently supplied artifact-tied semantic reference.'},
      'DECODER_COMPATIBILITY':{'status':'NOT_REACHED','findings':[]},'PRESERVATION':{'status':'NOT_REQUESTED'},'UNKNOWN_ABSTAIN':[]}
    try:
        model=parse(data);sub=model.Subgraphs(0);idx,md=md_bytes(data)
        graph_outputs=[]
        for i in range(sub.OutputsLength()):
            t=sub.Tensors(sub.Outputs(i));signature=t.ShapeSignatureAsNumpy()
            graph_outputs.append({'position':i,'tensor_index':int(sub.Outputs(i)),'shape':t.ShapeAsNumpy().tolist(),'shape_signature':signature.tolist() if isinstance(signature,np.ndarray) else [],'dtype_enum':int(t.Type())})
        report['STRUCTURAL']['facts']={'graph_output_count':sub.OutputsLength(),'graph_outputs':graph_outputs,'metadata_present':md is not None}
        report['canonical_graph_sha256']=sha(canonical(data))
        if baseline:
            b=baseline.read_bytes();bm=parse(b);bi,_=md_bytes(b)
            nonmeta=model.BuffersLength()==bm.BuffersLength() and idx==bi and all(np.array_equal(model.Buffers(i).DataAsNumpy(),bm.Buffers(i).DataAsNumpy()) for i in range(model.BuffersLength()) if i!=idx)
            report['PRESERVATION']={'baseline_sha256':sha(b),'canonical_equal':canonical(data)==canonical(b),'nonmetadata_buffers_equal':nonmeta,'status':'PRESERVED_UNDER_DEFINED_COMPARISON' if nonmeta and canonical(data)==canonical(b) else 'DIFFERENT_OR_UNSUPPORTED_COMPARISON'}
        if md is None:
            report['STRUCTURAL']['status']='ABSTAIN_NO_METADATA';report['DECODER_COMPATIBILITY']['status']='ABSTAIN_NO_METADATA';return report
        info=inspect(data);output_md=info['metadata']['subgraph_metadata'][0].get('output_tensor_metadata',[])
        report['STRUCTURAL']['facts']['metadata_output_count']=len(output_md)
        try:
            pop=metadata.MetadataPopulator.with_model_buffer(data);pop.load_metadata_buffer(md);pop.populate();report['STRUCTURAL']['status']='ACCEPTED_BY_METADATA_POPULATOR_0_4_4'
        except Exception as exc:
            report['STRUCTURAL'].update(status='REJECTED_BY_METADATA_POPULATOR_0_4_4',diagnostic=str(exc),exception_type=type(exc).__name__);return report
        report['REFERENCE_BACKED_SEMANTIC']=reference_check(data,info,reference)
        p=run([PYTHON,SOURCE_SCRIPTS/'codegen_one.py',model_path.resolve(),evidence/'generated',evidence/'generation.json'],evidence/'logs/codegen',timeout=90)
        if p.returncode or not (evidence/'generation.json').exists():
            report['DECODER_COMPATIBILITY'].update(status='ABSTAIN_GENERATION_FAILED',exit_code=p.returncode);return report
        generation=json.loads((evidence/'generation.json').read_text());report['generation_diagnostics']=generation['diagnostics']
        sources=[pathlib.Path(p) for p in generation['files'] if p.endswith('.java')]
        if len(sources)!=1:report['DECODER_COMPATIBILITY']['status']='ABSTAIN_NO_UNIQUE_SOURCE';return report
        text=sources[0].read_text();report['generated_source_path']=str(sources[0]);report['generated_source_sha256']=sha(sources[0].read_bytes())
        tensor_pairs=re.findall(r'Tensor\s+(\w+)Tensor\s*=\s*model.getOutputTensor\((\d+)\)',text)
        file_pairs=re.findall(r'String\s+(\w+)LabelsFileName\s*=\s*extractor.getOutputTensorMetadata\((\d+)\).associatedFiles\((\d+)\).name\(\)',text)
        tensor_bindings={f:int(i) for f,i in tensor_pairs if sum(f==name for name,_ in tensor_pairs)==1}
        file_bindings={f:(int(i),int(j)) for f,i,j in file_pairs if sum(f==name for name,_,_ in file_pairs)==1}
        getters=re.findall(r'public List<Category> (\w+)\(\)\s*\{\s*return new TensorLabel\((\w+)Labels,\s*postprocess(\w+)\((\w+)\)\)\.getCategoryList\(\);',text)
        files=associated(data);findings=[]
        for getter,label_field,processor,tensor_field in getters:
            finding={'getter':getter,'status':'ABSTAIN','expression':'TensorLabel(List<String>, TensorBuffer).getCategoryList()'}
            if tensor_field not in tensor_bindings or label_field not in file_bindings:
                finding['diagnostic']='Unresolved actual tensor/associated-file binding.';findings.append(finding);continue
            i=tensor_bindings[tensor_field];mi,fi=file_bindings[label_field];filename=output_md[mi]['associated_files'][fi]['name']
            finding.update(output_position=i,metadata_position_for_labels=mi,associated_file_position=fi,label_file=filename)
            body=re.search(r'private TensorProcessor buildDefault'+re.escape(processor)+r'Postprocessor\(\)\s*\{(.*?)\n  \}',text,re.S)
            ops=re.findall(r'\.add\(new (\w+)\(',body.group(1)) if body else []
            if not body or any(op!='DequantizeOp' for op in ops):
                finding['diagnostic']='Default postprocessor is outside the modeled shape-preserving path.';findings.append(finding);continue
            shape=graph_outputs[i]['shape'];signature=graph_outputs[i]['shape_signature']
            if any(d<=0 for d in shape+signature):
                finding['diagnostic']='Dynamic or nonpositive output shape/signature; fixed decoder shape cannot be justified.';findings.append(finding);continue
            if filename not in files:
                finding['diagnostic']='Actually referenced associated label payload is unavailable.';findings.append(finding);continue
            try:
                labels=load_java_utf8_labels(files[filename])
            except LabelEncodingUnsupported as error:
                finding['diagnostic']=str(error);findings.append(finding);continue
            axis=next((a for a,n in enumerate(shape) if n>1),None)
            finding.update(shape=shape,selected_axis=axis,label_count=len(labels),label_sha256=sha(files[filename]))
            if axis is None:reason='no axis has size greater than one'
            elif shape[axis]!=len(labels):reason=f'selected axis {axis} has size {shape[axis]}, which differs from label count {len(labels)}'
            elif axis!=len(shape)-1:reason=f'selected axis {axis} is not the final axis required by getCategoryList'
            else:reason=None
            finding['status']='INCOMPATIBLE' if reason else 'COMPATIBLE_PRECONDITIONS'
            finding['diagnostic']=f'Generated category getter {getter} for output {i} is incompatible with the selected TensorLabel path because {reason}.' if reason else f'Generated category getter {getter} for output {i} satisfies the modeled TensorLabel default-path preconditions; label meaning is not checked.'
            findings.append(finding)
        statuses=[x['status'] for x in findings]
        report['DECODER_COMPATIBILITY']={'status':'INCOMPATIBLE' if 'INCOMPATIBLE' in statuses else 'ABSTAIN' if 'ABSTAIN' in statuses else 'COMPATIBLE_PRECONDITIONS' if statuses else 'INAPPLICABLE_NO_SELECTED_GETTER','findings':findings}
        return report
    except Exception as exc:
        report['controller_error']={'exception_type':type(exc).__name__,'message':str(exc),'trace':traceback.format_exc()};return report
    finally:
        if report['REFERENCE_BACKED_SEMANTIC']['status']=='ABSTAIN':report['UNKNOWN_ABSTAIN'].append('Semantic meaning/order is not established by this run.')
        report['UNKNOWN_ABSTAIN'].append('Source compilation, numerical inference and deployed application behavior are not certified by this static command.')
        save(evidence/'result.json',report)

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('model',type=pathlib.Path);ap.add_argument('--evidence-dir',required=True,type=pathlib.Path);ap.add_argument('--reference',type=pathlib.Path);ap.add_argument('--baseline',type=pathlib.Path);args=ap.parse_args()
    report=check(args.model,args.evidence_dir.resolve(),args.reference,args.baseline);print(json.dumps(report,indent=2))
    if 'controller_error' in report or report['DECODER_COMPATIBILITY']['status'].startswith('ABSTAIN_GENERATION'):raise SystemExit(3)
    if report['STRUCTURAL']['status'].startswith('REJECTED') or report['DECODER_COMPATIBILITY']['status']=='INCOMPATIBLE' or report['REFERENCE_BACKED_SEMANTIC']['status']=='REFERENCE_DISAGREEMENT':raise SystemExit(2)
if __name__=='__main__':main()
