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
- [ ] **Reconcile the manuscript with the new execution history.** Make a new
  editorial working copy and update its claim ledger, handoff and current-pointer
  pins together. Disclose the unavailable October raw evidence, known-outcome
  November rerun, interrupted/resumed collection, reader correction and bounded
  P3 core. Preserve historical manuscripts, pins and PENDING audit records.
- [ ] **Decide which auxiliary claims still have inspectable support.** For
  Hand/E4/E5/parser claims retained in the companion, identify available evidence
  or narrow/remove the new draft's wording. The focal rerun did not recreate
  those histories or the full P3 search/synset inquiry. Keep E5's negative result
  and missing-record limitations visible; do not inherit old PASS summaries.
- [ ] **Complete human author verification against the revised artifacts.**
  Carry the [six author questions](work/label-resource-revision-20261020/ARTIFACT_HANDOFF.md)
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

PR #18 and PR #19 were reviewed and squash-integrated on 11 November. The user's
follow-up authorizes review and squash merge of [PR #20](https://github.com/lcresearch/landmark-metadata/pull/20);
its verified GitHub merged state is the integration completion record. Research
and human-verification tasks above remain open after repository integration.

## Completed foundations

| Completed scope | Record and limits |
|---|---|
| Bounded contribution and significance assessments | [Contribution comparison](research/20261004-contribution-review/CONTRIBUTION_COMPARISON.md) and [significance assessment](research/20261004-significance-review/SIGNIFICANCE_ASSESSMENT.md); support a controlled empirical case, not an exhaustive novelty claim |
| Maintained evidence readers and integrity guards | [October repairs](work/review-fixes-20261021/README.md) and [November binding repairs](work/review-fixes-20261110/README.md); synthetic regressions do not authenticate missing old executions |
| Recovery of pinned focal inputs | [Recovery record](work/input-recovery-20261110/README.md); matching model/reference/input bytes, not recovered execution logs |
| New focal execution and local packaging | [Results](work/focal-rerun-20261110/RESULTS.md) and [receipt](work/focal-rerun-20261110/delivery-record.json); E1/E2/P2 audited, P3 core complete, 2,120 archive members verified, human review and external delivery still open |
| Current editorial source and audit preparation | [October revision](work/label-resource-revision-20261020/REVISION_NOTES.md); new evidence has not yet been incorporated and author questions remain unsigned |

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
