# Measured outcomes and actionable implications

The most direct supported use of this study is **designing and interpreting tests
of a particular generated interface and its model package**. The evidence shows
specific ways a load-only check, a raw-output comparison, or a nominally matched
preflight can miss a later interface consequence. It does not measure how often
this happens in deployment, developer time saved, or harm to users. This is an
importance assessment, not a new experiment or a novelty certification.

## Inspection scope

This task follows [the bounded protocol](PROTOCOL.md) and reuses the
[claim inventory](../20261004-contribution-review/CLAIM_INVENTORY.md). Evidence
levels are kept separate:

- **Recorded experiment:** an existing execution or comparison reported by the
  study. Its report is readable; this is not a fresh model run.
- **Read back now:** selected old result records and input/output bytes were
  inspected and compared in this task, as detailed below. Current SHA-256 values
  identify those bytes; they do not authenticate the full original archive.
- **Source inspected:** first-party harness/checker code establishes which calls
  and checks the program expresses. It does not by itself prove their execution.
- **Engineering implication:** a test or diagnostic action logically supported
  by the observed counterexample. It is not a measured developer benefit.

No generator, compiler, model, interpreter, emulator, or inference was executed.
No new model was downloaded. The old sealed manifests, APK contents, generated
classes, graph/weight equality and publisher-reference retrievals were not
reauthenticated in this task. Human audit remains pending.

### Bounded readback performed now

The program actually executed for this readback and its output remain outside
the source-only repository at
`/workspace/significance-review-20261004/outcomes/read_existing.py` and
`/workspace/significance-review-20261004/outcomes/readback.json`. The
[provenance index](outcome-sources.json) records their digests, the 59 external
files read, and inspected repository source/report digests. The readback is a
fixed finite selection, not a complete replay or a reusable archive verifier.

The first-party code is retained as
[scripts/read_existing_outcomes.py](scripts/read_existing_outcomes.py). It adapts
the executed script by requiring a new external `--output-dir`, refusing existing
or in-repository output directories, writing its report exclusively, and allowing
explicit historical input roots. The comparison selection/logic is retained.
`outcome-sources.json` records both distinct script hashes and their relationship.
This maintained version was syntax/CLI checked, including both output-refusal
paths; it was **not** used to produce the readback reported above. The old report
hash was unchanged after those checks. A future readback command is:

```bash
python research/20261004-significance-review/scripts/read_existing_outcomes.py \
  --output-dir /workspace/significance-review-20261004/outcomes-next
```

The historical input roots default to the locators below and may be supplied
with `--e2e-root` and `--p2p3-root` after recovering those excluded inputs. The
script reports comparison booleans as data; a zero process exit is not a
universal evidence-PASS certificate. Review the report and its inspection scope.

| Selection | Fresh readback of old evidence | Not re-established here |
|---|---|---|
| E1 primary: original, description, deletion, restoration; two prescribed inputs each | Four stage records, input bytes, raw float bytes, and six successful decoded lists. All loads/inferences recorded PASS. Both deletion observations record getter FAIL; stack traces enter `ContractModel$Outputs.getProbabilityAsCategoryList` and report 999 labels versus axis-1 size 1000. All raw payloads equal their phase original; each input/raw digest agrees with its record. Successful lists retain all 1000 score bits and labels. | New execution, sealed-manifest authenticity, APK identity, graph/code preservation or replay independence. |
| E2 primary: original, description, permutation, inverse; two inputs each | Four stage records and eight decoded lists. All getters recorded PASS. All raw payloads equal their phase original; digests match records. Every successful list has positions 0–999, and every decoded score bit equals both raw output and original. Permutation changes 999 labels on each input; controls/restoration change zero. | Predeclaration chronology or independence of the original execution. |
| P2 deletion: wrapper and Android Task | Both existing device records and stacks read. Wrapper records load/process PASS and actual getter failure on both inputs. Task records failure during construction, with the nested label-cardinality cause; input preparation/classify are not reached. | Complete ten-unit P2 re-audit, Task raw tensors, timings, or identical native implementations. |
| P3 stored comparison and bridge records | Recounted the complete 1000-position stored display-label table: original/restoration each agree at 1000 positions; permutation agrees at one. Bridge/reference-chain JSON read for scope. | Model-byte bridge, reference authority/independence and retrieved-document hashes are historical results, not recomputed here. |

