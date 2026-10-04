"""Seal the delivery root once; installed environments are outside archive scope."""
import datetime
import hashlib
import json
import os
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
target = ROOT / 'SHA256SUMS'
if target.exists():
    raise SystemExit('Already sealed; create a new delivery directory instead.')
paths = []
for parent, dirs, names in os.walk(ROOT):
    # sdk is only excluded at the delivery root; other exclusions are cache/env names.
    dirs[:] = [d for d in dirs if d not in ['venv', '.venv', '__pycache__']
               and not (pathlib.Path(parent) == ROOT and d == 'sdk')]
    for name in names:
        path = pathlib.Path(parent) / name
        if path.is_file() and path != target:
            paths.append(path)
scope = ROOT / 'MANIFEST_SCOPE.json'
record = {'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'scope': 'Local evidence, reports, scripts, models, saved outputs, archived SDK downloads and wheels. This is not a standalone offline or public distribution.',
          'excluded': ['installed root sdk/ including AVD state', 'venv/', '.venv/', '__pycache__/', 'root SHA256SUMS itself'],
          'historical_roots': 'Audited separately through phase0/inventory.json and verification/final-integrity.json; not duplicated by this manifest.',
          'sealed_phase_manifests': ['E1/SHA256SUMS','E2/SHA256SUMS','E3/SHA256SUMS','E4/SHA256SUMS','E5/SHA256SUMS','E7/SHA256SUMS'],
          'entry_count_including_this_scope_file': len(paths) + (0 if scope in paths else 1)}
with scope.open('x') as handle:
    json.dump(record, handle, indent=2)
paths.append(scope)
lines = []
total = 0
for path in sorted(set(paths)):
    with path.open('rb') as handle:
        digest = hashlib.file_digest(handle, 'sha256').hexdigest()
    lines.append(f'{digest}  {path.relative_to(ROOT)}')
    total += path.stat().st_size
with target.open('x') as handle:
    handle.write('\n'.join(lines) + '\n')
print(json.dumps({'entries': len(lines), 'bytes': total,
                  'manifest_sha256': hashlib.sha256(target.read_bytes()).hexdigest()}, indent=2))
