"""Run one authorized stage with exclusive external logs and explicit exit status."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import subprocess
import time

REPO = Path(__file__).resolve().parents[2]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', required=True, type=Path)
    ap.add_argument('--label', required=True)
    ap.add_argument('--cwd', type=Path)
    ap.add_argument('--timeout', type=int, default=3600)
    ap.add_argument('command', nargs=argparse.REMAINDER)
    args = ap.parse_args()
    root = args.root.resolve()
    if root.is_relative_to(REPO) or not (root / 'PROTOCOL.md').is_file():
        raise ValueError('Expected an initialized external run')
    if not re.fullmatch(r'[a-zA-Z0-9_-]+', args.label):
        raise ValueError('Invalid stage name')
    command = args.command[1:] if args.command[:1] == ['--'] else args.command
    if not command:
        raise ValueError('Missing command')
    logs = root / 'stages' / args.label
    logs.mkdir(parents=True, exist_ok=False)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONOPTIMIZE='0',
               OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
    record = {'command': command, 'cwd': str((args.cwd or root).resolve()),
              'started_utc': datetime.now(timezone.utc).isoformat(), 'timeout': args.timeout,
              'status': 'RUNNING'}
    path = logs / 'command.json'
    path.write_text(json.dumps(record, indent=2) + '\n')
    started = time.monotonic()
    try:
        with (logs / 'stdout').open('xb') as out, (logs / 'stderr').open('xb') as err:
            result = subprocess.run(command, cwd=record['cwd'], env=env, stdin=subprocess.DEVNULL,
                                    stdout=out, stderr=err, timeout=args.timeout)
        record.update(status='COMPLETED', exit_code=result.returncode)
    except (OSError, subprocess.TimeoutExpired) as error:
        record.update(status='EXECUTION_ERROR', exit_code=None, error=str(error))
    record.update(completed_utc=datetime.now(timezone.utc).isoformat(),
                  elapsed_seconds=round(time.monotonic() - started, 3))
    path.write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps(record, indent=2))
    return 0 if record.get('exit_code') == 0 else 1


if __name__ == '__main__':
    raise SystemExit(main())
