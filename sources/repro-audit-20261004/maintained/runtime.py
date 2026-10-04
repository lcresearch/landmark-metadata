"""Run the retained generator with the active interpreter and external evidence."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys

PYTHON = Path(sys.executable)
SOURCE_SCRIPTS = Path(__file__).resolve().parents[2] / 'metadata-contract-paper/scripts'
REPOSITORY = Path(__file__).resolve().parents[3]

def require_external(path):
    path = Path(path).resolve()
    if path.is_relative_to(REPOSITORY):
        raise ValueError('Generated evidence must stay outside the source-only repository')
    return path

def sha(data):
    return hashlib.sha256(data).hexdigest()

def save(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')

def run(command, log, timeout=120):
    log = Path(log)
    log.parent.mkdir(parents=True, exist_ok=True)
    command = list(map(str, command))
    record = {'command': command, 'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        result = subprocess.run(command, capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        log.with_suffix(log.suffix + '.stdout').write_bytes(exc.stdout or b'')
        log.with_suffix(log.suffix + '.stderr').write_bytes(exc.stderr or b'')
        save(log.with_suffix(log.suffix + '.command.json'), dict(record, timeout_seconds=timeout))
        raise
    log.with_suffix(log.suffix + '.stdout').write_bytes(result.stdout)
    log.with_suffix(log.suffix + '.stderr').write_bytes(result.stderr)
    save(log.with_suffix(log.suffix + '.command.json'), dict(record, exit_code=result.returncode))
    return result
