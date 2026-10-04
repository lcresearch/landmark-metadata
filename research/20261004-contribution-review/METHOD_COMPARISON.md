# Four closest method papers: bounded technical comparison

This is a fresh reading of recovered, digest-pinned full-text bytes. All four
PDFs match the hashes recorded by the earlier literature audit. This task
re-extracted the texts and inspected the method, implementation, evaluation, and
limitation passages identified below. It made no new download, installed or ran
none of the papers' tools, and did not rerun this project's experiments. Exact
paths, hashes, commands, and access status are in `method-sources.json`.

The comparison supports an empirical positioning of the current study. It does
not establish a new general contract-analysis algorithm or an exhaustive novelty
claim. The current working manuscript already cites these four papers; the old
audit's instruction to add missing citations no longer describes the current
manuscript.

## Versions and direct comparison

Page numbers refer to one-based PDF pages of the exact reviewed files. The
arXiv files are author versions, not asserted to be identical to publisher PDFs.
DocTer v4 postdates its ISSTA 2022 publication.

| Work and exact version | Analysis object and contract/evidence source | Automated and manual parts | Executed evaluation and its scope | Overlap that constrains our claim |
|---|---|---|---|---|
| [MLGuard](https://doi.org/10.1145/3617574.3617859), SE4SafeML 2023; arXiv 2309.01379v1 | Developer-specified ML preconditions/postconditions, schema and probabilistic validation/response configuration | Proposed code-template instantiation produces model guards; optional validation-model training/AutoML; developer supplies the contract | The reviewed paper is a vision. Prototype construction and industry evaluation are future phases, not completed experiments | ML contracts, generated checking wrappers, and runtime violation handling are prior ideas. Distinguish a proposed guard generator from our experiments on an existing generated interface; do not dismiss conceptual overlap because it is a vision paper |
| [DocTer](https://doi.org/10.1145/3533767.3534220), ISSTA 2022; arXiv 2109.01002v4 | Natural-language API parameter descriptions; structure, dtype, shape, values, and dependencies between parameters | Authors annotate a subset with abstract constraints; normalized dependency-tree patterns and association rules support automatic extraction; derived dependencies order input generation | Generates conforming and violating inputs and invokes DL APIs. Reported setup: TensorFlow 2.1.0, PyTorch 1.5.0, MXNet 1.6.0; extraction and crash-oriented testing | Automatic shape/type/value constraints, dependent-parameter checking, and controlled constraint violations already exist. Our label-deletion intervention is not a new category of constraint-guided testing |
| [ACETest](https://doi.org/10.1145/3597926.3598088), ISSTA 2023; arXiv 2305.17914v2 | Actual DL operator validation code, operator/API metadata, and error-handling paths | LLVM/SVF analysis finds paths; restricted user-controllability propagation constructs constraints; library-specific property handlers and common-function summaries include manual work; Z3 solves constraints | Generated Python tests invoke operators, with native/OneDNN/CUDA modes as applicable. Reported targets: TensorFlow 2.9.0 and PyTorch 1.13.0; crashes are the bug oracle | Implementation-derived preconditions, library-specific summaries, path reasoning, and solver-assisted testing are direct prior art. Calling a checker consumer-aware or adding runtime obligations does not by itself supply a technical increment |
| [DARA](https://doi.org/10.1007/s10664-025-10711-4), Empirical Software Engineering 2025, 30:155; preserved journal version | Model-derived computational-graph architecture compared with supplied `model_type`, `architecture`, and `task` labels | Dynamic-graph tracing or static parsing; abstract graph/feature extraction; trained classifiers; pipeline design and input choices supplied by authors; evaluation labels obtained from package metadata | Reported evaluation uses 4,108 PTM packages after explicit loading/tag exclusions, with classification and ablations. It assesses architecture/naming metadata, not exact class-index references | Model-content versus metadata consistency is established work. DARA is not merely a model-card completeness checker. Learned architecture assessment and exact supplied-reference agreement answer different questions |

## Passage-level observations

### MLGuard

- **§3.1, p. 3:** engineers write an ML Contract Specification tailored to an
  application; the specification includes probabilistic conditions, detection
  strategies, and response choices. The paper explicitly draws on declarative
  constraints in Deequ.
- **§3.2, p. 3:** a proposed trainer creates validation models from that
  configuration. AutoML and learned trigger thresholds are future mechanisms,
  not an evaluated automatically inferred contract system.
- **§3.3, pp. 3–4:** the code generator selects and instantiates contract code
  templates. The resulting wrapper contains the trained model, validation
  models, and checks/violation handlers. This is particularly close conceptual
  prior art for any claim about generated wrappers enforcing ML contracts.
- **§§4–5, p. 4:** the heading “FUTURE PLANS” and its Phase 2 prototype / Phase 3
  industry case studies delimit the evidence. There is no completed tool
  evaluation reported in this version; we did not inspect subsequent releases.

**Implication:** keep the distinction between executing an existing official
generated interface under controlled package interventions and proposing a
contract guard. Drop any claim that this study introduces ML contracts or
generated enforcement wrappers.

### DocTer

- **§2.1, p. 3; §§2.2–2.3, pp. 4–6:** rule construction, constraint extraction,
  and testing are separate phases. Manual abstract-constraint annotations feed
  optimization/association-based mappings from dependency-tree patterns to
  constraints. This is more than keyword matching or a hand-written rule for
  each API.
- **§2.4, pp. 6–7:** constraints can refer to another parameter's type or shape.
  A dependency graph supports topological input-generation order. Do not claim
  that relating separately described constraints is itself missing from prior
  work.
- **§2.5, pp. 7–8:** conforming inputs exercise core behavior; violating inputs
  exercise validation. Boundary mutations and concrete API calls are already
  part of the method. Its severe-crash oracle includes segmentation fault,
  floating-point exception, abort, and bus error; it excludes MXNet assertion
  aborts used as exceptions. Our caught Java getter exception must not be
  equated with that oracle.
- **§3 and §4.1, p. 8; §4.3, p. 10:** the paper describes library/version/API
  exclusions, manual annotation/tuning, an independently sampled parameter set,
  and a constraint-unguided input-generation comparator. These are reported
  evaluations, not results reproduced in this task.
- **§4.4 and §5, pp. 11–12:** incorrect/incomplete documents limit generated-input
  validity; nested or indirect parameter constraints are unsupported. Annotation
  effort is disclosed. The paper also reports intra-document inconsistencies;
  characterizing it as only shape fuzzing would be too narrow.

**Implication:** our exact output/resource/getter observation is a different
experimental target from its operator inputs, but mutation, dependency checking,
and constraint-guided execution are not new. A `.tflite` package is not its
declared interface, so inability to feed that package directly to DocTer is not
a comparative detection failure.

### ACETest

- **§3.1, p. 3; §3.2, pp. 4–5:** error-handling calls anchor backward CFG
  traversal. Extracted validation paths leading to core functionality are kept;
  testing aims to reach deeper operator logic. The source-to-constraint linkage
  is already substantive program analysis.
- **§3.3, pp. 5–7:** identification of controllable inputs, parameter/property
  propagation, and instruction constraints operate under a defined constraint
  model. Some library input/property functions must be manually identified;
  common validation functions have hand-implemented constraint construction.
  Thus a proposal using manually audited decoder summaries must explain its
  additional algorithm, rather than presenting summaries plus extraction as new.
- **§3.4 and §4, p. 7:** Z3 samples solutions; unconstrained properties are
  generated randomly and some extreme-value mutations are added. Python scripts
  invoke actual APIs. LLVM/SVF, one-time loop unrolling, ignored loop-continuation
  conditions, and adaptation work for a new library are explicit.
- **§5.1, p. 8; §5.2.2, p. 9:** eligibility excludes unsupported parameters,
  dependent/non-independent APIs, deprecated/TPU-only APIs and APIs without an
  explicit operator mapping. Constraint validation samples 25 operators per
  library and caps inspected paths for large cases. Do not promote the sampled
  result into a universal extraction guarantee.
- **§5.2.2, p. 9; §5.4.3 and §6, pp. 10–11:** missing constraints can arise from
  loops, incomplete linking, pointer limitations, and properties outside the
  implemented model. Testing core logic can miss validation-code bugs. The
  paper explicitly limits bug identification to crashes and discusses
  randomness, manual-analysis subjectivity, and SVF dependence.

**Implication:** the current project does not implement a comparable general
source-derived analysis or constraint solver. A future getter/resource join and
runtime-obligation system remains a proposal whose increment and held-out
evaluation would have to be demonstrated. The absence of a deployment residual
guard in this reviewed evaluation does not establish that such a guard would
be novel.

### DARA

- **§7.2.1, p. 31:** pretrained weights support an architecture representation,
  features, and predicted naming labels. Figure 7 defines inconsistencies as
  disagreement between classifier predictions and creator-supplied metadata.
- **§7.2.2, p. 32:** dynamic graphs use dummy-input tracing; static graphs use
  native parsing. Input choices were refined as conversions failed, and
  unsupported static operations are logged/omitted. This is an implemented
  computational-graph analysis, not text-only inspection.
- **§7.2.3, p. 33:** abstract architectures include layers, parameters,
  input/output dimensions, and connectivity. Those architectural dimensions do
  not alone specify the meaning of an individual classifier output position.
- **§7.3.1, p. 39; §7.3.3, p. 40:** evaluation labels come from `config.json`
  and model-card task tags. Large models, incompatible dummy inputs, missing
  configuration, untrusted custom code, and missing task tags cause exclusions.
  The anomaly decision compares graph-derived predictions with package labels.
- **§7.4, p. 41; §8, pp. 46–49:** reported results and limitations include
  similar architectures with differing training/task roles, feature information
  loss, imbalanced data, and ecosystem scope. These do not establish exact
  class-order correctness or decoder safety.
- **§9.2, pp. 50–51:** DARA is an assessment tool; anomalies warrant caution.
  Upload suggestions, warnings, and periodic checks are discussed applications,
  not reported proof that a platform deployment prevents our getter failures.

**Implication:** preserve the specific difference between architecture/naming
assessment and our reference-backed tensor/label association with observed
consumer behavior. Drop broad claims of inventing graph-versus-metadata
consistency or validating arbitrary semantics. In this comparison, DARA's
metadata labels (`task`, etc.) and E2's classifier display labels are different
objects despite sharing the word “label.”

## What remains defensible, conditional, or unsupported

| Candidate contribution | Recommendation after these four papers | Reason and remaining evidence requirement |
|---|---|---|
| Controlled evidence linking package associations to public-interface failure, successful association change, and reversal while graph/weights and generated code stay fixed | **Keep as an empirical contribution**, subject to the project's evidence audit | This is the concrete question answered by E1/E2/P3. These inspected methods/evaluations target other objects/oracles. Difference in target alone is not proof of research importance or novelty across the field |
| Contrasting the enforcement stage in pinned generated-wrapper and Task configurations | **Keep, narrowly stated** | An empirical boundary comparison; shared libraries and native-integration differences remain. Neither wrappers nor runtime preconditions originate in this study |
| E5 as a new automatic consumer-derived constraint-analysis method | **Withhold** | Current E5 is a template-scoped supporting checker. ACETest is direct prior art for implementation-derived conditions and manual summaries; DocTer already models parameter dependencies. A new analyzer is not supplied by relabeling the current one |
| S/I/D separation, with P as experimental preservation evidence | **Keep as analytical vocabulary** | Useful for stating what each observation supports. This bounded review does not establish a new exhaustive taxonomy; P is not a peer correctness dimension |
| ABSTAIN or a proposed runtime DEFER state as a standalone innovation | **Drop as an independent novelty claim** | A state name proves neither useful coverage nor correct residual checks. This task verifies no such implemented runtime-obligation method |
| Parser-specific preflight counterexamples and repair | **Keep as a scoped engineering observation** | Consumer compatibility depends on the loader's actual string semantics. The current counterexamples concern our checker/baseline, not a newly established official-tool defect or a new general differential-testing method |
| “No previous work joins graph, resources, getter and decoder” | **Drop the universal statement** | The described methods/evaluations of these exact four versions do not demonstrate that particular complete chain. A bounded non-observation cannot establish field-wide absence or firstness |

The strongest current positioning from this subcomparison is a controlled
empirical characterization with a supporting diagnostic. Its distinctive
object, intervention design, and observed execution boundaries should be
explained positively. Whether that characterization is sufficiently new and
important still depends on the broader bounded comparison and separate
significance assessment. These papers are technical-positioning references,
not experimental baselines that we ran or ranked.

## Evidence limits

The review inspected the cited full-text passages, not the papers' repositories,
later work, or all literature on contracts and artifact consistency. Fresh
extraction used `pdftotext` 25.03.0. DocTer emitted three “Badly formatted number”
warnings but exited successfully; the comparison relies on readable prose and
method descriptions rather than a numerical reanalysis of its extracted tables.
All publication/version identities remain those pinned by the historical audit;
no fresh bibliographic-service response is claimed. Independent human review
remains pending.
