# Agent pre-audit before human verification

**The inspected core saved evidence supports E1/E2/P2 and the qualified P3
reference. This is not human verification or a new inference replay.** The review
also identifies limited chronology evidence and still-missing later parser raw
records. All human verdicts remain PENDING.

- [Consolidated findings and item dispositions](AUDIT_REPORT.md)
- [Short human continuation sheet](HUMAN_HANDOFF.md)
- [Frozen protocol](PROTOCOL.md)
- [Delivery validation](VALIDATION.md)
- [Machine-readable scope and evidence index](audit-index.json)
- Independent area reports: [executable path](reviews/executable.md),
  [preservation](reviews/preservation.md), [observations](reviews/observations.md),
  [reference](reviews/reference.md), [secondary claims](reviews/secondary.md),
  and the separately delegated [chronology subcheck](reviews/chronology.md).

The frozen target is the four-page manuscript at commit
`24f660cf093c3e52efc0cde0c39e7aea1df48053`, SHA-256
`c79ba7f62a194abd487ec4b8ccedb60428ec4edd1f43e6ee155518ffd8bb416e`.
Neither that manuscript nor the old human-audit map was changed. Five reviewers
started in fresh task contexts; the observation reviewer delegated chronology to
another fresh agent. They share infrastructure and inputs. This is separation of
review tasks, not blinded/forensic independence or human inter-rater validation.

The full selected focal package was reverified: 2,749 payload files match its
pinned identity index. Reviewers then performed new saved-byte comparisons,
disassembly and source inspection. Numerical observation counts are repeated
inputs/configurations, not independent models or newly executed inferences.

## Source and external evidence

This directory contains necessary review prose and first-party audit source.
Per-file raw inventories, decoded rows, class/DEX extracts and command stdout
remain under `/workspace/agent-preaudit-20261007T0749Z/`. The index pins their
locations, hashes and sizes. The original and recovered evidence remain unchanged.
Nothing was uploaded to a data archive; a local path is not a public download.

Scripts under `scripts/` are **exact executed command/source snapshots**, with
original absolute roots and output locations. Do not blindly rerun fixed-path
scripts into this review or preserved evidence: prepare a new external directory
and redirect their output constants/arguments first. The preservation script has
an explicit new-output argument and refuses to overwrite findings; other snapshots
need output-path adaptation. Record any adaptation. These are not a new universal
validator or a turnkey fresh-machine package. A command returning zero does not
replace inspection of its scoped comparison results.

The observation helper initially assumed the wrong label filename; the correction
and retained initial stdout/re-execution are disclosed in its report. The
reference helper likewise records its commit-serialization refinement. These are
audit-helper issues, not hidden changes to experimental inputs or natural defects.

This work is delivered through [PR #13](https://github.com/lcresearch/landmark-metadata/pull/13),
based on `paper/workshop-convergence`
(PR #12), whose earlier #10/#11 prerequisites are still open. No merge, submission
or human signature is authorized by this pre-audit.
