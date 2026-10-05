# Human audit entry — verification pending

This entry prepares a person to audit the current manuscript. **No human review
has been completed or signed here.** Agent preparation, source checks, manuscript
review and earlier automated experiments remain distinct from human verification.

The target is the manuscript delivered by PR #9 at repository commit
`ba1b5c5a0e5df44c28e7232b044bc6741d29bb47`:

- [Manuscript](../../work/paper-rewrite-20261004/manuscript/paper.tex), SHA-256
  `43b92dbb0230fc1232093be6a33fca435188dc2f43ae499ac6bfa8e362f37bb2`.
- [Claim–evidence ledger](../../work/paper-rewrite-20261004/CLAIM_EVIDENCE.md)
  and [source index](../../work/paper-rewrite-20261004/claim-sources.json).
- [Current manuscript pointer](../CURRENT_MANUSCRIPT.json). If its target/digest
  changes, record and review the changed claims before carrying forward a verdict.

## Start the audit

1. Read the [checklist](CHECKLIST.md). HA01–HA07 cover the focal execution,
   preservation, same-Android comparison and qualified reference. HA08–HA10
   cover the secondary claims and interpretation. Use manuscript labels and
   ledger IDs to locate claims, rather than relying on changing page numbers.
2. Copy the [human review record template](REVIEW_RECORD_TEMPLATE.md) to a new
   review record. Leave identity, observations and attestation blank until the
   person performing the review supplies them. Declare scope and relationship
   to the work; author verification is not independent human reproduction.
3. Locate the required bytes using the checklist, [input inventory](../reproduction/INPUTS.md)
   and [toolchain inventory](../reproduction/TOOLCHAIN.md). Record expected-hash
   provenance and observed identities. Source files in Git are not the excluded
   models, generated code, APKs, device records or raw outputs.
4. Inspect/recompute the relevant observations and record what actually happened,
   including disagreements and missing material. Earlier reported outcomes are
   comparison targets, not values to force. Checking one witness is not checking
   all conditions, inputs or output positions.
5. The human records a scoped conclusion for each item. A completed checklist
   preparation or a zero-exit automated command does not supply that conclusion.

The [machine-readable map](audit-map.json) ties each audit item to the pinned
manuscript, ledger claims, source IDs, evidence families and initially pending
human status. It is an index, not an executable validator or a set of verdicts.
Necessary review text may be committed through a PR; raw evidence, generated
outputs and review execution logs remain outside Git.

## Keep evidence histories separate

These roots are historical provenance locators, not portable download links.
Their current contents have **not** been checked for this preparation task.

| Family | Historical root / role | What the earlier handoff established |
|---|---|---|
| ORIGINAL | `/workspace/metadata-contract-e2e-20261004T030536Z` | Selected model/resource/input bytes and one generated-source example were rehashed; a finite readback inspected primary E1/E2 observations. This was not every APK/class or all archive entries. |
| BUILD_AUDIT | `/workspace/metadata-contract-audit-20261004T062010Z` | Reports describe a separate E1/E2 construction audit with installed tools, new outputs/signing key/AVD and an added AssetManager hash observation. It is not the primary run or a fresh toolchain installation. |
| P2P3 | `/workspace/metadata-contract-p2p3-20261004T073824Z` | Selected P2 deletion records and stored P3 comparisons were read back. Selected reference inputs were rehashed; the full graph/reference bridge and all P2 units were not recomputed by that readback. |
| RECONSTRUCTION | Separate `/workspace/repro-*` roots | The reproduction handoff recorded missing roots, the external evidence index and the required frozen E5 catalog at their checked locations. That earlier exact-path result is not a new availability check here. Older ORIGINAL records cannot fill those gaps. |

Read the dated availability and verification levels in
[inputs.json](../reproduction/inputs.json) and [validation.json](../reproduction/validation.json).
A manifest-file hash does not validate its entries. Local presence does not
establish a usable external deposit. The [deposit plan](../reproduction/DEPOSIT_PLAN.md)
remains a separate task; document missing evidence rather than silently substituting
a different run, model version or newly generated catalog.

## Commands and inspection methods

Use the [current command guide](../reproduction/COMMANDS.md) for prerequisites,
new external output directories and distinctions between source checks, saved
record readback, recomputation and fresh execution. This entry does not require
a new Android run merely to prepare the audit.

The finite reader covers 59 selected old files and can return zero while a
comparison boolean is false. It does not inspect every APK, recompute graph
preservation, establish P3 reference authority or execute inference. The full
reconstruction reader needs different evidence and a separately pinned E5
manifest. Inspect the commands and the actual output fields before drawing a
conclusion; neither reader automatically signs a human item.

Historical checklists remain unchanged:
[E1–E7](../../sources/metadata-contract-e2e-20261004T030536Z/HUMAN_AUDIT.md),
[P2/P3](../../research/20261004-p2-p3/HUMAN_AUDIT.md), and
[P3](../../research/20261004-p2-p3/P3/HUMAN_AUDIT.md).
Their `bash commands.sh verify` instruction is not a current portable entry:
it assumes excluded material and fixed historical paths; its optional record
mode writes under the evidence root. Follow the maintained command guide rather
than replaying old command histories against saved evidence. P3's current target
is qualified **display-order agreement**, not generic class-ID or prediction truth.

## Human status vocabulary

| Status | Required meaning |
|---|---|
| PENDING | No human conclusion has been supplied. This is the initial state of every item. |
| SUPPORTED_WITHIN_SCOPE | A named human inspected the necessary evidence for the stated scope and records observations supporting that scope. This is not universal correctness or a new runtime result. |
| DISCREPANCY_FOUND | Observed evidence contradicts a specified claim or expected identity. Preserve the discrepancy and its manuscript consequence. |
| BLOCKED_MISSING_EVIDENCE | Necessary bytes or provenance are unavailable; list them. A source/report review alone cannot establish the missing runtime/preservation result. |
| INCONCLUSIVE | Some inspection occurred, but interpretation or coverage does not resolve the stated scope. Report completed and uncompleted parts separately. |

An excluded item needs a written scope justification and remains outside any
completion claim; it is not a supported item. Each checklist item can contain
several comparisons. Record sub-results if they differ; do not hide an unverified
comparison behind one successful check. No overall human-audit completion is
inferred automatically from a count of statuses.

## Preparation checks

Agent checks matched the target manuscript, ten upstream index/checklist hashes
and all 48 source identities in the editorial ledger. The map covers all 16
claims through ten items; all 13 item/subitem status rows remain PENDING, and
the ten inspection links resolve. The repository source check passes, including
354 unchanged imported files. Its 12 existing warnings concern seven unavailable
historical locators and five unchecked external manifest digests.

Two agent reviews inspected the new entry against repository sources. Their
corrections made E1 full numerical comparison, all ten P2 executed APKs and the
separate rebuild evidence routes explicit. These are documentation checks;
excluded raw evidence, current external availability and experimental results
were not newly verified. No model experiment or human review was performed.
