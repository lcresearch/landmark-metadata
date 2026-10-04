# Maintained observation readback

Use [verify_observations.py](verify_observations.py) for future readback of the
fresh reconstruction evidence. It derives from the
[original exported reader](../../sources/repro-audit-20261004/claims/verify_observations.py),
whose SHA-256 is
`21fe5355b655c8bd41c5721f07699c92cda5b9b3133522409df559b257602cd2`.
The original reader, export manifest, claim map and recorded 677-check result
remain unchanged as historical provenance. That check count predates these
repairs and does not establish that the old reader rejects incomplete evidence.

The old Hand reader could accept empty manifests without checking any execution.
The maintained reader requires original, container control, metadata exchange
and restoration exactly once in each primary/replay manifest before following
their artifact paths. Missing, duplicate, unexpected or malformed identities
record failed checks and make the aggregate command fail. The same completeness
rule covers all 20 Task variant/mode pairs, each Android execution's two named
inputs, and each experiment's four build variants. Complete manifests may be
reordered. Actual output/status/hash comparisons remain in place.

Recover the excluded `/workspace/repro-task`, `/workspace/repro-hand`,
`/workspace/repro-android` and `/workspace/repro-external` evidence first. From
the repository root, run:

```sh
python work/observation-review-20261004/verify_observations.py \
  --output-dir /workspace/new-observation-review
```

The command reads the original absolute evidence paths and writes a separate
`observation-readback.json`. Choose a new output directory outside sealed
evidence; existing reports are never overwritten. Exit 0 requires every check
to pass and Android records to be complete. Missing or unreadable prerequisite
files also cause a nonzero exit. This source checkout is not a complete evidence
deposit, and the command does not execute models.

Nine new synthetic regression tests exercise empty, missing, duplicate,
unexpected and malformed manifests, successful reordered records, retained
status/shape/byte checks, aggregate exit status and report preservation. All
29 repository tests pass, including the earlier verifier and source checker
regressions. The 354 imported files and five claim-export hashes verify unchanged.
These are verifier tests; no excluded raw model evidence was rerun during this
repair and no independent human verification is claimed.
