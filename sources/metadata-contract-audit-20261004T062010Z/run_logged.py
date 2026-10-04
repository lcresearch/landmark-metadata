#!/usr/bin/env python3
"""Run exact argv and preserve output in a new audit log prefix."""
import datetime, json, os, pathlib, subprocess, sys
prefix = pathlib.Path(sys.argv[1])
argv = sys.argv[2:]
prefix.parent.mkdir(parents=True, exist_ok=True)
record = {'argv': argv, 'cwd': os.getcwd(), 'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
env = os.environ.copy()
env['PYTHONDONTWRITEBYTECODE'] = '1'
record['environment_override'] = {'PYTHONDONTWRITEBYTECODE': '1'}
with pathlib.Path(str(prefix)+'.stdout').open('xb') as stdout, pathlib.Path(str(prefix)+'.stderr').open('xb') as stderr:
    result = subprocess.run(argv, stdout=stdout, stderr=stderr, env=env)
record['returncode'] = result.returncode
record['finished_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
with pathlib.Path(str(prefix)+'.command.json').open('x') as handle:
    json.dump(record, handle, indent=2)
print(json.dumps(record))
sys.exit(result.returncode)
