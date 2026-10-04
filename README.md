# landmark-metadata

Source repository for **From Model Metadata to Executable Interfaces:
A Controlled Study of Tensor Binding and Decoder Contracts**.

The user requested **source only**: no SDK, emulator, model, raw execution data,
or build products are uploaded. This repository holds research code, manuscript
source and continuation documents, **not the complete evidence archive**.

## Start here

- [Current manuscript source](research/20261004-p2-p3/manuscript/paper.tex)
- [Completed same-Android comparison and display-reference findings](research/20261004-p2-p3/RESULTS_OVERVIEW.md)
- [Project memory and current evidence boundaries](MEMORY.md)
- [Current TODO](TODO.md)
- [Decisions and scope](docs/DECISIONS.md)
- [Future agent instructions](AGENTS.md)
- [Exact source import paths and SHA-256 hashes](docs/SOURCE_IMPORT.json)
- [P2/P3 source import and local evidence identity](docs/SOURCE_P2P3.json)

## Code map

| Source area | Purpose |
|---|---|
| [Initial Hand scripts](sources/hand-contract-repro/scripts) | Graph-preserving mutations, static binding, isolated decoder and replay work |
| [Earlier corpus/checker scripts](sources/metadata-contract-paper/scripts) | Metadata inspection, mutation, generation, CPU and decoder experiments |
| [E1–E7 scripts](sources/metadata-contract-e2e-20261004T030536Z/scripts) | Actual Android harness, classifier interventions, Task comparison, frozen external checks and Hand boundary experiment |
| [Frozen E4 protocol](sources/metadata-contract-e2e-20261004T030536Z/E4/protocol) | Predeclared candidates, scope, mutation rules and source snapshots |
| [Agent audit](sources/metadata-contract-audit-20261004T062010Z) | Preservation checks, fresh build scripts, baseline comparison and claim/literature audit scripts |
| [Previous audited manuscript revision](sources/metadata-contract-paper-revision-20261004T065132Z) | Preserved prior LaTeX, editorial scripts and revision notes |
| [Current P2/P3 follow-up](research/20261004-p2-p3) | Same-Android harnesses, reference inquiry, separate audits, current LaTeX and claim updates |

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

Run `python scripts/check_source_tree.py` for source integrity, syntax and
source-only scope checks. No model experiment is executed by that command.
`scripts/import_workspace_sources.py` records how this source snapshot was
selected; it requires the original local workspace and refuses to overwrite
changed imported files. `scripts/import_p2p3_sources.py` separately records the
new follow-up selection; both source manifests are checked without running models.

Future work should save source, TODO updates, concise decisions and continuation
notes here under the same source-only rule. Large evidence and build outputs
remain excluded unless the user explicitly changes that scope.
