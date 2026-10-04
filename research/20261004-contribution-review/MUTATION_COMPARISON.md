# Mutation, differential testing, and contract background

This is a bounded reading of two retrieved primary full texts and an unsuccessful
publisher retrieval for one background citation. It is not a systematic review,
an execution of either research tool, or a fresh verification of this project's
model experiments. The current manuscript at the protocol's starting commit is
the claim inventory. Retrieval records and hashes are in
[mutation-sources.json](mutation-sources.json); downloaded third-party material
remains outside Git.

## Source status

| Work | Inspected version and source level | Relevant locators |
| --- | --- | --- |
| Ma et al., *DeepMutation: Mutation Testing of Deep Learning Systems* | Full text, arXiv:1805.05206v2, 14 August 2018; retrieved PDF identifies this version. Publisher version/DOI not newly verified. | Sections III-A–C and Table I; IV-A–B and Table II; V-A–C and V-E. The Label Error definition is on PDF p. 4; model operators on pp. 5–6; evaluation on pp. 6–9. |
| Liu et al., *NNSmith: Generating Diverse and Valid Test Cases for Deep Learning Compilers* | Full text, arXiv:2207.13066v2, 30 December 2022. Its first page identifies ASPLOS 2023, Volume 2 and DOI `10.1145/3575693.3575707`; the publisher PDF was not separately retrieved. | Sections 2–4, especially 3.1, 3.2, and 4; evaluation Sections 5.1–5.4, Table 3 and the “False alarms” paragraph. Design starts on PDF p. 4, implementation p. 7, evaluation p. 8, bug examples pp. 10–11. |
| Meyer, *Applying “design by contract”* | The manuscript's bibliographic entry is *Computer* 25(10), 40–51, 1992, DOI `10.1109/2.161279`. Fresh DOI retrieval redirected to IEEE and returned HTTP 202 with an empty body and a WAF challenge header. No full text or abstract was obtained. | Bibliographic tuple remains inherited from the manuscript rather than newly authenticated. No source-passage claim is added here. |

There was one ordinary retrieval per work. The two successful full-text
retrievals ended source hunting. The IEEE challenge was not bypassed. Section
locators above concern the retrieved arXiv versions, not a claim that every later
tool release has the same scope.

## Technical comparison

| Dimension | DeepMutation, inspected paper | NNSmith, inspected paper | Current manuscript's narrower empirical object |
| --- | --- | --- | --- |
| Object and purpose | Training data/programs or trained DNNs are mutated to assess test-data quality and localize test weaknesses. | Synthesized DNN computation graphs exercise compiler/converter transformations and expose crashes or numerical inconsistencies. | A model package, selected resource, actual generated interface, and pinned consumer configuration; observations are interface outcomes and enforcement stages. |
| Intervention or generation | Source-level data/program mutation followed by training; or direct weight, neuron, activation, and layer mutation without training. | Operator specifications and an SMT solver generate valid, diverse graphs; input/weight search avoids exceptional floating-point values. | Predetermined description, associated-label deletion/permutation, restoration, and output-metadata exchanges. These are controlled artifact interventions, not a newly invented mutation-testing category. |
| What “label” means | The Label Error operator changes the label `l` in a training example `(d,l)` before training. It is not an associated deployment file mapping output positions to display strings. | The differential oracle is the numerical result of the reference implementation. The paper's operator/type constraints are not an independent class-order reference. | Associated label strings are consumed after the numerical result; later P3 supplies a separately scoped publisher display-order reference. |
| Comparison/oracle | Tests correctly handled by the original model are run on mutants; class-sensitive mutation score and average error rate measure behavioral differences. | Compiled results are compared with PyTorch reference results; an additional unoptimized compiler path helps localize conversion versus optimization problems. Numeric comparison tolerates floating-point variation. | Graph/weight and generated-code comparisons support causal isolation; output bytes, labels and exact failure stages measure effects. Raw equality is not the oracle for class meaning. |
| Preservation | Some layer mutations require matching input/output shapes to remain executable. Neither graph/weight identity nor identical numeric computation is the general mutation goal. | Type-valid graphs and semantic preservation by a correct compiler are central. Multiple executable representations of one generated graph are compared; this already studies preservation across transformations. | For the focal associated-file interventions, graph/weights, embedded metadata and generated code are held fixed while selected resource bytes change. Runtime numeric equality is separately observed on fixed inputs. |
| Actually executed path | Keras 2.1.3 with TensorFlow 1.5.0; serialized `.h5` mutants, MNIST/CIFAR-10 and three DNNs in the reported evaluation. | PyTorch-to-ONNX generation with TVM, ONNXRuntime and TensorRT target paths; the paper reports compiler and exporter defects. | The recorded E1/E2 path calls the generated Android public getter. The later parser probes are isolated real-library expressions and Task initialization, not additional Android end-to-end executions. |

