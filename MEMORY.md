# Project continuation

Current as of 11 November 2026 (America/Los_Angeles). Read [TODO](TODO.md),
[decisions](docs/DECISIONS.md) and [repository policy](AGENTS.md) before work.
Use the [repository map](docs/REPOSITORY_CLEANUP.md) to distinguish maintained
code from preserved snapshots. This file summarizes current state; dated detail
belongs in its work record and Git history.

## Current code layout

The 11 November code cleanup puts the focal dependency closure in
[experiment](experiment/README.md), with an explicit 27-destination staging map.
Initialization copies selected model/E1/E2/P2 sources instead of whole historical
suites. [archive](archive/README.md) verifies and restores removed source paths
from fixed ancestor `e9da459f6043684cdecba913c9c711433371909d`; imported bytes and
historical manuscript pins are unchanged. Auxiliary reader inputs live under
[support](support/README.md). A fresh source-only initialization validated the
recovered model/reference pins; no Android/model execution was performed.
The original checkout's paper branch was left untouched. PR #21 now stacks on
[paper PR #22](https://github.com/lcresearch/landmark-metadata/pull/22); its current
paper and evidence pins are carried forward unchanged. The [follow-up review](docs/PR21_REVIEW.md)
fixes the ordinary source-check command and the paper readback/index paths, and
records fresh saved-byte checks without new inference. Both PRs remain unmerged.

## Current manuscript and research boundary

**Validation Boundaries for Model Label Resources: A Controlled Classifier Case
Study** now uses the [11 November short-paper revision](work/acceptance-paper-revision-20261111/REVISION_NOTES.md).
It incorporates the November E1/E2/P2 rerun and P3 six-input core, and explicitly
discloses old evidence loss, known outcomes, two interrupted collections, selected
continuations and the P2 reader correction. The four-page source retains the
narrow case-study framing; the October full companion stays historical/unchanged.
The [current pointer](docs/CURRENT_MANUSCRIPT.json) binds the new source, claim map,
handoff and 1,036-member evidence index while retaining old manuscript identities.
Saved-byte Android/P2/P3 rechecks and full 2,120-member archive verification pass;
these are new editorial readbacks, not new model execution or human verification.
The old 48-source index resolves 47 files in the checkout plus S40's exact old
Git version; the maintained reproduction README has since changed. No pin was
silently refreshed. The [six current author questions](work/acceptance-paper-revision-20261111/ARTIFACT_HANDOFF.md)
and all historical human-audit entries remain **PENDING**. No venue is selected.

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
The later manuscript revision re-read the whole archive and selected live files;
its reports are retained under `/home/hsz/landmark-evidence/paper-revision-20261111/`.
Original experiment records remain unchanged; the new review outputs postdate the archive.

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

The user subsequently authorized review and squash integration of the cleanup
and its prerequisites. On 11 November, both prerequisite PRs were squash-merged
into `main` and their sole parents and complete reviewed trees were verified:

- [PR #18](https://github.com/lcresearch/landmark-metadata/pull/18), input recovery:
  `f4a6d8f4db7e7a04ce49dd28e1e4298398208f6f`, matching reviewed head `05e6b22…`.
- [PR #19](https://github.com/lcresearch/landmark-metadata/pull/19), new focal run:
  `df56b9f6920a2478ff6c8c4fbd9d1e1f04aabc9b`, matching original reviewed head `a94b98f…`.

[PR #20](https://github.com/lcresearch/landmark-metadata/pull/20) contains the cleanup
and these integration notes; its verified GitHub merged state is the terminal
completion record. Dependent feature branches received content-preserving ancestry
sync commits before retargeting to main; no force push or direct main push was used.
Review passed 170 tests at #18 and 176 for the final code, source/import/manuscript
checks, and ten selected external-record digests. No new model execution or full
archive readback was performed during this review. Human verification remains pending.

PR #22 and the subsequent code-cleanup PR #21 are merged; current main is
`8005274e9eccbea30fb3189779f03e8d693b3720`. The acceptance-focused follow-up is on
`codex/acceptance-checks-cases-20261111` in [PR #23](https://github.com/lcresearch/landmark-metadata/pull/23),
open for review. It retains the preceding evidence index
and observations, with four explicit acceptance decisions and concise provenance.
The current task authorizes a PR and bounded public-report screening, not a merge
or a new natural-case execution.
Next: retain a second verified evidence copy, complete human review, resolve any
auxiliary claims retained for submission, provide reviewer access and select a venue. See [TODO](TODO.md) for completion criteria.
Do not start another broad model/mutant campaign by default.

The former 561-line continuation history remains available
[at the cleanup base](https://github.com/lcresearch/landmark-metadata/blob/a94b98ffdce5814b9db717ae8d4db4fd8a80f3f2/MEMORY.md).
Dated work records and historical audit targets remain in the tree. Their old
"current", open-PR and evidence-availability statements describe their own time;
they do not override this file, TODO or repository policy.

The [bounded public-report screen](work/case-screening-20261111/SHORTLIST.md)
re-read the existing seven reports and 69 comments. It selects Support #770
(unsupported segmentation/generated-interface combination) and #319 (default
versus metadata asset selection) as conditional reproduction candidates. Exact
linked model responses supplied TFL3 prefixes; full model hashes and historical
environments are still missing. #870's linked Drive file returned 404. No new
model execution or natural defect is established; the paper sample is unchanged.
Fresh public responses and availability prefixes are retained outside Git at
`/home/hsz/landmark-evidence/case-screening-20261111/`.
