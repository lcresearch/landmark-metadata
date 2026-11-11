# Research and repository decisions

These are working decisions and their reasons, followed by dated decision history.
They are not a record of completed human review. For current evidence availability
and delivery state, read [MEMORY](../MEMORY.md); dated entries describe their own
scope and do not renew old merge or publication authorizations.

| Decision | Reason and operational consequence |
|---|---|
| Use pull requests for every future repository change. | The user's latest instruction replaces direct pushes with feature-branch commits and a PR for review. Never update the default branch directly through Git or API, and do not merge or enable auto-merge without explicit user instruction. This includes documentation and memory updates. |
| Use Squash and merge for authorized PR merges. | The user explicitly defines "merge" as squash and merge. Preserve that default unless explicitly overridden, gate the operation on the reviewed head SHA, and verify a single-parent result. The preference does not authorize unrelated merges or direct main pushes. |
| Keep this repository source-only. | The user's latest scope excludes SDKs, emulators, and build products. Preserve code, necessary source documentation, TODO, and concise handoff notes; keep full binary evidence elsewhere. Do not describe this repository as the complete evidence archive or a self-contained offline reproduction package. |
| Separate a documented reproduction entry from a delivered evidence package. | `docs/reproduction/` inventories exact inputs, versions, hashes, command status and missing material. Selected local hash/readback checks and source-copy helpers do not establish a clean-machine install or new inference. Preserve the original and reconstructed result sets separately; an external deposit and fresh-workspace validation remain distinct tasks. |
| Treat the selected local recovery as saved-byte preservation. | The user chose local packaging and a missing list. The October original E1/E2, build-audit and P2/P3 package was verified outside Git but is now unavailable; the later reconstruction remains unrecovered. The November rerun has a separate local package and provenance. Matching shared bytes cannot establish later-run provenance. Package integrity, recorded-observation checks, fresh execution and human verification remain distinct; durable publication is a separate task. |
| Lead with controlled executable evidence. | E1 reaches the actual generated getter after successful inference; E2 returns successfully with changed label association. Together they establish observable interface changes under the tested computation-preserving interventions. |
| Keep S/I/D distinct; place P in experimental validity. | Structural acceptance, supplied-reference agreement, and decoder compatibility answer different questions. Preservation supports causal attribution and is not general model correctness. |
| Treat E5 as supporting diagnostics. | The audited five-condition comparison found no extra rejection beyond the reasonable simple baseline or official Task initialization. Limited template matching is not general consumer-code analysis. |
| Include resource parsing in the selected consumer's contract. | The historical Python splitter differs from Java FileUtil on VT and U+2028. Disclose the counterexamples and maintained valid-UTF-8 fix separately from the historical 65-fixture results; malformed encoding abstains. |
| Require fixed artifact identities and actual input records in readback. | A matching fixture count or leftover decoded files cannot establish complete evidence. E5 must match a separately pinned manifest; Task must validate prescribed inputs and their recorded status before counting successful observations. |
| Strengthen E2 only to supported display-reference agreement. | P3 links a publisher-prescribed external display order through an exactly graph/weight/output-equivalent TFHub artifact and its explicit classification/1 parent. Original/restoration match 1000 positions; permutation disagrees at 999. Stable-ID lineage remains ABSTAIN; prediction accuracy is unmeasured. Old E5 reference-free outputs are not rewritten. |
| Use completed same-Android P2 as the primary stage comparison. | Both official paths run on one API-30 x86_64 AVD. Task rejects deletion at construction; the wrapper at the getter after process returns. Different native integrations remain, and Task classify combines internal stages. Retain the public IllegalStateException and its informative IllegalArgumentException cause. |
| Keep Hand as a bounded secondary witness. | Static generic binding changes and unchanged Task output on one image do not establish a general failure, a complete metadata repair, or universal Task insensitivity. |
| Separate agent reconstruction from human verification. | The audit rebuilt using installed fixed tools and a new AVD. It does not complete independent human review or independent-operator/toolchain installation. |
| Bind the human audit to the current manuscript and evidence history. | `docs/human-audit/` maps ten inspection items to the 16 ledger claims, separates earlier agent work from human observations, and supplies an unsigned template. Keep original runs, installed-toolchain rebuilds and later reconstruction records distinct; missing raw evidence cannot inherit a report's PASS. Preparation can finish while every human status remains PENDING. |
| Freeze historical evidence. | New runs and corrections get new timestamped records. Missing executions, negative results, and failures remain visible; no retrospective filling of missing evidence. |
| Supplement historical READMEs and edit a separate manuscript working copy. | Preserve imported source bytes and original provenance. Current availability notes, an English audit summary and a source/parent digest index supply usable entry points without rewriting historical claims or implying that excluded evidence is present. |
| Treat consistency review as one part of publication assessment. | Source agreement, careful boundaries and fewer platform confounds do not establish novelty or practical significance. E5 still has zero demonstrated rejection increment in the audited core set. |
| Assess novelty and practical significance before the full rewrite. | Both bounded evidence tables are complete; use them to choose the final framing. Reproduction handoff and human-audit preparation may proceed in parallel. Completion does not certify publication readiness. Method novelty requires demonstrated capability beyond strong baselines. |
| Frame the rewritten draft as a controlled empirical study. | The completed contribution/significance comparisons support two empirical contributions: actual-interface consequences under preservation/reversal controls and configured enforcement stages. The claim–evidence ledger retains reference/provenance limits. E5 remains auxiliary; changing its name or adding abstractions would not establish a new method. |
| Separate local rewrite completion from verified PR delivery. | The initial HTTP 401 delayed publication. After API access recovered, #8's merge and remote base were verified; the feature branch was published through the GitHub API with matching Git identities and PR #9 opened. Direct Git push still returned 401. Publication does not authorize a PR merge or complete human audit. |
| Use the bounded contribution comparison to narrow the claim. | The completed comparison in `research/20261004-contribution-review/` supports controlled empirical characterization of resource/getter associations and configured enforcement stages. Existing official checks and prior constraint/mutation/differential methods rule out broad method-firstness claims; E5 stays supporting. The comparison is purposive and some full-text overlap remains unresolved. |
| State concrete relevance without claiming measured operational impact. | The bounded assessment in `research/20261004-significance-review/` links observed outcomes to documented integration workflows and public reports. It supports test-coverage and diagnostic lessons; frequency, developer benefit, production exposure and user harm remain unmeasured. Zero natural artifacts were reproduced. |
| Cite public Support #770 as both motivation and an antecedent. | A 2022 generated segmentation getter failure and member-recommended Task alternative connect the question to developer experience, but narrow novelty. The member describes an unsupported model/frontend combination; this is not a newly reproduced supported-path defect. |
| Compare against ordinary strong protections. | Full model-package pinning covers appended resources and detects the interventions. Task initialization, actual getter tests and reference-map checks already address relevant properties. Explain their distinct coverage; do not imply a hash bypass or measured cost savings from earlier rejection. |
| Stop indiscriminate expansion. | Additional similar mutants/models do not resolve the current evidence and novelty questions. Pursue bounded references/natural cases and a conditional method extension only when their outcome can change the contribution. |

