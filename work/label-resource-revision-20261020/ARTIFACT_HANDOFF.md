# Minimal evidence and author handoff

This is the evidence route for the revised short case study, not a new archive or
audit system. The exact short/companion paths and SHA-256 values are in
[CURRENT_MANUSCRIPT.json](../../docs/CURRENT_MANUSCRIPT.json); the revision is
`work/label-resource-revision-20261020/manuscript/`, based on main
`65004d4ac573118d58eb8c6f3125d67c0b330d62`. The preceding short source remains
`work/preaudit-followup-20261008/manuscript/paper.tex`, SHA-256
`aac0903bc50d41dc1066232f6be13f9596b3241bff8168eac625c0da58ab67b4`.
Use [CLAIM_EVIDENCE.md](CLAIM_EVIDENCE.md) for all 16 historical claim IDs and
the matrix's observed/source/analytical distinctions.

## What was and was not checked in this revision

On 20 October 2026 (America/Los_Angeles), exact-path filesystem checks found
the following external locations **absent on this cloud machine**:

- `/workspace/evidence-recovery-20261005T170453Z/package-v2` and its sibling
  `delivery/focal-saved-evidence.tar.gz`;
- `/workspace/metadata-contract-e2e-20261004T030536Z`,
  `/workspace/metadata-contract-audit-20261004T062010Z`, and
  `/workspace/metadata-contract-p2p3-20261004T073824Z`;
- all five primary model paths and all six P3 reference bodies listed in
  `docs/reproduction/inputs.json`;
- `/workspace/parser-followup-20261008T032600Z` and the nine exact later
  reconstruction locators listed in the preserved
  [missing inventory](../evidence-recovery-20261005/MISSING.md).

These were successful path checks, not access-denied results. They establish
current unavailability at those locations, not absence on other machines,
historical nonexistence, or invalidity of earlier experiments. Repository reports,
scripts, locks and provenance indexes were inspected; all 48 files in the
preserved claim-source index were rehashed and match. No excluded raw model,
APK, stack, tensor, card body, label reference or evidence archive was accessed
or rehashed this round. No Android/model inference or JVM parser run was added.
Current source/test/TeX results belong in [VALIDATION.md](VALIDATION.md).

Historical evidence stays explicitly dated: the
[5 October recovery](../evidence-recovery-20261005/README.md) records a verified
2,749-file local package; the [7 October pre-audit](../agent-preaudit-20261007/AUDIT_REPORT.md)
records saved-byte, compiled-call, preservation, observation and reference checks;
the [8 October parser report](../preaudit-followup-20261008/parser/REPORT.md)
records its separate isolated probes. Their PASS statements are not this round's
execution results. Original focal evidence, later missing reconstruction and the
newer parser run remain distinct provenance histories.

## A. Inspect saved evidence for the retained core claims

The smallest existing selection is the original focal package, described by
[package-plan.json](../evidence-recovery-20261005/package-plan.json) and
[delivery-record.json](../evidence-recovery-20261005/delivery-record.json).
Its recorded archive SHA-256 is
`1e6f9737ecdaf426b8e4a30391fd1298b6f503e39d8c17423c521376b86c746e`;
its `SHA256SUMS` file is pinned as
`a689674abb65452d8eb02a17d6af3f097884bd8c2ad4cb4a8353e33914197a3c`.
These are historical pins, not fresh measurements or download links.

The full model and associated-resource identities below come from the preserved
[input index](../../docs/reproduction/inputs.json). All use the member
`labels_without_background.txt`; no current byte check is implied.

| Condition | Whole-model SHA-256 | Label payload SHA-256 |
|---|---|---|
| Original | `6c7ab0a6e5dcbf38a8c33b960996a55a3b4300b36a018c4545801de3a3c8bde0` | `e697a491aa735cc6c2aaf982f8e86e8fc7b0a1ea7750a2cc6a2bdfc1e109012f` |
| Description control | `ed16d9573d8fe3e489c27637036a4e5c8476d15f013b7116f89864d55432f51d` | same as original |
| Deletion | `739f08462e831806db6a9bce7ed5b70a037fce593003028e5d6911dbd284fd83` | `7da978074d861c47f650a000db04db008aaecafcc1ae3e58eb71718e36c5ff4a` |
| Permutation | `455a04a2c6193ea81bef8fbc47e193aee0449b8cebdc9cc487c7e9e85fe42da7` | `334152d1cce3445fc73c27c32001b5a6e8b7e548a37cc0e050ea363ebde18d3a` |
| Restoration | `0a605ed10a38fc6f92fc4e266f5560756d2809e2669c45aa3b5a631cd88cea72` | same as original |

