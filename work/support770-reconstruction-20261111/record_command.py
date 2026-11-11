"""Run one bounded command into a fresh stage; never overwrite a prior failure."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--cwd', type=Path, required=True)
    parser.add_argument('--timeout', type=int, required=True)
    parser.add_argument('command', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ['--'] else args.command
    if not command or args.timeout <= 0:
        parser.error('command and positive timeout required')
    args.output.mkdir(parents=True, exist_ok=False)
    record = {'command': command, 'cwd': str(args.cwd.resolve()),
              'timeout_seconds': args.timeout,
              'started_utc': datetime.now(timezone.utc).isoformat(),
              'runner_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'environment': {k: os.environ.get(k) for k in (
                  'JAVA_HOME', 'GRADLE_USER_HOME', 'ANDROID_SDK_ROOT',
                  'ANDROID_USER_HOME', 'ANDROID_AVD_HOME', 'PYTHONDONTWRITEBYTECODE')}}
    destination = args.output / 'command.json'
    destination.write_text(json.dumps(record, indent=2) + '\n')
    start = time.monotonic()
    with (args.output / 'stdout').open('wb') as out, (args.output / 'stderr').open('wb') as err:
        try:
            process = subprocess.Popen(command, cwd=args.cwd, stdout=out, stderr=err,
                                       start_new_session=True)
            try:
                record['exit_code'] = process.wait(timeout=args.timeout)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                record['exit_code'] = process.wait()
                record['timeout'] = True
        except OSError as exc:
            record['launch_error'] = repr(exc)
            record['exit_code'] = 127
    record['elapsed_seconds'] = time.monotonic() - start
    record['finished_utc'] = datetime.now(timezone.utc).isoformat()
    record['status'] = 'PASS' if record['exit_code'] == 0 else 'FAIL'
    destination.write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps(record), flush=True)
    raise SystemExit(0 if record['status'] == 'PASS' else 1)


if __name__ == '__main__':
    main()