For the active checklist use `TODO.md`. For continuation context and local sealed-evidence identities use `MEMORY.md`. Update both after substantive completed work, distinguishing proposed methods and planned experiments from observed results.


## 2026-10-07 UTC — Converge on a bounded workshop short paper

The user requested continued submission convergence, then preferred a short paper.
Prepare SQA4AI 2027's four-page research/experience format as a working candidate,
with the detailed seven-page source retained separately. Do not claim the user
selected a venue, that a workshop is easy to enter, or that short-paper status
waives novelty and soundness. Official candidate sources and their limits are in
`work/workshop-convergence-20261007/VENUES.md`.

Keep controlled E1/E2 public-interface evidence and same-Android stages primary.
Compress history and static counts, retain #770, keep E5 auxiliary and P separate
from S/I/D. Distinguish local focal recovery, omitted secondary payloads and
unrecovered later records. The old audit target is preserved; the new claim map
explicitly identifies the new manuscript and leaves human statuses pending.
Submission needs author verification, appropriate anonymous evidence access,
claim-scope decisions and final venue compliance. No broad model search, new
method, evidence publication or submission is authorized by this editorial task.
Deliver source/docs through a new PR stacked on the still-open evidence-recovery
branch; do not merge without the user's explicit instruction.


## 2026-10-07 UTC — Agent pre-audit before the user's human verification

Honor the request to use independent agents as checklist reviewers, while marking
all findings as agent work and keeping human statuses PENDING. Five fresh-context
reviewers plus a chronology subreview inspected shared saved inputs; no blinding,
forensic independence or human signature is asserted. New computations and static
disassembly are distinct from the historical executions; no model rerun occurred.

