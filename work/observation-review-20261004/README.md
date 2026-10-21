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

Each Hand record must also have the controller's `completed: true`, a zero
exit status and successful initialization, input preparation and detection in
the worker result. A failed or missing status cannot be rescued by stale decoded
files. Only records passing both completion and output checks enter the reported
record count; fewer than eight validated records makes Hand incomplete.

Successful Linux Task executions also require exactly the two named input
records. Each must report successful input preparation and classification and
1,000 returned categories. The reader checks the prescribed RGB bytes in
`/workspace/repro-task/inputs/` against each recorded input digest before reading
its decoded categories. Empty, duplicate or contradictory records cannot be
counted as successful observations merely because decoded files remain. Task's
`classify` call combines inference and decoding; the per-input records do not
claim separate observations of those internal stages.

E5 requires the frozen original catalog's 65 artifact identities before reading
model payloads or checking aggregate result counts. The default manifest is
`/workspace/repro-external/E5/results.json`, pinned to SHA-256
`bf49a475696eec4b38fb17587f6541a8393da14297e5dca1d433a051ba166e79`
recorded by claim C32 in the preserved claim map. Local file/report agreement
alone cannot establish that a later catalog contains the original fixtures.

Every baseline record is bound to its named core Android model's actual digest,
for all five variants and all four modes. The permutation condition uses E2;
the other four use E1. Both the Task baseline and E5 readers check this binding
independently, so a different E5 fixture with the same acceptance status cannot
stand in for the named model. The E5 zero-extra-rejections conclusion is emitted
only when all of that section's checks pass; a failed section reports `null`
and `complete: false` instead of a numerical conclusion.

Recover the excluded `/workspace/repro-task`, `/workspace/repro-hand`,
`/workspace/repro-android` and `/workspace/repro-external` evidence first. From
the repository root, run:

```sh
python work/observation-review-20261004/verify_observations.py \
  --output-dir /workspace/new-observation-review
```

If the current catalog is a later run, locate the frozen original with
`--required-manifest /path/to/frozen-original-catalog.json`. An explicitly
reviewed alternative manifest may contain an `artifact_sha256s` array of the 65
original digests; also pass its previously recorded digest using
`--required-manifest-sha256`. Never calculate the required digest from the run
being examined. Missing, malformed or mismatched manifests and substituted
fixture identities produce failed checks and a nonzero aggregate exit.

The command reads the original absolute evidence paths and writes a separate
`observation-readback.json`. Choose a new output directory outside sealed
evidence; existing reports are never overwritten. Exit 0 requires every check
to pass and Android records to be complete. Missing or unreadable prerequisite
files also cause a nonzero exit. This source checkout is not a complete evidence
deposit, and the command does not execute models.

The synthetic regression tests exercise empty, missing, duplicate, unexpected
and malformed manifests, successful reordered records, retained status/shape/
byte checks, aggregate exit status and report preservation. They cover Task
input records and bytes, frozen E5 identities, same-status substitutions for
each baseline mode, missing core digests/files, failed Hand input preparation
and controller completion, and explicit manifest overrides. Run them without
model dependencies:

```sh
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -p test_observation_readback.py -v
```

These are verifier tests; no excluded raw model evidence was rerun during this
repair and no independent human verification is claimed.
