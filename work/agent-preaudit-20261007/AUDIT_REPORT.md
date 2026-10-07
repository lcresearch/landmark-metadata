# Consolidated agent pre-audit findings

**No material contradiction was found in the inspected core saved E1/E2/P2
observations or the qualified P3 reference chain.** The review supports those
claims within the specified saved-record scope. It does not authenticate past
executions independently of their records, rerun inference or complete human
verification. It does not certify novelty or acceptance.

Target, protocol, reviewers, exact report/input-index identities and limits are in
[audit-index.json](audit-index.json). Reports use the frozen four-page draft and
its [claim crosswalk](../workshop-convergence-20261007/CLAIM_EVIDENCE.md).

## Core evidence newly inspected

| Area | Fresh saved-evidence observation | Important boundary |
|---|---|---|
| Actual public call | New disassembly of seven distinct application-class identities and four DEX identities traces the real generated getter. The raw observation reads a duplicate without backing writes. | Static binary inspection plus saved execution attribution; no new source-to-binary rebuild or inference. |
| Model identity | All 26 final APK paths contain the matching working/staged model and DEX. Binary manifests and saved install/instrumentation links agree. All 18 later preload hashes agree; original eight have no preload read. | No device-pulled installed APK or native interpreter-buffer interception is claimed. |
| Preservation | Twenty-one model aliases represent five byte conditions. All 165 nonmetadata buffers and complete schema-known computation/output order agree; metadata buffer 165 has no tensor references. | Shared schema parser; separate exact prefix/one-byte checks constrain the mutation surface. P is preservation, not universal correctness. |
| Resource/code controls | Description changes one metadata byte. Label mutants preserve metadata/prefix. Java and generated classes match; DEX equality holds within each build family. | Restoration recovers label bytes, not the original ZIP container. Original/rebuild/P2 full DEX differs across families. |
| E1/E2 observations | Original primary and separate rebuild each have eight phase aliases/16 inputs/14 returned lists. P2 has ten configurations/18 actual inputs/16 lists. All 42 saved raw tensors and 44,000 returned categories were checked. | These are one focal graph's repeated observations. Replay numerics are outside this new primary-only readback. |
| E1 failure | Six inspected wrapper deletion observations reach the actual getter after recorded process success; raw bytes match corresponding controls. Stacks and attributed logs corroborate the recorded failure. | Exceptions were caught. Task deletion never reaches either planned input. |
| E2 association | Full score bits, raw values, top indices, 999 changed strings and inverse restoration agree. All eight successful Task/wrapper pairs align by class index/output position. | Task raw tensors remain unobserved; wrapper Category index is unset. |
| P3 | Independent comparison of the actual saved models and reference bytes confirms computational equivalence, publisher-card parent/background rule and 1,000/1/1,000 display agreements. Saved Git objects and card blobs also match. | Qualified display-order reference; stable class IDs, training lineage, release-time documentation and authenticated historical retrieval remain outside the conclusion. |

The coordinator independently reverified all 2,749 selected package payloads and
the pinned manifest before reconciliation. Matching package bytes do not prove
experimental truth. Correlated comparison counts in individual reports are not
accuracy or reliability statistics.

## Item-by-item disposition

Every **human status is PENDING**, including items with a supported agent result.

