# Manuscript claim–evidence ledger

This ledger supports the new [working manuscript](manuscript/paper.tex). It
reorganizes the existing evidence around contracts, executed consequences and
consumer boundaries. **This editorial task runs no model, generator, model-code
compiler, emulator or inference experiment.** It does not upgrade a reported observation
into a fresh execution. The local starting revision is
`87290c2f7571d1fdf5cc2e56286a0ecff5b984ac`; PR #8's merge was reported by the user,
not independently verified against GitHub during the blocked connection.

The accompanying [source index](claim-sources.json) records exact repository
source/report digests computed for this ledger, claim-to-source mappings, and
selected external evidence locators/digests copied from the earlier provenance
indexes. External result bytes are not included in Git and are **not rehashed in
this editorial task**. A report hash identifies the report, not the correctness
or completeness of its excluded execution evidence.

## Evidence status

| Label | Meaning in this ledger |
|---|---|
| R — recorded experiment | Existing execution/comparison report, read for this rewrite. No new execution is claimed. |
| B — previously read back | The significance review and later reproduction handoff inspected selected old raw/input/decoded records. The handoff actually ran the maintained finite reader; this rewrite reuses its recorded outcome. |
| S — inspected source/provenance | Existing first-party source, fixed-version implementation review, or documented reference chain explains the claimed mechanism. Source inspection alone does not prove an execution or source-to-binary equivalence. |
| J — bounded judgment | An analytical definition, literature comparison or engineering implication, with its supporting scope stated. It is not a new measured benefit. |
| U — unresolved | External reference authority, full archive authentication, human verification or an unmeasured consequence remains open as specified. |

“Previously read back” covers the fixed 59-file selection described in
[MEASURED_OUTCOMES.md](../../research/20261004-significance-review/MEASURED_OUTCOMES.md)
and [handoff validation](../../docs/reproduction/validation.json). It checks
primary E1/E2 observations, P2 deletion records and stored P3 rows. It does not
recompute the graph/weights bridge, authenticate every APK/class/archive, or
repeat all ten P2 units. The later reconstructed corpus and parser-probe raw
results were absent at their checked `/workspace/repro-*` locators; their
preserved reports remain a different evidence level.

## Claims in narrative order

Source IDs below resolve to the repository paths and exact locators in
`claim-sources.json`. Section anchors are the manuscript's LaTeX labels.

