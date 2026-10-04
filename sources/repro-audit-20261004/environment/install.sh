#!/usr/bin/env bash
set -euo pipefail
export UV_CACHE_DIR=/workspace/repro-control/uv-cache
export UV_PYTHON_INSTALL_DIR=/workspace/repro-control/python
export PYTHONDONTWRITEBYTECODE=1
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=1
export XDG_CACHE_HOME=/workspace/repro-control/runtime-cache
export MPLCONFIGDIR=/workspace/repro-control/runtime-cache/matplotlib
mkdir -p "$XDG_CACHE_HOME" "$MPLCONFIGDIR"
repo=/workspace/landmark-metadata
uv python install --no-bin 3.11.16
python_bin="$UV_PYTHON_INSTALL_DIR/cpython-3.11.16-linux-x86_64-gnu/bin/python3.11"
for environment in /workspace/hand-contract-repro /workspace/repro-hand; do
  test -f "$environment/requirements.lock"
  if [ ! -x "$environment/.venv/bin/python" ]; then
    uv venv --python "$python_bin" "$environment/.venv"
  fi
  uv pip install --python "$environment/.venv/bin/python" --no-deps -r "$environment/requirements.lock"
  uv pip check --python "$environment/.venv/bin/python"
  "$environment/.venv/bin/python" - "$environment/requirements.lock" <<'PY'
import importlib.metadata, pathlib, sys
if sys.version_info[:3] != (3, 11, 16):
    raise RuntimeError('Expected CPython 3.11.16')
rows = pathlib.Path(sys.argv[1]).read_text().splitlines()
for row in rows:
    if not row or row.startswith('#'):
        continue
    name, expected = row.split('==')
    actual = importlib.metadata.version(name)
    if actual != expected:
        raise RuntimeError(f'{name}: expected {expected}, observed {actual}')
print('PASS: exact Python and dependency versions:', len(rows))
PY
done
/workspace/hand-contract-repro/.venv/bin/python -c 'import numpy, tflite_runtime.interpreter, tflite_support; print("PASS: base imports")'
/workspace/repro-hand/.venv/bin/python -c 'import numpy, mediapipe; print("PASS: Hand Task imports")'
# The retained snapshot contains these verified archives. This is a dependency
# refresh/cache check, not a clean-machine model experiment or emulator boot.
python "$repo/sources/repro-audit-20261004/android/restore_prerequisites.py" \
  --root /workspace/repro-android --hand /workspace/hand-contract-repro --verify-cache
"/workspace/hand-contract-repro/toolchains/jdk-17.0.12+7/bin/java" -version
"/workspace/repro-android/sdk/platform-tools/adb" version
cd "$repo"
python scripts/check_source_tree.py
