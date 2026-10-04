# Current research TODO

This is the single active checklist. Timestamped TODOs under `sources/` describe
earlier states. Read `MEMORY.md` for evidence boundaries and `AGENTS.md` for the
source-only repository policy.

## Active priorities: assess the contribution before the full rewrite

The checkboxes below distinguish completed deliverables from planned work.
Completion of a bounded comparison does not certify novelty or publication readiness.
P0/P1/P2 here are priority levels, separate from the historical experiment and
follow-up names. The same-Android P2 comparison and bounded P3 reference inquiry
remain complete. Stronger execution evidence does not by itself establish novelty
or practical significance.

Complete the two P0 assessments before choosing the contribution and doing the
full manuscript rewrite. Reproduction handoff and human-audit preparation can
proceed in parallel. Record whether the evidence supports a bounded empirical
study, a method contribution, or a shorter case/experience report; do not assume
the strongest framing in advance.

- [x] **P0 — Contribution and closest-work comparison (agent).** Completed the
  [bounded comparison](research/20261004-contribution-review/CONTRIBUTION_COMPARISON.md):
  seven full-text comparisons, two explicit source-access limits, fixed official
  implementation paths, and keep/narrow/drop recommendations. The result supports
  bounded empirical framing, with E5 as a supporting diagnostic; it does not
  certify novelty or significance. The claim–evidence–prior-work–remaining-difference
  table records source scope, inaccessible material, existing constraints and
  unresolved overlap. This closes the agreed bounded comparison, not an exhaustive
  novelty search. An E5 method claim still requires capability beyond strong baselines.
- [ ] **P0 — Research significance assessment (agent).** Identify the concrete
  usage scenarios, limitations of existing checks, and engineering consequences
  relevant to the observed mechanism. Produce an evidence table separating
  measured outcomes, reproducible public cases, issue reports, and hypotheses.
  Evaluate the Java/Python parsing counterexamples as defects in the studied
  checks, without presenting them as natural defects in official deployment
  tools. Completion means an explicit account of what practical relevance is
  supported and what remains unknown. Any natural-case search must follow the
  bounded optional protocol below; zero findings is acceptable.
- [ ] **P1 — Determine the framing and rewrite the main argument (agent;
  depends on P0).** Organize the current working manuscript as: contract
  definitions → E1 actual getter failure → E2 successful but changed association
  → same-Android enforcement-stage comparison → Hand reference semantics and
  consumer boundary → external checks and preflight limits. Include the parser
  counterexamples at their demonstrated scope; keep S/I/D separate and P as
  intervention-preservation evidence. Completion means a coherent revised draft
  with claims traceable to evidence and the P0 positioning decision. Compress
  internal research history and Hand provenance into supporting material while
  retaining the one-image boundary. Preserve historical manuscript snapshots.
- [ ] **P1 — Reproduction handoff (agent; can run in parallel).** Document the
  required inputs, exact dependencies, acquisition locations, hashes, commands,
  expected outcomes and missing materials in a usable entry point. Distinguish
  documented commands from commands freshly verified against available inputs.
  Completion means an explicit prerequisite and availability inventory, with a
  separate plan for an independently usable evidence deposit. The repository
  remains source-only; an inventory is not a complete archived reproduction.
- [ ] **P1 — Actual human audit (agent preparation; human verification).**
  Prepare a checklist and evidence index for the generated getter call, packaged
  model identity, preservation comparisons, exact exceptions and P3 reference
  chain. Completion requires an actual human's reviewer identity, date, scope,
  method and conclusions; checklist preparation or an agent rerun does not close
  this item. Distinguish author verification from independent reproduction.
- [ ] **P2 — Venue selection and formatting (author decision; agent support).**
  Choose a venue and paper category consistent with the P0 assessment and revised
  contribution. Completion means the selected template has been rendered and
  checked for length, anonymization, AI-assistance disclosure and reproduction
  requirements. The existing generic reading draft does not establish venue fit.

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
- [x] E2: predeclare label permutation; verify tested raw/score equality, changed
  exposed association, and restoration.
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

- [ ] Natural cases only if the significance assessment or selected venue makes
  them necessary: predefine mechanisms, sources and stopping conditions before
  looking. Count recovered and verified
  artifacts separately from issue reports; injected failures are never natural
  defects. Zero findings is acceptable. This round did not search for natural cases.

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
  or merge/enable auto-merge without an explicit user instruction. Report access
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
