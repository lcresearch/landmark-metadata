# E2 — fixed cyclic permutation of associated labels

The transformation is fixed before inspecting E1 Android predictions. Execution is gated on a reproducible working original E1 interface. Experimental unit: the same component × variant × consumer configuration; inputs are repeated observations.

Use the E1 original and description control. For permutation, transform the original label lines `[L0, L1, ..., L999]` to `[L1, ..., L999, L0]` with the same filename and fixed deterministic ZIP writer. Preserve label count and multiset; duplicate strings, if present, are retained with multiplicity. For restoration, rotate the resulting lines right by one; require equality of associated payloads to original. Do not select a permutation based on predictions.

Run original, description_control, label_permutation, permutation_restoration through the exact unchanged generated public API and E1 pinned Android consumer. Use the two inputs already fixed in E1. Make separate primary and same-environment replay records. Record every stage and exact failures if any; a successful decoding outcome is not assumed.

Require canonical graph, every non-metadata buffer, embedded metadata, pre-ZIP TFLite prefix, tensor shapes, generated Java and generated classes to remain equal. Check source/classes/DEX as in E1. Compare raw output bytes, argmax, top-five index sequence (stable lowest-index tie break), scores and score bits, and returned category labels at corresponding list positions. Category.getIndex may be unset by this TensorLabel API; preserve it but do not confuse it with tensor position. List-order correspondence is to be checked against the actual library implementation and raw values.

Expected association mapping, to be tested: permutation label at position i equals original label at position `(i+1) mod 1000`; every score remains unchanged. Restoration should restore original associations. Describe changed associations relative to original only. No independently tied class-order reference currently exists; semantic truth must be ABSTAIN. Decoder D is expected to pass a count-preserving order mutation; this is an intentional scope boundary, not a false negative.

Commands, from the project root:

```bash
PYTHONDONTWRITEBYTECODE=1 /workspace/hand-contract-repro/.venv/bin/python scripts/prepare_e2.py
python scripts/build_android.py --experiment E2
python scripts/run_android.py --experiment E2 --run primary
python scripts/run_android.py --experiment E2 --run replay
```

No whole-manuscript rewrite is planned. Report whether the actual generated interface exposes different labels for the same output scores, and keep reference-backed semantic correctness separate.