| Checklist item | Agent disposition | Human follow-up |
|---|---|---|
| HA01 actual generated call | Supported within inspected scope | Inspect the actual getter and one original/rebuild compiled-call trace. |
| HA02 loaded artifact identity | Supported within inspected scope | Inspect the APK/model identity table and saved install/preload attribution; retain its limits. |
| HA03 preservation | Supported within inspected scope | Review computational comparison, unreferenced metadata buffer, description control and ZIP/code scopes. |
| HA04 E1 observations | Supported within inspected scope | Read complete deletion stacks and stage records, then review full raw comparisons. |
| HA05 E2 observations and chronology | **Partial** | Observations are supported; decide whether predeclaration wording is justified by the available local chronology. |
| HA06 same-Android boundaries | Supported within inspected scope | Verify Task cause chain, 18 actual inputs and eight aligned successful pairs. |
| HA07 publisher reference | Supported within inspected scope | Assess authority/date/granularity of the exact parent card and label mapping. |
| HA08 Hand | **Partial** | Source/metadata/buffer/decoded comparisons and repair are checked; fresh Hand-class disassembly and source-to-installed-library equivalence were not. |
| HA09 structural/external/preflight (parent item) | **Partial** | Read the three distinct subresults below. |
| HA09a external/development | **Partial** | Saved E4 counts/compile warnings support the summary; independently recomputing 15 graph groups/exclusion bridges and detailed development counts remains undone. |
| HA09b E5/baselines | **Partial** | Original 65 fixture identities/judgments and 25 core baseline records agree; full getter-condition reevaluation and the raw isolated Gesture probe were not done. |
| HA09c later parser probes | **Blocked: missing evidence** | Later actual-library probe records and separately pinned E5 reconstruction catalog remain unrecovered. |
| HA10 antecedent/contribution | **Partial** | Actual #770 issue/member reply supports its attribution; closest full texts were not reread and novelty/significance cannot be signed by agent consensus. |

Original Hand/E4/E5/baseline material is **present outside the selected focal
package** and was inspected at its own paths. It is not globally missing. The
later parser/reconstruction records are a separate, unrecovered evidence history.

## Findings requiring a decision

**F1 — E2 chronology has limited independent support.** The saved freeze identifies
the exact plan and asserts it preceded E1 predictions, but contains no timestamp.
Mutable original filesystem mtime and recorded command starts are consistent with
that order; they do not independently prove it. The transformation itself is
deterministic and its complete saved effects were verified. This is an evidence
limitation, not proof of post-hoc selection or false experimental results.

Suggested author action: inspect contemporaneous records and attest only to the
scope actually supported. If stronger timing support is unavailable, change the
short paper's “E2 predeclares” to “E2 uses a deterministic one-position cyclic
shift,” and qualify the full companion's stronger prior-inspection sentence.
The frozen manuscript is intentionally unchanged in this audit PR.

**F2 — Later parser execution cannot be rechecked from its own raw evidence.**
The current short paper already attributes these findings to a reconstruction
report and discloses unrecovered raw probes. Keep that attribution, recover the
correct later records, or omit the auxiliary execution claim. Present original
E5 files cannot replace a different pinned reconstruction. A new run would be
new evidence, not recovery of the missing history.

**F3 — Secondary coverage is substantial but incomplete.** Hand, frozen external
checks and baseline records were read directly. The remaining checks are listed
per item above; do not convert PARTIAL into full validation because their reports
agree. The main E1/E2/P2/P3 findings do not depend on calling these secondary
checks complete.

## Audit execution issues, transparently retained

The new observation reader initially hardcoded `labels.txt` instead of the actual
`labels_without_background.txt`; four filename assertions failed while actual
members parsed. The initial stdout is retained. Its detailed JSON was overwritten
by that reviewer's rerun; the separately reconstructed initial-helper rerun is
explicitly labeled, not represented as the original output. The corrected reader
passes the bounded comparisons without modifying any preserved experiment input.

The reference reader initially stripped a commit-signature trailing newline;
retaining the original bytes allowed correct Git object serialization. This
changed the audit calculation, not source evidence. The preservation reader was
refined to fail closed and reject overwritten outputs, then rerun in a new
directory with identical substantive comparisons. Exact scripts and deviations
remain available in the area reports.

## Scope of independence and remaining work

Five fresh-context area reviewers and one chronology subreview shared the same
machine, tooling, manuscript and evidence. They were not recruited humans, not
blind to the manuscript's expected observations, and not independent sources of
the historical data. The coordinator reviewed scripts/results and reconciled
scope instead of treating agreement as a confidence score.

Next is the [human continuation sheet](HUMAN_HANDOFF.md): inspect key original
records and authority links, resolve F1 and retained auxiliary claims, and sign
the existing human template against this exact manuscript. Persistent anonymous
evidence delivery remains a separate pending task.
