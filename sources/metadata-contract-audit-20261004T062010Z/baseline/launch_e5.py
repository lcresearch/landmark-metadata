"""Execute unchanged E5 with a logger shim that cannot append to sealed logs."""
import datetime
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys

sys.dont_write_bytecode = True
AUDIT = Path(__file__).resolve().parent
OLD = Path('/workspace/metadata-contract-e2e-20261004T030536Z')
sys.path.insert(0, str(OLD / 'scripts'))
import common

def isolated_run(command, log, timeout=120, cwd=None, binary=False):
    log = Path(log).resolve()
    if not log.is_relative_to(AUDIT):
        raise RuntimeError('Refusing log outside new audit tree: ' + str(log))
    log.parent.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy(); env['JAVA_HOME'] = str(common.JDK); env['PYTHONDONTWRITEBYTECODE'] = '1'
    record = {'command': list(map(str, command)), 'cwd': str(cwd or AUDIT),
              'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'adaptation': 'Original common.run append to OLD/commands-executed.sh omitted; all output under new audit tree.'}
    try:
        process = subprocess.run(record['command'], cwd=record['cwd'], env=env,
                                 capture_output=True, timeout=timeout)
        record['exit_code'] = process.returncode
        log.with_suffix(log.suffix + '.stdout').write_bytes(process.stdout)
        log.with_suffix(log.suffix + '.stderr').write_bytes(process.stderr)
    except subprocess.TimeoutExpired as exc:
        record.update(exit_code=None, timeout_seconds=timeout)
        log.with_suffix(log.suffix + '.stdout').write_bytes(exc.stdout or b'')
        log.with_suffix(log.suffix + '.stderr').write_bytes(exc.stderr or b'')
        common.save(log.with_suffix(log.suffix + '.command.json'), record)
        raise
    record['finished_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    common.save(log.with_suffix(log.suffix + '.command.json'), record)
    return process

common.run = isolated_run
sys.argv[0] = str(OLD / 'scripts/preflight.py')
runpy.run_path(sys.argv[0], run_name='__main__')
