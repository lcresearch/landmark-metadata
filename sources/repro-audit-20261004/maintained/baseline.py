"""Read-only model checks with all output confined to the supplied new directory."""
import argparse
import hashlib
import importlib.metadata
import json
import math
from pathlib import Path
import sys
sys.dont_write_bytecode = True
import traceback
from java_labels import LabelEncodingUnsupported, load_java_utf8_labels
from runtime import require_external

sys.dont_write_bytecode = True

def sha(data):
    return hashlib.sha256(data).hexdigest()

def save(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')

def model_facts(data):
    import numpy as np
    from tflite_support import metadata
    from tensorflow_lite_support.metadata import schema_py_generated as schema
    model = schema.Model.GetRootAsModel(data, 0)
    graph = model.Subgraphs(0)
    md = None
    for i in range(model.MetadataLength()):
        entry = model.Metadata(i)
        if entry.Name() == b'TFLITE_METADATA':
            md = model.Buffers(entry.Buffer()).DataAsNumpy().tobytes()
    displayer = metadata.MetadataDisplayer.with_model_buffer(data)
    info = json.loads(displayer.get_metadata_json())
    outputs = []
    for i in range(graph.OutputsLength()):
        tensor = graph.Tensors(graph.Outputs(i))
        sig = tensor.ShapeSignatureAsNumpy()
        outputs.append({'position': i, 'tensor_index': int(graph.Outputs(i)),
                        'shape': tensor.ShapeAsNumpy().tolist(),
                        'shape_signature': sig.tolist() if isinstance(sig, np.ndarray) else []})
    return model, md, displayer, info, outputs

def check(mode, model_path, dest):
    dest = require_external(dest)
    from tflite_support import metadata
    data = model_path.read_bytes()
    report = {'check': mode, 'model_sha256': sha(data), 'model_path': str(model_path),
              'status': 'NOT_REACHED', 'stage': mode,
              'tflite_support_version': importlib.metadata.version('tflite-support')}
    try:
        if mode == 'task_init':
            from tflite_support.task import core, processor, vision
            report['options'] = {'num_threads': 1, 'use_coral': False, 'max_results': -1}
            options = vision.ImageClassifierOptions(
                base_options=core.BaseOptions(file_name=str(model_path), num_threads=1, use_coral=False),
                classification_options=processor.ClassificationOptions(max_results=-1))
            classifier = vision.ImageClassifier.create_from_options(options)
            report.update(status='PASS', stage='TASK_INITIALIZATION',
                          classify_status='NOT_RUN', inference_status='NOT_RUN',
                          decoder_status='NOT_RUN')
            del classifier
            return report
        model, md, displayer, info, outputs = model_facts(data)
        output_md = info['subgraph_metadata'][0].get('output_tensor_metadata', [])
        report['facts'] = {'graph_output_count': len(outputs),
                           'output_metadata_entry_count': len(output_md),
                           'graph_outputs': outputs}
        if mode == 'displayer':
            save(dest / 'metadata.json', info)
            packed = displayer.get_packed_associated_file_list()
            payloads = []
            for i, name in enumerate(packed):
                payload = displayer.get_associated_file_buffer(name)
                (dest / ('associated-%d.bin' % i)).write_bytes(payload)
                payloads.append({'name': name, 'bytes': len(payload), 'sha256': sha(payload)})
            report.update(status='READABLE', stage='METADATA_DISPLAY', associated_payloads=payloads,
                          qualification='Readability and resource retrieval, not semantic or consumer validation.')
        elif mode == 'populator':
            copied = dest / 'populated-copy.tflite'
            copied.write_bytes(data)
            populator = metadata.MetadataPopulator.with_model_file(str(copied))
            populator.load_metadata_buffer(md)
            populator.populate()
            populated = copied.read_bytes()
            report.update(status='ACCEPTED', stage='METADATA_POPULATION',
                          populated_copy=str(copied), populated_sha256=sha(populated),
                          populated_bytes_equal_input=(populated == data),
                          qualification='Official population acceptance; label-order meaning is not established.')
        elif mode == 'simple_baseline':
            report['selected_path'] = 'TensorLabel(List<String>, TensorBuffer).getCategoryList(); default shape-preserving processor'
            report['binding_scope'] = 'Single graph output and unique output-0 TENSOR_AXIS_LABELS resource; the core generated binding is checked separately against existing E5 output.'
            if len(outputs) != 1 or len(output_md) != 1:
                report.update(status='ABSTAIN', diagnostic='Outside single-output baseline scope.'); return report
            candidates = [(i, f) for i, f in enumerate(output_md[0].get('associated_files', []))
                          if f.get('type') == 'TENSOR_AXIS_LABELS']
            if len(candidates) != 1:
                report.update(status='ABSTAIN', diagnostic='No unique selected label resource.'); return report
            file_index, file_info = candidates[0]
            payload = displayer.get_associated_file_buffer(file_info['name'])
            try:
                labels = load_java_utf8_labels(payload)
            except LabelEncodingUnsupported as error:
                report.update(status='ABSTAIN', diagnostic=str(error)); return report
            shape = outputs[0]['shape']; signature = outputs[0]['shape_signature']
            report['selected_binding'] = {'output_position': 0, 'metadata_position': 0,
                                          'associated_file_position': file_index,
                                          'label_file': file_info['name'], 'label_count': len(labels),
                                          'label_payload_sha256': sha(payload)}
            if any(d <= 0 for d in shape + signature):
                report.update(status='ABSTAIN', diagnostic='Dynamic or nonpositive shape/signature.'); return report
            axis = next((i for i, d in enumerate(shape) if d > 1), None)
            constraints = {
                'nonunit_axis_exists': axis is not None,
                'labels_match_selected_axis': axis is not None and len(labels) == shape[axis],
                'selected_axis_is_last': axis is not None and axis == len(shape) - 1,
                'labels_match_flat_size': len(labels) == math.prod(shape),
            }
            report.update(selected_axis=axis, flat_size=math.prod(shape), constraints=constraints,
                          status='COMPATIBLE_PRECONDITIONS' if all(constraints.values()) else 'INCOMPATIBLE',
                          stage='STATIC_SELECTED_DECODER_CHECK',
                          diagnostic='; '.join(k for k, v in constraints.items() if not v) or 'All modeled preconditions hold.',
                          semantic_status='ABSTAIN_NO_CLASS_ORDER_REFERENCE')
        else:
            raise ValueError('Unknown mode: ' + mode)
    except Exception as exc:
        report.update(status='FAIL', earliest_failing_stage=report['stage'],
                      exception_type=type(exc).__name__, exception_message=str(exc),
                      stack_trace=traceback.format_exc())
        if mode == 'task_init':
            report.update(stage='TASK_INITIALIZATION', earliest_failing_stage='TASK_INITIALIZATION',
                          classify_status='NOT_REACHED', inference_status='NOT_REACHED', decoder_status='NOT_REACHED')
    return report

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode'); parser.add_argument('model', type=Path); parser.add_argument('dest', type=Path)
    args = parser.parse_args()
    args.dest = require_external(args.dest)
    args.dest.mkdir(parents=True, exist_ok=False)
    result = check(args.mode, args.model.resolve(), args.dest)
    save(args.dest / 'result.json', result)
    print(json.dumps(result, indent=2))
    sys.exit(2 if result['status'] in ['FAIL', 'INCOMPATIBLE'] else 0)
