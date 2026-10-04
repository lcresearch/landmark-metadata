import hashlib, json, pathlib, struct, sys, traceback
import numpy as np
from tflite_support.task import core, processor, vision
from common import save
model,inputs,dest=map(pathlib.Path,sys.argv[1:4]);dest.mkdir(parents=True,exist_ok=True)
report={'model_sha256':hashlib.sha256(model.read_bytes()).hexdigest(),'initialization_status':'NOT_REACHED','classify_status':'NOT_REACHED','inference_status':'NOT_REACHED','decoder_status':'NOT_REACHED','observations':[]}
stage='task_initialization'
try:
    options=vision.ImageClassifierOptions(base_options=core.BaseOptions(file_name=str(model),num_threads=1,use_coral=False),classification_options=processor.ClassificationOptions(max_results=-1))
    classifier=vision.ImageClassifier.create_from_options(options)
    report['initialization_status']='PASS';save(dest/'result.json',report)
    for case in ['gray127','rgb_pattern']:
        stage='input_preparation';data=(inputs/(case+'-input.rgb')).read_bytes();array=np.frombuffer(data,dtype=np.uint8).reshape(224,224,3).copy()
        image=vision.TensorImage.create_from_array(array)
        row={'input':case,'input_sha256':hashlib.sha256(data).hexdigest(),'input_preparation_status':'PASS'}
        stage='classify_combined_inference_and_decoding';result=classifier.classify(image)
        heads=[]
        for head in result.classifications:
            heads.append({'head_index':head.head_index,'categories':[{'index':c.index,'label':c.category_name,'display_name':c.display_name,'score':c.score,'score_float_bits':struct.unpack('<I',struct.pack('<f',c.score))[0]} for c in head.categories]})
        save(dest/(case+'-decoded.json'),heads)
        row.update(classify_status='PASS',returned_categories=sum(len(h['categories']) for h in heads));report['observations'].append(row)
    report.update(classify_status='PASS',inference_status='PASS',decoder_status='PASS')
except Exception as exc:
    report.update(earliest_failing_stage=stage,exception_type=type(exc).__name__,exception_message=str(exc),stack_trace=traceback.format_exc())
    if stage=='task_initialization':report['initialization_status']='FAIL'
    elif stage=='classify_combined_inference_and_decoding':report.update(classify_status='FAIL',inference_status='UNKNOWN_WITHIN_COMBINED_CALL',decoder_status='UNKNOWN_WITHIN_COMBINED_CALL')
    else:report['input_preparation_status']='FAIL'
save(dest/'result.json',report)
print(json.dumps({k:v for k,v in report.items() if k not in ['observations','stack_trace']},indent=2))
