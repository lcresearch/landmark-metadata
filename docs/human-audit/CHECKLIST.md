# Human inspection checklist

All items are **PENDING**. Use the [record template](REVIEW_RECORD_TEMPLATE.md)
for actual observations and human conclusions. The comparisons below describe
what earlier records report; disagreement is an audit finding, not something to
repair by substituting evidence. A source/report check supports a narrower scope
than inspecting the required raw objects.

`C…` and `S…` refer to the [manuscript ledger and hashed sources](../../work/paper-rewrite-20261004/claim-sources.json).
Raw locators use **E** = `/workspace/metadata-contract-e2e-20261004T030536Z`,
**A** = `/workspace/metadata-contract-audit-20261004T062010Z`, and
**F** = `/workspace/metadata-contract-p2p3-20261004T073824Z`.
Angle-bracket selectors and `*` denote required sets to enumerate, not verified
files. Record the actual expanded paths, units and hashes. Current raw-file
availability was not inspected for this preparation.

Before HA01, record the target manuscript hash/commit, review scope and recovered
evidence families using [the entry guide](README.md). Keep S, I and D separate;
P checks what the intervention preserved. The core original E1/E2 denominator
is eight phase/variant aliases, five byte conditions, one graph and 16 input
observations. Construction audits and replays do not add independent models.

<a id="ha01"></a>

## HA01 — The actual generated public call

**Target:** C3 and C2R; manuscript `sec:e1` and the construction audit in `sec:e2`.
Open [instrumentation source](../../sources/metadata-contract-e2e-20261004T030536Z/scripts/ContractInstrumentation.java),
[bytecode audit](../../sources/metadata-contract-audit-20261004T062010Z/preservation/bytecode/report.md)
and [rebuild report](../../sources/metadata-contract-audit-20261004T062010Z/rebuild/AUDIT_REPORT.md)
(S04, S06, S07, S43).

**Required evidence:** generated `ContractModel.java` under
`E/E1/variants/<variant>/generated/src/main/java/org/example/contract/`;
generated/harness classes, DEX and executed APKs for the selected units;
`A/preservation/bytecode/` input manifest, javap/decompiler outputs and results.
For C2R, inspect the separate `A/rebuild/{E1,E2}/variants/<variant>/` generated
source (`generated/src/main/java/org/example/contract/ContractModel.java`),
`build/classes/`, `build/dex/` and `build/consumer.apk`, with its corresponding
`A/rebuild/{E1,E2}/executions/primary/<variant>/device/` records. Original-run
artifacts cannot stand in for these rebuilt binaries and executions.

Trace `newInstance → process(TensorImage) → Outputs.getProbabilityAsCategoryList`
in source and the executed compiled path. Check resource/postprocessor selection
and the actual TensorLabel call. Verify the raw-output observation only reads a
duplicate and that preceding accessors do not change the original buffer. A
handwritten decoder probe is not this E1 execution.

**Earlier agent coverage:** the preservation audit disassembled classes/DEX and
checked saved executions; C2R regenerated/rebuilt with installed tools. The later
finite reader did not repeat disassembly. Record exactly which artifacts the
human inspected; source alone does not certify the executed binary.

<a id="ha02"></a>

## HA02 — Which model bytes reached the consumer

**Target:** C2, C2R, C3 and C6. Open [input identities](../reproduction/INPUTS.md),
[preservation report](../../sources/metadata-contract-audit-20261004T062010Z/preservation/AUDIT_REPORT.md)
and [P2 results](../../research/20261004-p2-p3/P2/EXPERIMENT_P2_RESULTS.md)
(S07, S09, S10, S41–S43).

**Required evidence:** working models, staged assets, actual executed APKs and
install/build records; `A/rebuild/results.json`; P2 `static-results.json`,
`build-results.json`, device records and resolved dependencies. Five complete
model/resource identities and condition aliases are in the input inventory.

Compare the working file with `assets/model.tflite` inside each relevant APK.
Attribute that APK to the run's package/install record. For C2R and P2, compare
the recorded AssetManager read immediately before construction using the same
context and asset name. **Original E1 instrumentation has no preload hash.**
The later observation identifies an AssetManager read, not an intercepted native
interpreter buffer. The original audit did not inspect a separately device-pulled
installed APK; do not imply it did.

**Earlier agent coverage:** the handoff rehashed five selected original models
and resource members, but P2 copied files and the E2 restoration alias were
existence-only checks. Do not turn that inventory into a new packaging audit.