Description changes embedded M; deletion/permutation change F. The recorded
canonical G/W/O digest is
`73e57df01115600419abb72de4b2c3257200e12eb205d335bcbfc203a589bee8`.
The original generated Java digest is
`60c1fb6022891cc2bd41b5bacdd2194361eb0ca40e37da2eddf6cba963279670`.
The input index retains exact two-input byte definitions/digests, metadata hashes
and phase aliases. Restoration is not whole-package identity restoration.

Package-relative payload roots are `payload/metadata-contract-e2e-20261004T030536Z`
(**E**), `payload/metadata-contract-audit-20261004T062010Z` (**A**), and
`payload/metadata-contract-p2p3-20261004T073824Z` (**P**). Keep these histories
separate when relocating files.

| Retained question | Required material and route |
|---|---|
| Was the generated getter actually called? | **E** `scripts/ContractInstrumentation.java`, generated `ContractModel.java`, compiled classes/DEX, build/install attribution and `E1/executions/primary/*/device/result.json`. Repository harness source and [executable review](../agent-preaudit-20261007/reviews/executable.md) describe the call trace. Raw observation duplicates the buffer; it does not substitute a decoder. |
| What changed and what stayed fixed? | All five model/resource bytes; **A** `preservation/` comparisons and **P** P2 preservation/asset records. Check ordered computation and all 165 non-metadata buffers separately from M, F, source/classes and within-family DEX. Working/APK/pre-load agreement does not intercept native interpreter memory. |
| E1 exception and E2 complete associations? | **E** `E1`/`E2/executions/primary/*/device/`: `result.json`, both `*-input.rgb`, `*-output-0.f32`, successful `*-decoded.json`, complete exception stacks and stage records. Match all 1,000 score/label positions for both inputs; compare restoration. Preserve caught failures and distinguish replay/build audit. |
| P2 configured enforcement stages? | **P** `P2/dependencies/resolved-lock.json`, final wrapper/Task harnesses, ten final APK/build/install identities, `P2/executions/primary/{wrapper,task}/*/device/`, and `review/mechanism/`. [Repository lock](../../research/20261004-p2-p3/P2/dependencies/resolved-lock.json) pins dependencies; [mechanism review](../../research/20261004-p2-p3/review/mechanism/MECHANISM_REVIEW.md) preserves the cause chain. Align Task class index to wrapper output position, not list rank. |
| P3 qualified publisher reference? | **P** `P3/retrieved/I06-tfhub-lite-model`, `F07-pinned-lite-card`, `F10-pinned-parent-card`, `F11-explicit-class-order` bodies/records; `P3/analysis/artifact-bridge.json`, `reference-chain.json`, `full-display-order-comparison.json`. Follow exact graph/weights/output bridge, card→parent relation and prescribed background removal; compare all positions. |

P2 uses wrapper Support 0.4.4/TFLite Java/native 2.13.0 and Task Vision/Base 0.4.4
on one API-30 x86_64 AVD, CPU/one thread. Task's embedded interpreter version
remains unknown. Its public deletion exception is `IllegalStateException`
(native-address wrapper) with `IllegalArgumentException` cause identifying
1,000 classes versus 999 labels; it is not evidence of a missing native library.
Task classify combines internal stages; no Task raw tensor was captured.

P3's TFHub artifact is pinned as
`7276a936443685daae8612fc3cb9370247cb1f4966286cd95e02c44e1183f0dd`;
the catalog commit is `81fdea8ffa53b5acbd66a012d17fb8f9602c714b`; the external
1,001-line reference is
`536feacc519de3d418de26b2effb4d75694a8c4c0063e36499a46fa8061e2da9`.
The [P3 report](../../research/20261004-p2-p3/P3/EXPERIMENT_P3_RESULTS.md)
pins both cards and explains duplicates. Its 999/1,000 disagreements are display
positions, not prediction errors or independent success trials. Deletion was not
part of that reference comparison.

