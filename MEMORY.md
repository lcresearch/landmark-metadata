# Project continuation

Current as of 11 November 2026 (America/Los_Angeles). Read [TODO](TODO.md),
[decisions](docs/DECISIONS.md) and [repository policy](AGENTS.md) before work.
Use the [repository map](docs/REPOSITORY_CLEANUP.md) to distinguish maintained
code from preserved snapshots. This file summarizes current state; dated detail
belongs in its work record and Git history.

## Current manuscript and research boundary

**Validation Boundaries for Model Label Resources: A Controlled Classifier Case
Study** lives in [the October 20 revision](work/label-resource-revision-20261020/REVISION_NOTES.md).
The [current pointer](docs/CURRENT_MANUSCRIPT.json) pins short/full sources,
claim ledger, handoff and predecessors. Its October validation recorded four
short-paper pages and eight companion pages. No venue is selected.
The November rerun has **not** been incorporated into that manuscript.
The [six author questions](work/label-resource-revision-20261020/ARTIFACT_HANDOFF.md)
and all historical human-audit entries remain **PENDING**.

The contribution is a bounded empirical study: one classifier graph, five model
byte conditions, two synthetic inputs and selected consumer configurations.
S/I/D stay separate; P supports intervention validity. E5 showed no extra rejection
over the matched simple baseline or Task initialization. Do not infer prevalence,
natural defects, prediction accuracy, production crashes or a new detector advantage.
Hand/E4/parser history is auxiliary and was not recreated by the focal rerun.

## New focal execution — 10 November 2026

The user authorized rerunning experiments after losing the former cloud evidence.
[Input recovery](work/input-recovery-20261110/README.md) matched all five model
conditions, both RGB inputs and six P3 input bodies to existing pins. The
[new runbook](work/focal-rerun-20261110/README.md) records verified prerequisites,
commands and deviations; [RESULTS](work/focal-rerun-20261110/RESULTS.md) records
actual outcomes. Matching fresh results do not authenticate the old execution.

- E1/E2 primary/replay: eight builds, sixteen condition/phase records, 32 input
  observations, 28 decoded lists and four caught deletion-getter failures after
  inference. Raw outputs match; permutation changes 999 label positions and
  restoration reverses the change. The strict automated audit passes.
- P2: ten configurations, 18 observations, 16 decoded lists and ten wrapper
  tensors; all 348 maintained checks pass. Eight shared successful pairs have
  identical returned score bits/labels. Task rejects deletion at construction;
  the wrapper rejects it at the getter. Task native raw tensors were not observed.
- P3 core: 165 non-metadata buffers match; original/permutation/restoration match
  the qualified display reference at 1000/1/1000 positions. Stable IDs remain
  ABSTAIN. The full 30-request search and auxiliary synset inquiry were not rerun.

Two E1 chat interruptions and their original records remain preserved. Completed
scientific outcomes were kept; only missing transport collections were continued
with separate invocation and selection/copy identities. The first P2 readback
failed because its expected Java cause omitted a prefix. The corrected reader
requires the full exact message; the original reader/FAIL and unchanged device
bytes remain available. Setup and P3-analysis failures are also retained.

Historical model/reference, eleven wheel, Android/JDK and Java pins matched.
Python 3.11.16 is a newly recorded uv distribution; the old interpreter was not
pinned. The run used a software AVD with `-accel off`. The execution host saw
`/dev/kvm`; acceleration usability was not established. All phases finished,
the owned emulator was stopped and 176 source/regression tests passed.

## Evidence availability and retention

Current external locations, recorded by the November run:

| Material | Location / identity |
|---|---|
| Recovered focal inputs | `/home/hsz/landmark-evidence/input-recovery-20261110` |
| Recovered references | `/home/hsz/landmark-evidence/reference-recovery-20261110` |
| New execution and retained failed attempts | `/home/hsz/landmark-evidence/focal-rerun-20261110` |
| New local archive | `/home/hsz/landmark-evidence/focal-rerun-20261110-evidence.tar.gz` |

