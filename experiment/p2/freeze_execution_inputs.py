from pathlib import Path
import hashlib,json,datetime
r=Path(__file__).resolve().parents[1]
paths=[r/'EXPERIMENT_P2_PLAN.md',r/'PLAN_FREEZE.json',r/'dependencies/resolved-lock.json',r/'static-results.json',r/'build-results.json']+sorted((r/'scripts').glob('*'))+sorted((r/'build').glob('*/*/consumer.apk'))
record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'before_first_model_execution','files':[{'path':str(p.relative_to(r)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths if p.is_file()]}
with (r/'EXECUTION_INPUT_FREEZE.json').open('x') as f:json.dump(record,f,indent=2)
