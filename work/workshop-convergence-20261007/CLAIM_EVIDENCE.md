# Workshop claim disposition and audit crosswalk

This is the current compact claim map, not a replacement for the detailed
[16-claim ledger](../paper-rewrite-20261004/CLAIM_EVIDENCE.md) and its
[48-source index](../paper-rewrite-20261004/claim-sources.json). Those files and
their hashes are preserved. [revision-map.json](revision-map.json) pins this
manuscript, its predecessor and the added recovery records. All human statuses
remain **PENDING**; automated editorial review is not a human verdict.

Evidence levels: **focal recovered** means the selected original E1/E2,
construction-audit or P2/P3 family is in the locally verified package. It does
not mean every causal/reference assertion was rederived in the recovery.
**Historical report/source** means the retained source/report supports the
wording, without a complete raw family in that selected package. **Unrecovered
later raw** is distinct from an intentionally omitted secondary family.
This revision runs no model experiment and newly hashes no model/APK.

| Existing ID | Current section / disposition | Evidence level and retained boundary | Human route |
|---|---|---|---|
| C1 | `sec:contracts`; retained | Analytical definitions and pinned implementation review. S/I/D are different questions; P is experimental preservation, not correctness. | HA03/HA09/HA10 |
| C2 | `sec:e1`, `sec:e2`; retained | Focal recovered; graph/buffer, resource, generated-code and tested-output comparisons remain separate. Recovery did not independently rederive all graph/binding assertions. No whole-APK identity. | HA02/HA03 |
| C2R | `sec:e2`; shortened | Focal recovered historical construction audit; installed tools reused. New AVD/build outputs, no independent human reproduction or old/new DEX equality. | HA01/HA02/HA03/HA04 |
| C3 | `sec:e1`; primary claim | Focal recovered actual getter failure after successful `process`, for both fixed inputs. Caught exception, injected deletion, no natural original defect or application-crash claim. | HA01/HA04 |
| C4 | `sec:e2`; primary claim | Focal recovered permutation/reversal; full returned lists and scores. 999/1,000 strings change. Output/list positions are not the unset wrapper category-index field. | HA05 |
| C5 | `sec:p3`; retained | Focal P3 references and saved comparison rows recovered. Qualified graph-equivalence bridge and publisher display order; stable class IDs and release-time/training lineage unresolved. Recovery did not re-establish reference authority. | HA07 |
| C6 | `sec:consumers`; primary claim | Focal recovered ten P2 units and 18 actual input observations; Task deletion fails before inputs. Same Android environment, differing native integrations, Task raw tensor unobserved. | HA06 |
| C7 | `sec:hand`; shortened boundary | Historical report/source; outside focal package. Reference bridge, identical syntax repair before generic bytecode result, unchanged official Task fields on one image. No universal insensitivity or complete swap repair. | HA08 |
| C8 | `sec:preflight`; retained summary | Historical report/source; outside focal package. Fifteen new graphs, zero external runtime executions; compilation/fallback exclusions retained. Not nine natural defects. | HA09a |
| C8D | Omitted from short draft; 11/10 retained in full companion, detailed 46/105/23 counts in preceding ledger | Historical report/source. Development data informed the work; isolated decoder probes are not actual generated Android calls. | HA09a |
| C9 | `sec:preflight`; retained baseline finding | Historical report/source; focal P2 does not alone authenticate the complete three-way baseline comparison. Five core conditions, zero extra E5 rejection. Limited patterns, no general data flow or runtime obligations. | HA09b |
| C9E | `sec:preflight`; dynamic abstention retained; 65-fixture scope in full companion, full tally in preceding ledger | Historical evaluation report remains distinct from the unrecovered later pinned E5 catalog. No detector accuracy; dynamic-signature abstention includes known isolated failure. | HA09b |
| C10 | `sec:preflight`; explicitly report-supported limitation | Preserved report/probe/helper source; later raw probes unrecovered. Java/Python parser mismatch is a limitation of our own checks, not a new Android/natural-library failure. No freshly verified correction claim. | HA09c |
| C11 | Introduction, `sec:discussion`, `sec:related`; retained | Source/public report #770, existing unsupported segmentation-route antecedent. No reproduction or natural-case denominator increment. | HA10 |
| C12 | Introduction, `sec:related`; narrowed | Controlled empirical characterization and configured stage comparison. Six directly discussed papers among the prior seven full-text reviews. No general analyzer/constraint novelty or field-wide firstness. | HA10 |
| C13 | `sec:discussion`, `sec:validity`; coverage implications (table in full companion) | Implications of existing observations and known integrity behavior, not measured operational benefit. Whole-package hashes, Task checks and actual getter/reference tests remain strong defenses. | HA10 |

## Evidence availability changed; experimental findings did not

The [recovery record](../evidence-recovery-20261005/delivery-record.json) identifies
2,749 selected payload files and complete archive-member verification. Saved checks
cover 26 executed APKs, 14 initial builds and 34 complete records, including replay
and the separate installed-toolchain construction audit. These totals must not be
substituted for the manuscript's primary E1/E2 16-input or P2 18-input denominators.

Hand, development/external-corpus and checker/baseline raw families are **outside
the selected package**, not all declared lost. The later `repro-*` evidence and
parser records are **unrecovered after the bounded search**. In particular the
later E5 result pin `bf49a475696eec4b38fb17587f6541a8393da14297e5dca1d433a051ba166e79`
cannot be replaced by an older catalog. See the separate
[missing-material inventory](../evidence-recovery-20261005/MISSING.md).

## Human audit target

Use the existing [inspection checklist](../../docs/human-audit/CHECKLIST.md) and
[unsigned template](../../docs/human-audit/REVIEW_RECORD_TEMPLATE.md), but record
the **new manuscript digest from revision-map.json** plus this crosswalk. The old
`docs/human-audit/audit-map.json` remains an intentionally pinned preparation
snapshot of the preceding manuscript. Its old `CURRENT_MANUSCRIPT.json` digest
identifies that earlier pointer, not the newly updated one. No audit verdict is
carried forward. A person must record scope and evidence for the retained claims;
moving detailed counts out of the paper does not mark them verified.
