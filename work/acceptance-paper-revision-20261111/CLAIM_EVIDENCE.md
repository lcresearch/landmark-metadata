# Acceptance-focused short-paper claim–evidence map

Target: **Validation Boundaries for Model Label Resources: A Controlled Classifier
Case Study**, [new short source](manuscript/paper.tex), based on main
`8005274e9eccbea30fb3189779f03e8d693b3720`. The current source, ledger, handoff and
index identities are pinned together in [CURRENT_MANUSCRIPT.json](../../docs/CURRENT_MANUSCRIPT.json).
This revision reorganizes the **10 November known-outcome rerun** around acceptance
requirements. It reuses the preceding revision’s saved-byte checks; no experiment
or raw-evidence audit is newly executed here. The lost October execution history
and human verification remain unresolved.

The [October short/full sources and ledger](../label-resource-revision-20261020/CLAIM_EVIDENCE.md)
are preserved. The full companion remains **historical October context**, not an
updated November report. All human claim statuses below remain **PENDING**.

## Acceptance decisions and evidentiary status

The short paper promotes the existing coverage matrix into its research question.
Section IV derives four engineering decisions; none is a new measured benefit.

| Acceptance requirement | Empirical basis | Recommended assertion and limit |
|---|---|---|
| Category access | C3; N2/N3; V1–V4 | Exercise the actual getter after process and inspect its result. The observed counterexample is configuration/input-specific; no user-study benefit was measured. |
| Specified display mapping | C4/C5; N4/N6; V2/V4/V6 | Compare the complete ordered mapping to an artifact-linked reference. An old list establishes change only; a legitimate replacement needs its own approved mapping. No accuracy or stable-ID claim. |
| Consumer compatibility | C6; N5/N8; V5 | Observe initialization and output access separately in the selected consumer, retaining the cause chain. No interpreter-isolated, latency or debugging-time claim. |
| Approved complete bytes | C13; N2; V7 | Verify a trusted complete-package digest, including resources. Both interventions change it. This protection is analytical coverage, not a new executed baseline or hash-bypass finding. |

The compressed evidence-history paragraph retains loss, known outcomes, both E1
interruptions, exclusion/selection, the P2 reader correction and P3 core-only scope.
N0/N1/N7/N8 below preserve the operational details. Supplementary public-report
screening is outside the paper’s experimental results and cannot enlarge its sample.

## Evidence keys and exact identities

[N0–N9 in evidence-index.json](../rerun-paper-revision-20261111/evidence-index.json) identify 1036 selected archive
members. Every entry gives its archive path, current root plus relative path,
byte size, SHA-256 and group membership. These are files, including preserved
copies/aliases, **not independent observations or models**. The complete November
archive has 2,120 members including its manifest. Its embedded manifest and every
member were checked against the existing [delivery receipt](../focal-rerun-20261110/delivery-record.json),
then all 1036 selected live files were separately rehashed against that manifest.
The index also identifies new editorial readbacks separately from archived run data.

Archive prefixes map to the roots in that index:
`run/` → `/home/hsz/landmark-evidence/focal-rerun-20261110/`,
`recovered-inputs/` → `/home/hsz/landmark-evidence/input-recovery-20261110/`,
`recovered-references/` → `/home/hsz/landmark-evidence/reference-recovery-20261110/`.
Paths below are **literal archive-member paths**, not downloadable URLs. A family
wildcard is a reading route; exact selected members and hashes are enumerated in
the JSON index. Original controller/invocation paths remain unchanged in the data.

