# Candidate claims and implemented scope

This is a source-level inventory at repository starting commit
`81af34b10f8093e646179e51e658d597e6acc84b`, following `PROTOCOL.md`.
It does not rerun models, authenticate all recorded execution bytes, complete
human verification, or establish novelty against literature. The accompanying
comparison must determine whether the empirical distinctions below remain
substantial after accounting for existing work.

## Evidence levels used here

- **Recorded observation:** the current paper and preserved report state a
  result. Reading those records does not independently reproduce it.
- **Source inspected now:** first-party scripts show the intended intervention,
  API call, measurement or check. Source establishes that mechanism in the
  inspected program, not that its claimed historical invocation succeeded.
- **Still pending:** raw-record authentication not performed in this task,
  documentary interpretation requiring human review, and conclusions beyond
  the measured configuration.

The current manuscript is
`work/review-followup-20261004/manuscript/paper.tex`, SHA-256
`6e77175d25ff0834978463bdb2359ab82e6cf62bc8e2d611960c23dcf8b48537`.
Line locators below refer to this unchanged source. Other abbreviated roots are:

| Alias | Repository path |
|---|---|
| E2E | `sources/metadata-contract-e2e-20261004T030536Z` |
| AUDIT | `sources/metadata-contract-audit-20261004T062010Z` |
| REPRO | `sources/repro-audit-20261004` |
| P23 | `research/20261004-p2-p3` |

## Claim inventory

