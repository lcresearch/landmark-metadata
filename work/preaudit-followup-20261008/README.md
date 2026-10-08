# Follow-up to the agent pre-audit

This revision addresses the two actionable findings in the
[frozen pre-audit](../agent-preaudit-20261007/AUDIT_REPORT.md): E2 chronology and
the missing later label-parser records. It retains the controlled E1/E2 and
same-Android comparison as the main contributions, the qualified P3 display
reference, Hand's bounded role, #770 as antecedent, and E5 as a supporting tool.

- [Revised short manuscript](manuscript/paper.tex)
- [Detailed companion](manuscript/paper-full.tex)
- [Claim–evidence crosswalk](CLAIM_EVIDENCE.md)
- [Changes and interpretation](CHANGES.md)
- [New isolated parser experiment](parser/REPORT.md)
- [Current human continuation sheet](HUMAN_HANDOFF.md)
- [Revision identities and claim statuses](revision-map.json)
- [Build and verification](BUILD_REVIEW.md)

The 20261008 directory name is the UTC work date. This is a new source area,
based on verified PR #13 head `57ff5585039e7f63de54a67981d5d98cb9ba84e8`.
The previously audited manuscripts, claim maps, audit records and imported
sources stay byte-identical. This branch is stacked on `audit/agent-preaudit`;
it does not merge PR #13 or its prerequisites.

The retained deterministic permutation result does not depend on certifying its
historical predeclaration. Its saved freeze lacks a timestamp. Mutable local
times are consistent with the declared order but cannot independently prove it.
The new short paper drops that chronology claim; the full companion explains
the evidence limit explicitly.

The bounded search did not recover the old parser/Task records or pinned E5
catalog. A separately recorded JVM run confirms the two parser/decoder outcomes
with actual Support 0.4.4 APIs, an ordinary LF control and synthetic scores.
The unchanged helper also matches 22 existing valid cases and abstains on three
malformed inputs. It does not run Task, the entire checker or all 65 fixtures.

All human statuses remain **PENDING**. Agent readback and separately recorded
new isolated-library execution do not complete human author verification, replay
the Android experiments, recover missing history, or deliver durable anonymous
evidence. Models, dependencies, raw outputs, compiled probes and rendered papers
remain outside Git.
