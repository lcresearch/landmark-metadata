import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform
import sys

root = Path(__file__).resolve().parent
packages = {}
for name in ['tflite-support', 'numpy', 'flatbuffers', 'protobuf']:
    try: packages[name] = importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError: packages[name] = 'NOT_INSTALLED'
site = Path(importlib.metadata.distribution('tflite-support').locate_file(''))
files = [site / 'tensorflow_lite_support/metadata/python/metadata.py',
         site / 'tensorflow_lite_support/python/task/vision/image_classifier.py',
         site / 'tensorflow_lite_support/python/task/vision/pybinds/_pywrap_image_classifier.so',
         site / 'tensorflow_lite_support/codegen/python/_pywrap_codegen.so']
records = []
for path in files:
    row = {'path': str(path), 'exists': path.is_file()}
    if path.is_file():
        data = path.read_bytes(); row.update(sha256=hashlib.sha256(data).hexdigest(), bytes=len(data))
        if path.suffix == '.py':
            target = root / 'sources' / ('installed-' + path.name)
            target.write_bytes(data); row['snapshot'] = str(target)
    records.append(row)
value = {'python_executable': sys.executable, 'python_version': sys.version,
         'platform': platform.platform(), 'packages': packages, 'files': records,
         'embedded_task_tflite_version': 'NOT_SEPARATELY_ESTABLISHED',
         'source_build_equivalence': 'NOT_ESTABLISHED'}
(root / 'versions.json').write_text(json.dumps(value, indent=2) + '\n')
print(json.dumps(value, indent=2))
