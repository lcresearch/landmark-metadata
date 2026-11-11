"""Bounded public-link availability check; never execute or fully fetch model assets.

Observed issue/document URLs only. Retain response prefixes outside Git; a 200 or
redirect is not proof of original artifact identity or successful reproduction.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, build_opener, HTTPRedirectHandler

REPO = Path(__file__).resolve().parents[2]
URLS = [
    ('770-overview', 'https://www.tensorflow.org/lite/examples/segmentation/overview'),
    ('770-task-guide', 'https://www.tensorflow.org/lite/inference_with_metadata/task_library/image_segmenter'),
    ('319-default', 'https://tfhub.dev/tensorflow/lite-model/mobilebert/1/default/1?lite-format=tflite'),
    ('319-metadata', 'https://tfhub.dev/tensorflow/lite-model/mobilebert/1/metadata/1?lite-format=tflite'),
    ('870-drive', 'https://drive.google.com/file/d/1Ke46il3g3xi70RPNa8KKUWhGfJj81ORX/view?usp=sharing'),
]
LIMIT = 1024 * 1024


def inspect(item, output):
    key, url = item
    row = {'id': key, 'url': url, 'started_utc': datetime.now(timezone.utc).isoformat(),
           'redirects': [], 'scope': 'Availability only; no original model hash or execution'}

    class Redirects(HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            row['redirects'].append({'status': code, 'from': req.full_url, 'to': newurl})
            return super().redirect_request(req, fp, code, msg, headers, newurl)

    try:
        opener = build_opener(Redirects())
        request = Request(url, headers={'User-Agent': 'landmark-research-availability/1.0'})
        try:
            response = opener.open(request, timeout=20)
        except HTTPError as exc:
            response = exc
        with response:
            content_type = response.headers.get('Content-Type', '')
            # Read enough to distinguish an HTML/login/challenge page from a
            # binary response. Never acquire the complete binary as a side effect.
            cap = LIMIT if 'text/' in content_type or 'json' in content_type else 4096
            data = response.read(cap + 1)
            truncated = len(data) > cap
            data = data[:cap]
            path = output / (key + '.response-prefix')
            path.write_bytes(data)
            row.update(status=response.status, final_url=response.geturl(),
                       content_type=content_type, content_length=response.headers.get('Content-Length'),
                       retained_bytes=len(data), truncated=truncated,
                       sha256=hashlib.sha256(data).hexdigest(), local_file=str(path))
    except Exception as exc:
        row.update(error_type=type(exc).__name__, error=str(exc))
    row['completed_utc'] = datetime.now(timezone.utc).isoformat()
    (output / (key + '.json')).write_text(json.dumps(row, indent=2) + '\n')
    return row


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if output.is_relative_to(REPO) or output.exists():
        raise ValueError('Use a fresh directory outside the source repository')
    output.mkdir(parents=True, exist_ok=False)
    with ThreadPoolExecutor(max_workers=3) as executor:
        rows = list(executor.map(lambda item: inspect(item, output), URLS))
    (output / 'availability.json').write_text(json.dumps(rows, indent=2) + '\n')
    print(json.dumps(rows, indent=2))


if __name__ == '__main__':
    main()