| Candidate | Recorded observation and locator | Mechanism inspected in this task | Retain / narrow / withhold |
|---|---|---|---|
| E1: interface failure with preserved computation | Paper lines 63–106; `E2E/E1/EXPERIMENT_E1_RESULTS.md`: deletion loads and runs, then actual generated getter throws; description/restoration succeed; source/classes/DEX and tested raw outputs equal. | `E2E/scripts/prepare_e1.py`, `rewrite_associated` and `prepare` (10–58) distinguish ZIP payload, embedded metadata, model prefix, nonmetadata buffers and canonical graph. `E2E/scripts/ContractInstrumentation.java` calls `newInstance` (52), `process` (69), duplicates the output buffer (72), then calls the generated getter (81); failures are caught (86–90). | **Retain** as a controlled executed-interface result, contingent on the preserved runtime evidence. **Narrow** the intervention to the associated resource; it does not change embedded metadata. **Withhold** natural EfficientNet defect, application crash, accuracy loss, or deployment impact. Source inspection alone cannot authenticate generated-source/class equality or the exception stack. |
| E2: successful changed association | Paper 108–122; `E2E/E2/EXPERIMENT_E2_RESULTS.md`: 999/1,000 exposed strings change, score bits and positions do not; inverse restores result. | `E2E/scripts/prepare_e2.py:13–22` uses a deterministic one-position cyclic shift, checks string multiset preservation, and constructs its inverse. The actual getter harness is the E1 harness. | **Retain** successful association change and reversal on tested inputs. Predetermination before inspecting E1 predictions is a protocol/timeline claim, not established by this script alone: its execution is gated on E1 completion. **Withhold** prediction correctness and accuracy effects. P3 supports a narrower external display-order judgment, separately. |
| P3: publisher display-order agreement | Paper 124–132; `P23/P3/EXPERIMENT_P3_RESULTS.md`: exact focal graph linked to a separately retrieved TFHub artifact; original/restoration match all 1,000 reference display labels, permutation disagrees at 999. | `P23/P3/scripts/analyze_reference.py`, `graph` (25–43) checks metadata-buffer isolation and describes graph/order; 49–61 compare exact graph/165 nonmetadata buffers; 65–83 apply the parent card's prescribed background omission and compare every position. | **Retain** disagreement with the publisher display-order specification through the reported graph/weight bridge. **Withhold** stable synset-ID provenance, reconstruction of export/training lineage, release-time-document identity, and image correctness. This task reads the comparison code/report; it does not reauthenticate retrieved bytes or validate the publisher interpretation. |
| E3/P2: consumer enforcement boundaries | Paper 138–173; `P23/P2/EXPERIMENT_P2_RESULTS.md:5–31`: 10 configurations, one graph, 18 actual input observations; wrapper fails at getter, same-AVD Task fails during creation. | `P23/P2/scripts/ContractInstrumentation.java:54–98` hashes the selected asset and separates `process`, raw observation and getter. `TaskInstrumentation.java:25–35` retains cause chains and calls actual Task creation and `classify`; `classify` is atomic at this observation boundary. | **Retain** different observed rejection stages on the same Android API/ABI. **Narrow** to configured consumers: native integrations differ; source provenance does not prove identical interpreter implementations. **Withhold** causal attribution to one isolated API/version variable, independently implemented frontends, Task raw-tensor equality, latency savings or safety superiority. |
| Hand: role witness and consumer boundary | Paper 175–185; `E2E/E7/EXPERIMENT_HAND_RESULTS.md`: source-backed output roles disagree; identical repair precedes static wrapper binding evidence; four Task conditions have equal decoded outputs on one image. | `E2E/scripts/hand_task_one.py` executes the MediaPipe Task and serializes decoded results/float bits. The report separates the source-pinned component from the focal hash and records their graph bridge. No new third-party Hand source inspection or bytecode execution is performed here. | **Retain** secondary reference/boundary case. **Narrow** generic binding evidence to repaired Java and static bytecode, Task invariance to the measured input/fields. **Withhold** complete repair by swap, universal Task metadata insensitivity, a second Android-wrapper end-to-end failure, normalized raw coordinates, or task accuracy. |
| E4: frozen external application | Paper 192–214; `E2E/E4/EXPERIMENT_E4_RESULTS.md:3–40`: 15 new canonical groups, all S accepted/all I abstained; 8 compile/7 fail; D 4 compatible/9 incompatible/2 inapplicable; no external runtime. | The preserved report retains unavailable candidates and exclusions; these counts were read, not recalculated here. Its incompatible paths include five compilation failures and four explicitly unsupported non-RGB fallback paths. | **Retain** bounded application/coverage and limitations of frozen rules. **Withhold** 9 natural deployed defects, supported runtime failures, prevalence, general semantic accuracy, independent preregistration, or 15 successful end-to-end replications. |
| E5: template-based preflight | Paper 218–225 and 231–254; `AUDIT/baseline/RESULTS.md:31–62`: zero additional rejected conditions over simple selected-path baseline or Task initialization in five core fixtures. | `REPRO/maintained/preflight.py`, `reference_check` (17–42), `check` (44–120): invokes generator, regex-matches declared tensor/resource/getter names, joins by naming conventions, and applies explicitly encoded decoder conditions. Detailed limits below. | **Retain** scoped supporting diagnostic and separate S/I/D/P reporting. **Downgrade** any claim of new general program analysis or superior detection. **Withhold** automatically derived library preconditions, runtime obligations, sound handling of arbitrary getters, universal semantic inference, or demonstrated extra detection on the core set. |
| Parser counterexamples and correction | Paper 227–229; `REPRO/reports/CHECKER_AUDIT.md`, finding 1: historical E5/simple baseline use Python line semantics; VT gives false compatibility and U+2028 false incompatibility relative to actual Java probes; original 65 judgments unchanged after correction. | `REPRO/probes/probe_label_parser.py:83–124` constructs both injected resources and invokes real `DecoderProbe`, E5, simple baseline and Task initialization; it uses fixed synthetic scores, not inference. `REPRO/maintained/java_labels.py:14–34` models CR/LF/CRLF, Java blank-line filtering and valid UTF-8, with malformed-UTF-8 abstention. | **Retain** a consumer-semantic modeling defect in our own checker and a bounded correction. **Withhold** a new official-validator bug, natural model defect, Android end-to-end parser failure, or completed runtime-obligation method. Historical execution/65-fixture-regression claims require their raw records; they are not freshly rerun here. |
| S/I/D with P separate | Paper 37–61 explicitly treats S/I/D as separate judgments and P as an intervention check. | `REPRO/maintained/preflight.py:47–70` records these separate objects; P compares canonical graph/nonmetadata buffers; I consumes supplied provenance/mapping; D applies a selected template's preconditions. | **Retain** analytical vocabulary and experimental discipline. **Withhold** a complete taxonomy of all deployment contracts, a new correctness hierarchy, or automatic proof that supplied semantic provenance is valid. P is not a fourth model-correctness judgment. |

## What E5 actually analyzes

Historical `E2E/E5/preflight.py` SHA-256:
`8a149290196809e7cc0ed2ac642e212223f71ca4d46fb15dbd1976ce5c976166`.
Maintained `REPRO/maintained/preflight.py` SHA-256:
`0e8791987ac1733a8187041b57f3136ca2d83689989f1681b4598e746e5f6612`.
The maintained parser helper SHA-256 is
`1f6fb25e5992c63708a514d8658ee0be982bee9e428e6a5db12f47e9a6e7e771`.
These hashes were computed in this task; runtime evidence hashes were not.