| ID / section | Manuscript wording supported by the evidence | Evidence and verification stage | Required boundary |
|---|---|---|---|
| **C1 — `sec:contracts`** | We distinguish structural acceptance S, reference-backed association agreement I, and compatibility D with the selected decoder. P separately checks what an intervention preserved. | J/S: S01–S03, S19. The Support 0.4.4 implementation review locates schema/population, selected-resource loading and decoder conditions separately. | Analytical vocabulary, not an exhaustive taxonomy or a new hierarchy of model correctness. Reader success is not population acceptance. D concerns the modeled path; reference authority is not inferred from shape or a supplied hash. |
| **C2 — `sec:e1`, `sec:e2`** | The classifier resource interventions preserve recorded graph/weights, embedded metadata, generated Java, generated classes and tested numerical outputs; the description control changes metadata. | R/S: S04–S08, S10; B for selected numerical outputs: S15–S17. Preservation reports separate 165 nonmetadata buffers, canonical graph, pre-ZIP bytes, metadata and associated ZIP payloads. | Graph equality does not mean complete-package equality. Source/classes/DEX equality is within the specified build comparison, not whole-APK equality or a claim about every rebuild. Restoration restores the payload/observed behavior; publisher container bytes need not return. Native interpreter-loaded bytes were not intercepted. |
| **C2R — `sec:e2`** | The recorded construction audit regenerated and built eight E1/E2 phase/variant aliases representing five artifact–consumer configurations, then reproduced the outcomes on 16 input observations in a new AVD. | R: S43 directly reports the construction scope, denominator, stage outcomes, source/class comparisons and within-rebuild DEX equality. It reused installed SDK/JDK/Python, with new output directories and signing key. | This is the historical construction audit, not a build performed for the rewrite or an archived-toolchain installation. Generated classes match historical classes; full DEX matches across fresh conditions only because the harness added a pre-load asset hash. No fresh-versus-historical DEX equality is claimed. The 59-file readback does not validate this separate reconstruction record, and agent reconstruction is not human verification. |
| **C3 — `sec:e1`** | Deleting one of 1,000 labels allows the actual generated classifier to load and complete `process`, then its unmodified `getProbabilityAsCategoryList()` throws `IllegalArgumentException: Label number 999 mismatch the shape on axis 1`. | R/B/S: S04, S06, S07, S15–S17. The harness calls `ContractModel.newInstance`, `process(TensorImage)` and the actual generated getter; raw output is observed through a duplicated buffer. Both prescribed inputs record the failure. | The harness catches the exception: no application-crash claim. This is an injected condition, not a natural EfficientNet defect. Construction already loads labels; the getter performs the selected decoder check. No handwritten decoder substitutes for this E1 call. |
| **C4 — `sec:e2`** | A deterministic one-position cyclic label shift completes the actual getter while keeping raw values, returned score bits and tested top indices fixed; 999 of 1,000 exposed display strings change, and inverse restoration recovers the baseline association. | R/B/S: S05, S06, S08, S15–S17. Full decoded lists and scores were previously compared. Position 904 on `rgb_pattern` retains score `0.23542051017284393` while `window screen` changes to `window shade`. | Inputs are repeated observations, not independent models. E2 alone establishes association change relative to original; I requires C5's separate reference. A deterministic script does not independently prove predeclaration chronology. One unchanged display position reflects duplicate `maillot` names, not proof of an unchanged stable class identity. |
| **C5 — `sec:e2`** | Original and restoration agree at all 1,000 positions with the qualified publisher display-order specification; the permutation disagrees at 999. | R/S plus B of stored comparison rows: S11–S13, S15–S18. The reference connects the exact focal computation to TFHub Lite0 fp32/2, its pinned parent card and the prescribed external label file with background removed. All 165 nonmetadata buffers and ordered computation fields are reported equal in the bridge. | **I_display only.** Stable class-ID/training lineage remains ABSTAIN. The reference is a preserved snapshot of an unversioned label URL and later pinned publisher card, not certified release-time documentation. No image classification error or accuracy loss follows. The old E5 I abstentions are not rewritten. |
| **C6 — `sec:consumers`** | In the same API-30 x86_64 Android environment, the wrapper rejects deletion at the getter after `process`, while Task ImageClassifier 0.4.4 rejects it during construction; original, description, permutation and restoration complete both public paths. | R/B/S: S09, S10, S13–S17 and S02. Ten component × condition × consumer units represent one graph, five model-byte conditions, two consumers and 18 actual input observations. The Task cause chain states 1,000 classes versus 999 labels beneath an outer native-address exception. | Native integrations still differ; the Task embedded interpreter version is not established. `classify` is atomic at the instrumented boundary. Task internal raw tensors are not observed. Two planned deletion inputs were not reached and are not added to the denominator. No isolated API-version causality, independent-implementation, cost or safety superiority claim. |
| **C7 — `sec:hand`** | Hand supplies a source-backed output-role mismatch and metadata-sensitive generic binding; the official MediaPipe Task returns identical decoded fields for original, container control, exchange and restoration on one fixed image. | R/S: S20–S22. The v0.10.14 source-to-model link uses a graph/weight bridge: 172 nonmetadata buffers agree although component hashes differ. Generic Java had original compile failures and requires the same disclosed separator repair before bytecode binding comparison. | Secondary boundary case, not a second demonstrated Android-wrapper runtime failure. One image cannot prove universal metadata insensitivity. Swapping entries does not repair handedness representation, category-decoder suitability or coordinate normalization. Source interpretation/bridge still require human audit. |
| **C8 — `sec:preflight`** | The frozen external examination covers 15 new canonical graphs: all S accepted and all I abstained; eight raw wrappers compiled and seven failed. Frozen D reports four compatible, nine incompatible and two inapplicable paths. | R: S23. The denominator starts with 20 declared URLs, 16 successful downloads and four unavailable; extraction yields 18 occurrences, then one prior component and two prior-graph occurrences are excluded. | No external-original runtime executions. Five of nine D-incompatible wrappers fail compilation; four have explicit unsupported non-RGB fallback warnings. No nine natural defects, runtime generalization, prevalence or detector-accuracy estimate. Same-session freeze is not independent preregistration. |
| **C8D — `sec:preflight`** | The development corpus contains 11 metadata-bearing binary components representing ten canonical graphs, with 46 variants. Its 35 structurally accepted variants account for 105 CPU invocations on three synthetic inputs; 23 isolated JVM decoder probes agree with the selected API conditions. | R: S45's recovered-evidence audit directly records 11/10/46/35/105/23; the original study report S46, reproduction/design note S47 and original manuscript S48 report the same design counts and separate host inference from decoder probes. | Counts are inherited recorded outcomes, not recomputed for this rewrite. Mutants, aliases, repeated inputs and the two palm binaries sharing one graph do not increase independent model count. The 23 isolated expressions are not actual Android generated-interface executions or independent detector-accuracy labels. Three of five deletions start from already incompatible originals; five deletions do not mean five newly induced failures. |
| **C9 — `sec:preflight`** | E5 is a supporting, template-specific diagnostic. On five core byte conditions it has zero additional rejections over the exact-path simple baseline or Task initialization: each rejects only deletion. | R/S: S19, S24–S26, S02. Metadata displayer and populator separately accept the five; a distinct output-metadata-count reduction is rejected by the populator. | Existing official checks already enforce the decoder rule. E5 encodes preconditions and uses limited regex/naming joins; it does not infer arbitrary contracts, trace full data flow or generate runtime obligations. Unknown syntax can evade recognition. Dynamic-signature abstentions are not detections. Zero increment on these conditions is not universal equivalence. |
| **C9E — `sec:preflight`** | The frozen E5 evaluation covers 65 byte-distinct fixtures: S accepts 52, rejects 11 and abstains on two no-metadata originals. D records 27 incompatible, eight compatible, 14 inapplicable, three dynamic-signature abstentions, two no-metadata abstentions and 11 not reached; all 65 I judgments abstain. | R: S44 directly supplies the condition-group table and detection/abstention counts; S26 identifies the historical implementation. The dynamic abstentions include the already failing isolated Gesture deletion. Four distinct conditions with successful Android getters receive no incompatible/structural-rejection judgment in this evaluation. | These are fixtures assembled from development, E1/E2 and external phases, not 65 independent models or successes. The two absent-metadata D abstentions must be included to total 65. Frozen semantic abstentions remain unchanged after later P3/Hand reference work. No precision/recall, universal abstention guarantee or advantage over strong baselines follows; C9 supplies the separate core baseline comparison. |
| **C10 — `sec:preflight`** | Injected VT and U+2028 resources expose opposite errors in our historical E5 and simple-baseline Python label parsing relative to real Java FileUtil/TensorLabel probes; the maintained helper models the selected Java line behavior for valid UTF-8. | R/S: S27–S29 and S02. Recorded probe uses 1,000 fixed synthetic scores; Java/TensorLabel and Task initialization execute without model inference. The report records false compatibility for VT and false incompatibility for U+2028. | Raw probe results were absent at checked locators, so this rewrite relies on the preserved report and source, not fresh revalidation. These are our approximation defects, not natural official-library bugs or Android end-to-end parser results. Original 65-fixture judgments are reported unchanged, not rerun here. Malformed UTF-8 remains outside the helper's successful decision scope. |
| **C11 — `sec:related`, `sec:discussion`** | Support issue #770 is a 2022 antecedent for a generated segmentation getter/TensorLabel failure; a repository-member reply calls that drag-and-drop route unsupported for the model and recommends Task Library. | Public report/S: S30–S32, selected report R1. The bounded search triaged 30 unique issues, inspected seven plus 69 comments, and reproduced zero natural artifacts. Exact issue/comment response hashes are retained below and in the source index. | Cite as both motivation **and prior engineering evidence**, not a newly discovered supported-path defect. Issue model/toolchain identities were not recovered. The segmentation shape/axis problem differs from E1's injected classifier deletion. Search truncation/oldest-first ordering precludes incidence estimates. |
| **C12 — `sec:related`** | The contribution is controlled empirical characterization of package-to-public-interface consequences and configured enforcement stages, with a qualified display reference and preservation/reversal controls. | J/S: S01, S02, S33–S37. Prior work already covers ML contracts/wrappers, documentation- and implementation-derived constraints, graph/metadata assessment, mutation and differential testing. | No firstness for metadata-based wrappers, cardinality checks or contract analysis. No novel general analyzer is implemented. Seven full texts were inspected in the bounded comparison; Stalnaker remains abstract-only and Meyer full text unresolved. Different object/oracle does not prove exhaustive novelty or venue fit. |
| **C13 — `sec:discussion`, `sec:validity`** | The observations clarify what load tests, raw-output regressions, getter tests, package pins and qualified association comparisons establish for these interfaces. | J grounded in R/B/S: S15, S30, S38–S40. E1 distinguishes computation from successful output access; E2 distinguishes successful decoding from the reference association. Official documentation establishes relevant workflows. | Ordinary strong defenses remain available: a trusted **whole-package** hash detects both resource mutations; actual getter tests expose E1; a correct artifact-linked map comparison exposes E2. No adoption, frequency, debugging time, latency, prevented incident or production-harm measurement. This is bounded engineering relevance, not proven ecosystem impact. |

