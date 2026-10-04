# Independent checker and evidence-auditor review

This review inspects the repository policies, current manuscript, the source tree,
and the E5 / static-baseline / preservation / rebuild / claim-recomputation paths.
It supplies new executable counterexamples rather than treating the previous
review as evidence. Repository historical snapshots were not changed. No claim
below establishes that a historical model execution was fabricated or incorrect.

The source inventory contains 187 Python/Java/Shell file instances and 97 unique
byte sequences (5,569 source lines); 90 instances duplicate another file. See the
external `source-inventory.json`. An inventory or successful syntax check is not
a behavioral proof of every source file.

## 1. High: E5 and the simple baseline use different label-line semantics from the actual consumer

Locations under `sources/`:

- `metadata-contract-e2e-20261004T030536Z/scripts/preflight.py:93` (also `E5/preflight.py:93`).
- `metadata-contract-paper/scripts/suite_static.py:87`–`95` and the E4 frozen copy.
- `metadata-contract-audit-20261004T062010Z/baseline/audit_one.py:97`–`114`.

Python `str.splitlines()` splits vertical tabs and Unicode line separators;
Java `FileUtil.loadLabels` in the pinned Support 0.4.4 uses a reader with CR/LF
line semantics. The checker therefore computes the wrong *loaded* label count.
This affects the supported, unchanged generated Java template, independently of
the already disclosed limitations of the getter/processor regular expressions.

Actual experiment used the exact EfficientNet artifact
`6c7ab0a6e5dcbf38a8c33b960996a55a3b4300b36a018c4545801de3a3c8bde0`,
the unmodified E5 command and generator, and actual pinned FileUtil/TensorLabel
classes. Only the associated-label payload was mutated. Every condition passed
official metadata population; all three generated-source hashes were identical;
all pre-ZIP prefixes, canonical graphs, and nonmetadata buffers were preserved.

| Declared condition | E5 count / decision / exit | Actual FileUtil + TensorLabel | Simple baseline | Official Linux Task initialization |
|---|---|---|---|---|
| Original LF file | 1000 / compatible / 0 | 1000 labels, 1000 categories, PASS | compatible | PASS |
| Replace first LF with vertical tab | 1000 / compatible / 0 | 999 labels; `IllegalArgumentException: Label number 999 mismatch the shape on axis 1` | compatible | FAIL: expected 999 labels |
| Insert U+2028 plus text inside first label | 1001 / incompatible / 2 | 1000 labels, 1000 categories, PASS | incompatible | PASS |

Thus both a false compatible decision and a false incompatible decision are
demonstrated. Agreement with this simple baseline cannot independently validate
the line-reading assumption: both implementations share the same defect.

Evidence:

- `/workspace/repro-audit/independent-audit/label-parser/results.json`
- `/workspace/repro-audit/independent-audit/label-parser/baseline-task-comparison.json`
- Per-condition E5 reports, copied source digests, compiled-probe command,
  Java stdout/stderr and model/resource digests are in the same external directory.

Reproduction after recovering the pinned Python/JDK/JAR prerequisites:

```bash
python /workspace/repro-audit/independent-audit/probe_label_parser.py \
  --output-dir /workspace/repro-audit/independent-audit/label-parser-next
```

The probe calls the repository's unchanged `DecoderProbe.java` with 1000 fixed
synthetic float scores. It executes the real decoder libraries and Task
initialization, but performs no Android wrapper execution or model inference.
These are deliberately injected new label fixtures, not newly discovered natural
model defects, and not evidence that any of the original 65 E5 fixture outcomes
was wrong. The current manuscript's line 206 parser caveat does not describe this
additional input-parsing failure. Keep the historical counts, but add the new
counterexamples and fix Java-compatible line parsing in a new maintained source
area before presenting the checker as reliably implementing that consumer's
preconditions. Add differential checks against the actual Java loader.

## 2. Medium: rebuild auditor can report successful reproduction without a single raw observation

`metadata-contract-audit-20261004T062010Z/rebuild/scripts/audit_results.py:38`
records missing raw files as `UNVERIFIABLE` and continues. Lines 64–66 check eight
phase records but do not require 16 complete observations or five configurations.
Line 72 writes a fixed successful E1/E2 interpretation; line 74 exits nonzero only
for `FAIL`, ignoring `UNVERIFIABLE`.

The executed synthetic fixture contains eight phase records with no raw files at
all. The unchanged auditor logic produces:

```json
{"exit_code": 0,
 "summary": {"PASS": 56, "FAIL": 0, "UNVERIFIABLE": 16},
 "input_observations": 0,
 "narrative_claims_reproduced": true}
```

