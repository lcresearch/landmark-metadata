# Commands and verification scope

Commands below were run from `/workspace/landmark-evidence-recovery` unless
stated otherwise. Python 3 commands read saved bytes, copy selected files or
check source; they do not execute a model. External logs and report identities
are listed in `delivery-record.json`. Reusing an existing output is refused by
the maintained staging and coverage tools.

## Historical discovery

The two scripts under `discovery/` were run from the new external `search/` and
`scope/` directories. They are fixed-path command snapshots, not safe rerun
entry points. Exact `rg` arguments, candidate bounds and archive operations are
recorded in `search/search-results.json`; the follow-up text search is recorded
in `search/content-reference-search.json`.

## Staging

An initial call used `--output .../package`. Independent scope comparison then
identified 29 omitted text dependency records. The plan added explicit exceptions
and this second call produced the delivery target:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 work/evidence-recovery-20261005/stage_evidence.py stage \
  --plan work/evidence-recovery-20261005/package-plan.json \
  --output /workspace/evidence-recovery-20261005T170453Z/package-v2
PYTHONDONTWRITEBYTECODE=1 python3 work/evidence-recovery-20261005/stage_evidence.py verify \
  --package /workspace/evidence-recovery-20261005T170453Z/package-v2 \
  --checksums-sha256 a689674abb65452d8eb02a17d6af3f097884bd8c2ad4cb4a8353e33914197a3c
```

The stage returns nonzero and records issues for missing, changed or unlisted
selected historical files. `verify` checks the package against its trusted
checksum identity and separately reports historical identity status; package
integrity alone is not experimental truth or historical completeness.

## Saved-record checks

```bash
PYTHONDONTWRITEBYTECODE=1 python3 work/evidence-recovery-20261005/check_focal_coverage.py \
  --package /workspace/evidence-recovery-20261005T170453Z/package-v2 \
  --output /workspace/evidence-recovery-20261005T170453Z/coverage/coverage-v1.json
PYTHONDONTWRITEBYTECODE=1 python3 research/20261004-significance-review/scripts/read_existing_outcomes.py \
  --e2e-root /workspace/evidence-recovery-20261005T170453Z/package-v2/payload/metadata-contract-e2e-20261004T030536Z \
  --p2p3-root /workspace/evidence-recovery-20261005T170453Z/package-v2/payload/metadata-contract-p2p3-20261004T073824Z \
  --output-dir /workspace/evidence-recovery-20261005T170453Z/readback-v2
```

The first command reads all 34 complete saved records and package identities in
its stated scope. It does not rederive preservation or reference semantics.
The second reads only 59 selected files; its comparison booleans were inspected
and none was false. Exit zero alone was not used as the conclusion.

## Archive creation and verification

The archive was created with an exclusive output handle:

```python
from pathlib import Path
import tarfile
root = Path('/workspace/evidence-recovery-20261005T170453Z')
with (root/'delivery/focal-saved-evidence.tar.gz').open('xb') as output:
    with tarfile.open(fileobj=output, mode='w:gz', compresslevel=3) as archive:
        archive.add(root/'package-v2', arcname='focal-saved-evidence', recursive=True)
```

```bash
PYTHONDONTWRITEBYTECODE=1 python3 work/evidence-recovery-20261005/verify_archive.py \
  --archive /workspace/evidence-recovery-20261005T170453Z/delivery/focal-saved-evidence.tar.gz \
  --checksums-sha256 a689674abb65452d8eb02a17d6af3f097884bd8c2ad4cb4a8353e33914197a3c
```

This streamed every regular member, rejected links/special objects and checked
the exact file inventory and digest of every file without extracting anything.
The resulting archive digest identifies this copy; future tar/gzip timestamps
can change container bytes, so a new archive needs its own digest while preserving
the payload checks. No APK equality or new execution follows from archive equality.

## Source/tool validation

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_stage_evidence.py -v
PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_source_tree.py
git diff --check
```

There are 43 synthetic staging/archive regressions. Separate coverage probes
show that a missing APK fails under ordinary Python and `-O`, and an existing
report path is not overwritten. These probes are tiny constructed test fixtures,
not model experiments or new natural defects. Original manuscript, input
inventories and imported evidence snapshots remain unchanged.
