# Reading the imported snapshots

The READMEs under `sources/` describe their original local packages. Their bytes
are preserved and checked against [SOURCE_IMPORT.json](SOURCE_IMPORT.json).
Use the [current repository index](../README.md) and [active TODO](../TODO.md)
for current navigation and planning. These notes supplement the historical
READMEs without changing their recorded contents.

| Historical entry | Available here | References outside this source-only import |
|---|---|---|
| [Audit README](../sources/metadata-contract-audit-20261004T062010Z/README.md) | Reports, plans and first-party checking/build scripts; [English summary](AUDIT_SUMMARY_EN.md) | Root `results.json`, `SHA256SUMS`, raw tensors, APKs, dependency archives and SDK/AVD state. `commands.sh` is imported, but its verification requires the excluded manifest and evidence. `rebuild/sdk/` is intentionally absent. |
| [Revision README](../sources/metadata-contract-paper-revision-20261004T065132Z/README.md) | Historical `manuscript/paper.tex`, editorial scripts, revision notes and retained review text | `manuscript/paper.pdf`, `CLAIM_EVIDENCE.json`, `SOURCE_PROVENANCE.json`, rendered pages and execution evidence. The old full-workspace verification command cannot run from this import alone. |

The audit README's `/workspace/metadata-contract-next/TODO.md` is a historical
locator. [TODO.md](../TODO.md) is the active plan. Original root package paths
and their manifest digests in [MEMORY.md](../MEMORY.md) identify excluded
evidence; knowing a digest does not recover or verify those bytes.

`python scripts/check_source_tree.py` checks file targets in current Markdown
documents, including `docs/` and the new work area. Historical source READMEs
are checked relative to their own directory, including file-like backtick
locators; unavailable targets produce warnings. Those warnings never excuse
changed imported bytes, forbidden artifacts or credential-like content, which
remain failures. This is a local file-navigation check, not a network/anchor
validator or a complete Markdown parser.

To compile a manuscript, copy its source into a separate directory with a
suitable TeX installation. Keep all build outputs outside this repository.
Compilation checks manuscript construction; it does not reproduce experiments.