E1/E2 above contain eight phase/variant aliases and 16 repeated input
observations, representing five model-byte conditions of one canonical graph.
They are not eight independent models. Fourteen decoded lists and two caught
getter exceptions were available in these primary records. P2 is a separate
later comparison. Nothing in this readback pools them into a larger independent
sample.

The E2 `rgb_pattern` witness is also present in the decoded bytes: position 904,
score `0.23542051017284393` (float bits `1047597587`), changes from `window screen`
to `window shade`. The recorded P3 display-order reference supports the former
association for that position through its qualified graph bridge. Neither the
synthetic input nor that display-order comparison establishes the correct class
of an image or stable class identities for repeated display names.

## Scenario–check–consequence matrix

The scenarios below describe decisions an integrator or test author could face.
The controlled interventions establish the corresponding mechanism; they do not
establish how frequently practitioners make these changes.

| Engineering scenario / existing check | Observed consequence and evidence | Supported developer action | Remaining importance gap |
|---|---|---|---|
| Accept a packaged classifier after metadata parsing/population, compilation and a load smoke test | Recorded E1/baseline: all five core conditions populate and compile; deletion loads, runs and then fails in the actual category getter. E1 stages/exception/raw bytes read back now. | Include the public output getter used by the application in an integration smoke test; record its failure separately from loading and inference. On this fixture, a load-only check is insufficient to establish category-getter success. | No user study, incident rate or measured reduction in escaped defects. This does not show load-only tests are common. |
| Accept a resource update because numerical regression outputs match | Recorded E2: permutation and inverse preserve raw outputs, yet permutation changes 999 exposed labels while getter succeeds. Bytes and full decoded lists read back now; P3 adds a recorded publisher display-order specification. | If association stability is a requirement, compare label–score–position associations as well as raw scores. Use a trusted reference for correctness; use baseline comparison only for change detection, since intended label changes may be legitimate. | No demonstrated prediction-accuracy loss, wrong image classification, user-facing decision or production exposure. |
| Choose or migrate between official consumer configurations | Recorded P2: same API-30 x86_64 Android environment, wrapper rejects deletion at getter; Task 0.4.4 rejects during construction. Deletion device records read back now. | Place exception handling/tests at the selected consumer's public boundary; do not infer one API's acceptance or failure stage from another. | Stage ordering is not elapsed time. No latency, energy, safety-superiority or migration-cost result; native integration/version differences remain. |
| Diagnose Android Task's outer initialization exception | P2 cause chain starts with `IllegalStateException: Error getting native address of native library: task_vision_jni`, followed by `IllegalArgumentException` identifying 1000 classes versus 999 labels. Read back now and actual catch/cause-chain source inspected. | Preserve and inspect the cause chain; in this unit the nested diagnostic points to label cardinality, not proof of a missing native library. | No measured debugging-time saving, no claim that all native-address errors have this cause. |
| Add static preflight before constructing a consumer | Recorded five-condition baseline: E5, the matched simple decoder baseline and Task initialization reject exactly deletion; metadata displayer/populator have different scopes. Report/code inspected, raw baseline invocations not replayed here. | A selected-path preflight can place an existing cardinality diagnostic before this runtime call. Keep its scope and library/resource parsing fixed. | Zero extra rejected core conditions for E5 over the strong baseline or Task initialization. No novel rule, overall detection superiority or practical benefit measurement. |
| Reimplement the consumer's label count in another language | Recorded checker audit: Python `splitlines()` gives false compatibility on VT and false incompatibility on U+2028 relative to actual Java FileUtil/TensorLabel probes. Report and probe/helper source inspected; raw probe path unavailable at its checked locator. | Match the loader's parsing semantics and differentially test representative boundaries against the actual pinned library; a shared parsing assumption makes baseline agreement insufficient. | These are injected resources exposing our checker/baseline bug. No natural official-validator defect, model inference or Android end-to-end parser failure is established. |
| Transfer a metadata finding across consumer paths | Recorded Hand: role-reference mismatch and changed generic bytecode binding; official Hand Task decoded outputs unchanged on one prescribed image. Report/source inventory inspected, no fresh bytecode/Task run. | State the actual consumer and affected association. An index-role mismatch does not establish that every task API uses that association or that swapping it repairs decoder suitability. | No universal metadata insensitivity, second executed Android-wrapper failure, task accuracy or user impact. |
| Treat broader static applicability as deployment incidence | Recorded E4: 15 new canonical groups, all structural checks accepted/all semantic checks abstained; 8 raw wrappers compile, 7 fail; no external runtime. Report read. | Distinguish unsupported generation, static decoder incompatibility, missing reference and executed failure when reporting scope. | No prevalence denominator, supported natural end-to-end failure, general detector accuracy or runtime generalization. |