Preserve the audited manuscript and original evidence. List proposed chronology
wording changes separately: existing E2 freeze bytes support the declared fixed
transform, but timing lacks an independently attested timestamp. Partial Hand/
external/baseline scope and missing later parser raw evidence remain visible.
Present original secondary files are not labeled missing merely because they
were omitted from the focal package. The final report and human continuation
sheet guide author verification; agent consensus is not a reliability measure.

Store new first-party audit source, concise reports, identity index and TODO in
Git via a PR stacked on #12. Keep raw inventories, disassembly, binaries and logs
outside the source repository. Do not merge, sign as human, archive publicly or
submit a paper without the corresponding user authorization.

## 2026-10-08 UTC — Narrow chronology and separate new parser evidence

The user authorized the two prioritized tasks: revise the manuscript from the
pre-audit, then recover or freshly check the missing parser evidence. Preserve
the old manuscripts and audit records; publish new short/full sources, claim map
and target identities. Drop categorical E2 before-prediction timing while keeping
the verified deterministic transformation and saved outcomes.

Bounded recovery found no old parser/Task records or separately pinned E5 catalog.
The new fixed-library JVM experiment confirms the parsing/decoder mechanism and
22+3 existing helper cases; it does not authenticate missing historical execution,
run Android inference, Task initialization or all 65 reconstructed fixtures.
Keep both the new evidence and old gap visible. S/I/D/P and E5's auxiliary scope
are unchanged. Human statuses remain PENDING. Deliver through a new PR stacked
on #13; keep raw evidence/builds outside Git and do not merge or submit.

## 2026-10-08 UTC — Execute the authorized squash integration

The user's “ok. squash and merge” authorizes the reviewed #10–#14 sequence and
necessary base synchronization. Verify actual main equals the exact reviewed
predecessor tree before retaining a child tree; stop on unrelated main changes.
Append feature-branch synchronization commits without force pushes, retarget
each PR to main, pin the approved head in each squash request, and verify the
single-parent result and complete tree. No direct default-branch push is used.

Keep review snapshots and scientific payloads unchanged. Update current TODO
and continuation notes in the final #14 PR; its merged state is the terminal
completion record, avoiding an unapproved extra bookkeeping PR. Research human
signatures, evidence gaps and submission decisions remain pending after merge.


## 2026-10-20 America/Los_Angeles — Focus the label-resource case study

Use one core classifier and two empirical contributions: controlled actual-getter
outcomes under computation/code preservation, and two configured public enforcement
stages on the same Android environment. Label interventions change F; the description
control changes M. P3 qualifies display order, not stable identity or accuracy.
Promote the existing companion coverage analysis into the short paper, explicitly
separating observations, source mechanisms and analytical integrity implications.
Keep E5's negative result; move auxiliary Hand/static/parser details to the companion.

New source belongs in `work/label-resource-revision-20261020/`; preserve old sources,
audit targets and evidence pins. This revision inspects source and builds documents,
not raw external evidence or new inference. Keep six author questions unsigned and
persistent anonymous delivery open. Use the existing checkout, a feature branch and
an unmerged PR; do not publish evidence, select a venue, submit or sign for authors.

## 2026-10-21 UTC — Repair evidence verification without rewriting history

The user requested implementation of the comprehensive review's findings.
Gate PASS on actual checked identities, completion and relevant comparisons,
not self-reported record counts or independent checks of unmatched artifacts.
Validate the full compressed archive and extraction-path consistency, and
preserve import inventory coverage when original workspace files disappear.

Historical P2/parser readers and the old Android initializer remain byte-preserved.
New maintained entry points supply stricter readback and truthful local-input
provenance; current commands select those entry points. Preserve evidence failures
and distinguish failed historical-outcome comparisons from unreadable evidence.
Synthetic verifier tests are not new scientific execution or authentication of
unavailable raw records. Manuscripts and human PENDING statuses remain unchanged.

Record the already authorized and verified PR #15 squash in current navigation,
without rewriting dated provenance or the manuscript's original review anchor.
Publish the repair as a new feature-branch PR; merge authorization is separate.

The user's subsequent “review and merge” authorizes PR #16 after final review.
Use squash with the exact reviewed head, then verify the merged tree and sole
parent on main. Keep the live PR's merged state as the terminal completion
record, without rewriting historical scientific evidence or creating a separate
bookkeeping PR. Publication, submission and human-signature permissions are unchanged.

