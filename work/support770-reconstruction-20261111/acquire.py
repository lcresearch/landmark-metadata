"""Acquire a fixed public asset, retaining at most two transport attempts."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import time
import urllib.error
import urllib.request


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('url')
    parser.add_argument('output', type=Path)
    parser.add_argument('--max-bytes', type=int, required=True)
    args = parser.parse_args()
    if args.max_bytes <= 0:
        parser.error('--max-bytes must be positive')
    args.output.mkdir(parents=True, exist_ok=False)
    deadline = time.monotonic() + 600
    for attempt in range(1, 3):
        fatal = False
        record = {'url': args.url, 'attempt': attempt,
                  'started_utc': datetime.now(timezone.utc).isoformat()}
        partial = args.output / f'attempt-{attempt}.body'
        try:
            request = urllib.request.Request(args.url, headers={'User-Agent': 'landmark-research/1'})
            with urllib.request.urlopen(request, timeout=30) as response, partial.open('xb') as out:
                record.update(status=response.status, final_url=response.url,
                              headers=dict(response.headers))
                count = 0
                while True:
                    chunk = response.read(1 << 20)
                    if not chunk:
                        break
                    count += len(chunk)
                    out.write(chunk)
                    if count > args.max_bytes or time.monotonic() > deadline:
                        raise RuntimeError('Acquisition byte/time bound reached')
                length = response.headers.get('Content-Length')
                if length is not None and count != int(length):
                    raise RuntimeError('Incomplete Content-Length')
            record['complete'] = True
        except Exception as exc:
            fatal = isinstance(exc, RuntimeError)
            record['error'] = repr(exc)
            record['complete'] = False
            if isinstance(exc, urllib.error.HTTPError):
                record.update(status=exc.code, headers=dict(exc.headers))
                partial.write_bytes(exc.read(65536))
        if partial.exists():
            record.update(bytes=partial.stat().st_size,
                          sha256=hashlib.sha256(partial.read_bytes()).hexdigest())
        record['finished_utc'] = datetime.now(timezone.utc).isoformat()
        (args.output / f'attempt-{attempt}.json').write_text(json.dumps(record, indent=2) + '\n')
        print(json.dumps({k: record.get(k) for k in ('attempt','status','complete','bytes','sha256','error')}), flush=True)
        if record['complete']:
            shutil.copyfile(partial, args.output / 'complete.body')
            return
        if fatal or time.monotonic() > deadline:
            break
    raise SystemExit(1)


if __name__ == '__main__':
    main()
