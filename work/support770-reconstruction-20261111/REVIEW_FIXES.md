# PR #25 review fixes — 11 November 2026

The user authorized repairing the three findings against `ebc9fe3`, adding
regressions, updating [PR #25](https://github.com/lcresearch/landmark-metadata/pull/25)
and reviewing the result again. No inference, APK build, generation or emulator
execution is part of this follow-up. Merge authorization remains separate.

| Finding | Repair | Regression evidence |
|---|---|---|
| Missing claimed outputs still passed | Require stage-consistent output descriptors/files, exact shape/byte count, segmentation/mask counts and model-associated labels. Scientific failures remain valid when their stages and reached artifacts are complete. | Missing descriptors/files, wrong sizes/shapes/counts/kinds/labels, inconsistent stage states and valid earlier failure cases |
| Invocation status did not identify the consumer | Match install/instrument/collect arguments and working directory to the APK, fixed consumer/class and owned serial; check successful transport, ordering from the frozen build, and collected bytes against device files. | `/bin/true`, wrong APK/serial/class/package, failed install, stale ordering, matching wrong build metadata and mismatched collection bytes |
| Build steps could exceed the 600-second consumer limit | Give each consumer one monotonic deadline, pass its remaining budget and absolute deadline to every child, reject late completion and preserve FAIL. The recorder refuses expired launches and kills a timed-out process group. | Fake-clock cumulative slow steps, no launch after expiry, retained failure and independent consumer budgets, process-launch delay and timeout/exit-zero race |

Twenty-two new regression tests plus the existing suite pass: **223 tests**.
The tests use temporary synthetic records and mocked clocks/process boundaries;
they do not execute model code or consume the sealed evidence as mutable fixtures.
The four-step deadline example receives 180/180/180/63 seconds, with one shared
deadline, and cannot proceed to a fifth step after exhausting 600 seconds.

The revised reader passes **117 checks** on the unchanged saved run. Outcomes
remain wrapper **FAIL at category_getter** and Task **PASS through mask access**.
Replaying both original review counterexamples in memory now fails at the required
output and command-identity checks. These are additional saved-byte checks, not
new scientific observations, authenticated provenance or human verification.

Validation outputs are retained separately at
`/home/hsz/landmark-evidence/support770-review-fixes-20261111/`. The original
`support770-reconstruction-20261111` root, its selected archive and its repository
delivery receipt are not rewritten or resealed. All 272 inventoried files (269
selected evidence files, the manifest, archive and receipt) retain their exact
bytes and modification times. The original 66-check readback and its executed
source snapshots remain available with their original identities.

The final `readback-rereview.json` is 12577 bytes, SHA-256
`ce7507d81cd78fb7a0244269e559eee74444cefd9d414d1cccf828d3489df6a0`;
`review-counterexamples.json` is 432 bytes, SHA-256
`fe01f1cfb411d747a44205c1449653f37b0472e9041eeef82f642f7a7ddcb327`.
`preservation.json` is 116 bytes, SHA-256
`ee68d4e5def61fcef22ef9a28813e0c3c44049ca954e1522a823be11b21e0051`.
These follow-up reports are separate from the original sealed manifest/receipt.

The final source/import/manuscript checks and diff check pass. Review of the fixes
and adversarial cases found no remaining blocker among the three findings. The
actual runtime/build source snapshots differ from the repaired current tools;
the new deadline handling is regression-tested, not retroactively claimed to have
executed in the recorded experiment. Current manuscript pins, model results and
human PENDING statuses are unchanged. The final remote head is checked when the
updated PR is delivered and remains open for user review.
