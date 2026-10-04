# landmark-metadata

Source repository for **From Model Metadata to Executable Interfaces:
A Controlled Study of Tensor Binding and Decoder Contracts**.

The user requested **source only**: no SDK, emulator, model, raw execution data,
or build products are uploaded. This repository holds research code, manuscript
source and continuation documents, **not the complete evidence archive**.

## Start here

- [Current manuscript source](work/review-followup-20261004/manuscript/paper.tex)
- [Current manuscript and preserved-parent digests](docs/CURRENT_MANUSCRIPT.json)
- [Completed same-Android comparison and display-reference findings](research/20261004-p2-p3/RESULTS_OVERVIEW.md)
- [Fresh reproduction and repository audit (2026-10-04)](sources/repro-audit-20261004/REPORT.md)
- [Maintained checker fix and reproduction entry points](sources/repro-audit-20261004/README.md)
- [Maintained observation reader and completeness fixes](work/observation-review-20261004/README.md)
- [Project memory and current evidence boundaries](MEMORY.md)
- [Current TODO](TODO.md)
- [Contribution and related-work comparison](research/20261004-contribution-review/CONTRIBUTION_COMPARISON.md)
- [Research significance assessment and public antecedents](research/20261004-significance-review/README.md)
- [Decisions and scope](docs/DECISIONS.md)
- [Future agent instructions](AGENTS.md)
- [Exact source import paths and SHA-256 hashes](docs/SOURCE_IMPORT.json)
- [P2/P3 source import and local evidence identity](docs/SOURCE_P2P3.json)
- [Repository review disposition](docs/REVIEW_FOLLOWUP.md)
- [Historical README availability notes](docs/HISTORICAL_README_NOTES.md)
- [English summary of the historical audit](docs/AUDIT_SUMMARY_EN.md)

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
| [Current editorial follow-up](work/review-followup-20261004) | Current LaTeX; no new model execution or human audit |
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

The current paper source can be compiled in a **separate work directory** with
a suitable TeX installation. It is a generic reading draft; human review and
venue-specific formatting remain pending.

The fresh audit reproduced the main controlled results and found a label-reader
mismatch in the evaluated checker plus weaknesses in historical report scripts.
The maintained checker corrects the parser; the current manuscript distinguishes
that correction and its isolated counterexamples from the historical 65-fixture
evaluation. The maintained observation reader also requires the frozen E5
artifact set and validates Task inputs before counting successful observations.
Read the [repair scope](docs/OBSERVATION_REPAIR.md) and fresh audit before relying
on historical summary prose or interpreting a zero exit code as verified evidence.

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