## 2026-11-10 America/Los_Angeles — Bind saved observations to their artifacts

The user's request to implement the repository audit authorizes source repairs
and their feature-branch PR. Require saved build/controller/worker records to
agree with the artifacts and invocations they identify; a frozen failed build
or a matching pair of stale output files is insufficient. Recompute the Hand
worker's float serialization from decoded JSON. Validate the entire P2/P3 import
selection and existing index before any destination writes, preserving unchanged
snapshot/index bytes and timestamps on an identical import.

Keep the P2 evidence-validity, coverage and historical-outcome dimensions distinct.
These checks establish consistency within the supplied evidence, not authenticated
execution, independent provenance or human verification. Inspect preserved producer
formats and use synthetic positive/adversarial tests while original raw inputs are
unavailable. Preserve imported code, manuscripts, historical reports and their pins.
Report real-record compatibility as untested until the excluded prerequisites are
recovered. See the [follow-up record](../work/review-fixes-20261110/README.md).

## 2026-11-10 America/Los_Angeles — Preserve evidence loss and new input provenance

The user reported losing the original materials in the former cloud `/workspace`.
Treat those execution records as unavailable unless independently recovered; do
not claim that hashes, old reports or newly matching results reconstruct their
provenance. The current task permits reading available material and recovering
public/deterministic inputs. The exact focal model, its four interventions, two
RGB inputs and six P3 input bodies now match the historical input pins.

Record these as fresh acquisition/reconstruction in new local directories outside
Git. Retain the current scripts, byte identities, unsuccessful location checks and
limitations in the [recovery note](../work/input-recovery-20261110/README.md).
An input hash match is not graph-bridge recomputation, inference, recovered old
execution evidence or human verification. Keep manuscripts and historical records
unchanged; any future experiment receives a new protocol/run identity and must
preserve deviations. Local storage alone does not complete durable external backup
or anonymous reviewer access. Deliver this source/doc work as a new unmerged PR.

## 2026-11-10 America/Los_Angeles — Execute a fresh focal study after input recovery

The user explicitly requested rerunning experiments using the repository guide.
Use new external roots, matched model/reference pins, exact archived SDK/JDK/Java
dependencies and the eleven pinned wheels. Record the fresh Python distribution
separately; an unpinned old interpreter binary cannot be claimed identical.
Keep all historical imports, manuscript sources, evidence claims and human
PENDING statuses unchanged. The [new protocol and runbook](../work/focal-rerun-20261110/README.md)
cover E1/E2 primary/replay, paired Android P2 and the six-input P3 core.

This is a known-outcome rerun, not recovered old execution provenance or human
verification. P3 does not recreate the original 30-request search or auxiliary
synset inquiry. Preserve failed setup/analysis attempts and interrupted collectors.
After two chat interruptions, keep completed per-condition records and continue
only missing transport collections, with separate invocation folders and explicit
selection/copy hashes. Do not retry a complete scientific FAIL to obtain a PASS.
Use one software AVD serially; uninstall only this run's test package when changing
to P2's distinct signing key. Keep raw files and locally verified archives outside
Git; local packaging is not external backup or anonymous reviewer delivery.


## 2026-11-11 America/Los_Angeles — Separate current navigation from historical records

The user requested repository cleanup and a PR. Keep README, MEMORY and TODO as
concise current entry points; preserve their full former text at the fixed cleanup
base in Git. The [repository map](REPOSITORY_CLEANUP.md) identifies maintained
code, immutable snapshots, historical reviews and excluded material. Timestamped
names and identical bytes alone are not deletion criteria: older producers and
readers still support the new run, and duplicate imports preserve provenance.

Do not move or deduplicate imported sources, rewrite manuscript/audit pins, change
human PENDING statuses, delete external evidence or rerun experiments as part of
navigation cleanup. The November run remains separate from the October manuscript.
Prioritize a second verified evidence copy, provenance reconciliation and human
review over new experiment expansion. Deliver this cleanup on its own feature
branch/PR based on the still-open #19; no merge is authorized by this request.

The subsequent user instruction, “OK 审查并合并”, authorizes reviewing and squash
integrating #20 and its necessary #18/#19 prerequisites into main. Verify each
reviewed head, sole squash parent and resulting file tree. Synchronize dependent
feature-branch ancestry only after proving main equals the reviewed predecessor
tree, without force pushes. Keep final integration notes in #20; its verified
GitHub merged state closes delivery. Research evidence and human-review limits
remain unchanged by repository integration.
