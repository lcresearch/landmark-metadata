# landmark-metadata

Source repository for **Validation Boundaries for Model Label Resources:
A Controlled Classifier Case Study**.

This repository contains research code, manuscript source and necessary text.
Models, SDKs, emulators, builds, raw observations and evidence archives stay
outside Git. It is not a complete evidence archive or an offline reproduction kit.

## Current state — 11 November 2026

The current manuscript is the **20 October revision**. A **new 10 November focal
rerun** completed E1/E2, the paired Android P2 comparison and the six-input P3 core.
The manuscript has not yet been reconciled with that new execution history.
The old cloud execution evidence is unavailable; matching inputs and new results
do not recover its provenance. Human verification and durable external evidence
delivery remain pending.

The study concerns one classifier graph, five byte conditions and two synthetic
inputs. Keep structural acceptance S, reference-backed association I and selected
decoder compatibility D separate; P checks intervention preservation. E5 remains
a supporting tool with no additional rejection over the audited simple/Task
baseline. These data do not establish natural defects, prevalence or task accuracy.

## Start here

| Task | Entry point |
|---|---|
| Read the current paper | [Current manuscript source](work/label-resource-revision-20261020/manuscript/paper.tex), [full companion](work/label-resource-revision-20261020/manuscript/paper-full.tex), [claim–evidence map](work/label-resource-revision-20261020/CLAIM_EVIDENCE.md) |
| Inspect the new execution | [Observed results](work/focal-rerun-20261110/RESULTS.md), [runbook and prerequisites](work/focal-rerun-20261110/README.md), [local archive receipt](work/focal-rerun-20261110/delivery-record.json) |
| Continue the project | [Active TODO](TODO.md), [current memory](MEMORY.md), [decisions](docs/DECISIONS.md), [repository policy](AGENTS.md) |
| Locate code or decide what to retain | [Repository map and cleanup decisions](docs/REPOSITORY_CLEANUP.md) |
| Check provenance and author questions | [Current manuscript pins](docs/CURRENT_MANUSCRIPT.json), [unsigned author handoff](work/label-resource-revision-20261020/ARTIFACT_HANDOFF.md), [input recovery](work/input-recovery-20261110/README.md) |
| Trace historical sources | [Original import index](docs/SOURCE_IMPORT.json), [P2/P3 import index](docs/SOURCE_P2P3.json), [historical reading notes](docs/HISTORICAL_README_NOTES.md) |

## Source checks

Run from the checkout with Python 3:

```sh
python3 scripts/check_source_tree.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

These commands check source scope, navigation, syntax, 354 preserved imports,
the import-backed memory hash, seven manuscript/predecessor pins and verifier
regressions. They do not run model experiments or revalidate excluded raw evidence.
Historical missing-evidence locators produce warnings; changed imported bytes fail.

## Reproduction and manuscript builds

Use the [new focal runbook](work/focal-rerun-20261110/README.md) for the executed
November sequence and its external prerequisites. The [historical guide and
input/toolchain inventories](docs/reproduction/README.md) remain provenance
references. Imported absolute `/workspace` paths are intentional historical facts;
new runs require separate directories and recorded path adaptations. Never run
historical sealing/finalization tools over retained evidence.

The manuscript's [October validation record](work/label-resource-revision-20261020/VALIDATION.md)
records four short-paper pages and eight companion pages in provisional IEEEtran
format. Build outside the checkout. No venue has been selected, and this cleanup
does not rebuild the paper or update its scientific claims.

Publish source changes on a feature branch through a PR. Merging requires an
explicit instruction; use squash by default. Keep excluded evidence outside the
repository, including Releases and LFS. `TODO.md` is the sole active checklist;
timestamped plans and reports describe their original scope.
