# Hand Landmark Metadata Research Artifacts

Partial snapshot uploaded on 2026-10-04 at the author's request.

## Included

- [Research TODO](artifacts/research_todo_metadata_contract.html): complete HTML source recovered from `research_todo_metadata_contract.html` (22,013 UTF-8 bytes).
- [paper.pdf text extract](artifacts/paper.pdf.extracted.txt): complete text returned for all 5 pages of `paper.pdf`.
- [paper1.pdf text extract](artifacts/paper1.pdf.extracted.txt): complete text returned for all 7 pages of `paper1.pdf`.

The two `.pdf.extracted.txt` files are text extractions, **not original PDFs**, regenerated PDFs, or manuscript source. Page markers and extraction artifacts are preserved. PDF layout, embedded images, and exact PDF bytes are not preserved. The original PDF downloads failed, so no PDF binaries are claimed to be included.

The HTML source was recovered through a full text read; its UTF-8 byte count matches the source file metadata. Byte-for-byte comparison against a downloaded original was not possible.

## Completeness and research status

This repository is **not yet the complete reproducibility package**. The full experiment/source/log trees, manuscript source, models and fixtures, generated Java/classes/DEX, APKs, raw inputs/outputs, dependency archives, source-reference snapshots, and evidence/checksum bundles were not accessible for this upload. The latest in-progress manuscript revision is also not included.

Statements in the preserved drafts about artifacts being archived describe their original research workspace; they do not establish that those artifacts are present here. These working drafts retain their original limitations and pending human-review status. No new experiments, scientific validation, or reproduction were performed for this upload.

The three source filenames were `research_todo_metadata_contract.html`, `paper.pdf`, and `paper1.pdf`. No filenames or contents have been invented to stand in for unavailable original artifacts.

## Integrity

`SHA256SUMS` records SHA-256 hashes of the three uploaded artifact files. For the PDF extracts these hashes identify the text files only, not their source PDFs. Run from the repository root:

```sh
sha256sum -c SHA256SUMS
```

## Remaining import

Import the original PDFs and complete project/evidence archives when available, preserving historical revisions separately from the current manuscript revision. Until that happens, use this repository as a partial document snapshot, not an independently runnable reproduction.
