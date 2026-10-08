# Build and verification after the agent pre-audit

The revised short draft renders to **four pages including 18 references**;
the detailed companion renders to **seven pages including 18 references**.
Both use the unchanged IEEEtran V1.8b conference class and ordinary margins.
The final logs have no undefined citations/references or overfull boxes.
The root agent inspected all four short-paper page images with no visible
clipping or overlap. The full companion was rendered without a separate
all-page visual audit. Formatting remains provisional, not submission approval.

## Exact executed document command

From `/workspace/landmark-preaudit-followup`:

```sh
PYTHONDONTWRITEBYTECODE=1 python work/preaudit-followup-20261008/build_documents.py \
  --output /workspace/preaudit-followup-build-20261008T0330Z \
  --ieeetran /workspace/workshop-convergence-build-20261007/tex/IEEEtran.cls
```

The source driver verifies the external template's SHA-256
`da751920a317ed318b7b5cd7fa585a6cc7d28502d457856382e9be24b10a3bd7`,
refuses an existing output directory, copies the exact manuscript sources and
records both LaTeX passes, output extraction and page rendering. A future run
must choose a new external directory. It does not promise PDF byte identity;
PDF metadata contains build times. The output directory suffix is an identifier,
not the authoritative execution time; `commands.json` records actual times.

The build used pdfTeX 1.40.26 / TeX Live 2025/dev/Debian and Poppler 25.03.0.
`commands.json`, `SHA256SUMS`, raw logs, PDFs and page images stay outside Git.
Their exact source/output identities are in `revision-map.json`.

## Probe and independent agent review

The [parser report](parser/REPORT.md) identifies the separate fresh JVM run,
its exact 151-file manifest and 379-check saved-record verifier. The expected
VT decoder failure is preserved as a failure, despite the controller's successful
verification of the expected observation. No full checker, Task or Android/model
execution was added.

A separate fresh-context editorial agent inspected both new manuscripts, the
claim map, actual Java/helper/probe source, all three raw decoder outputs, full
oracle string lists and eight pinned dependency JARs. It rechecked 22 helper
comparisons and three abstentions and found no blocking scope/claim issue.
This is shared-infrastructure agent review, not human verification. Its cosmetic
crosswalk correction was applied; manuscript bytes were unchanged after review.

The new target keeps all 16 claim IDs and every human status PENDING. Historical
manuscripts, imported sources, old audit indexes and evidence are preserved;
partial secondary coverage and missing historical parser/Task/catalog records
remain explicit. Source checks inspect repository integrity, not experimental
truth or public evidence availability.

## Final repository and identity checks

`python scripts/check_source_tree.py` passed: all 354 imported files unchanged,
249 Python/17 shell syntax checks, 45 JSON documents and 369 navigation targets.
Twelve existing warnings still identify historical unavailable locators or
unchecked excluded evidence digests; they are not suppressed or counted as passes.

The coordinator separately checked 269 identity/scope conditions with no failure,
including all 48 old ledger sources, new source/evidence pins, exact parser file
membership, preserved source/research/audit trees, all 16 pending claim routes,
13 pending human items, and both built manuscript copies. This count is an
internal consistency checklist, not a scientific reliability metric.
`git diff --check` passed. No maintained checker implementation changed, so its
full repository regression suite was not rerun; the new drivers were exercised
and the helper's fixed differential cases were run as reported.

Check output is retained at
`/workspace/preaudit-followup-validation-20261008T033116Z/`.
`PARSER_SHA256SUMS` independently lists the 151 frozen probe payloads plus their
manifest and passed `sha256sum --check --quiet`. It is outside the frozen probe
directory to preserve that directory's exact file set. Source/index checks do
not make this a durable or anonymous public archive.

## Remaining submission work

Use the [current human handoff](HUMAN_HANDOFF.md) and the existing
[submission checklist](../workshop-convergence-20261007/SUBMISSION_READINESS.md).
Human verification, anonymous durable evidence access, author/venue decisions,
final disclosure and explicit submission authorization remain open. E2's
historical timing is narrowed in the paper rather than retroactively certified.
