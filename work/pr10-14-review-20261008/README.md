# Review and integration plan for PRs 10–14

**Scoped review passes for the final stack; no unresolved content blocker.**
This is source/provenance/claim review and local Git integration simulation,
not human research verification or new model execution. All five PRs remain open.
The selected-text request did not explicitly authorize merging; no remote base,
default branch, auto-merge setting or scientific evidence has been changed.

## Reviewed versions

Main at review: `ba1b5c5a0e5df44c28e7232b044bc6741d29bb47`.

| PR | Head reviewed | Existing base | Disposition |
|---|---|---|---|
| #10 human audit entry | `72ff55041be97ba04e377fa9c4a18b948b8dc106` | main | Scoped pass; all 16 claim routes, pending/unsigned human records and original target identities agree. |
| #11 local recovery | `e23d62e3af56376eb0f1946dd30eb7cba870fa04` | docs/human-audit-entry | Scoped pass; recovery selection, helper logic and recorded identities/limits agree. |
| #12 workshop draft | `24f660cf093c3e52efc0cde0c39e7aea1df48053` | evidence/local-recovery | Accept as the preserved intermediate draft in this stack; its categorical E2 chronology is corrected by #14. |
| #13 agent pre-audit | `57ff5585039e7f63de54a67981d5d98cb9ba84e8` | paper/workshop-convergence | Scoped pass; audit/report/source identities and preserved targets agree. |
| #14 post-audit revision | `4ac89999402b97d404e68a72d72348f73705ce06` | audit/agent-preaudit | Scoped pass; current wording separates deterministic observations, historical timing limits and fresh isolated parser evidence. |

GitHub reported all five mergeable against their existing bases and no status
checks. #10–#12 had GitHub review approvals; #13–#14 had no recorded review
decision. Those repository review states are not human research audit signatures.

## Fresh checks and reviewer scope

Three fresh-context review groups inspected handoff/recovery, manuscript/claim
boundaries, and audit/probe code. Delegated subchecks shared the same environment
and evidence; they are not independent human replication.

- Source check passes with all 354 imported files unchanged and the 12 existing
  warnings retained. The warnings identify historical locators/excluded evidence.
- All **83 repository regression tests pass**. These are repository tests,
  not new Android/model or isolated-JVM experiments.
- #10's ten upstream pins, 48 claim-ledger sources, all 16 routes and pending
  human fields agree. #11's 14 external report/index pins, three historical
  manifest anchors, delivered helpers and 30 small delivery entries agree.
  That review did not reread the entire recovery archive or rerun recovery.
- #13's 47 indexed identities, 19 copied source/report records, 111 audit-manifest
  entries and 2,749 focal package identities agree. Saved findings/denominators
  remain bounded readback, not independent authentication of old executions.
- #14's probe/build review checked the exact 151 probe files, 35 recorded
  subprocess calls, fixed classpaths, transformations and scores, all 22 valid
  helper cases and three abstentions, and the 50-file document-build manifest.
  Current manuscript/companion/crosswalk pins, all 16 claim IDs and 13 human
  item/subitem statuses agree; every human status stays PENDING.
- S/I/D remain distinct; P is preservation. #770 remains an antecedent. E5
  remains auxiliary, with no additional rejection on the five core conditions.
  The new JVM run does not recover old Task/parser/catalog evidence or validate
  the whole checker/all 65 reconstructed fixtures.

The new review notes, plan and simulator do not change the scientific payload
reviewed at #14's head above. Their delivery commit requires the same final
source/navigation checks and a fresh head/tree check before any actual merge.

## Integration finding and tested resolution

Although all PRs are clean against their current stacked bases, a naive
retarget-to-main sequence after squash is not clean. Local simulation of #10's
squash followed by #11 produces README.md and TODO.md conflicts. Squashing
changes ancestry, so the old base commits are not ancestors of the new main.

The [local-only simulator](simulate_stack.py) verifies a safe sequential plan:

1. Squash #10 into main after rechecking its exact reviewed head.
2. Before each #11–#14, require the actual main tree to equal the reviewed
   predecessor's entire tree. If it differs, stop and review the intervening
   changes; never select the child tree blindly or discard unrelated main work.
3. Where needed, append a two-parent base-synchronization commit on that PR's
   feature branch: original reviewed head plus the new main, retaining the exact
   reviewed child tree. This is a branch synchronization, not the final PR merge.
   It is a normal fast-forward push of the feature branch, with no force push.
4. Retarget that PR to main, recheck its new head and expected incremental tree,
   then **Squash and merge**. Verify the resulting single-parent main commit and
   exact expected tree before continuing. Keep base branches until the chain is
   complete so automatic branch deletion does not hide an unresolved dependency.

The resolved simulation requires synchronization for #11, #12, #13 and #14 and
passes all five expected-tree comparisons. It creates only local dangling Git
objects; it does not update any branch/remote ref or pull request. Actual GitHub
operations still require explicit merge authorization and fresh identity checks.

## Nonblocking reuse-hardening note

The executed `parser/verify_probe.py` validates manifest bytes and reported
case counts, but does not independently enforce all expected unique case names,
input payloads and trusted pin anchors. The separate reviewer checked those
properties against the current fixed artifacts and original sources, with no
mismatch. Preserve this executed snapshot. If promoted into a general verifier,
add independently fixed case/input/pin checks and corresponding negative tests;
the current result is not a general evidence-authentication claim.

## Retained open research tasks

Human verification, anonymous durable evidence delivery, secondary subchecks,
missing historical parser/Task/catalog material and author/venue/submission
decisions remain pending. They are disclosed research/publication limitations,
not reasons to misstate these source/document PRs as technically unmergeable.
Merging source does not close them.

Raw review output is outside Git at
`/workspace/pr10-14-review-20261008T061937Z/`: frozen PR identities, source check,
regression output, initial conflict and resolved simulation records. No new
model, Java decoder or document build was run during this stack review.
