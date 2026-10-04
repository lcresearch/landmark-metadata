# E5 — scoped pre-flight command and evaluation

E1–E4 are complete. Implement a command for the exact Support 0.4.4 default generated Java consumer. Keep STRUCTURAL, REFERENCE_BACKED_SEMANTIC, DECODER_COMPATIBILITY, PRESERVATION and UNKNOWN/ABSTAIN separate. No overall “model invalid” judgment.

Use actual generated source to identify each category getter, the tensor output it uses, the metadata/associated-file index actually loaded, and the default postprocessor. Apply the understood TensorLabel(List, TensorBuffer).getCategoryList preconditions only if these bindings are unambiguous and the default processor preserves shape. Dynamic shapes/signatures and unmodeled processors abstain. Do not assume every model output uses this decoder. Passing D does not certify source compilation, other consumers or semantics.

Reference comparison is optional and must carry an externally supplied contract, exact source bytes/hash and exact artifact binding. With no such independently supplied reference, abstain. The command can verify provided evidence bytes and perform the stated comparison, but cannot independently certify the source interpretation; make that qualification visible. In this evaluation, do not create an “independent” reference by exporting original labels. No supplied reference will be used for the model-semantics evaluation.

Optional --baseline performs the established graph/non-metadata-buffer preservation comparison. Preserve exact generated sources, diagnostics and per-model JSON. Run each distinct artifact once; retain aliases to original experiment/variant names. Evaluate all preserved 46 old variants, the two no-metadata originals, E1/E2 artifacts, and the 15 new E4 canonical representatives. Deduplicate byte-identical fixtures rather than inflating counts with original/replay aliases.

Report S rejections, D findings, inapplicability and abstention by mutation class; check that known successfully executed E1/E2 conditions are not rejected. Compare with actual observed E1 getter failures and E3 initialization rejection. Label permutations should pass D while semantics abstain; this is intentional scope. For Hand and other uncompilable sources, a D finding must not be described as preventing the first observed failure: raw javac already rejects those sources.

No precision/recall or general accuracy estimate. This is development/control evaluation plus agreement with previously frozen external observations, not a new independently labeled detector benchmark. A mismatch between the new parser and frozen results must be retained and investigated with a new version, not silently changed in E4.

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 /workspace/hand-contract-repro/.venv/bin/python scripts/preflight.py E1/variants/label_deletion/model.tflite --evidence-dir E5/demo-deletion
PYTHONDONTWRITEBYTECODE=1 /workspace/hand-contract-repro/.venv/bin/python scripts/evaluate_preflight.py
```
