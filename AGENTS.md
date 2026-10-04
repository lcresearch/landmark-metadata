# Project continuation and repository policy

The user chose `https://github.com/lcresearch/landmark-metadata` as the ongoing
home for this research project's **source code and necessary text documents**.
Their latest scope correction is authoritative: **do not upload SDKs,
emulators, or build products; source only**.

At the start of project work, read `MEMORY.md`, `TODO.md`, and
`docs/DECISIONS.md`. Consult the current manuscript and source index in README.

## What to save here

- First-party experiment, mutation, harness, checker, audit and build scripts.
- Manuscript source, source configuration, dependency lock text, and protocols.
- TODO updates and concise user-facing notes about findings, decisions, their
  rationale, evidence locations, limitations, and next steps.
- After meaningful authorized project work, commit and push these source/doc
  changes to this repository, verify the remote commit, and report any blocker.
  The user has authorized this ongoing project synchronization. Do not promise
  unattended background synchronization or cross-session recall without reading
  the repository. Do not overwrite unrelated remote changes or force-push.

## What stays outside Git

SDKs, installed dependencies, virtual environments, emulator images/state,
model assets, generated wrapper outputs, APKs/classes/DEX, raw tensors/results,
execution logs, rendered papers/figures, archives, keys and credentials.
Record external evidence paths/digests when useful, but never claim that a
source-only import is a complete archived experiment. Do not upload excluded
files to Releases or LFS as a workaround for the user's scope.

## Research integrity

- `sources/` imports are byte-preserved historical snapshots. Add new work in a
  new source area instead of rewriting those snapshots or sealed local evidence.
- Keep structural acceptance S, reference-backed association I, and selected
  decoder compatibility D separate. P checks intervention preservation.
- Recheck claims against actual artifacts before strengthening them. Textual
  summaries in this repository do not replace the excluded execution evidence.
- E5 remains a supporting tool; the audited five-condition comparison showed
  no additional rejection over the matched simple baseline or Task initialization.
- Human audit is pending. Automated audits and fresh agent builds are not human
  verification. Do not count mutations/aliases/inputs as independent models.
- Preserve negative and incomplete results. Do not claim prevalence, task
  accuracy, natural EfficientNet defects or production crashes from these data.

For imported scripts, original absolute workspace paths and external evidence
dependencies remain intentional historical facts. Do not advertise a portable,
self-contained reproduction until those prerequisites have actually been made
available and tested. Run syntax/source checks without executing experiments
unless the active task calls for execution.