| Key | Exact reading route and decisive fields | Evidentiary scope |
|---|---|---|
| N0 | `recovered-inputs/availability-before-recovery.json`, `input-recovery.json`, `independent-readback.json`, `original-acquisition.json` | The loss report is user testimony; the availability record documents 39 absent recorded paths and a bounded filename search, not proof that every backup is gone. Matching freshly recovered input bytes do not recover old execution records. |
| N1 | `run/PROTOCOL.md`; `run/provenance/pre-execution-source-freeze.json` (`protocol_sha256`, `source_files`, `adaptations`); `fresh-environment.json`; `run/python-setup/downloads.json`; `run/android/prerequisites/prerequisite-integrity-check.json`, `emulator-command.json`; `run/round/P2/EXECUTION_INPUT_FREEZE.json` and `prerequisites/dependency-pin-verification.json` | Known outcomes, initial freeze, matched dependency bytes, new Python distribution and software AVD. Continuation/reader/analyzer corrections have later identities. The old interpreter binary was not pinned; device presence does not establish usable KVM. |
| N2 | `run/android/model-preservation-audit.json` (`rows[*].checks`, `canonical_graph_sha256`, `distinct_canonical_graphs`); `run/android/audit-results.json` (`code_checks`); actual `run/android/{E1,E2}/variants/*/model.tflite`, generated `ContractModel.java`, classes, DEX and `build/consumer.apk` | Eight build aliases reduce to five model byte conditions and one graph. All 165 non-metadata buffers, ordered computation and selected code/native objects are compared. Description changes M; label interventions preserve M and pre-ZIP prefix. Equality is within the tested build family; APK asset/pre-load hashes do not intercept native interpreter memory. |
| N3 | `run/android/E1/static-results.json` (`structural_status`, `generation_status`), `build-results.json`; `executions/{primary,replay}/results.json` and `*/device/result.json`, both `*-input.rgb`, `*-output-0.f32`, successful `*-decoded.json`; install/instrumentation command records | Four conditions × two phases × two inputs = 16 observations: 12 returned lists and four caught getter failures. `observations[*]` identifies input preparation, inference, getter status, exact exception and generated getter stack. Primary aliases are selected views, not extra executions. |
| N4 | Equivalent `run/android/E2/` preparation/build and `executions/{primary,replay}/` records, actual continuation folders and complete input/raw/decoded files | Four conditions × two phases × two inputs = 16 returned lists. Every corresponding raw byte/score bit agrees; the full permutation maps to the next original position and changes 999 strings per input/phase. Restoration equals the original list. |
| N5 | `run/round/P2/{build-results,execution-results,EXECUTION_INPUT_FREEZE}.json`; `executions/primary/{wrapper,task}/*/device/`; `run/readback/p2-after-message-fix.json` (`sections`, `units`, `cross_consumer_returned_score_comparisons`, `read_file_sha256`) | All 112 files read by the maintained P2 reader are included by exact identity. Ten configurations, 18 reached input observations, 16 lists, ten wrapper raw tensors and eight shared successful pairs. Public stages/cause chains distinguish wrapper getter from Task construction. Native Task raw tensors are unobserved. |
| N6 | `recovered-references/{I01-publisher-model,I06-tfhub-lite-model,F01-publisher-labels,F07-pinned-lite-card,F10-pinned-parent-card,F11-explicit-class-order}/body` and acquisition records; `run/p3-core-attempt2/{input-identities,bridge,graph-descriptor,display-order-comparison,results}.json` | Six pinned inputs; `bridge.checks` and per-buffer hashes; all 1,000 positional comparisons; `matching_positions` = 1000/1/1000. Explicit card→parent/background rule. No deletion comparison, 30-request search or auxiliary synset rerun. Stable IDs ABSTAIN; prediction accuracy NOT_EVALUATED. |
| N7 | `run/stages/e1-primary/command.json`, `run/stages/e1-primary-attempt2/command.json` and their earlier RUNNING versions; `run/provenance/primary-attempt1-relocation.json`; E1 `primary-interrupted-attempt1/` and `*-provenance/{previous-results,continuation}.json` plus partial files | Two `INTERRUPTED` stages with null exit codes. The first attempt is retained but excluded; the second contributes original/description/deletion, and separate continuation contributes restoration. Selection, relocation and copied-view hashes preserve invocation history; do not pool first-attempt or alias files into the 32 observations. |
| N8 | `run/readback/p2.json`, `p2-after-message-fix.json`, `verify_p2_records.before-message-fix.py`, `verify_p2_records.after-message-fix.py`; `run/stages/android-metadata/`, `run/stages/p3-core/`, `run/p3-core/` | The original P2 exact-message FAIL is preserved. The full Java cause appears in unchanged device bytes and historical documentation; the reader correction changes the expected string, not outcomes. Failed metadata acquisition and the first P3 restoration-name analysis attempt remain separate from successful later attempts. |
| N9 | `MANIFEST.json` in the archive; packaging source `rerun-source/package_evidence.py`; committed run receipt and separately indexed new `archive/archive-readback.json` | Archive SHA-256 `57970b8ff5a4127caf11b13bdc9837ed2479c13dbb488cfc5262506a76535afd`; 3,321,366,905 bytes, 2,120 members. Local byte integrity, not authenticated historical provenance, a complete offline environment, external backup or anonymous reviewer access. |

