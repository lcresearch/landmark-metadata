# New focal execution results

Run date: 10 November 2026 (America/Los_Angeles; log timestamps use UTC).
External root: `/home/hsz/landmark-evidence/focal-rerun-20261110`.
This known-outcome rerun uses newly acquired matching inputs and a new build/
execution history. It does not recover or authenticate the missing October run.
The [runbook](README.md) records dependencies, commands, failures and interruptions.

## E1/E2: completed and independently checked

The strict Android audit completed with `PASS` at
`2026-11-11T05:46:40.160639+00:00`. It reads actual files rather than accepting
stored success flags alone:

- Eight builds and sixteen condition/phase records cover 32 input observations.
- Four caught deletion-getter exceptions and 28 successful category lists match
  the stated comparison targets. The exceptions occur after successful inference.
- Each same-input raw output is byte-identical across conditions and replay.
  Successful returned score bits agree with the raw tensors.
- Both permutation inputs change 999 of 1,000 displayed labels; restoration
  returns the full decoded output to the original. E2 getters still succeed.
- Actual generated source, classes, DEX and native payloads are equal across all
  eight E1/E2 builds. APK model assets, device-loaded model identities and prescribed
  RGB bytes are checked against their actual artifacts.
- Five distinct model byte conditions reduce to one canonical graph:
  `73e57df01115600419abb72de4b2c3257200e12eb205d335bcbfc203a589bee8`.

The planned primary/replay view excludes the initial interrupted attempt. E1
primary retains three complete condition records from the second attempt and a separate
restoration continuation. Subsequent E1/E2 phases use per-condition invocations.
All old/partial data and selection/relocation hashes remain available. This is an
explicitly resumed collection; no uninterrupted-controller history is asserted.
There is one independent model graph, not 32 models or independent image samples.

Primary external audit records:

- `android/audit-results.json`: actual build, input, raw and decoded checks.
- `android/model-preservation-audit.json`: independently recomputed preservation.
- `android/E1/results.json`, `android/E2/results.json`: producer summaries,
  subordinate to actual artifacts and the independent audit.
- `android/E1/executions/`, `android/E2/executions/`: complete device bytes,
  actual commands, interrupted attempts and continuation provenance.

## P2: paired Android comparison

Ten APKs were built and their 28 selected archive/Java/native prerequisites matched
historical pins. Preparation and the execution-input freeze completed before P2
instrumentation. The E1/E2 package was removed because P2 uses a distinct signing
key, and the same new software AVD passed functional readiness again.

All ten configurations completed. The maintained independent reader passes all
348 checks, separately reporting evidence validity, coverage and historical
outcomes as `PASS`. It reads 18 reached input observations, 16 decoded lists and
ten wrapper raw tensors. Across eight shared successful condition/input pairs,
all 1,000 returned score bit patterns and labels agree by output/class index.
Task's returned category scores are not independently observed native raw tensors.

Deletion is rejected at the wrapper getter after successful inference, and at
Task's public construction call before input preparation/classification. The Task
outer `IllegalStateException` wraps an `IllegalArgumentException` describing the
1,000-output/999-label mismatch; it is not a missing-library result.

The initial maintained readback reported one historical-outcome failure because
its expected cause text omitted `Error occurred when initializing ImageClassifier:`.
That prefix appears in both the unchanged fresh device record and the
[preserved historical description](../../research/20261004-p2-p3/P2/MANUSCRIPT_IMPACT.md).
The reader now requires the complete exact Java cause text. Its positive synthetic
fixture uses an independent literal, and negative cases reject truncated/extended
messages, a wrong cardinality and a wrong exception type. No result bytes were
normalized, edited or rerun to obtain a pass.

`readback/p2.json` and the original reader copy retain the initial failure.
`readback/p2-after-message-fix.json` is the new successful readback. The full
P2 device/controller evidence is under `round/P2/executions/primary/`.

## P3: six-input core completed

All six pinned reference bodies and all five model identities passed their pins.
The fresh core analysis recomputed the graph/weights/ordered-output bridge:
all 165 non-metadata buffers match, as do computation fields, ordered outputs and
the associated label bytes. The pinned lite card names the parent classification
card; that card explicitly prescribes the external label file and background
offset. Comparing all 1,000 positions gives:

| Condition | Matching positions | Differing positions |
|---|---:|---:|
| Original | 1,000 | 0 |
| Injected permutation | 1 | 999 |
| Restoration | 1,000 | 0 |

The source/method is adapted from the preserved P3 analyzer, not a new independent
implementation. Its first invocation stopped on a restoration-name mapping bug;
the original source/partial output remains in `p3-core/`. The corrected invocation
completed in `p3-core-attempt2/`, with all new identities and detailed comparisons.

Stable class IDs remain `ABSTAIN`; prediction accuracy is not evaluated. The old
30-request search and auxiliary synset comparison were not rerun. The catalog
revision is not asserted to be release-time documentation, and repeated matching
display strings do not establish unique class identities.

## Limits and retention

These results concern injected resource interventions on one classifier, selected
consumer/toolchain configurations and two synthetic inputs. They do not establish
natural model defects, prevalence, task accuracy, production crashes or a new
detector advantage. E5's earlier negative baseline result remains unchanged.
Human review is still pending. Broader Hand/E4/E5 and parser history were not
recreated, and no manuscript claim or human signoff was silently updated.

All raw data, tools and builds stay outside Git. Experiment execution and automated
readback are complete, and the owned emulator was stopped after verifying its
process identity. Local archive verification is recorded separately; local
retention does not establish remote backup or anonymous reviewer access.
The new local archive is 3,321,366,905 bytes, with all 2,120 members verified by
stream readback. Archive SHA-256:
`57970b8ff5a4127caf11b13bdc9837ed2479c13dbb488cfc5262506a76535afd`.
The [delivery receipt](delivery-record.json) records exact locations and selected
report digests. The archive deliberately excludes installed runtimes/caches and
keys; it is not a portable, complete offline reproduction environment. Final
documentation and this receipt postdate sealing; executed source hashes are
retained inside the package. All 176 source/regression tests pass. These checks
complement actual execution and do not substitute for human review.