<a id="ha03"></a>

## HA03 — Separate preservation comparisons

**Target:** C2 and C2R; P in `sec:contracts`. Open
[preservation report](../../sources/metadata-contract-audit-20261004T062010Z/preservation/AUDIT_REPORT.md),
[rebuild report](../../sources/metadata-contract-audit-20261004T062010Z/rebuild/AUDIT_REPORT.md)
and [toolchain identities](../reproduction/TOOLCHAIN.md) (S04–S08, S10, S43).

**Required evidence:** all five model-byte conditions, appended label members,
the pinned schema/canonicalizer, E1/E2 static/build records, generated source,
classes/DEX and audit comparison inputs. HA04 checks E1 tested numerics; HA05
checks E2 tested numerics and association changes.

Independently compare computational fields/output order and all 165 nonmetadata
buffers; inspect metadata buffer 165 and whether any graph tensor references it.
Compare embedded metadata, pre-ZIP bytes and the selected ZIP payload separately.
Label interventions preserve embedded metadata; the description control changes
one metadata byte. Restoration recovers payload/behavior, not publisher ZIP bytes.

Compare generated Java/classes/DEX within the exact recorded build scope, not
whole APKs. C2R classes match earlier generated classes, while its full DEX
equality is across the new builds only because the harness gained hashing.
Record each normalization algorithm: the original canonicalizer and independent
audit serialization can have different digests while each shows within-method
equality. Whole-model hashing in the handoff did not redo these comparisons.

<a id="ha04"></a>

## HA04 — E1 stage outcome and exact failure

**Target:** C3 and the numerical part of C2; `sec:e1`. C2R applies when the
separate construction audit in `sec:e2` is selected. Open
[E1 report](../../sources/metadata-contract-e2e-20261004T030536Z/E1/EXPERIMENT_E1_RESULTS.md)
and [selected readback scope](../../research/20261004-significance-review/MEASURED_OUTCOMES.md)
(S04, S07, S15–S17, S43).

**Required evidence:** `E/E1/executions/primary/<variant>/device/result.json`,
input/raw tensors, attributed logcat/stack and run commands for original,
description control, deletion and restoration; use the separate A/rebuild
records if reviewing C2R. Both prescribed inputs must be accounted for.

Check stage records rather than the instrumentation exit code. Recorded originals,
description controls and restorations return 1,000 categories. Deletion completes
loading and `process`, leaves a 4,000-byte raw output for each input, and reaches
the real getter with `IllegalArgumentException: Label number 999 mismatch the shape on axis 1`.
Check the generated-getter stack frame and the earliest failing stage. The
harness catches this exception; it is not an application-crash result.

For each prescribed input, compare the complete E1 raw output bytes of description
control, deletion and restoration against original; file presence and size alone
do not establish numerical equality. Compare every returned score bit and label
for the successful control/restoration lists against original. When auditing
C2R, repeat within its rebuilt E1 records and compare its observations to the
matching historical primary records; report those comparisons separately.

Attribute cumulative logcat by the recorded run/time/PID. Exit zero can coexist
with a caught getter failure. Deletion returns no decoded list: an empty-loop
or vacuous decoded-equality summary must not count as successful decoding.

<a id="ha05"></a>

## HA05 — E2 full association comparison and reversal

**Target:** C4; `sec:e2`. Open
[E2 report](../../sources/metadata-contract-e2e-20261004T030536Z/E2/EXPERIMENT_E2_RESULTS.md),
[mutation source](../../sources/metadata-contract-e2e-20261004T030536Z/scripts/prepare_e2.py)
and [saved-observation scope](../../research/20261004-significance-review/MEASURED_OUTCOMES.md)
(S05–S08, S15–S17).

**Required evidence:** `E/phase0/pre-E2-freeze.json`, E2 resource bytes,
`results.json`, `deviations.json` and primary device records for all four
conditions; each input RGB file, `*-output-0.f32` and `*-decoded.json`.
If reviewing replay, retain the interrupted attempt and separately identified
`replay-recovery-20261004T034600Z` records.

Inspect chronology independently of deterministic source code. Verify the
declared one-position left shift preserves filename, count and multiset.
Reconstruct/compare both exact RGB inputs; compare every raw value, returned score
bit, argmax/top-five index and all 1,000 display strings. Reported permutation
changes 999 strings; adjacent `maillot` entries account for the unchanged string.
At RGB-pattern position 904, score `0.23542051017284393` is unchanged while
`window screen` becomes `window shade`. Inverse restoration recovers the lists.

