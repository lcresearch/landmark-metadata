# Repository map and cleanup decisions

Reviewed 11 November 2026 from commit
`a94b98ffdce5814b9db717ae8d4db4fd8a80f3f2` (PR #19's head).
This is the retention/navigation guide; [TODO](../TODO.md) is the active plan.
The map now includes the subsequent November short-paper revision.

## What this cleanup changes

The checkout contained 573 tracked files totaling 4,014,038 bytes, with no
untracked or ignored build/cache files reported by Git. All 54 byte-identical
file groups were within `sources/` or the imported P2/P3 snapshot. They retain
experiment-specific provenance, so deduplicating them would damage the preserved
import layout. No tracked source file or external evidence is deleted or moved.

The clutter was in current entry points: README mixed active and historical
links; MEMORY (561 lines) and TODO (382 lines) accumulated completed work and
superseded instructions. This cleanup replaces those entry points with current
state, a single actionable checklist and the map below. It removes stale
root-level instructions such as preparing already completed work and describing
all new execution as still pending. It also makes explicit that the October
manuscript has not yet incorporated the November rerun.

Full pre-cleanup text is preserved in Git, without adding duplicate archive docs:
[README](https://github.com/lcresearch/landmark-metadata/blob/a94b98ffdce5814b9db717ae8d4db4fd8a80f3f2/README.md),
[MEMORY](https://github.com/lcresearch/landmark-metadata/blob/a94b98ffdce5814b9db717ae8d4db4fd8a80f3f2/MEMORY.md),
[TODO](https://github.com/lcresearch/landmark-metadata/blob/a94b98ffdce5814b9db717ae8d4db4fd8a80f3f2/TODO.md).
For an offline copy from local Git, for example:

```sh
git show a94b98ffdce5814b9db717ae8d4db4fd8a80f3f2:MEMORY.md
```

## Keep and use now

A timestamped directory name does not by itself make code obsolete. In particular,
the new run still uses maintained readers and preserved producers from older areas.

| Area | Why it is needed / current entry |
|---|---|
| [Current short-paper revision](../work/rerun-paper-revision-20261111) | November short TeX, claim map, exact evidence index, readback helpers, handoff and build validation; old full companion remains historical |
| [New focal run](../work/focal-rerun-20261110) | Actual runbook/protocol, setup, collection continuation, P3 core, packaging code, results and archive receipt; start here for a new focal run |
| [Input recovery](../work/input-recovery-20261110) | Pinned model/input reconstruction and reference retrieval; supplies prerequisites for the new run |
| [Repository scripts](../scripts) and [tests](../tests) | Source/import/manuscript integrity, preserved import selection, maintained Android initialization and regression coverage |
| [Maintained observation reader](../work/observation-review-20261004) | Strict Hand/Task/Android evidence readback; historical exported reader stays unchanged |
| [Maintained P2/parser readers](../work/review-fixes-20261021) and [November repair record](../work/review-fixes-20261110) | Actual-file attribution, completeness and format checks; use these maintained tools instead of assuming old readers enforce current checks |
| [Evidence recovery tools](../work/evidence-recovery-20261005) | Archive verification, safe staging and focal coverage checks remain useful; the October package/results and missing list are historical, and are not the new run's receipt |
| [Reproduction guide and inventories](reproduction/README.md) | Input/toolchain/command pins and historical prerequisites; use the new runbook for the November sequence |
| [Source import index](SOURCE_IMPORT.json), [P2/P3 index](SOURCE_P2P3.json), [manuscript index](CURRENT_MANUSCRIPT.json) | Guard 354 imported files and current/historical manuscript and evidence-index identities; never delete or refresh pins merely to make a cleanup pass |
| [Policy](../AGENTS.md), [decisions](DECISIONS.md), [memory](../MEMORY.md), [TODO](../TODO.md) | Authoritative continuation entry points; keep current summaries short and dated detail in its work record |

## Keep for history, provenance or qualified secondary use

These areas are not additional independent models, active checklists or proof
that the excluded raw evidence is available. Do not run old finalization scripts
over retained evidence or rewrite historical outcomes.

| Area | Retention decision |
|---|---|
| [October manuscript and companion](../work/label-resource-revision-20261020) | Preserved predecessor sources, ledger and handoff; the full companion has not been rewritten or newly verified for November |
| [All imported sources](../sources) | Byte-preserved snapshots. Includes initial Hand, corpus/checker, E1–E7 harnesses/protocols, audits and old papers. [Fresh reconstruction snapshot](../sources/repro-audit-20261004) also supplies pinned prerequisite and experiment code used by the new run |
| [P2/P3 import](../research/20261004-p2-p3) | Protected same-Android/reference source and manuscript parent; the new run reuses these producers through recorded external working copies |
| [Contribution review](../research/20261004-contribution-review) and [significance review](../research/20261004-significance-review) | Bounded prior-work and public-report assessments explain the narrow framing and negative findings; they are not a current venue/deadline survey |
| [Earlier editorial follow-up](../work/review-followup-20261004), [full rewrite](../work/paper-rewrite-20261004), [workshop draft](../work/workshop-convergence-20261007) | Historical manuscripts and claim lineage. The full rewrite's [claim source index](../work/paper-rewrite-20261004/claim-sources.json) remains a provenance dependency |
| [Agent pre-audit](../work/agent-preaudit-20261007) and [post-audit/parser follow-up](../work/preaudit-followup-20261008) | Keep audit chronology, narrowed claims, isolated parser source and limitations; agent work is not human verification |
| [Human-audit preparation](human-audit/README.md) | Frozen older target and unsigned template; use the current manuscript handoff to prepare a newly bound review, never retroactively mark this target verified |
| [PR stack review](../work/pr10-14-review-20261008) and [integration](../work/pr10-14-integration-20261008) | Completed review/merge provenance; no active merge instruction |
| [Historical README notes](HISTORICAL_README_NOTES.md), [audit summary](AUDIT_SUMMARY_EN.md), [review follow-up](REVIEW_FOLLOWUP.md), [observation repair](OBSERVATION_REPAIR.md) | Dated explanations of snapshot limits and earlier repairs; subordinate to current state and maintained tool entry points |

## Do not keep here / do not expand by default

| Material or work | Decision |
|---|---|
| SDKs, dependency installations, emulator state, model assets, builds, logs, raw tensors/results, rendered papers/figures, archives and credentials | Stay outside Git, Releases and LFS under [policy](../AGENTS.md). This cleanup found no disposable generated files in the checkout and does not delete external files |
| Extra root TODOs, PDF text extracts or copies of the same continuation log | Unnecessary active entry points. Use the current root documents plus fixed Git history; keep authentic historical copies inside protected snapshots |
| More similar mutants, broad model collection or a nominal new checker method | Deferred. Resolve evidence retention, manuscript provenance and human verification first; use [TODO](../TODO.md) for the conditional research criteria |
| The new evidence archive and raw attempts outside Git | Retain, including failures and interruptions. Arrange a second verified copy before considering any later storage cleanup; deletion is outside this task |

## Cleanup validation

The source checker passes: 354 imports, the import-backed memory hash and seven
manuscript/predecessor pins remain valid. All 176 regression tests pass, and
`git diff --check` passes. The 12 warnings still identify unavailable historical
locators and unchecked external manifest hashes. Only five current Markdown
documents change; no experiment, paper build or external archive readback was
performed for this cleanup. The initial navigation cleanup reduced
README/MEMORY/TODO from 1,052 to 259 lines, before the final integration notes.

The subsequent authorized merge review also checked the #18/#19 prerequisite
source changes, passed 170 tests at #18 and 176 for the final code, and matched
ten selected external-record digests to the committed receipt. It did not rerun
model experiments or read back the complete archive. Both prerequisite squash
commits have one parent and exactly their reviewed trees; [MEMORY](../MEMORY.md)
records their identities and the final #20 integration entry point.

## Earlier source-only cleanup

The earlier cleanup began from `fba2efc` (including import `fb9f8ed`). It removed
`artifacts/research_todo_metadata_contract.html`, two lossy PDF text extracts
(`artifacts/paper.pdf.extracted.txt`, `artifacts/paper1.pdf.extracted.txt`) and the
old `SHA256SUMS` covering only those three documents. They were superseded as
navigation by actual manuscript sources and the single root TODO, not declared
scientifically false. Retrieve them with `git show fba2efc:<original-path>`.
That original import was approximately 1.3 MB; it is not the current checkout size.
No published Git history was rewritten in either cleanup.
