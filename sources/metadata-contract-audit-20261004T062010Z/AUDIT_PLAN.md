# Agent technical audit plan

Started: 2026-10-04 06:20:10 UTC. This is an automated, same-workspace technical audit, not independent human verification.

## Frozen inputs

- `/workspace/metadata-contract-e2e-20261004T030536Z`: sealed E1/E2/E3/E4/E5/E7 evidence; all files read-only.
- `/workspace/metadata-contract-paper-rewrite-20261004T052625Z`: sealed manuscript revision and claim map; read-only.
- `/workspace/metadata-contract-paper` and `/workspace/hand-contract-repro`: archived prior evidence and installed toolchains; no historical evidence edits.
- `/workspace/metadata-contract-next/TODO.md`: planning document; save the pre-audit version, then update actual statuses at completion.

## Questions and assignments

1. Preservation agent: recompute model/metadata/associated-file differences, APK asset identities, generated source/classes/DEX equality, saved raw output and decoded result comparisons, and getter reachability from source/bytecode.
2. Rebuild agent: fresh output directory and AVD; regenerate and build E1/E2 from saved inputs, execute the actual unchanged generated public interface, and add a disclosed harness-only asset-digest observation. Reuse pinned installed tools; this does not rebuild the complete toolchain from archived distributions. Preserve deviations and shut down the emulator.
3. Baseline agent: separately exercise official metadata reading/population, an implementation-matched decoder baseline, official Linux Task initialization, and unchanged E5 logic on core fixtures. Redirect all evidence writes to this audit directory. Identify exact source enforcement and checker limitations.
4. Claim agent: audit manuscript claims, counting units, E3 attribution, E4/E5 coverage, and Hand source/graph bridge and scope.
5. Literature agent: bounded full-text audit of MLGuard, DocTer, ACETest and DARA. Preserve retrieved files and provenance. Inaccessible material remains unverified; no exhaustive novelty claim.
6. Root: before/after manifest integrity, cross-review findings, consolidated machine-readable and prose results, manuscript-impact note and TODO update.

## Decisions fixed before new runs

- No modifications to generated Java to obtain a desired result. Any harness addition is recorded separately.
- Old APK replay does not count as a fresh build. New builds reuse the installed pinned toolchain and are labeled accordingly.
- E1 expected failure and E2 expected association change are hypotheses to verify, not assumptions.
- No new models or new mutation rules. No Android Task comparison in this audit; P2 remains a separate experiment.
- PASS means the explicitly stated audit assertion is supported, not that a model is universally correct. FAIL means an assertion failed. UNVERIFIABLE means required evidence or execution is unavailable. A consumer rejecting a mutant can support an audit assertion.
- S, I and D remain separate. P is intervention preservation. Associated label payload changes are not automatically changes to embedded metadata tables.
- No class-order oracle or human review is assumed. No prevalence, accuracy, production-crash, natural EfficientNet defect or independent-reproduction claim.
- Preserve negative outcomes, command output and all deviations. Do not rerun selectively to obtain an expected result.

## Deliverables

`AUDIT_REPORT.md`, `results.json`, sub-audit reports/scripts/commands, `MANUSCRIPT_IMPACT.md`, `SHA256SUMS`, and an updated external TODO with an archived snapshot here. Old sealed evidence and manuscript stay unchanged.
