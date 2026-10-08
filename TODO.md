# Current research TODO

This is the single active checklist. Timestamped TODOs under `sources/` describe
earlier states. Read `MEMORY.md` for evidence boundaries and `AGENTS.md` for the
source-only repository policy.

## Active priorities: short-paper submission convergence

The checkboxes below distinguish completed deliverables from planned work.
Completion of a bounded comparison does not certify novelty or publication readiness.
P0/P1/P2 here are priority levels, separate from the historical experiment and
follow-up names. The same-Android P2 comparison and bounded P3 reference inquiry
remain complete. Stronger execution evidence does not by itself establish novelty
or practical significance.

Both bounded P0 assessments and the local manuscript rewrite are complete.
The selected framing is a controlled empirical study, with E5 supporting the
analysis rather than supplying a new detection method. The documented
reproduction handoff and human-audit entry preparation are complete; external
evidence delivery and actual human verification remain open. The rewrite and
completed agent review were squash-merged in
[PR #9](https://github.com/lcresearch/landmark-metadata/pull/9), commit `ba1b5c5`.
Venue/category selection still determines the submission form.

The user now prefers a short workshop paper. The current
[post-audit draft](work/preaudit-followup-20261008/README.md) uses four-page
IEEE conference formatting provisionally for SQA4AI 2027; a seven-page companion
retains detail. The candidate deadlines are abstract 19 October and paper
23 October 2026, AoE. This is not a selected venue or submission approval.
[Remaining submission work](work/workshop-convergence-20261007/SUBMISSION_READINESS.md)
separates author verification, anonymous persistent evidence access and retained
secondary-claim decisions. The old human-audit entry stays pinned to its old
source; use the new claim crosswalk and manuscript digest.

- [x] **P1 — Review the full PR #10–#14 stack (agent).**
  [Scoped review and integration plan](work/pr10-14-review-20261008/README.md)
  found no unresolved final-stack content blocker. Source checks and all 83
  repository tests pass; local content-preserving squash simulation passes.
  A naive retarget after squash conflicts; #11–#14 need guarded branch/base sync.
- [x] **P1 — Authorize sequential Squash and merge of #10–#14.**
  The user explicitly authorized “ok. squash and merge”.
- [x] **P1 — Squash and verify prerequisites #10–#13.**
  Merged commits are `dec99fac`, `6e318506`, `10450f91`, and `52e6eafc`.
  Each has exactly one parent and the reviewed PR's complete tree. See the
  [integration record](work/pr10-14-integration-20261008/README.md).

**Final integration gate: [PR #14](https://github.com/lcresearch/landmark-metadata/pull/14).**
This terminal PR carries the revised draft, parser follow-up and these status
updates. Its GitHub **MERGED** state completes the five-PR integration; OPEN
means that final step remains in progress. The operation verifies its reviewed
head, single-parent squash and exact tree. Human research verification and
evidence delivery remain separate open tasks below.

- [x] **P1 — Narrow audit-sensitive manuscript claims (agent).** New short/full
  sources remove categorical E2 predeclaration timing, retain the deterministic
  transform and observed results, and distinguish saved-byte pre-audit from
  execution. The new claim map preserves all 16 IDs and PENDING human statuses;
  prior manuscripts and audit targets remain unchanged.
- [x] **P1 — Bounded parser recovery and fresh isolated check (agent).** The
  [follow-up](work/preaudit-followup-20261008/parser/REPORT.md) did not recover the
  old records. Actual Support 0.4.4 JVM probes confirm LF success, VT count
  mismatch and U+2028 success; the unchanged helper matches 22 valid cases and
  abstains on three malformed cases. New raw evidence is outside Git. No Task,
  Android/model inference, whole-checker or all-65 regression was rerun.
- [x] **P1 — Deliver the post-audit revision and parser source through [PR #14](https://github.com/lcresearch/landmark-metadata/pull/14).**
  The feature branch and PR are published; raw evidence/build outputs remain outside Git.
- [x] **P1 — Review [PR #14](https://github.com/lcresearch/landmark-metadata/pull/14) after #13.** Branch
  `paper/preaudit-followup` was reviewed on `audit/agent-preaudit`; authorized
  integration synchronizes it with main before squash. The narrowed chronology
  and separation of new parser evidence from missing history remain intact.

- [x] **P1 — Independent-agent pre-audit before human review (agent).**
  [Completed pre-audit](work/agent-preaudit-20261007/README.md) used five fresh
  review contexts plus a chronology subreview. New saved-byte comparisons and
  disassembly support core E1/E2/P2 and qualified P3; no new inference was run.
  All 13 human item/subitem statuses remain PENDING. Reports identify partial
  secondary coverage, missing later parser raw records and limited E2 timing
  evidence; the frozen manuscript and old audit map are unchanged.
- [ ] **P1 — Resolve pre-audit findings and perform human author verification.**
  Use the [six-part handoff](work/agent-preaudit-20261007/HUMAN_HANDOFF.md).
  E2 wording is now narrowed and parser evidence supplemented separately. Use the
  [new target handoff](work/preaudit-followup-20261008/HUMAN_HANDOFF.md) to assess
  these edits and retained secondary limits. Check key raw records and authority
  links, then record human conclusions against the new manuscript hash. Agent
  agreement and source/hash checks are not a signature.
- [x] **P1 — Review [PR #13](https://github.com/lcresearch/landmark-metadata/pull/13) after #12 and its prerequisites.**
  Previously stacked on `paper/workshop-convergence`, now squash-merged as
  `52e6eafc`. Raw audit outputs remain outside Git; human verification stays pending.

- [x] **P1 — Prepare a short workshop draft and candidate comparison (agent).**
  Added a four-page IEEE short draft including references, a seven-page companion,
  all-16-claim disposition map, official CFP candidates and submission checklist.
  Retained E1/E2/P2 as the core, #770 as antecedent, S/I/D with P separate, and
  E5 as supporting evidence. Explicitly distinguishes focal recovered evidence,
  secondary families outside the package and unrecovered later raw records.
  No new model experiment, author verification, deposit or submission.
- [x] **P1 — Review [PR #12](https://github.com/lcresearch/landmark-metadata/pull/12) after its #10/#11 prerequisites.**
  Previously stacked on `evidence/local-recovery`, now squash-merged as
  `10450f91`. Its chronology wording is superseded by the current #14 revision.
- [ ] **P1 — Make the retained-claim evidence decision before submission.**
  Complete HA01–HA07 for core claims; for Hand, external/static checks and parser
  observations, identify inspectable support or narrow the retained wording.
  Missing later records do not invalidate distinct recovered original evidence;
  old evidence must not be relabeled as the missing run.

- [x] **P0 — Contribution and closest-work comparison (agent).** Completed the
  [bounded comparison](research/20261004-contribution-review/CONTRIBUTION_COMPARISON.md):
  seven full-text comparisons, two explicit source-access limits, fixed official
  implementation paths, and keep/narrow/drop recommendations. The result supports
  bounded empirical framing, with E5 as a supporting diagnostic; it does not
  certify novelty or significance. The claim–evidence–prior-work–remaining-difference
  table records source scope, inaccessible material, existing constraints and
  unresolved overlap. This closes the agreed bounded comparison, not an exhaustive
  novelty search. An E5 method claim still requires capability beyond strong baselines.
- [x] **P0 — Research significance assessment (agent).** Completed the
  [bounded assessment](research/20261004-significance-review/SIGNIFICANCE_ASSESSMENT.md):
  selected old E1/E2/P2/P3 records read back, six official workflow documents,
  and eight fixed public-report queries (30 unique issues triaged, seven inspected
  with comments). Supports concrete integration-test and diagnostic relevance;
  no measured prevalence, operational benefit or new natural-case reproduction.
  Support #770 is both a practical antecedent and a limit on first-discovery claims.
  Ordinary full-package hashes, Task initialization, actual getter tests and
  reference-map comparisons remain strong defenses. Parser counterexamples concern
  our historical checker/baseline. This closes the assessment, not an importance
  or publication-readiness certification; no new model experiment or human audit.
- [x] **P1 — Determine the framing and rewrite the main argument (agent).**
  The [new working draft](work/paper-rewrite-20261004/manuscript/paper.tex) follows: contract
  definitions → E1 actual getter failure → E2 successful but changed association
  → same-Android enforcement-stage comparison → Hand reference semantics and
  consumer boundary → external checks and preflight limits. The
  [claim–evidence table](work/paper-rewrite-20261004/CLAIM_EVIDENCE.md) records
  source identities and verification limits. The draft incorporates both P0
  assessments, #770 as motivation and antecedent, parser counterexamples, S/I/D
  separation and P as preservation. E5 stays auxiliary and Hand retains its
  one-image boundary. Old drafts are unchanged. Agent review and an eight-page
  generic reading build are complete; no model experiment or human audit was
  rerun, and venue-length compliance is not established.
- [x] **P1 — Deliver the rewrite through a new PR.**
  [PR #9](https://github.com/lcresearch/landmark-metadata/pull/9) publishes
  `paper/executable-contract-rewrite`. PR #8's merge was verified at remote main
  `ccf1a98eca39d49f06e54f4c3def675a90c10540`, then incorporated without changing
  manuscript bytes. Git direct push still returned HTTP 401; the authenticated
  GitHub API published the feature branch with matching tree/commit hashes.
- [x] **P1 — Review the rewritten draft in PR #9.** Separate content and
  repository/provenance reviews found no blocking issue. All 48 ledger source
  hashes, 354 imported files and manuscript identities match; all 40 repository
  regression tests pass. The user authorized Squash and merge; merge only the
  final verified head. PR review does not complete human research audit.
- [x] **P1 — Reproduction handoff (agent).** Added the
  [reproduction entry](docs/reproduction/README.md), input/toolchain inventories,
  exact source and historical execution commands, expected outcomes and missing
  material. Rehashed selected currently available original inputs/dependencies;
  exercised source-copy helpers and the finite old-record reader in new external
  directories. Full reconstructed-record readback remains blocked by absent
  `/workspace/repro-*` inputs. No installation, build, emulator or inference was
  rerun. This completes the documented handoff and separate deposit plan, not a
  portable archived or fresh-machine reproduction.
- [x] **P1 — Recover and verify a selected local evidence package (agent).**
  [Local recovery](work/evidence-recovery-20261005/README.md) preserves 2,749
  original E1/E2, build-audit and P2/P3 files outside Git with matching historical
  identities. The archive's complete inventory was checked; saved-record checks
  cover 26 executed APKs, 14 separate initial builds and 34 complete run records.
  Later reconstruction material remains [unrecovered](work/evidence-recovery-20261005/MISSING.md).
  This completes the user's selected local-package scope, not durable delivery,
  a new model run or human verification.
- [ ] **P1 — Deliver and validate a durable external evidence package.** Follow the
  [deposit plan](docs/reproduction/DEPOSIT_PLAN.md): choose destination/access,
  recover missing inputs and configuration, preserve independently pinned
  manifests, and verify the selected build/run in a fresh workspace. Keep binary
  evidence outside Git. The selected local package is ready, but later `repro-*`
  records and the pinned E5 catalog remain unrecovered. Local saved-byte checks
  do not complete persistent delivery or a fresh-workspace build/run.
- [x] **P1 — Prepare the human audit entry (agent).** The
  [entry](docs/human-audit/README.md), [inspection checklist](docs/human-audit/CHECKLIST.md),
  [machine-readable map](docs/human-audit/audit-map.json) and
  [unsigned review template](docs/human-audit/REVIEW_RECORD_TEMPLATE.md) bind ten
  audit items to all 16 current ledger claims/subclaims. They identify exact
  source/provenance routes, required external evidence and earlier agent scope.
  Historical checklists remain unchanged; no external evidence or model run was
  newly checked, and every human status remains PENDING.
- [ ] **P1 — Complete the actual human audit (human).** Use the prepared entry;
  record reviewer identity/role, date, exact artifact identities, scope, method,
  observations and per-item conclusions. Missing raw prerequisites stay blocked
  rather than inheriting an agent PASS. Checklist preparation and agent reviews
  do not close this item. Distinguish author verification, independent human
  audit and independent human reproduction.
- [ ] **P2 — Venue selection and formatting (author decision; agent support).**
  Choose a venue and paper category consistent with the P0 assessment and revised
  contribution. Completion means the selected template has been rendered and
  checked for length, anonymization, AI-assistance disclosure and reproduction
  requirements. The new four-page IEEE draft establishes a provisional rendered
  length, not final venue selection or complete submission compliance.

Do not expand the model collection, add similar mutants or build a general
checker by default. Additional experiments need a specific unresolved question
that can change the core claim or contribution decision.

## Completed

- [x] Close the remaining maintained readback gaps: require the separately
  pinned E5 fixture set and validate exact Task input records, bytes/hashes,
  statuses and category counts before counting success; add negative and
  reordered-positive regressions without modifying historical evidence.
- [x] Close the PR #1 claim-reader completeness gap in a new maintained source
  area; require exact Hand/Task/Android identities, preserve exported audit
  provenance, and pass all 29 repository regression tests.

- [x] Repair PR #1 evidence completeness/identity checks and reconstruction I/O;
  add eleven synthetic regressions. Full fixture reruns still require excluded
  assets and a separately frozen 65-artifact digest manifest.

- [x] E1: execute the actual generated EfficientNet Android getter; reach the
  label-deletion exception after successful loading and inference.
- [x] E2: execute the deterministic label permutation; verify tested raw/score
  equality, changed exposed association, and restoration. Independent support
  for historical predeclaration timing remains limited; current wording is narrowed.
- [x] Audit core preservation and source/bytecode relationships using separate
  checking scripts; rebuild in new output directories and a new AVD with the
  existing pinned toolchain. This is not independent human reproduction.
- [x] Compare official reading/population, the matched simple decoder baseline,
  E5 and Task initialization on five core conditions. E5 adds no rejection in
  this set; keep it as a supporting diagnostic tool.
- [x] Review four specified related works in full and revise the manuscript;
  disclose limited E5 parsing, audit scope and cross-platform E3 limitations.
- [x] Prepare source-only repository: code, manuscript source, protocols and
  concise project notes; remove stale HTML TODO and PDF text-extract entry points.
- [x] Follow up on repository review: add historical README availability notes
  and an English audit summary; preserve imported snapshots byte-for-byte.
- [x] Extend the source check to current Markdown and historical source READMEs,
  cross-check the MEMORY/import/source digest and add nine regression tests.
- [x] Create a separate editorial manuscript working copy: consistent E5 name,
  explicit E4 component flow, label-payload restoration boundaries and disclosed
  abstract-only background citations, applied to the completed P2/P3 manuscript.
  Preserve all 17 bibliography entries and the qualified reference findings.

## Completed follow-up: P2 — same-Android consumer comparison

- [x] Declare the comparison plan and dependency versions before execution.
- [x] Run generated wrapper and Android Task ImageClassifier on the same
  emulator/API/ABI with identical model bytes and inputs. Reuse original,
  description control, deletion, permutation and restoration conditions.
- [x] Record load, initialization, input preparation, inference and public
  output/decoding stages, exact diagnostics and stages not reached.
- [x] Explain checks using the actual implementations; retain remaining runtime
  and integration differences. Do not change versions to obtain an expected result.
- [x] Update manuscript: on the same Android API-30 x86_64 AVD, Task rejects
  deletion during construction; the generated wrapper rejects at its getter
  after successful process. Task classify is atomic; different native
  integrations remain. Separate scripts verified all ten configurations.

## Completed follow-up: P3 — qualified display-order reference

- [x] Independent class-order reference: declare publisher/export/training
  source scope, connect the reference to the exact artifact, compare the full
  mapping and handle index offsets, background classes and duplicate names.
- [x] Establish the narrower publisher-prescribed display-order chain: the
  graph/weight/output-equivalent TFHub fp32/2 artifact links to classification/1,
  whose card prescribes the external labels and background offset. Original and
  restoration match 1000 positions; permutation disagrees at 999.
- [x] Record the uncompleted part: stable class-ID lineage remains ABSTAIN.
  Duplicate display names are not unique IDs. End the bounded search; do not
  describe display-order disagreement as image prediction error or accuracy loss.
- [x] Preserve historical E5 abstentions and complete separate automated
  reference-chain and raw-runtime-record audits. Human audit remains pending.

## Optional, bounded follow-up — not required to finish this draft

- [x] Complete the [bounded public-report inquiry](research/20261004-significance-review/PUBLIC_REPORTS.md)
  under its declared query and inspection budget. Seven reports inspected,
  including negative/configuration explanations; zero artifact-reproduced natural
  cases. This is contextual evidence, not a natural-defect corpus.
- [ ] Natural-artifact reproduction only if a specific unresolved question or
  selected venue warrants it. Declare exact candidates, inputs and stopping
  conditions before acquisition/execution; keep it separate from the completed
  report review. Count recovered and verified artifacts separately from reports;
  injected failures are never natural defects. Zero findings is acceptable.

## Conditional method work — not the current default

- [ ] Only pursue consumer-path contract analysis if it demonstrates useful
  capability beyond a strong baseline on previously uninspected supported
  structures. Distinguish static judgments, missing runtime state and missing
  semantic evidence. No runtime-obligation generator has been established here.
- [ ] Stop the extension if it adds no demonstrated capability; finish the
  bounded empirical study instead of growing a nominal contribution.

## Ongoing repository upkeep

- Save project source changes, necessary manuscript/protocol documents, TODO
  updates and concise decision/handoff notes here after meaningful work.
- Commit on a feature branch, push that branch and open a PR for user review.
  Verify the remote branch and PR. Never update `main`/the default branch directly
  or merge/enable auto-merge without an explicit user instruction. An authorized
  "merge" means **Squash and merge** unless the user explicitly says otherwise. Report access
  blockers; do not promise background synchronization.
- Keep SDKs, emulators, dependencies, models, generated wrapper outputs, raw
  results, logs, rendered documents, archives and compiled products outside Git.
- Preserve sealed evidence and historical source snapshots. Do not repeat the
  completed core audits and baseline comparisons without a new change or
  unresolved contradiction, and do not expand random
  model collections merely to increase counts.

## Fresh reproduction audit

- [x] Reconstruct official inputs and pinned prerequisites in the new cloud
  machine; rerun base corpus, E1/E2 primary/replay, Linux Task, Hand and E4/E5.
  Independently check complete raw records, artifact hashes and preservation.
- [x] Demonstrate Java/Python label-reader disagreement with real decoder-library
  counterexamples; add maintained parser/checker/baseline corrections and verify
  all 65 original fixture decisions remain unchanged.
- [x] Exercise missing-evidence and misleading-report branches separately;
  preserve negative results and add strict checks for fresh reconstruction.

## Corrections from the fresh audit

- [x] Revise the manuscript's library-equivalent label-count wording,
  disclose VT/U+2028 counterexamples and distinguish the corrected checker from
  the historical 65-fixture evaluation. Preserve the original draft and update
  the current source digest index.
- [ ] Replace remaining historical report templates if they are promoted to
  reusable tools: required evidence must gate prose, status and exit code;
  empty evidence and companion failures must fail explicitly.
- [x] Repeat the bounded literature checks using recovered, digest-verified
  full texts where available, and extend the declared comparison to mutation
  and differential testing. The [new source indexes](research/20261004-contribution-review/README.md)
  distinguish five recovered PDFs, two new PDFs, and unresolved Stalnaker/Meyer
  full-text access. The earlier blocked retrieval attempts remain historical.
- [ ] Review/save the cloud configuration draft and publish the retained
  environment; independently test restoration in a future fresh task before
  calling it verified snapshot restoration.
