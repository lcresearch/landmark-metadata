# Evidence-binding and immutable-import follow-up

Date: 10 November 2026 (America/Los_Angeles). Review base:
`2ba12520f3bbeec509bd0257b443bcbf6f6494d8`, the merged PR #16 commit.
The user requested a careful repository audit and implementation of the work
possible with the available checkout. This follow-up repairs five reproducible
source-level findings; it does not rerun or authenticate historical experiments.

## Findings and repairs

| Finding | Previous acceptance gap | Maintained repair |
|---|---|---|
| P1: P2 execution attribution | Frozen build rows could report failure or wrong APK hashes while saved output still received PASS; install/controller records were ignored. | Require all six successful build stages, actual APK/asset digests, exact controller identities and build/device snapshots, successful install/instrumentation for the selected APK/application, and consistent stage/failure records. |
| P1: Task model attribution | All ten worker model hashes could be replaced while the reader still counted 16 decoded observations. | Hash each Task model, match the corresponding Android condition, and bind every worker result, including deletion rejection, before accepting observations. |
| P2: Hand execution attribution | A successful-looking worker result did not have to identify the actual bundle/image or match its controller snapshot. | Validate the four variant identities and paths, actual bundle/image bytes, worker hashes, controller command and observed result. |
| P2: Hand float payload | Every output could contain the same one-byte blob with a matching recorded digest while complete landmark JSON remained. | Check finite coordinate structure and decoded digest; independently reconstruct the producer's float serialization and compare every stored byte. |
| P2: immutable P2/P3 import | A new file could be copied before a changed manifest or later source was rejected. | Preflight the whole source selection, destinations and index before writing; reject changed, missing, unindexed or linked entries and preserve an identical import without rewriting its index. |

The P2 repair is in [verify_p2_records.py](../review-fixes-20261021/verify_p2_records.py).
Task and Hand use [verify_observations.py](../observation-review-20261004/verify_observations.py).
The importer is [import_p2p3_sources.py](../../scripts/import_p2p3_sources.py).
Its no-write guarantee concerns validation failures; it is not a transactional
filesystem implementation for interrupted writes or hardware/I/O failures.

## Validation and compatibility

All **165** repository tests passed with:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_source_tree.py
git diff --check
```

The suite adds 21 test methods across
[P2 readback](../../tests/test_p2_readback.py),
[observation readback](../../tests/test_observation_readback.py) and
[immutable imports](../../tests/test_import_p2p3_sources.py), with multiple
adversarial cases inside those tests. Positive fixtures retain all expected P2,
Task and Hand outcomes, reordered complete manifests and relocated P2 evidence.
Hand's positive fixture now uses actual coordinate dictionaries and an independently
packed 127-float payload, instead of placeholder landmark values and byte strings.
Negative fixtures keep other records internally consistent where needed, so a
failure tests the intended missing binding rather than an incidental stale hash.

Record formats were inspected against preserved P2 `build.py`, `run.py` and
`common.py`, reconstructed Task `run_task.py`, and Hand `prepare_variants.py`,
`run_tasks.py` and `hand_task_one.py`. These are static compatibility checks and
synthetic fixtures; **real historical record compatibility remains untested**
because the excluded raw roots are unavailable. The source checker validates
354 imported files and seven current/predecessor artifact pins. Its historical
path and unchecked external-evidence warnings remain expected and visible.

The pre-repair synthetic counterexamples were recorded locally under
`/tmp/landmark-repo-review-oivccbwm/`; test execution output is at
`/tmp/landmark-evidence-fixes-tests.log`. These are temporary diagnostic locations,
not an archived experiment or a durable evidence deposit. The committed regression
sources are the reproducible description of the acceptance gaps.

## Remaining boundaries and next steps

Recover unchanged raw artifacts and records listed in the
[current commands](../../docs/reproduction/COMMANDS.md), then run the maintained
readers to new external outputs and inspect every failed comparison. Newly required
records must not be reconstructed from prose to obtain PASS. P2 continues to
separate evidence validity, coverage and historical outcomes; Task classify still
does not expose an independently observed internal inference stage.

Saved-file agreement cannot prove that a process executed those bytes or provide
independent provenance. No Android, model, JVM or manuscript build occurred in
this follow-up. Preserved source imports, their indices, manuscript bytes and
historical reports remain unchanged. E5's zero incremental core rejection, the
bounded case-study scope, pending human audit and unresolved external evidence
delivery remain unchanged. The manuscript's 48-entry source index retains its
historical review anchor; a later edit to an indexed document does not justify
rewriting that provenance.

Deliver on `codex/evidence-attribution-fixes` through a new PR. This request
authorizes the repair PR, not its merge, evidence publication or paper submission.