Use wrapper list/output position, not its unset Category index. One witness is
not a full comparison. The interrupted replay is not converted into success by
the separate recovery. E2 alone establishes baseline-relative association change;
the reference-backed interpretation requires HA07.

<a id="ha06"></a>

## HA06 — Same-Android consumer boundaries

**Target:** C6; `sec:consumers`. Open
[P2 results](../../research/20261004-p2-p3/P2/EXPERIMENT_P2_RESULTS.md),
[Task instrumentation](../../research/20261004-p2-p3/P2/scripts/TaskInstrumentation.java)
and [mechanism review](../../research/20261004-p2-p3/review/mechanism/MECHANISM_REVIEW.md)
(S02, S09, S10, S13–S17).

**Required evidence:** `F/P2/executions/primary/{wrapper,task}/<variant>/device/`,
the final executed APK for each of the ten condition × consumer configurations,
input/configuration freeze, dependency/version records,
`F/verification/runtime-record-review.json` and the cited source/binary inspection.
Keep initial unexecuted build attempts separate from the executed final APKs.

Check exact model/input bytes, same API-30 x86_64 AVD and selected options.
Account for ten configurations and 18 actual input observations: Task deletion
rejects before two planned inputs. The wrapper fails at its getter after process;
Task fails at construction with outer `IllegalStateException` about obtaining
the native address and an `IllegalArgumentException` cause reporting 1,000
classes versus 999 labels. Inspect the complete preserved cause chain, not
only its outer message or a source-level expected exception.

Align Task class indices with wrapper positions in all eight successful shared
condition/input pairs. This checks returned scores/labels, not unobserved Task
raw tensors. `classify` is atomic at this instrumentation boundary. Shared Support
components, different native integrations and the unknown embedded Task interpreter
remain limits. The finite 59-file readback checked only the two deletion records,
not this entire P2 comparison.

<a id="ha07"></a>

## HA07 — Qualified independent display-order reference

**Target:** C5; `sec:p3`. Open
[P3 report](../../research/20261004-p2-p3/P3/EXPERIMENT_P3_RESULTS.md),
[source excerpts](../../research/20261004-p2-p3/P3/SOURCE_EXCERPTS.md),
[reference audit](../../research/20261004-p2-p3/review/reference-audit/AUDIT_REPORT.md)
and the [reference input inventory](../reproduction/INPUTS.md)
(S11–S13, S15–S18).

**Required evidence:** `F/P3/retrieved/` bodies and retrieval records for
`I01-publisher-model`, `I06-tfhub-lite-model`, `F07-pinned-lite-card`,
`F10-pinned-parent-card` and `F11-explicit-class-order`;
`F/P3/analysis/{artifact-bridge,reference-chain,full-display-order-comparison,candidate-synset-comparison}.json`;
saved commit/tree responses and the retained first audit attempt.

Check every link: focal model → graph/weight/output-equivalent TFHub fp32/2 →
commit-pinned Lite card → explicitly named classification/1 parent → prescribed
external label file and background omission. Recompute the bridge across all
computational fields, ordered outputs and 165 nonmetadata buffers. The packages
are not byte-identical. Check all 1,000 positions after the independently
prescribed offset: reported original/restoration agree everywhere, permutation
disagrees at 999 positions.

Assess authority and scope, not only matching hashes. The pinned card is a later
retrieved snapshot; the label URL is unversioned. Duplicate `crane`/`maillot`
names do not establish stable IDs or training lineage. This supports
I_display only, not image prediction correctness. Earlier readback recounted
stored rows and rehashed selected bodies; it did not recompute the full bridge
or establish the source chain's authority. Couple the result to HA05 execution
evidence separately; P3 itself runs no inference.

<a id="ha08"></a>

## HA08 — Hand reference and consumer boundary

**Target:** C7; `sec:hand`. Open
[reference chain](../../sources/metadata-contract-e2e-20261004T030536Z/E7/REFERENCE_CHAIN.md)
and [Hand results](../../sources/metadata-contract-e2e-20261004T030536Z/E7/EXPERIMENT_HAND_RESULTS.md)
(S20–S22).

**Required evidence:** E7 original/source-pinned model components, immutable
source/external-file declarations, `source-component-equivalence.json`, original
and exchanged metadata, generated sources/repair patches/classes/disassembly,
and Task image/options/primary/replay decoded records. Use E7's exact recorded
paths; these secondary inputs are not made complete by the focal inventory.

