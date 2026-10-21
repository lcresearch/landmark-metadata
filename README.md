# landmark-metadata

Source repository for **Validation Boundaries for Model Label Resources:
A Controlled Classifier Case Study**.

The user requested **source only**: no SDK, emulator, model, raw execution data,
or build products are uploaded. This repository holds research code, manuscript
source and continuation documents, **not the complete evidence archive**.

## Start here

- [Current manuscript source](work/label-resource-revision-20261020/manuscript/paper.tex)
- [Full companion](work/label-resource-revision-20261020/manuscript/paper-full.tex)
- [Manuscript claim–evidence table](work/label-resource-revision-20261020/CLAIM_EVIDENCE.md)
- [Revision scope and section-by-section changes](work/label-resource-revision-20261020/REVISION_NOTES.md)
- [Minimal evidence handoff and six unsigned author questions](work/label-resource-revision-20261020/ARTIFACT_HANDOFF.md)
- [Current build and validation results](work/label-resource-revision-20261020/VALIDATION.md)
- [Current manuscript and preserved-parent digests](docs/CURRENT_MANUSCRIPT.json)
- [Project memory](MEMORY.md), [active TODO](TODO.md), [decisions](docs/DECISIONS.md), and [agent instructions](AGENTS.md)
- [Completed same-Android comparison and display-reference findings](research/20261004-p2-p3/RESULTS_OVERVIEW.md)
- [Contribution comparison](research/20261004-contribution-review/CONTRIBUTION_COMPARISON.md) and [significance assessment](research/20261004-significance-review/SIGNIFICANCE_ASSESSMENT.md)
- [Documented reproduction commands and missing prerequisites](docs/reproduction/README.md)
- [Historical local evidence recovery and unresolved material](work/evidence-recovery-20261005/README.md)
- [Preserved October 8 manuscript/parser revision](work/preaudit-followup-20261008/README.md)
- [Preserved agent pre-audit](work/agent-preaudit-20261007/README.md) and [old unsigned human-audit target](docs/human-audit/README.md)
- [PR #10–#14 integration record](work/pr10-14-integration-20261008/README.md)
- [Original source identities](docs/SOURCE_IMPORT.json) and [P2/P3 source identities](docs/SOURCE_P2P3.json)

The new revision starts from main `65004d4ac573118d58eb8c6f3125d67c0b330d62`.
PR #14's public page was checked as **Merged**; older conditional/open-stack
statements are historical. This revision uses a new feature branch and requires
its own unmerged PR review. No author verification, deposit or submission follows
from the earlier merge.

## Code map

| Source area | Purpose |
|---|---|
| [Fresh reconstruction and corrections](sources/repro-audit-20261004) | Official prerequisite restoration, experiment replay, strict evidence checks, Java label-parser fix and new audit findings |
| [Initial Hand scripts](sources/hand-contract-repro/scripts) | Graph-preserving mutations, static binding, isolated decoder and replay work |
| [Earlier corpus/checker scripts](sources/metadata-contract-paper/scripts) | Metadata inspection, mutation, generation, CPU and decoder experiments |
| [E1–E7 scripts](sources/metadata-contract-e2e-20261004T030536Z/scripts) | Actual Android harness, classifier interventions, Task comparison, frozen external checks and Hand boundary experiment |
| [Frozen E4 protocol](sources/metadata-contract-e2e-20261004T030536Z/E4/protocol) | Predeclared candidates, scope, mutation rules and source snapshots |
| [Agent audit](sources/metadata-contract-audit-20261004T062010Z) | Preservation checks, fresh build scripts, baseline comparison and claim/literature audit scripts |
| [Preserved audit-informed revision](sources/metadata-contract-paper-revision-20261004T065132Z) | Historical LaTeX, editorial scripts and revision notes |
| [Preserved P2/P3 follow-up](research/20261004-p2-p3) | Same-Android harnesses, reference inquiry, separate audits and manuscript parent |
| [Preserved editorial follow-up](work/review-followup-20261004) | Earlier LaTeX with parser-scope corrections; unchanged by the new rewrite |
| [Preserved full paper rewrite](work/paper-rewrite-20261004) | Controlled execution narrative, claim–evidence ledger, contribution/significance integration and build/review notes |
| [Preserved workshop convergence](work/workshop-convergence-20261007) | Previously audited four-page source, longer companion, venue comparison and submission work |
| [Preserved post-audit draft](work/preaudit-followup-20261008) | Narrowed E2 chronology and separately identified October 8 JVM parser evidence |
| [Current label-resource revision](work/label-resource-revision-20261020/REVISION_NOTES.md) | Focused classifier case, seven-row coverage matrix, claim crosswalk and minimal evidence/author handoff |
| [Maintained observation reader](work/observation-review-20261004) | Exact Hand, Task and Android evidence identities; preserves the exported audit snapshot |

`sources/` retains original timestamped names and source bytes. Per-experiment
implementation snapshots are intentional historical versions, not extra models.
Text reports explain the history; the raw evidence they reference stays outside
this repository. Older HTML TODO and PDF text extracts have been removed from
the current tree; Git history retains them. `TODO.md` is the single active plan.
Old TODO copies inside timestamped source snapshots are historical records,
not current instructions. See [cleanup notes](docs/REPOSITORY_CLEANUP.md).

## Use and limits

Imported scripts may reference original `/workspace/...` paths and missing local
artifacts. They are preserved for inspection and continuation, not presented as
a turnkey clean-machine reproduction. Install/recover prerequisites separately
and review paths before running. Do not execute historical sealing/finalization
scripts against immutable evidence.

The current short source builds to **four pages including 16 references** in
provisional 10pt IEEEtran conference format; its detailed companion builds to
eight pages with 18 references. Build in a new directory outside the checkout.
The [validation record](work/label-resource-revision-20261020/VALIDATION.md)
gives commands, actual checks and the retained IEEEtran activation. No venue
has been selected or freshly assessed for compliance in this revision.

This round checked sources, regression tests and document builds. The original
external evidence roots are unavailable at their recorded paths in this cloud
session; historical recovery/readback reports are not fresh verification here.
The [handoff](work/label-resource-revision-20261020/ARTIFACT_HANDOFF.md) distinguishes
saved-record inspection, new execution and persistent anonymous delivery. The
latter and human author verification remain open. The prior parser supplement
is a bounded October 8 JVM experiment, separate from unrecovered later
reconstruction records and the unverified reconstructed 65-fixture catalog.

Run `python scripts/check_source_tree.py` for source integrity, syntax and
source-only scope checks. No model experiment is executed by that command.
Current Markdown file targets, imported source digests/sizes, the import-backed
`MEMORY.md` source hash and both manuscript digests are checked. Historical
README evidence locators produce warnings; excluded evidence hashes are reported
as unchecked. Run `PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -v`
for checker regression tests without creating caches in the source tree.
`scripts/import_workspace_sources.py` records how this source snapshot was
selected; it requires the original local workspace and refuses to overwrite
changed imported files. `scripts/import_p2p3_sources.py` separately records the
new follow-up selection; both source manifests are checked without running models.

Future work should save source, TODO updates, concise decisions and continuation
notes here under the same source-only rule, using a feature branch and pull
request for user review. Do not push directly to the default branch or merge
without an explicit user instruction. Large evidence and build outputs
remain excluded unless the user explicitly changes that scope.