The complete Task cause is:
`Error occurred when initializing ImageClassifier: Got 1000 class(es) for output index 0, expected 999 according to the label map.`
The outer `IllegalStateException` remains in the cause chain; the cardinality
`IllegalArgumentException` is not a missing-library diagnosis. The new readback
passes all 348 checks with evidence-validity, coverage and historical-outcome
sections reported separately. Negative tests reject truncation, additional text,
wrong cardinality and wrong exception type.

## Disposition of all 16 existing claim IDs

Historical S IDs resolve in the unchanged [48-source index](../paper-rewrite-20261004/claim-sources.json).
At the preceding saved-byte review, forty-seven indexed files matched in the checkout. **S40 is a maintained
reproduction README that has changed**; its exact old bytes were recovered from
Git commit `87290c2f7571d1fdf5cc2e56286a0ecff5b984ac` and match the old hash. The frozen November
index records both identities and that resolution. Subsequent code cleanup moved
some source paths into the fixed Git archive; use the archive manifest for those
paths rather than interpreting the old index as current working-tree availability. No old pin was refreshed to
hide the mismatch. Source identity does not make an old report's underlying
execution evidence available. Current availability is supported by N0/N9.

| Claim | Current disposition and paper location | Specific evidence | Limit / human status |
|---|---|---|---|
| C1 | Retain as definitions, §II/IV | N1 protocol; historical S01–S03/S19 | S structural acceptance, I reference-backed association and D selected decoder compatibility are distinct; P is intervention preservation. These are analytical distinctions, not a new inference method. PENDING. |
| C2 | Rebind preservation/restoration to November, §II/III and Table I | N2 actual models/code/APKs and audit; N3/N4 full raw/decoded comparisons; N5 wrapper pairs | Description changes M; other interventions change F. Restoration is payload/behavior, not original ZIP identity. No cross-history DEX or native-memory claim. PENDING. |
| C2R | Historical construction audit stays historical; new replay is separately identified, §II/V | Old S43; new N3/N4 phase records and N7 selection | New primary/replay are agent-collected observations on one graph, not independent human reproduction. Original audit raw records remain unavailable. PENDING. |
| C3 | Rebind actual-getter failure to November, §III-A | N3 deletion device records for both inputs/phases; N2 actual source/classes and APK attribution | Inference succeeds before four caught getter errors. Injected condition, not a natural defect or observed production crash. PENDING. |
| C4 | Rebind association change to November, §III-B | N4 all raw/decoded positions, permutation/restoration and replay; N7 timing/selection | 999 changed display strings, not 999 image errors. Wrapper category index is unset; use verified output positions. Known-outcome rerun cannot establish October predeclaration timing. PENDING. |
| C5 | Retain only newly rechecked six-input P3 core, §III-B | N6 bridge checks, pinned bodies, card relation, explicit offset and full map | 1000/1/1000 matching positions; stable IDs ABSTAIN. No fresh 30-request search, synset inquiry, deletion mapping, training-lineage or image-truth claim. PENDING. |
| C6 | Rebind configured stage comparison to November, §III-C | N5 actual files and maintained reader; N8 initial/corrected readback; source S10 and pinned Task/TensorLabel implementation references | Ten configurations, 18 observations, eight successful pairs. Task raw tensors unobserved; classify combines stages and native integrations/interpreters differ. PENDING. |
| C7 | Historical auxiliary Hand context only, §IV signpost | S20–S22 and unchanged October companion | Not rerun or newly raw-verified. No second executed generated Android wrapper claim. PENDING. |
| C8 | Historical external static context only, §IV signpost | S23 and unchanged October companion | No new external-original execution, prevalence or natural runtime-defect claim; old denominator is not a November sample. PENDING. |
| C8D | Not a quantitative result in this short paper | S45–S48 and preserved development ledger | Development counts/aliases are historical; not rechecked as independent runtime cases. PENDING. |
| C9 | Retain explicitly historical negative result, §IV | S24–S26, especially [old baseline table](../../sources/metadata-contract-audit-20261004T062010Z/baseline/RESULTS.md) | E5 added zero rejections over the matched simple/Task baseline on five conditions. That baseline family was not rerun/recovered; new P2 is not a new E5 comparison. PENDING. |
| C9E | Historical E5 fixture limits only | S26/S44, earlier ledger and companion | Missing later E5 catalog remains missing. No all-65 validation or method superiority. PENDING. |
| C10 | Historical parser lesson only, §IV signpost | [8 October isolated parser report](../preaudit-followup-20261008/parser/REPORT.md), S27–S29 with their distinct history | No new JVM/FileUtil experiment, Task inference or complete checker validation; original raw history was not recovered. PENDING. |
| C11 | Retain documented engineering antecedent, §I/V | S30–S32 and unchanged references [15–16] | Support #770 concerned an unsupported segmentation route. Its artifact was not reproduced here. PENDING. |
| C12 | Retain two bounded empirical contributions, §I/VI | N2–N7 for this case; S01/S02/S33–S37 for the dated prior-work comparison | Controlled interface contrast and configured stages; P3 qualifies interpretation. No new method, field-wide firstness or fresh literature survey. PENDING. |
| C13 | Update coverage matrix, Table II/§IV | V1–V7 below, tied to N3–N6 and versioned source | Property coverage plus analytical integrity reasoning; no measured developer omissions, cost savings or prevention rate. PENDING. |