The fixture also has six distinct placeholder model byte sequences, rather than
the required five; this is recorded but not rejected. Synthetic source/class/DEX
and APK entries are byte placeholders, not executed models. This intentionally
isolates the auditor's missing-evidence policy.

The full historical pipeline has additional protection:
`finalize_index.py:15` requires both FAIL and UNVERIFIABLE to be zero, and
`verify_completed_audit.py` reads raw files independently. Therefore this is a
bug in the standalone auditor/its report, not proof that the complete historical
pipeline accepted missing evidence. Required evidence must gate the auditor's
own status, exit code, and positive prose; a later caller should not need to
repair its success semantics.

## 3. Medium: preservation auditor's exit code disagrees with its overall FAIL

`metadata-contract-audit-20261004T062010Z/preservation/audit_preservation.py:335`–`346`
merges a companion bytecode failure into `result['status']='FAIL'`, but line 354
computes exit status only from the local `status_counts['FAIL']`.

Executing the unchanged final block with local checks PASS and a companion
`{"status":"FAIL"}` produces an overall FAIL JSON and stdout, but exit code 0.
A shell runner that checks return status can treat that failed audit as success.
Derive exit status from the final aggregate result, and explicitly define how
required unavailable companion evidence affects it.

Related source-only finding: `preservation/bytecode/audit.py:78`–`89` writes overall
PASS and several review findings as literals. Computed `equality`,
`apk_dex_matches_build`, and manifest-recheck booleans do not gate those labels.
This file is suitable for preserving conclusions from a particular reviewed run;
it is not a reusable automatic verifier as written. The broader preservation
script independently checks several of these identities, so this does not imply
that the historical bytecode evidence actually differed.

## 4. Medium: count/report generation can claim a successful test that was absent

`metadata-contract-e2e-20261004T030536Z/scripts/summarize_e5.py:19` computes
`all(...)` over the failed-getter subset without requiring that subset to exist.
Line 25 writes historical 65/27/etc. counts and success prose unconditionally.
With input `{"fixtures":[]}`, the actual summary script exits 0,
reports `known_getter_failure_flagged=true`, and writes both “All 65 semantic
judgments abstain” and “D flags 27 selected category paths.” Machine counts are
correctly zero; the boolean and prose disagree with the evidence.

The E4 summary has related fixed-prose behavior independently tested by the
external-suite reviewer in `/workspace/repro-external/failure-injection/`.
Treat these scripts as historical report templates until their positive claims
are conditional on observed data and required denominators.

## 5. Medium: Python optimization removes evidence assertions

`metadata-contract-audit-20261004T062010Z/claims/recompute.py` contains 47 assert
statements. A harmless probe of the actual line 76 count assertion with empty
counts raises `AssertionError` under normal compilation but accepts the input
under `compile(..., optimize=1)`, equivalent to the assertion elimination of
`python -O` / `PYTHONOPTIMIZE`. The final `assertions: PASS` at line 121 is a
literal. Other integrity/download scripts have the same design.

The test did not download, alter, or execute any unverified artifact. It
demonstrates the verifier logic only. Use explicit validation exceptions for
mandatory checks (or reject optimized interpreters before work); do not weaken
signatures, TLS or expected hashes to complete setup. Ordinary nonoptimized
historical runs are not invalidated by this counterexample.

## Reproduction and scope

All synthetic auditor probes can be repeated with:

```bash
python /workspace/repro-audit/independent-audit/probe_audit_failures.py
```

Results are in `/workspace/repro-audit/independent-audit/probe-results.json`.
The rebuild probe executes the full historical script through its AST, changing
only the imported external path bindings. The preservation probe executes the
unchanged final aggregation block. The optimized-assertion probe executes one
unchanged assertion in a deliberately invalid, harmless namespace. These scopes
are recorded in the result JSON rather than being presented as historical
evidence revalidation.

Previously disclosed scope limits remain limits, not newly detected software
bugs: E3 mixes consumer/platform/runtime configuration; E2 does not establish
independent class-order correctness; Hand does not establish a second executed
Android failure; the source repository excludes raw historical evidence; human
verification is pending. New independent reruns elsewhere in this session must
state exactly which of those gaps they actually address.

Safe source-only handoff files: `probe_audit_failures.py`, `probe_label_parser.py`,
and this report. Do not commit `label-parser/`, `audit-probes-*/`, model assets,
JARs, Java classes, raw result JSON, command logs, or installed dependencies.
