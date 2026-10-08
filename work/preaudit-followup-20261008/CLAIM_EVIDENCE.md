# Post-audit claim disposition and human crosswalk

This is the current compact claim map. It preserves the IDs of the detailed
[16-claim ledger](../paper-rewrite-20261004/CLAIM_EVIDENCE.md) and its
[48-source index](../paper-rewrite-20261004/claim-sources.json). Those files and
their hashes are preserved. [revision-map.json](revision-map.json) pins these
manuscripts, predecessors and evidence indexes. All human statuses
remain **PENDING**; automated editorial review is not a human verdict.

Evidence levels: **focal recovered + agent readback** identifies the selected
original E1/E2, construction-audit and P2/P3 package plus the subsequent pre-audit's
fresh saved-byte comparisons, static disassembly and observation/reference checks.
These are not new model executions or independent authentication of old executions.
**Secondary partial** identifies present original evidence outside the focal
package and the explicitly incomplete pre-audit scope. **Unrecovered later raw**
remains distinct from those present original families. The new parser follow-up
has its own plan and evidence history; it cannot close the missing reconstruction
catalog or inherit a human verdict.

| Existing ID | Current section / disposition | Evidence level and retained boundary | Human route |
|---|---|---|---|
| C1 | `sec:contracts`; retained | Analytical definitions and pinned implementation review. S/I/D are different questions; P is experimental preservation, not correctness. | HA03/HA09/HA10 |
| C2 | `sec:e1`, `sec:e2`; retained | Focal recovered + agent readback: all 165 nonmetadata buffers, schema-known computation/output order, resource/prefix and generated-code comparisons supported within scope. Exact model/APK asset linkage checked; no native interpreter-buffer interception. Code equality remains within the declared build families, not entire APK equality. | HA02/HA03 |
| C2R | `sec:e2`; shortened | Focal recovered historical construction audit; installed tools reused. New AVD/build outputs, no independent human reproduction or old/new DEX equality. | HA01/HA02/HA03/HA04 |
| C3 | `sec:e1`; primary claim | Focal recovered + agent readback: actual compiled getter calls, saved exception stacks/stages and full primary raw comparisons support failure after successful `process`. Caught exception, injected deletion, no natural original defect or application-crash claim. | HA01/HA04 |
| C4 | `sec:e2`; primary claim | Deterministic cyclic transform, full returned lists/scores, 999/1,000 changed strings and reversal checked. Historical predeclaration timing remains independently unestablished; categorical timing claim removed. Positions are not the unset wrapper category-index field. | HA05 |
| C5 | `sec:p3`; retained | Agent rechecked actual saved cards, reference bytes, graph/buffer/output bridge and full display mapping. Qualified publisher display order; stable class IDs, release-time/training lineage and authenticated historical retrieval unresolved. | HA07 |
| C6 | `sec:consumers`; primary claim | Ten P2 units, 18 actual inputs, exact Task cause chain and eight successful cross-consumer pairs checked from saved records. Task deletion precedes inputs. Same Android environment, differing native integrations, Task raw tensor unobserved. | HA06 |
| C7 | `sec:hand`; shortened boundary | Secondary partial: source/metadata/buffer bridge, exact separator repair, saved javap and eight decoded records on one image checked. No new Hand-class disassembly, source-to-installed-library equivalence or Task run. No universal insensitivity or complete swap repair. | HA08 |
| C8 | `sec:preflight`; retained summary | Secondary partial: freeze/download/payload identities, saved group counts and compile/warning records checked. Fifteen canonicalizations and prior-graph exclusion bridges not independently recomputed. Zero external runtime executions; not nine natural defects. | HA09a |
| C8D | Omitted from short draft; 11/10 retained in full companion, detailed 46/105/23 counts in preceding ledger | Historical report/source; detailed development counts not independently rechecked. Development data informed the work; isolated probes are not actual generated Android calls. | HA09a |
| C9 | `sec:preflight`; retained baseline finding | Secondary partial: all 25 core baseline records checked, five conditions and zero extra E5 rejection. No fresh baseline execution or full getter reevaluation. Limited patterns, no general data flow or runtime obligations. | HA09b |
| C9E | `sec:preflight`; dynamic abstention retained; 65-fixture scope in full companion, full tally in preceding ledger | Original 65 identities/judgments checked, distinct from the missing later pinned E5 catalog. Full decoder reevaluation and raw dynamic Gesture probe not checked. No detector accuracy or new all-65 correction validation. | HA09b |
| C10 | `sec:preflight`; fresh bounded parser evidence | New isolated JVM run uses actual Support 0.4.4 FileUtil/TensorLabel: original succeeds, VT yields 999 labels and exception, U+2028 yields 1,000 labels and succeeds; Python counts 1,000/1,000/1,001. Unchanged helper matches complete strings in 22 existing valid cases and abstains on three malformed cases. No fresh Task, whole-checker or all-65 regression; historical raw probes/catalog remain missing. This concerns our approximation, not a new Android/natural-library defect. | HA09c: new probe; historical gap stays open |
| C11 | Introduction, `sec:discussion`, `sec:related`; retained | Actual saved #770 issue and member reply rechecked. Existing unsupported segmentation-route antecedent; no natural-artifact reproduction or denominator increment. | HA10 |
| C12 | Introduction, `sec:related`; narrowed | Controlled empirical characterization and configured stage comparison. Prior bounded seven-full-text review remains its own history; no new literature/full-text audit here. No general analyzer/constraint novelty or field-wide firstness. | HA10 |
| C13 | `sec:discussion`, `sec:validity`; coverage implications (table in full companion) | Implications of existing observations and known integrity behavior, not measured operational benefit. Whole-package hashes, Task checks and actual getter/reference tests remain strong defenses. | HA10 |

## Keep observation, recovery and new execution histories separate

The [recovery record](../evidence-recovery-20261005/delivery-record.json) identifies
2,749 selected payload files and complete archive-member verification. Saved checks
cover 26 executed APKs, 14 initial builds and 34 complete records, including replay
and the separate installed-toolchain construction audit. These totals must not be
substituted for the manuscript's primary E1/E2 16-input or P2 18-input denominators.

Hand, development/external-corpus and checker/baseline raw families are present
**outside the selected package** and were partly inspected in the pre-audit.
The later `repro-*` evidence and parser records are a separate missing history.
In particular the
later E5 result pin `bf49a475696eec4b38fb17587f6541a8393da14297e5dca1d433a051ba166e79`
cannot be replaced by an older catalog or new isolated probe. See the separate
[missing-material inventory](../evidence-recovery-20261005/MISSING.md).

## Human audit target

Use this crosswalk and [current human handoff](HUMAN_HANDOFF.md) with the existing
[inspection checklist](../../docs/human-audit/CHECKLIST.md) and
[unsigned template](../../docs/human-audit/REVIEW_RECORD_TEMPLATE.md), but record
the **new manuscript digest from revision-map.json** plus this crosswalk. The old
`docs/human-audit/audit-map.json` remains an intentionally pinned preparation
snapshot of the preceding manuscript. Its old `CURRENT_MANUSCRIPT.json` digest
identifies that earlier pointer, not the newly updated one. No audit verdict is
carried forward. A person must record scope and evidence for the retained claims;
moving detailed counts out of the paper does not mark them verified. The
pre-audit's own `audit-index.json` remains bound to the preceding four-page
source; its scoped findings can inform this target but no human verdict transfers.