## Counting and reference rules for tables

- **E1/E2 primary:** eight phase/variant aliases, five unique model-byte
  conditions, one graph, 16 actual input observations, 14 returned category
  lists and two caught getter exceptions. Report replay/rebuilds separately;
  repeating the same inputs or reusing aliases does not increase model count.
- **Historical construction audit (C2R):** another eight phase/variant records,
  five byte conditions and 16 input observations, using freshly generated/build
  outputs and a new AVD with the existing installed toolchain. This separate
  audit must not be pooled into independent model counts or confused with the
  subsequent reconstruction under `/workspace/repro-*`.
- **P2:** ten consumer configurations, one graph, five byte conditions, 18
  actual input observations and 16 returned category lists. The wrapper supplies
  ten raw tensors; Task supplies no internal raw tensor observation. Compare
  returned categories by class index, not ranked-list position.
- **P3:** compare all 1,000 positions after the independently prescribed
  background removal. Repeated display strings (`crane`, `maillot`) prevent
  substituting display-string equality for stable class-ID identity.
- **Hand:** distinguish focal hash
  `6acda74af3fbf40e68265c20c7394b2bad81a16a481dcd79ad7a081887c3d6b9`
  from source-pinned component hash
  `11c272b891e1a99ab034208e23937a8008388cf11ed2a9d776ed3d01d0ba00e3`.
  Their recorded canonical graph hash is
  `fb3baefeb2c67e5c11013ede2408204bc431e99cffc34e81f19df16a7b711793`;
  file identity is not asserted.