Existing checks, once the package is supplied:

- [verify_archive.py](../evidence-recovery-20261005/verify_archive.py) checks an
  archive against the independently pinned checksum-file hash, without extraction.
- [stage_evidence.py verify](../evidence-recovery-20261005/stage_evidence.py)
  checks a recovered package's bytes and file set against that pin.
- [check_focal_coverage.py](../evidence-recovery-20261005/check_focal_coverage.py)
  accepts `--package` and a new external `--output`; checks APK/model linkage,
  complete stages/inputs/raw/decoded records and successful shared P2 pairs.
  It does not recompute graph preservation or authenticate P3 authority.
- [read_existing_outcomes.py](../../research/20261004-significance-review/scripts/read_existing_outcomes.py)
  accepts relocated E1/E2 and P2/P3 roots, reads a fixed 59-file selection and
  stored P3 comparisons. Inspect every output boolean: exit zero alone is not
  a complete PASS. It does not rederive the reference bridge.
- [Pre-audit area scripts](../agent-preaudit-20261007/README.md) and the
  [P3 analyzer](../../research/20261004-p2-p3/P3/scripts/analyze_reference.py)
  document deeper checks. They retain historical absolute paths/dependencies;
  inspect and adapt copies in a new external directory before use. Do not run
  sealing/finalization scripts or import write-on-import historical modules
  against preserved evidence.

These tools were read as source this round; they were not run on absent evidence.
The matrix's structural-population and E5 baseline rows additionally rely on the
dated [baseline report](../../sources/metadata-contract-audit-20261004T062010Z/baseline/RESULTS.md).
Its raw `baseline/conditions/` family is intentionally outside the focal package;
include that bounded family if delivering raw support for those rows. Do not
replace it with missing later E5 reconstruction records.

## B. Rebuild and execute in a fresh environment

This is separate from A and was not performed here. The existing
[command guide](../../docs/reproduction/COMMANDS.md),
[toolchain index](../../docs/reproduction/TOOLCHAIN.md) and input index describe
pinned tools, absent configuration and path adaptation. A new execution needs
models, dependency binaries, SDK/AVD, generated source/build outputs and fresh
run directories; those are deliberately excluded from Git. A successful source
test or saved-record reader is not a new Android build/inference result. Current
editorial work does not need to recover auxiliary Hand/E4/65-fixture histories.

## C. Persistent anonymous reviewer delivery

**OPEN:** no persistent anonymous evidence URL is supplied or verified in this
revision. A historically verified local package is not reviewer access. The
author must approve the access/destination and redistribution/anonymization scope,
then test retrieval and identity for the retained evidence. This task neither
uploads evidence nor creates a Release, changes visibility or selects new storage.
Source-only Git delivery and an unmerged manuscript PR do not close this item.

## Six author questions; all unsigned

Reviewer name/role: **PENDING**. Date: **PENDING**. Inspected manuscript digest:
**PENDING**. Record actual observations and a conclusion for each question; agent
agreement, tool PASS and PR merge cannot supply an author's signature.

| Question | Human observation / conclusion |
|---|---|
| 1. Do source, compiled-call trace and attributed execution records establish a call to the actual generated getter after `process`, with no replacement decoder? | PENDING |
| 2. Do model/resource/APK identities and separate G/W/O, M, F, H comparisons support the stated intervention surface and restoration scope? | PENDING |
| 3. Do complete E1 stage records/stacks show the caught getter failure after successful process, with corresponding raw outputs preserved? | PENDING |
| 4. Do full E2 mappings/score bits for both inputs show 999 changed strings and restoration, using verified output positions and appropriately limited chronology? | PENDING |
| 5. Do P2's final configurations, public return stages and cause chain support the comparison while retaining native-integration/interpreter and Task-observability limits? | PENDING |
| 6. Do the P3 artifact bridge, exact parent card, explicit offset and pinned full map justify qualified publisher display-order agreement without claiming image truth or stable class-ID lineage? | PENDING |

Author verification can inspect saved evidence without pretending to be a new
independent researcher reproducing every experiment. Its scope must be stated.
Existing historical human-audit targets stay unchanged; sign against this new
manuscript's actual digest only after making the corresponding observations.
