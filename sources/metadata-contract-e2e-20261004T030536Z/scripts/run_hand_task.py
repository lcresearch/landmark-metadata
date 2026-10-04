import argparse, json
from common import ROOT, save, run
ap=argparse.ArgumentParser();ap.add_argument('--run',required=True);args=ap.parse_args();base=ROOT/'E7';dest=base/'executions'/args.run;dest.mkdir(parents=True,exist_ok=False)
records=[]
for static in json.loads((base/'static-results.json').read_text()):
    name=static['variant'];folder=dest/name;folder.mkdir()
    p=run([base/'venv/bin/python',ROOT/'scripts/hand_task_one.py',ROOT/static['artifact_paths']['bundle'],base/'thumb_up.jpg',folder/'outputs'],folder/'logs/task',timeout=120)
    path=folder/'outputs/result.json';observed=json.loads(path.read_text()) if path.exists() else {'earliest_failing_stage':'worker_process','exit_code':p.returncode}
    records.append(dict(static,consumer='official MediaPipe HandLandmarker',consumer_version='0.10.14',platform='Linux x86_64 CPU; IMAGE mode',execution_run=args.run,observed=observed,raw_tflite_tensors='NOT_EXPOSED_BY_TASK_API'))
    save(dest/'results.json',records);print(name,observed.get('initialization_status'),observed.get('detect_status'),observed.get('path_exercised'),observed.get('exception_message',''),flush=True)