## Coverage-matrix row crosswalk

In the short paper, **O** now means a **November observation**, **S** a versioned
source explanation, and **A** an analytical implication. The table's S legend is
not an additional experimental outcome. Historical E5 results are explicitly
outside these new O cells. Empty P3 deletion coverage remains unmeasured.

| Row | Exact new evidence / explanation | Interpretation |
|---|---|---|
| V1 population | N3/N4 `static-results.json` structural fields, generation logs and preparation-stage records; executed `prepare_e1.py:prepare` calls `MetadataPopulator` and E2 invokes that same function. Source route also indexed by the N1 source freeze. | New acceptance at the tested operation; not all official validators or label-count correctness. |
| V2 raw regression | N3/N4 complete 4,000-byte raw files for both inputs/phases, compared in the Android audit; N5's ten wrapper tensors. | Equal bytes under fixed inputs/configuration; no native Task raw-tensor observation. |
| V3 wrapper construction/process | N3/N4 `device/result.json`: `model_loading_status`, `observations[*].inference_status`; N5 wrapper units. | Both stages return even for deletion; the subsequent getter can fail. |
| V4 generated getter | N3 deletion exception/stack and absence of decoded output; N4 full returned lists; N2 unchanged generated source/classes; S10 TensorLabel path. | Four caught deletion errors; successful permutation still changes 999 strings. |
| V5 Task initialization | N5 Task device records, controller/build attribution and empty deletion observation list; N8 full cause text; S10 implementation trace. | Construction rejects count mismatch before either classify input. No semantic truth oracle. |
| V6 reference map | N6 six pinned bodies; `bridge.json` checks and all entries in `display-order-comparison.json`. | Qualified display agreement only; deletion unmeasured, full historical search not repeated. |
| V7 full-package identity | Different actual model SHA-256 values in N2 and [input inventory](../../docs/reproduction/inputs.json); analytical property of trusted complete-package identity. | Would detect changed package bytes; no executed release-defense experiment or semantic guarantee for approved replacements. |

## Reading and reproduction status

The new [saved-byte readback helper](../rerun-paper-revision-20261111/recheck_core.py) applies only recorded output
redirections to pinned historical Android audits, then invokes maintained P2 and
P3 readers into a fresh directory. Original receipt-pinned records were checked
unchanged afterward. Its adapted sources and patches are retained with new
readbacks; this is reuse of those audit methods, not an independent implementation.
[Archive verification](../rerun-paper-revision-20261111/verify_new_archive.py) reads without extracting or mutating
input material. [Index construction](../rerun-paper-revision-20261111/index_evidence.py) verifies every selected
current file against the already pinned archive manifest. See [VALIDATION](VALIDATION.md)
for this editorial build; the [preceding validation](../rerun-paper-revision-20261111/VALIDATION.md) records actual saved-byte commands/results and limits. See [author handoff](ARTIFACT_HANDOFF.md)
for six still-unsigned questions.