The [delivery receipt](work/focal-rerun-20261110/delivery-record.json) records
3,321,366,905 bytes, 2,120 members verified by full readback and archive SHA-256
`57970b8ff5a4127caf11b13bdc9837ed2479c13dbb488cfc5262506a76535afd`.
It is local retention, not remote backup, reviewer access or a complete offline
environment. The receipt/final docs postdate archive sealing; the archive is not
a snapshot of the final PR tree. Executed source identities are retained inside.
This cleanup does not re-read the raw archive or delete external files.

The old cloud `/workspace` material is unavailable here: all 39 inventoried paths
were absent and a bounded local filename search found no archive candidate.
This does not prove permanent loss from every backup. The October selected
`focal-saved-evidence.tar.gz` was 1,924,911,456 bytes, SHA-256
`1e6f9737ecdaf426b8e4a30391fd1298b6f503e39d8c17423c521376b86c746e`;
its [historical recovery record](work/evidence-recovery-20261005/README.md) is
not evidence of current availability. Later reconstruction/parser/E5 gaps remain
separate, as recorded in the [missing list](work/evidence-recovery-20261005/MISSING.md).

Historical locators below preserve provenance and the import-backed hash guard.
They are not current paths or download links; excluded manifest hashes cannot
be verified from this source-only checkout:

| Local package | Identity |
|---|---|
| `/workspace/metadata-contract-e2e-20261004T030536Z` | `SHA256SUMS` SHA-256: `aba0739ac893ee69795556d43384029d20cc096a584156d0f0c37638fdc8751d` |
| `/workspace/metadata-contract-audit-20261004T062010Z` | `SHA256SUMS` SHA-256: `b73388bf6ce263d9fff7659a90166d80ae56544d540a12620768a1bc8a8af89d` |
| `/workspace/metadata-contract-paper-revision-20261004T065132Z` | Revised `manuscript/paper.tex` SHA-256: `390445a494c24cf9e9069ca3d5ab62e4d0174587f631856b764846d54908782d` |
| `/workspace/metadata-contract-p2p3-20261004T073824Z/P2` | Same-Android `SHA256SUMS` SHA-256: `d903826e8d6f666921ba9e6e9247fe541cb3b7c6b8170113c4b5c572f82f58d5` |
| `/workspace/metadata-contract-p2p3-20261004T073824Z/P3` | Reference inquiry `SHA256SUMS` SHA-256: `77345fcadf085095d23722ac7a16ef7c4d5d34c202e4f32b7046750cad919de3` |
| `/workspace/metadata-contract-p2p3-20261004T073824Z` | Final 1,159-entry `SHA256SUMS` SHA-256: `aed26d18de158a3eebf5dcd7a3996356da99419779b689addd1f083a6a0cec27`; excludes P2 SDK/AVD operational state |

## Repository delivery and next work

PR #17 was squash-merged at `fa8a318eabff681ee061e55a7908a20a7fda2113`.
On 11 November, [PR #18](https://github.com/lcresearch/landmark-metadata/pull/18)
(input recovery, `05e6b22…`) and
[PR #19](https://github.com/lcresearch/landmark-metadata/pull/19)
(new focal run, `a94b98f…`) were still open; #19 targets #18's branch.
The cleanup branch `codex/repository-cleanup-20261111` starts from #19's exact
head `a94b98ffdce5814b9db717ae8d4db4fd8a80f3f2` and targets that branch for review.
Check live PR state before integration; this request does not authorize merging.

Next: retain a second verified evidence copy, reconcile paper/claims with the new
run, resolve auxiliary evidence scope, complete human review, provide reviewer
access and select a venue. See [TODO](TODO.md) for completion criteria.
Do not start another broad model/mutant campaign by default.

The former 561-line continuation history remains available
[at the cleanup base](https://github.com/lcresearch/landmark-metadata/blob/a94b98ffdce5814b9db717ae8d4db4fd8a80f3f2/MEMORY.md).
Dated work records and historical audit targets remain in the tree. Their old
"current", open-PR and evidence-availability statements describe their own time;
they do not override this file, TODO or repository policy.
