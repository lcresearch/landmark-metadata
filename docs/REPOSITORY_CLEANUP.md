# Repository cleanup

The user requested a source-only repository and removal of confusing old content.
The remote was fetched before editing; the prior `main` state was commit
`fba2efc` (which includes the earlier `fb9f8ed` import).

Removed from the current tree:

- `artifacts/research_todo_metadata_contract.html`: an older parallel TODO with
  local browser state. It is superseded by the single active root `TODO.md`.
- `artifacts/paper.pdf.extracted.txt` and `artifacts/paper1.pdf.extracted.txt`:
  lossy text extractions of older drafts, superseded by actual manuscript source.
- The old `SHA256SUMS`: it covered only those three removed documents and was
  not a checksum of the research evidence or of the current source import.

Replaced the partial-upload README with a source index and explicit scope. Added
project continuation notes and agent instructions. Original imported source bytes
remain in timestamped `sources/` snapshots; root documents describe the current
state and active tasks. Historical snapshot TODOs are not active checklists.

No published Git history was rewritten. To inspect a removed file, use
`git show fba2efc:artifacts/research_todo_metadata_contract.html` (or the other
original path). This cleanup does not declare every sentence in those historical
drafts false; it removes stale/duplicate entry points.

The source import is approximately 1.3 MB, with exact per-file hashes in
`docs/SOURCE_IMPORT.json`. SDKs, emulator files, model/data files, rendered PDFs,
raw experiment outputs, compiled products, dependency archives and keys are
excluded. No Release or LFS upload is made.
