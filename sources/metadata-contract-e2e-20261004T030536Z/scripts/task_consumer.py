import argparse, inspect, json, pathlib, shutil
from tflite_support.task import vision
from tensorflow_lite_support.python.task.vision.pybinds import _pywrap_image_classifier
from common import ROOT, PYTHON, sha, save, run
ap=argparse.ArgumentParser();ap.add_argument('--run',required=True);args=ap.parse_args()
destination=ROOT/'E3/executions'/args.run;destination.mkdir(parents=True,exist_ok=False)
variants={}
for exp,selected in [('E1',['original','description_control','label_deletion']),('E2',['label_permutation'])]:
    for r in json.loads((ROOT/exp/'static-results.json').read_text()):
        if r['variant'] in selected:variants[r['variant']]=(exp,r)
records=[]
native=pathlib.Path(_pywrap_image_classifier.__file__);python_source=pathlib.Path(inspect.getfile(vision.ImageClassifier))
implementation={'python_source':str(python_source),'python_source_sha256':sha(python_source.read_bytes()),'native_library':str(native),'native_library_sha256':sha(native.read_bytes()),'package':'tflite-support 0.4.4 CPython 3.11 Linux x86_64','bundled_interpreter_version':'Not separately established; exact native wheel/binary preserved, not assumed equal to Android 2.13.0.'}
save(ROOT/'E3/implementation.json',implementation)
for name,(exp,static) in variants.items():
    folder=destination/name;folder.mkdir()
    model=ROOT/exp/'variants'/name/'model.tflite'
    p=run([PYTHON,ROOT/'scripts/task_one.py',model,ROOT/'E1/executions/primary/original/device',folder/'outputs'],folder/'logs/task',timeout=120)
    result_path=folder/'outputs/result.json';observed=json.loads(result_path.read_text()) if result_path.exists() else {'earliest_failing_stage':'worker_process','worker_exit_code':p.returncode}
    row={'experiment_id':'E3','component_name':static['component_name'],'component_sha256':static['component_sha256'],'variant':name,'variant_sha256':static['variant_sha256'],'canonical_graph_sha256':static['canonical_graph_sha256'],
      'metadata_sha256':static['metadata_sha256'],'associated_file_sha256':static['associated_file_sha256'],'preservation_check':static['preservation_check'],'consumer':'official Task Library ImageClassifier Python/C++','consumer_version':'tflite-support 0.4.4',
      'platform':'Linux x86_64 CPython 3.11.16 CPU num_threads=1 use_coral=False','runtime_version':implementation['bundled_interpreter_version'],
      'generation_status':'NOT_APPLICABLE_PREBUILT_TASK_API','compile_status':'NOT_APPLICABLE_PREBUILT_TASK_API','source_record':str((ROOT/exp/'static-results.json').relative_to(ROOT)),
      'execution_run':args.run,'evidence_status':'FRESH_TASK_EXECUTION','structural_status':static['structural_status'],'semantic_check':'ABSTAIN_NO_INDEPENDENT_CLASS_ORDER_REFERENCE','raw_output_hashes':'NOT_EXPOSED_BY_PUBLIC_TASK_API',
      'observed':observed,'artifact_paths':{'model':str(model.relative_to(ROOT)),'execution':str(folder.relative_to(ROOT))}}
    records.append(row);save(destination/'results.json',records)
    print(name,observed.get('initialization_status'),observed.get('classify_status'),observed.get('exception_message',''),flush=True)
