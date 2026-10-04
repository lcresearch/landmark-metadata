#!/usr/bin/env python3
"""Recover bounded background sources outside Git; no model/tool experiments."""
import argparse
import concurrent.futures
import datetime
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import urllib.error
import urllib.request


def sha(data):
    return hashlib.sha256(data).hexdigest()


def fetch(job, root):
    name, url = job
    row = {'id': name, 'url': url,
           'retrieved_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'BoundedContributionReview/1.0'})
        with urllib.request.urlopen(req, timeout=30) as response:
            data = response.read()
            row.update(http_status=response.status, final_url=response.geturl())
        target = root / name
        target.write_bytes(data)
        row.update(status='DOWNLOADED', path=str(target), sha256=sha(data), bytes=len(data))
        if name.endswith('.pdf'):
            row['status'] = 'PDF_RETRIEVED' if data.startswith(b'%PDF') else 'NOT_A_PDF'
    except (urllib.error.URLError, OSError, TimeoutError) as exc:
        row.update(status='UNAVAILABLE', error=str(exc), error_type=type(exc).__name__)
        if isinstance(exc, urllib.error.HTTPError):
            row['http_status'] = exc.code
    return row


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', required=True, type=Path)
    parser.add_argument('--historical-root', type=Path,
                        default=Path('/workspace/metadata-contract-paper'))
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=False)
    rows = []
    inputs = [
        ('aibom.pdf', args.historical_root / 'sources/aibom-paper.pdf',
         '674ee9127a82f3b5541f1685defbc216f0b38e727e550d226edb2c8432c55035'),
        ('historical-literature-downloads.json', args.historical_root / 'results/literature-downloads.json', None),
        ('stalnaker-historical-crossref.json', args.historical_root / 'hand-evidence/sources/stalnaker-reference.txt', None),
        ('aibom-historical-atom.xml', args.historical_root / 'hand-evidence/sources/aibom-reference.txt', None),
    ]
    for name, source, expected in inputs:
        try:
            data = source.read_bytes()
        except OSError as exc:
            rows.append({'id': name, 'status': 'UNAVAILABLE', 'source': str(source), 'error': str(exc)})
            continue
        digest = sha(data)
        row = {'id': name, 'source': str(source), 'sha256': digest, 'bytes': len(data)}
        if expected is not None and digest != expected:
            row['status'] = 'DIGEST_MISMATCH'
            rows.append(row)
            continue
        target = args.output_dir / name
        shutil.copyfile(source, target)
        row.update(status='RECOVERED', path=str(target), expected_sha256=expected)
        if name.endswith('.pdf'):
            command = ['pdftotext', '-layout', str(target), str(target.with_suffix('.txt'))]
            try:
                result = subprocess.run(command, capture_output=True, text=True, timeout=30)
                row.update(text_command=command, text_exit=result.returncode, text_stderr=result.stderr)
            except (OSError, subprocess.TimeoutExpired) as exc:
                row['text_error'] = str(exc)
        rows.append(row)
    jobs = [('stalnaker-crossref.json', 'https://api.crossref.org/works/10.1145/3776739'),
            ('stalnaker.pdf', 'https://dl.acm.org/doi/pdf/10.1145/3776739')]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        rows.extend(pool.map(lambda job: fetch(job, args.output_dir), jobs))
    (args.output_dir / 'retrieval.json').write_text(json.dumps(rows, indent=2) + '\n')
    print(json.dumps([{'id': row['id'], 'status': row['status'], 'sha256': row.get('sha256'),
                       'error': row.get('error')} for row in rows], indent=2))


if __name__ == '__main__':
    main()
