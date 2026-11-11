# landmark-metadata

Source repository for **Validation Boundaries for Model Label Resources:
A Controlled Classifier Case Study**.

This repository contains research code, manuscript source and necessary text.
Models, SDKs, emulators, builds, raw observations and evidence archives stay
outside Git. It is not a complete evidence archive or an offline reproduction kit.

## Current state — 11 November 2026

The current **11 November short-paper revision** incorporates the known-outcome
10 November rerun: E1/E2, paired Android P2 and the six-input P3 core. The follow-up
centers on four acceptance decisions and condenses evidence history. It discloses
the unavailable old cloud execution evidence, two interrupted collections and
selected continuations. The evidence map binds claims to concrete archived files
and newly checked bytes; matching results do not recover the lost provenance.
The October full companion remains explicitly historical context. Human
verification and durable external evidence delivery remain pending.

The study concerns one classifier graph, five byte conditions and two synthetic
inputs. Keep structural acceptance S, reference-backed association I and selected
decoder compatibility D separate; P checks intervention preservation. E5 remains
a supporting tool with no additional rejection over the audited simple/Task
baseline. These data do not establish natural defects, prevalence or task accuracy.

## Current code

Use [experiment/README.md](experiment/README.md) and its [runbook](experiment/RUNBOOK.md).
The exact staging dependency list is [experiment/source-map.json](experiment/source-map.json).
Historical source versions are [archived at a fixed Git commit](archive/README.md);
auxiliary evidence readers are separated from the focal execution in [support](support/README.md).

## Start here

| Task | Entry point |
|---|---|
| Read the current paper | [Current manuscript source](work/acceptance-paper-revision-20261111/manuscript/paper.tex), [claim–evidence map](work/acceptance-paper-revision-20261111/CLAIM_EVIDENCE.md), [historical October companion](work/label-resource-revision-20261020/manuscript/paper-full.tex) |
| Inspect the new execution | [Observed results](work/focal-rerun-20261110/RESULTS.md), [runbook and prerequisites](work/focal-rerun-20261110/README.md), [local archive receipt](work/focal-rerun-20261110/delivery-record.json) |
| Continue the project | [Active TODO](TODO.md), [current memory](MEMORY.md), [decisions](docs/DECISIONS.md), [repository policy](AGENTS.md) |
| Locate current code or historical versions | [Current experiment](experiment/README.md), [archive and restore](archive/README.md), [repository map](docs/REPOSITORY_CLEANUP.md) |
| Check provenance and author questions | [Current manuscript pins](docs/CURRENT_MANUSCRIPT.json), [unsigned author handoff](work/acceptance-paper-revision-20261111/ARTIFACT_HANDOFF.md), [exact evidence identities](work/rerun-paper-revision-20261111/evidence-index.json), [input recovery](work/input-recovery-20261110/README.md) |
| Trace historical sources | [Original import index](docs/SOURCE_IMPORT.json), [P2/P3 import index](docs/SOURCE_P2P3.json), [historical reading notes](docs/HISTORICAL_README_NOTES.md) |

## Source checks

Run from the checkout with Python 3:

```sh
python3 scripts/check_source_tree.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

These commands check source scope, navigation, syntax, 354 preserved imports
(in the working tree or verified Git archive), the import-backed memory hash,
current/historical manuscript and evidence-index pins, and verifier regressions.
They do not run model experiments or revalidate excluded raw evidence.
Historical missing-evidence locators produce warnings; changed imported bytes fail.
Archive verification requires local Git history containing the fixed pre-cleanup commit.

## Reproduction and manuscript builds

Use the [current focal runbook](experiment/RUNBOOK.md) for a new source layout.
The [November record](work/focal-rerun-20261110/README.md) preserves the executed
sequence and its external prerequisites. The layout change was source-staged and
regression-tested; no Android build or inference was repeated. The [historical guide and
input/toolchain inventories](docs/reproduction/README.md) remain provenance
references. Imported absolute `/workspace` paths are intentional historical facts;
new runs require separate directories and recorded path adaptations. Never run
historical sealing/finalization tools over retained evidence.

The [current validation record](work/acceptance-paper-revision-20261111/VALIDATION.md)
documents the four-page short-paper build, actual saved-byte readbacks and their
limits. Build outside the checkout. The October companion is unchanged and its
old eight-page build is historical. No venue has been selected; the manuscript
revision adds no Android/model execution or human signoff.

Publish source changes on a feature branch through a PR. Merging requires an
explicit instruction; use squash by default. Keep excluded evidence outside the
repository, including Releases and LFS. `TODO.md` is the sole active checklist;
timestamped plans and reports describe their original scope.
