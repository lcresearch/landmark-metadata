# Audit-informed manuscript revision

Read `manuscript/paper.pdf` and `REVISION_NOTES.md`. `manuscript/paper.tex` is the editable source; `manuscript-changes.patch` compares it with the preserved previous manuscript. `CLAIM_EVIDENCE.json` maps 12 claims to evidence, and `SOURCE_PROVENANCE.json` pins 51 inputs.

`verification/` records automated source/evidence checks, source regeneration, preservation of old packages and visual review. `review/` retains three AI reviews and their resolution. `TODO.before.md` and `TODO.after.md` preserve the task-list update.

The revision is an 8-page generic reading draft, not a venue-ready submission. Independent human audit is pending. No model experiment was launched during editing; the fresh Android construction and baseline comparisons reported in the paper come from the previously sealed audit.

To rebuild the PDF, copy this directory elsewhere and run `bash build.sh` in the copy with a compatible TeX installation. Original tooling: Python 3.12.14, pdfTeX 1.40.26 (TeX Live 2025/dev/Debian), Poppler 25.03.0. PDF binary reproducibility is not claimed. `python scripts/verify_revision.py` checks against preserved workspace evidence; it requires the external roots named in the provenance file. This manuscript package is not the standalone experiment reproduction deposit. The one-time finalization script mutates the working TODO and should not be rerun on the sealed package.
