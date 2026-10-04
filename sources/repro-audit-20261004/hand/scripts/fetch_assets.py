"""Recover exact official E7 assets without accepting a digest mismatch."""
import datetime
import hashlib
import json
from pathlib import Path
import re
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
FOCAL = '6acda74af3fbf40e68265c20c7394b2bad81a16a481dcd79ad7a081887c3d6b9'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def pinned_asset(name):
    source = (ROOT / 'sources/external_files.bzl').read_text()
    pattern = rf'name = "{name}",\s*sha256 = "([a-f0-9]{{64}})",\s*urls = \["([^"]+)"\]'
    match = re.search(pattern, source)
    if not match:
        raise ValueError(f'Pin missing from recovered immutable source: {name}')
    return match.group(2), match.group(1)


def main():
    (ROOT / 'assets').mkdir(parents=True, exist_ok=True)
    (ROOT / 'results').mkdir(parents=True, exist_ok=True)
    entries = [
        ('official-v1.task', 'https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task', None),
        ('source-pinned.task', *pinned_asset('com_google_mediapipe_hand_landmarker_task')),
        ('thumb_up.jpg', *pinned_asset('com_google_mediapipe_thumb_up_jpg')),
    ]
    records = []
    failed = False
    for name, url, expected in entries:
        record = {'file': name, 'url': url, 'expected_sha256': expected, 'retrieved_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
        path = ROOT / 'assets' / name
        try:
            if path.exists():
                data = path.read_bytes()
                record['source'] = 'retained_file'
            else:
                with urllib.request.urlopen(url, timeout=60) as response:
                    data = response.read()
                    record.update(http_status=response.status, final_url=response.url)
            actual = digest(data)
            record.update(sha256=actual, size=len(data))
            if expected is not None and expected != actual:
                raise ValueError(f'{name} SHA256 mismatch: expected {expected}, got {actual}')
            if name == 'official-v1.task':
                import io
                with zipfile.ZipFile(io.BytesIO(data)) as bundle:
                    component = bundle.read('hand_landmarks_detector.tflite')
                record['landmark_component_sha256'] = digest(component)
                if digest(component) != FOCAL:
                    raise ValueError('Version-1 bundle does not contain the exact focal component')
            if not path.exists():
                path.write_bytes(data)
            record['status'] = 'PASS'
        except Exception as exc:
            failed = True
            record.update(status='FAIL', exception_type=type(exc).__name__, error=str(exc))
        records.append(record)
        print(json.dumps(record), flush=True)
        (ROOT / 'results/assets.json').write_text(json.dumps(records, indent=2))
    return int(failed)


if __name__ == '__main__':
    raise SystemExit(main())