- **Development and frozen E5:** the 46 development variants and 65 E5 fixtures
  overlap with other phases. E5's D tally totals 65 only with both kinds of
  abstention and the 11 structurally rejected/not-reached cases retained.

## Selected external evidence identities

These are copied provenance records, not new hash measurements or portable
download promises. The complete input/dependency routes and missing-material
assessment belong to the [reproduction entry](../../docs/reproduction/README.md).

| Existing evidence object | SHA-256 | Prior source / limitation |
|---|---|---|
| `/workspace/metadata-contract-p2p3-20261004T073824Z/P2/results.json` | `8828d53f32d0eb6a8a5276092e5f2834f548389d780fde1d3726cde0b263d45d` | P2/P3 claim index; complete P2 not rerun here |
| `/workspace/metadata-contract-p2p3-20261004T073824Z/P3/results.json` | `da54d486f461450d89bf77a777108f8e88b31bc6fcbf9b08fcd042cc8db88f17` | P2/P3 claim index; reference authority/bridge not re-established here |
| `/workspace/landmark-handoff-audit-20261004/readback/readback.json` | `8b555a55d059eb4c6055ed1ad890a517b866513dcbcdaa00be4838158b5fbff7` | Handoff finite readback; successful report creation alone is not a universal PASS |
| `/workspace/significance-review-20261004/public-reports/issue-01.json` | `13c6b2fa40d607d5ac818df1910efac95f5da7168f8f10e20b06bae0c1f16d26` | Retrieved #770 issue response, not a reproduced model failure |
| `/workspace/significance-review-20261004/public-reports/issue-01-comments.json` | `a14fe9ceece4520dd97a622869f75ed6eb69d425ebc952f82c85d03f80b8c076` | Includes [member reply](https://github.com/tensorflow/tflite-support/issues/770#issuecomment-1108777779) defining the unsupported-path boundary |

Exact generator/runtime/compiler dependency identities remain in
[TOOLCHAIN.md](../../docs/reproduction/TOOLCHAIN.md) and
[toolchain.json](../../docs/reproduction/toolchain.json). The focal Android path
uses Support/codegen 0.4.4 and standalone TFLite 2.13.0; P2's Task uses 0.4.4 with
a separate native integration. The Hand Task uses MediaPipe 0.10.14. Do not
replace their recorded interpreter/version uncertainty with current host
versions or a claim that all consumers share one runtime.

## Verification still required

Human review remains pending for the central API call, loaded/package identity,
preservation comparisons, exact stacks, P3 authority/bridge and Hand source
interpretation. Source checks or agent review of this rewrite cannot sign those
items. The source-only handoff is complete as documentation; an independently
usable external evidence deposit and fresh-machine recovery are separate open
tasks. Missing reconstructed records must not be filled with the older E1/E2
selection or silently counted as verified.

The manuscript can state the positive findings C3–C6 directly while keeping
their specific bounds nearby. Aggregate limitations belong in `sec:validity`;
they do not replace the evidence needed for each affirmative claim.