Verify that focal `6acda7…` and source-pinned `11c272…` are different files linked
by 172 equal nonmetadata buffers and ordered computation. Derive output roles
from the pinned source, not shape alone. Inspect both raw Java compile failures
and the identical separator repair before the static getter/index comparison.
Separately check the one fixed Task image, four conditions and decoded fields.

One unchanged Task image is neither universal metadata insensitivity nor a
second executed generic-wrapper failure. Swapping entries is not a complete
repair: role association, scalar representation, category decoding and coordinate
normalization need separate treatment. Record separate source/static/runtime
sub-results if only part of this evidence can be recovered.

<a id="ha09"></a>

## HA09 — Structural, external and preflight scope

**Target:** C1, C8, C8D, C9, C9E and C10; `sec:contracts`, `sec:preflight`.
Open [E4 results](../../sources/metadata-contract-e2e-20261004T030536Z/E4/EXPERIMENT_E4_RESULTS.md),
[E5 results](../../sources/metadata-contract-e2e-20261004T030536Z/E5/EXPERIMENT_E5_RESULTS.md),
[official baselines](../../research/20261004-contribution-review/OFFICIAL_BASELINES.md),
[core comparison](../../sources/metadata-contract-audit-20261004T062010Z/baseline/RESULTS.md)
and [parser audit](../../sources/repro-audit-20261004/reports/CHECKER_AUDIT.md).

Record three sub-results, with their own missing materials:

- **HA09a — Development and external counts (S23, S45–S48).** Inspect candidate
  freeze, downloads/exclusions, graph grouping and raw compile/warning records.
  E4's 20 URLs → 16 downloads → 18 component occurrences → 15 new graphs
  yield eight compiles/seven failures, D=4 compatible/9 incompatible/2
  inapplicable, all I abstaining and zero external-original runtime executions.
  Preserve unsupported fallbacks and unavailable candidates. Development's 46
  variants/105 CPU calls/23 isolated JVM probes are not extra independent models.
- **HA09b — Selected-decoder and baseline scope (S01, S02, S19, S24–S26, S44).**
  Recover frozen fixture identities and per-fixture judgments. E5 adds zero
  rejection over the matched baseline or Task initialization on five core
  conditions. Its 65-fixture D denominator includes three dynamic and two
  no-metadata abstentions, plus 11 not reached. Inspect actual getter/resource/
  overload and Java label parsing; last-axis counting is not a general substitute.
  Keep S/I/D separate; P is experimental preservation. Abstention is not detection.
- **HA09c — Parser counterexamples (S27–S29).** Require the later reconstruction's
  actual-library probe inputs/results, not the old E1 files. VT and U+2028 concern
  defects in the historical Python checker/baseline; the probes use synthetic
  scores and Task initialization, not Android inference. The maintained parser
  is scoped to valid UTF-8. Those raw probe results and the separately pinned
  reconstruction E5 catalog were missing at the handoff's checked paths; record
  a blocked raw-evidence result if they remain unavailable.

Source review can assess implementation assumptions while these raw checks stay
blocked. No natural-defect, precision/recall, generalization or universal
abstention guarantee follows from the reported counts.

<a id="ha10"></a>

## HA10 — Antecedents, contribution and significance

**Target:** C11–C13; `sec:related`, `sec:discussion`, `sec:validity`.
Open [public reports](../../research/20261004-significance-review/PUBLIC_REPORTS.md),
[contribution comparison](../../research/20261004-contribution-review/CONTRIBUTION_COMPARISON.md)
and [significance assessment](../../research/20261004-significance-review/SIGNIFICANCE_ASSESSMENT.md)
(S01, S02, S15, S30–S40).

Inspect the retained #770 issue/member reply and their indexed source identities,
plus the inspected versions of the closest works when assessing overlap. The
2022 generated segmentation getter failure is both motivation and a prior
antecedent; the reply describes an unsupported consumer/model combination.
The study did not reproduce that natural artifact.

Check that contributions remain controlled execution and configured enforcement
comparison; E5 is supporting. Separate seven full-text comparisons from the
Stalnaker abstract-only and unresolved Meyer full-text scope. Whole-package hash
pinning, Task initialization, actual getter tests and qualified map comparisons
are existing protections. The evidence does not measure prevalence, operational
benefit or classification accuracy. Record unresolved overlap and significance
objections; neither agent consensus nor this checklist certifies novelty or
venue acceptance. Preserve the human/AI responsibility disclosure.
