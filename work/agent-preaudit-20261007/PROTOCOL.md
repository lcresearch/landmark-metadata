# Agent pre-audit protocol

User request: independent agents should walk through the human checklist before
the user performs the actual human review. This is **agent pre-audit**, never a
human signature or independently recruited human replication.

Frozen repository head: `24f660cf093c3e52efc0cde0c39e7aea1df48053`.
Target: `work/workshop-convergence-20261007/manuscript/paper.tex`, SHA-256
`c79ba7f62a194abd487ec4b8ccedb60428ec4edd1f43e6ee155518ffd8bb416e`.
Use that revision's claim crosswalk and the existing HA01–HA10 checklist;
HA09 has separate a/b/c subitems. All human statuses remain PENDING.

## Independence and scope

New reviewers receive fresh agent contexts and explicit subscopes, without the
coordinator's conversation history. They share the filesystem, model/tool
infrastructure, manuscript and existing reports. This is task/context separation,
not forensic independence, blinding or independent provenance of historical data.
Prior PASS summaries are locators, not substitutes for checking available bytes.

Read-only inputs include the source tree and saved evidence. Prefer the selected
package at `/workspace/evidence-recovery-20261005T170453Z/package-v2/`; preserve
its original family/relative paths and distinguish originals, rebuilds and later
reconstruction. Secondary original roots may be inspected if present, with their
own identities. Missing material stays missing. No model generation, new APK
build, emulator or inference is required for this pre-audit. Fresh readback,
hashing, static parsing and disassembly are authorized; record their exact scope.

Write new scripts, command records and raw audit output only below
`/workspace/agent-preaudit-20261007T0749Z/<reviewer>/`. Never rewrite preserved
inputs, prior reports or human-verdict fields. New reusable audit source and
concise text reports may subsequently enter Git after review; binary evidence
and raw result inventories stay outside it.

## Assigned review areas

1. HA01–HA02: actual generated/harness call, compiled-path evidence and APK/model
   identity attribution, including separate construction audit.
2. HA03: independent graph/buffer/metadata/resource preservation comparisons,
   generated source/classes/DEX equality at their stated scopes.
3. HA04–HA06: full E1/E2 saved input/output/stage comparisons, chronology and
   P2 public-boundary/cause-chain comparison. No inference rerun implied.
4. HA07: source authority chain, independently recomputed computational bridge
   and full display-map comparison; preserve display/stable-ID distinction.
5. HA08–HA10: Hand and secondary/raw availability, frozen counts/baselines,
   parser limitations, public antecedent and claim/novelty scope.

Each reviewer reports inspected paths/digests, commands/method, observations,
comparisons, limitations, discrepancies and the exact next human action. Separate
direct byte/computation checks from source/report consistency and missing-raw
judgments. State the denominator and do not promote a selected sample to all
executions. Do not fix evidence until it matches the manuscript.

## Disposition and stopping rules

Agent verdicts use `SUPPORTED_WITHIN_INSPECTED_SCOPE`, `PARTIAL`,
`DISCREPANCY_FOUND`, `BLOCKED_MISSING_EVIDENCE` or `NOT_CHECKED`. These do not alter
human statuses. An absent prerequisite limits that subcheck, not every other
independently supported claim. Conversely a matching digest does not validate
source authority or a recorded execution's truth.

The coordinator reconciles findings against concrete inputs, retains disagreement
and prepares a compact human handoff. Do not increase model count, invent missing
records, overwrite the frozen manuscript or turn agent agreement into reliability
statistics. Any suggested wording correction is listed for review separately.
Deliver new source/docs and TODO updates through a PR; no merge is authorized.
