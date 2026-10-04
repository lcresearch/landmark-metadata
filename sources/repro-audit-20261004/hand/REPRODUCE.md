# New Hand/E7 reconstruction scripts

Use the existing isolated checkout; no Git worktree is needed. Keep all dependencies, models, generated code, outputs and logs outside the source-only repository. Copy this source folder to a new workspace directory before a new run; scripts refuse to overwrite existing variant or execution directories.

Prerequisites used here:

- Shared `/workspace/hand-contract-repro/.venv` with its exact historical lock, JDK and Java dependencies restored by the main reproduction setup.
- A separate Python 3.11 environment under this folder's `.venv`, installed from `requirements.lock`.
- Verified official MediaPipe commit sources saved as `sources/external_files.bzl`, `sources/hand_landmarks_detector_graph.cc`, and `sources/hand_landmarker_test.py`; immutable base URL `https://raw.githubusercontent.com/google-ai-edge/mediapipe/4cf89a70942ca3252e46ace7e4552f53be9bef2e/`.
- HTTPS access to `storage.googleapis.com`, `raw.githubusercontent.com`, `github.com`, `pypi.org`, `files.pythonhosted.org` through the configured proxy with TLS verification enabled.

Actual Task reproduction commands executed in this run:

```sh
python /workspace/repro-hand/scripts/fetch_assets.py
/workspace/hand-contract-repro/.venv/bin/python /workspace/repro-hand/scripts/prepare_variants.py
python /workspace/repro-hand/scripts/run_tasks.py primary
python /workspace/repro-hand/scripts/run_tasks.py replay
```

`fetch_assets.py` reads task/image digest pins from immutable upstream source and validates the focal component hash. `prepare_variants.py` checks the graph/weight bridge and exact historical mutation before saving any variants. `run_tasks.py` invokes the unchanged historical `hand_task_one.py`, checks process completion plus report stage fields, saves complete outputs, and compares decoded hashes and replay records. It does not use the historical unconditional Markdown summarizer.

Fresh generic Hand compilation/CPU/decoder reproduction used byte-identical historical scripts copied outside the repository, with the recovered focal component at `/workspace/hand-contract-repro/artifacts/original.tflite`:

```sh
PYTHONDONTWRITEBYTECODE=1 /workspace/hand-contract-repro/.venv/bin/python /workspace/hand-contract-repro/scripts/run_all.py
```

The generic scripts intentionally record failed raw Java compilation, followed by the disclosed separator repair; this does not execute an unmodified Hand wrapper on Android. Their output directories must be new. Do not rerun historical `build_report.py`, sealing or import scripts against preserved evidence.

Read `REPORT.md` for observed outcomes and current limits. Existing evidence files are retained for review; their presence alone is not a claim that a new run occurred.