The DeepMutation distinction follows its operator tables and workflow, not
merely the absence of the word “metadata.” Its 16 described operators alter
training sources or model structure/parameters. The reviewed methods and
evaluation do not present associated-file-only mutations that preserve the
graph, weights and generated code while changing a generated category getter.
This is a distinction from this inspected paper; it does not establish that no
mutation-testing work studies resources or deployment interfaces.

NNSmith is a particularly important boundary on novelty wording. Section 3.1
already uses operator input requirements and output guarantees, and composes
type-transfer constraints across connected operators. Section 4 uses
documentation and implementation to write those specifications. Its evaluation
already distinguishes conversion and transformation defects, exceptions and
successful executions producing inconsistent results. Therefore “contracts
across deployment transformations,” “valid model generation,” “differential
execution,” and “crash versus silent inconsistency” cannot stand alone as new
contributions here.

In the inspected NNSmith design and evaluation, the tested relation is compiler
preservation of computation, assessed through outputs from a reference backend.
It does not report the specific relation of an associated display-label resource
to a generated public category getter with numerical computation and generated
code fixed. That bounded difference survives this comparison. NNSmith's compiler
“semantic bugs” concern inconsistent computed results; they must not be used as
evidence that this study measured prediction correctness or task accuracy.

## Contribution decisions

| Candidate wording | Decision | Reason and replacement boundary |
| --- | --- | --- |
| “We introduce mutation testing for ML deployment artifacts.” | **Drop** as a broad novelty claim. | Mutation and differential testing already provide the general method. Describe the concrete intervention object and preservation assertions instead. |
| “We are the first to check contracts across representations or consumers.” | **Drop**. | Too broad for the bounded source set; NNSmith already checks computational preservation across executable representations. No exhaustive firstness search was conducted. |
| “A controlled study isolates interface consequences of label resources while graph computation and generated code remain fixed.” | **Keep, bounded**. | The intervention target, held-fixed objects, actually exercised getter and observations distinguish this study from the two inspected papers. This still requires the project's artifact evidence and does not alone establish research significance. |
| “Consumer-aware constraints and constraint composition are new.” | **Drop** as stated. | NNSmith already models implementation-specific requirements and composes operator constraints. A new resource/getter analysis would require a distinct implemented technique and evaluation; the current supporting E5 does not demonstrate that increment. |
| “Different configured consumers enforce the same selected resource condition at different stages.” | **Keep, narrow**. | This is a recorded empirical comparison, not a new checking rule or proof about all consumers. Same-Android execution still has different native integrations. |
| “Successful label permutation is a newly discovered natural misclassification bug.” | **Drop**. | It is an injected resource intervention. The evidence supports changed association and later disagreement with a publisher display-order reference, not task accuracy or a natural EfficientNet defect. |
| “The Java/Python parser counterexamples establish a new differential-testing method.” | **Drop**; retain as a concrete diagnostic result. | Differential testing is established. These counterexamples show why a preflight check must match the chosen resource parser, including false acceptance and false rejection by the historical checker/baseline. |
| “Design by contract is a new conceptual basis.” | **Drop**. | Treat it as background. This task did not obtain Meyer's full text, so do not add a purported fresh passage-level confirmation or an implementation comparison to it. |

The defensible remaining claim is an empirical characterization of a specific
cross-artifact dependency and its observed consumer boundaries. Calling that
dependency a “contract” organizes the evidence; the name itself supplies no
algorithmic novelty. Assessing whether the distinction is important enough for
the intended venue remains the separate significance task. Neither these papers'
reported bug counts nor their documented downstream examples can substitute for
practical evidence about this project's mechanism.

## Suggested bounded related-work paragraph

DeepMutation changes training data/programs or model parameters and structure to
assess test-data quality; its label-error operator concerns training examples,
not deployment display-label resources. NNSmith generates type-valid graphs and
compares compiled results with a reference backend, testing preservation through
conversion and optimization. These works establish mutation, constraint-guided
testing, and differential execution as prior techniques. Our narrower empirical
object is an association between a fixed computation, a selected associated
resource, and an actually executed generated getter. For the focal resource
interventions, both numerical computation and generated code remain fixed while
interface outcomes change. This distinction concerns the inspected works and
does not constitute an exhaustive firstness claim.

## Open checks

- Confirm the publisher identity/version for DeepMutation when a final
  bibliography is prepared; this comparison is explicitly to arXiv v2.
- Meyer's publication metadata and full text were not freshly authenticated;
  retain the background citation with that audit status.
- No tool-versus-tool detection experiment was conducted. Do not treat either
  tool's different input format or research objective as a missed detection.
- Human interpretation review, significance assessment, and broader nearest-work
  completeness remain outside this bounded subtask.
