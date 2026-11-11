# Current research TODO

Updated 11 November 2026. This is the single active checklist; dated plans and
completed checklists are historical. Start with the [current state](MEMORY.md)
and follow the [repository policy](AGENTS.md).

## Next actions, in order

- [ ] **Retain a second verified copy of the new evidence.** The November
  [archive receipt](work/focal-rerun-20261110/delivery-record.json) identifies a
  verified local 3.32 GB package, not a remote backup. Agree on an external
  destination/access policy before upload, then verify the destination bytes.
  Keep evidence out of Git, Releases and LFS. Anonymous reviewer access is a
  separate delivery requirement; do not treat a private backup as its completion.
- [x] **Reconcile the short manuscript with the new execution history.** The
  [November revision](work/acceptance-paper-revision-20261111/REVISION_NOTES.md) and
  [claim map](work/acceptance-paper-revision-20261111/CLAIM_EVIDENCE.md) disclose the lost
  October material, known-outcome rerun, two interruptions/continuations, reader
  correction and P3 core-only scope. Current-pointer pins bind all new artifacts;
  historical manuscripts, old pins and PENDING audit targets remain preserved.
- [x] **Focus the paper on acceptance decisions and screen existing reports.**
  [PR #23](https://github.com/lcresearch/landmark-metadata/pull/23) contains the
  revised short paper and [two-candidate shortlist](work/case-screening-20261111/SHORTLIST.md).
  Seven reports/69 comments were re-read; linked material was checked without
  full model acquisition or execution. #770 and #319 remain conditional candidates.
- [ ] **Execute the authorized #770 reconstruction using the fixed shortlist.**
  Acquire full model identities and freeze one consumer configuration before
  execution. Apply the shortlist’s stop rules and preserve unsupported-path,
  asset-selection and historical-identity limits. Screening alone adds no
  experimental result or natural-defect count.
- [ ] **Resolve auxiliary evidence before submitting it.** The new short paper
  labels E5's negative result and Hand/static/parser context as historical. If
  retaining their detailed claims in a submitted companion, supply inspectable
  support or narrow/remove the submitted wording. The October companion remains
  unchanged and is not a newly verified November report.
- [ ] **Complete human author verification against the revised artifacts.**
  Carry the [six author questions](work/acceptance-paper-revision-20261111/ARTIFACT_HANDOFF.md)
  to the new source/evidence identities. Record reviewer, date, scope, observations
  and conclusions. Automated checks and agent reviews do not close this task;
  author verification, independent human audit and independent reproduction differ.
- [ ] **Prepare persistent reviewer access for the retained claims.** Adapt the
  [deposit plan](docs/reproduction/DEPOSIT_PLAN.md) to the new run and chosen
  external destination. Verify access and a selected build/run from the delivered
  package in a fresh workspace; local archive readback is not that validation.
- [ ] **Select a venue/category, then check submission requirements.** The
  four-page source is provisional. Recheck the selected venue's current template,
  length, anonymity, disclosure and artifact requirements before submission.
  Old venue suggestions/deadlines are historical; no venue or submission is approved.

PR #18–#20 are squash-merged; main reached `e9da459…`. The November manuscript
evidence revision was merged in [PR #22](https://github.com/lcresearch/landmark-metadata/pull/22).
The acceptance-focused editorial follow-up and bounded candidate screening use a
new [PR #23](https://github.com/lcresearch/landmark-metadata/pull/23); the user has now authorized review and squash merge, followed by bounded #770 execution.
Repository integration does not complete the remaining research/human tasks.

## Code-layout integration

[Cleanup PR #21](https://github.com/lcresearch/landmark-metadata/pull/21) and paper
PR #22 are squash-merged. The [compatibility review](docs/PR21_REVIEW.md) fixed
moved source paths and preserved paper/index pins. Their resulting main commit
is `8005274e9eccbea30fb3189779f03e8d693b3720`.

## Code-layout maintenance

The current entry is [experiment](experiment/README.md); the old source tree is
[archived and restorable](archive/README.md). Use the explicit staging map when
adding runtime dependencies. Before the next authorized inference run, use an
absent external root and record the new source identities; this cleanup only
validates source staging and regressions, not new scientific execution.

The maintained initialization/evidence-index refactor from PR #24 is merged at
`c82253d`; its source changes and regression coverage are preserved.

## Completed foundations

| Completed scope | Record and limits |
|---|---|
| Bounded contribution and significance assessments | [Contribution comparison](research/20261004-contribution-review/CONTRIBUTION_COMPARISON.md) and [significance assessment](research/20261004-significance-review/SIGNIFICANCE_ASSESSMENT.md); support a controlled empirical case, not an exhaustive novelty claim |
| Maintained evidence readers and integrity guards | [October repairs](work/review-fixes-20261021/README.md) and [November binding repairs](work/review-fixes-20261110/README.md); synthetic regressions do not authenticate missing old executions |
| Recovery of pinned focal inputs | [Recovery record](work/input-recovery-20261110/README.md); matching model/reference/input bytes, not recovered execution logs |
| New focal execution and local packaging | [Results](work/focal-rerun-20261110/RESULTS.md) and [receipt](work/focal-rerun-20261110/delivery-record.json); E1/E2/P2 audited, P3 core complete, 2,120 archive members verified, human review and external delivery still open |
| Current short paper and evidence map | [November revision](work/acceptance-paper-revision-20261111/REVISION_NOTES.md); new focal results incorporated with exact evidence identities, historical companion preserved, author questions unsigned |

## Deferred unless new evidence changes the decision

- Search for old raw records again only if a specific surviving workspace, backup
  or archive lead appears. The bounded local search found none; this is not proof
  that every backup is gone. Never reconstruct old execution records from summaries.
- Add a natural-artifact case only for a stated unresolved research question with
  fixed candidates and stopping rules. Existing public reports yielded zero
  artifact-reproduced natural cases; injected interventions are not natural defects.
- Pursue a method extension only if it adds demonstrated capability over strong
  baselines on previously uninspected supported structures. More similar mutants
  or a larger model count is not the current priority.
- Modernize historical report templates only if promoting them into maintained
  tools; keep the imported originals unchanged.

The [repository map](docs/REPOSITORY_CLEANUP.md) identifies maintained and historical
areas. The former 382-line checklist is preserved in
[Git at the cleanup base](https://github.com/lcresearch/landmark-metadata/blob/a94b98ffdce5814b9db717ae8d4db4fd8a80f3f2/TODO.md).
It is context, not a second active plan.