The first two rows are counterexamples to using those limited test oracles as
sufficient evidence of the public interface property. This is a direct logical
implication of the recorded observations, rather than a measured comparison of
developer testing workflows. The recommended actions may be conventional good
engineering; their availability does not itself establish a novel testing method.

## What can and cannot carry the significance argument

**Supported:** The tested public interface exposes behavior beyond raw model
computation. A resource mismatch can survive loading and successful inference;
a successful getter can expose a changed, reference-disagreeing display
association without changing scores. A comparison that records only raw values
or a single overall success bit omits these distinct outcomes. The same-Android
comparison makes the location of failure actionable for testing and diagnosis in
the two specified configurations.

**Supported, but narrower:** The parser counterexamples provide an executed
reason to audit consumer-specific parsing assumptions in a cross-language
preflight. The affected systems are the study's own checker and simple baseline;
fixing them improves its supporting artifact. The existing five-condition
comparison does not demonstrate that E5 detects more than the matched baseline
or Task initialization. `ABSTAIN` honestly bounds unsupported judgments; it is
not a detected failure or proof of practical utility.

**Not established:** Natural EfficientNet resource drift, industrial adoption of
the tested path, deployment prevalence, user harm, uncaught application crashes,
accuracy degradation, latency/energy savings, lower debugging cost, or prevented
incidents. Official workflow documentation and public issue reports can provide
context, but they must retain their separate evidence levels. They cannot
retroactively turn injected EfficientNet or parser conditions into naturally
observed deployment failures.

The most defensible positive importance statement is therefore:

> For the tested generated classifier interface, assurance of graph computation
> or structural population alone leaves observable output-interface properties
> unchecked. Controlled executions identify which additional getter, association
> and consumer-specific checks are required to distinguish the demonstrated
> outcomes.

This supports an empirical lesson for integration testing and diagnostic scope.
Whether it is sufficiently new and substantial for a particular venue remains a
separate judgment. A claim of demonstrated ecosystem-scale impact or a superior
new checker is not supported by this evidence.

## Source locators

All paths below are repository-relative. Their current hashes are in
[outcome-sources.json](outcome-sources.json).

- `sources/metadata-contract-e2e-20261004T030536Z/E1/EXPERIMENT_E1_RESULTS.md`
  and `E2/EXPERIMENT_E2_RESULTS.md`; actual generated-getter harness under the
  same root at `scripts/ContractInstrumentation.java`.
- `research/20261004-p2-p3/P2/EXPERIMENT_P2_RESULTS.md`,
  `P2/scripts/ContractInstrumentation.java`, and
  `P2/scripts/TaskInstrumentation.java`.
- `research/20261004-p2-p3/P3/EXPERIMENT_P3_RESULTS.md` and
  `P3/scripts/analyze_reference.py` (prior inventory inspected its computation;
  this task reuses that inventory, rather than re-executing the bridge).
- `sources/metadata-contract-audit-20261004T062010Z/baseline/RESULTS.md`.
- `sources/repro-audit-20261004/reports/CHECKER_AUDIT.md`,
  `probes/probe_label_parser.py`, and `maintained/java_labels.py` under that root.
- `sources/metadata-contract-e2e-20261004T030536Z/E4/EXPERIMENT_E4_RESULTS.md`
  and `E7/EXPERIMENT_HAND_RESULTS.md`.
