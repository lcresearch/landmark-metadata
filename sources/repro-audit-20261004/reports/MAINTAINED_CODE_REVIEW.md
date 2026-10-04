# Independent agent review of the maintained reproduction patch

Review date: 2026-10-04 UTC. Scope: `sources/repro-audit-20261004/maintained/{java_labels,preflight,baseline,runtime}.py`, related regression entry points, and `reproduction/run_task.py`. This was a second-agent code review, not independent human verification. No historical source snapshot was changed by this review. Diagnostic models, generated Java, bytecode and results stayed outside the source-only repository.

## Conclusion

The label-parser maintenance fix is correct for its declared valid-UTF-8 domain. Malformed UTF-8 explicitly abstains in the simple baseline, decoder check and supplied-reference class-order comparison. The selected interpreter, preserved virtualenv path and retained generator-source path resolve correctly. The Task reproduction runner checks its results and returns failure when required checks fail; its historical baseline intentionally reproduces the original study, while maintained-baseline regression is separate.

Two output-hygiene problems found in the initial patch were corrected by the root agent before review completion:

1. `baseline.py` and `preflight.py` originally set `sys.dont_write_bytecode` after importing local modules. Running a byte-identical external copy of the initial baseline produced `maintained-copy/__pycache__/java_labels.cpython-311.pyc`. The updated entry points set the flag before those imports.
2. The initial maintained baseline, preflight and Java-parser test accepted repository-internal output directories. The root added `require_external`, resolving the destination and rejecting repository descendants. The updated baseline API and CLI, preflight API, and test entry point use this guard. Direct guard checks rejected both an internal path and an internal path expressed with `../`, while permitting an external path.

No additional substantial defect was found in the reviewed maintenance change after those fixes. Existing E5 limitations for unknown getter/processor forms remain explicitly scoped historical limitations; this review did not broaden the checker.

## Actual diagnostic checks

The diagnostic model `/workspace/repro-review/malformed.tflite` was created outside the repository from the exact EfficientNet original at `/workspace/metadata-contract-paper/runs/6c7ab0a6e5dc/original/model.tflite`. The original TFLite prefix was preserved and a UTF-8 surrogate encoding (`ED A0 80`) was inserted into its associated label text before the first LF. This is a synthetic parser diagnostic, not an additional model or study condition.

The initial bytecode and malformed-baseline check used a byte-identical external copy of the initial maintained files:

```sh
/workspace/hand-contract-repro/.venv/bin/python \
  /workspace/repro-review/maintained-copy/baseline.py \
  simple_baseline /workspace/repro-review/malformed.tflite \
  /workspace/repro-review/baseline-malformed
```

Observed: exit 0 with explicit `status: ABSTAIN` and the unsupported-malformed-decoding diagnostic. The exit status does not mean compatible; the result status preserves abstention. Evidence: `/workspace/repro-review/baseline-malformed/result.json` and `baseline-malformed.stdout`. The external copied source plus its `__pycache__` preserve the original import-order problem; no cache was deliberately generated inside the repository.

The decoder path was exercised using the maintained preflight and real native generator:

```sh
PYTHONDONTWRITEBYTECODE=1 /workspace/hand-contract-repro/.venv/bin/python \
  /workspace/landmark-metadata/sources/repro-audit-20261004/maintained/preflight.py \
  /workspace/repro-review/malformed.tflite \
  --evidence-dir /workspace/repro-review/preflight-malformed
```

Observed: official structural population accepted, decoder status `ABSTAIN`, and one getter finding explicitly diagnosing malformed UTF-8. Evidence: `/workspace/repro-review/preflight-malformed/result.json`, its generated source and codegen logs, and `/workspace/repro-review/preflight-malformed.stdout`.

For the I/class-order branch, an explicitly synthetic supplied-reference fixture was written to `/workspace/repro-review/malformed-reference.json`, bound by digest to the malformed diagnostic model and to `/workspace/repro-review/semantic-contract.txt`. In the shared virtualenv with `PYTHONDONTWRITEBYTECODE=1`, the check directly invoked:

```python
result = reference_check(model.read_bytes(), inspect(model.read_bytes()), reference_path)
```

Observed: `status: ABSTAIN` with the same malformed-UTF-8 diagnostic. Evidence: `/workspace/repro-review/malformed-reference-result.json`. This fixture tests control flow and makes no semantic correctness claim.

After the root's output-guard fix, direct calls to `runtime.require_external` used these three inputs:

- `/workspace/landmark-metadata/review-must-reject`: rejected.
- `/workspace/landmark-metadata/sources/../review-must-reject`: rejected after resolution.
- `/workspace/repro-review/review-may-pass`: permitted.

Evidence: `/workspace/repro-review/output-guard-results.json`. These calls did not create those destinations.

These output paths are retained evidence. A replay must use fresh output directories because the entry points refuse to overwrite them.

## Remaining scope and failure behavior

`reproduction/run_task.py` deliberately invokes the historical baseline for original-study reproduction; `maintained/verify_fixture_regression.py` separately validates the repaired baseline. This separation was confirmed with the root agent. The reproduction runner gates its recorded checks, so worker exceptions do not become an overall success. An unexpected missing decoded file or missing category index can currently abort comparison before writing `checks.json` or running later independent baseline checks. That is a diagnostic-completeness limitation, not a false-PASS defect, and was not expanded into an unrelated robustness change here.

The root separately strengthened `hand/scripts/run_tasks.py` to require four conditions, successful stages, one hand with 21+21 landmarks, artifact/output digest checks, equality and replay agreement. Its additional regression evidence is at `/workspace/repro-hand-runner-regression/executions/{primary,replay}/results.json`. Readback confirmed four completed conditions in each phase and all four replay observations equal to primary. Those eight regression calls are separate from the main E7 reproduction's eight calls and are not counted as new study evidence or independent models.

## Documentation count correction

The fresh Hand report's package count was initially written as 26. Direct `wc -l` and parsed-line counts on `/workspace/repro-hand/requirements.lock` and its new source-area copy both showed exactly 25 package lines, zero blank lines and zero comments. The two fresh report copies were corrected to 25 exactly pinned packages. The dependency declarations and historical snapshots were not changed.
