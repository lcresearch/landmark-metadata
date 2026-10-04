"""Fetch public official inputs and preserve response provenance, including failures."""
import datetime
import hashlib
import json
from pathlib import Path
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ITEMS = [
    ('artifacts/official-latest.task', 'https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task'),
    ('artifacts/official-v1.task', 'https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task'),
    ('sources/metadata_schema.fbs', 'https://raw.githubusercontent.com/tensorflow/tflite-support/v0.4.4/tensorflow_lite_support/metadata/metadata_schema.fbs'),
    ('sources/hand_landmarks_detector_graph.cc', 'https://raw.githubusercontent.com/google-ai-edge/mediapipe/v0.10.14/mediapipe/tasks/cc/vision/hand_landmarker/hand_landmarks_detector_graph.cc'),
    ('sources/hand_landmarker.html', 'https://developers.google.com/mediapipe/solutions/vision/hand_landmarker'),
    ('sources/hand-model-card.pdf', 'https://storage.googleapis.com/mediapipe-assets/Model%20Card%20Hand%20Tracking%20%28Lite_Full%29%20with%20Fairness%20Oct%202021.pdf'),
    ('sources/litert-metadata.html', 'https://developers.google.com/edge/litert/android/metadata/overview'),
]

def main():
    records = []
    for rel, url in ITEMS:
        record = {'path': rel, 'url': url, 'retrieved_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'hand-contract-reproduction/1.0'})
            with urllib.request.urlopen(req, timeout=50) as resp:
                data = resp.read()
                record.update(final_url=resp.url, headers=dict(resp.headers), status=resp.status)
            path = ROOT / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            record.update(sha256=hashlib.sha256(data).hexdigest(), bytes=len(data))
            print(rel, record['sha256'], len(data), flush=True)
            if path.suffix == '.task':
                with zipfile.ZipFile(path) as z:
                    data = z.read('hand_landmarks_detector.tflite')
                name = 'original.tflite' if 'latest' in rel else 'v1-component.tflite'
                (ROOT / 'artifacts' / name).write_bytes(data)
                record['component_sha256'] = hashlib.sha256(data).hexdigest()
                print(name, record['component_sha256'], flush=True)
        except Exception as exc:
            record['error'] = repr(exc)
            print(rel, record['error'], flush=True)
        records.append(record)
        (ROOT / 'results' / 'downloads.json').write_text(json.dumps(records, indent=2))

if __name__ == '__main__':
    main()