The maintained implementation has the following defensible scope:

1. `check`, lines 78–89, recognizes `model.getOutputTensor(i)`,
   `getOutputTensorMetadata(i).associatedFiles(j).name()`, and one exact
   `TensorLabel(...postprocess...(...)).getCategoryList()` getter syntax. It
   joins uniquely named declarations. D does not select answers by model name
   or fixture hash. This is more specific than blindly counting the last axis.
2. Lines 90–96 inspect a named default-postprocessor body and operation names
   matched by `.add(new Word(`. Recognized operations other than `DequantizeOp`
   cause abstention. Nonpositive concrete dimensions or signatures also cause
   abstention, even where the current concrete Gesture shape is available.
3. Lines 99–110 load labels with the maintained Java-compatible helper and check
   the first nonunit axis exists, matches label count, and is the final axis.
   These conditions are programmed into the checker. It does not extract them
   automatically from library implementation or bytecode.
4. Lines 17–42 require exact artifact/source digests and a supplied role/class
   mapping. The tool checks that these inputs are present and consistent with
   the declared format; human judgment remains necessary for independence,
   source authority, interpretation and the stated artifact binding. Hashes
   alone cannot establish those semantic properties. P3's separate graph-bridge
   comparison is not evidence that E5 inferred or consumed that reference.
5. There is no data-flow/control-flow or type analysis connecting all `Outputs`
   assignments, buffer-map entries, `model.run`, processor installation, aliases
   or reset/customization paths. Factory expressions may evade the operation
   matcher. A getter that does not match can yield
   `INAPPLICABLE_NO_SELECTED_GETTER` (113), rather than justified abstention.
6. There is no `DEFER` result, symbolic shape predicate, runtime-obligation
   generation, check placement or discharge. Dynamic-signature abstentions
   cannot be presented as new detections. The helper correction changes label
   parsing, not these analysis boundaries.

`AUDIT/baseline/audit_one.py:86–117` is the strong simple comparator: it declares
one-output/one-selected-resource assumptions and checks the same chosen
TensorLabel path. Its historical `splitlines()` bug at 97–98 must be disclosed
alongside E5's; neither parser's defect establishes a benefit of E5 over this
baseline. Five core fixtures establish zero additional E5 rejection, not
universal equivalence between their coverage.

## Raw-evidence visibility on this host

The source-only Git repository excludes runtime evidence. That does **not** mean
all historical raw files are absent from the current host. This task performed
existence/size checks only, without content authentication:

| Local external path | Observation |
|---|---|
| `/workspace/metadata-contract-e2e-20261004T030536Z/E1/results.json` | File present, 100,173 bytes |
| `/workspace/metadata-contract-e2e-20261004T030536Z/E1/variants/original/model.tflite` | File present, 18,582,189 bytes |
| `/workspace/metadata-contract-audit-20261004T062010Z/rebuild/AUDIT_REPORT.md` | File present, 17,747 bytes |
| `/workspace/metadata-contract-p2p3-20261004T073824Z/P2/results.json` | File present, 115,818 bytes |
| `/workspace/metadata-contract-p2p3-20261004T073824Z/P3/results.json` | File present, 11,743 bytes |
| `/workspace/metadata-contract-p2p3-20261004T073824Z/P2/executions/primary/wrapper/label_deletion/device/result.json` | File present, 4,486 bytes |
| `/workspace/repro-audit/independent-audit/label-parser/results.json` | Absent at this historical locator |
| `/workspace/repro-external`, `/workspace/repro-task`, `/workspace/repro-audit` | Absent |

These observations are not a complete archive inventory, revalidation of
manifest integrity, or a claim that an absent locator's contents cannot exist
elsewhere. No model, generator, compiler, interpreter or inference was executed
for this inventory. Independent human verification remains pending.

## Candidate contribution after this inventory

A defensible candidate is the **bounded empirical characterization** of public
interface consequences and enforcement boundaries under controlled
model-package interventions, with explicit preservation and reference scopes.
E1/E2/P2 carry its executed evidence; P3 adds a qualified display-order reference;
Hand bounds propagation through another consumer; E4/E5 and the parser defect
expose coverage and modeling limits. Neither rephrasing this as “cross-artifact
contracts” nor correcting the project's own checker establishes novelty.

A method-paper claim based on automatic consumer-derived contract extraction or
staged/runtime validation is not implemented here. Whether the empirical
characterization is new and important enough remains the job of the bounded
related-work comparison and the separately planned significance assessment.
