# Bounded full-text technical comparison

Audit date: 2026-10-04 UTC. This is an automated research-agent literature audit, not independent human verification. It reviews four specified papers; it is not a systematic or exhaustive novelty search. No evaluated tool was installed or experimentally compared in this subtask. No historical evidence or manuscript was modified.

## Outcome

**PASS: all four full texts were available and method, implementation, evaluation, and limitation passages were inspected.** The publication identities were cross-checked against Crossref. The earlier abstract-only uncertainty about MLGuard, DocTer, and ACETest is resolved for the preserved versions below.

**Action required: the current manuscript's related-work comparison is incomplete.** `/workspace/metadata-contract-paper-rewrite-20261004T052625Z/manuscript/paper.tex:206` discusses DARA and documentation work, but does not cite MLGuard, DocTer, or ACETest. Adding those comparisons is justified. This audit does not establish that the current checker has an independently novel algorithm.

The reviewed methods do not demonstrate the particular complete join **model output → associated label resource → generated public getter → exact decoder implementation** in their reported methods and evaluations. This is a bounded distinction from four papers, not proof that no prior work covers the join. The current project must still demonstrate what it actually automates, what it assumes about templates, and what it adds over existing checks.

## Versions and provenance

Page numbers below are one-based PDF pages of these exact files. The three arXiv PDFs are author/preprint versions carrying the publication identity, not publisher-PDF identity claims. In particular, DocTer v4 was uploaded in 2024; the conference publication is ISSTA 2022.

| Work | Publication verified | Reviewed full text | SHA-256 |
|---|---|---|---|
| MLGuard: Defend Your Machine Learning Model! | SE4SafeML 2023; DOI `10.1145/3617574.3617859` | `sources/mlguard.pdf`, arXiv `2309.01379v1` | `82cac1ea02229afd329f73a3c672d84af4ac08bcea68c996628c2a37983d12be` |
| DocTer: Documentation-Guided Fuzzing for Testing Deep Learning API Functions | ISSTA 2022; DOI `10.1145/3533767.3534220` | `sources/docter.pdf`, arXiv `2109.01002v4` | `3510daa4fab4f0fef0d4c4014ca7abdf69c43cdf973bfeb3039a1798598d0ee8` |
| ACETest: Automated Constraint Extraction for Testing Deep Learning Operators | ISSTA 2023; DOI `10.1145/3597926.3598088` | `sources/acetest.pdf`, arXiv `2305.17914v2` | `932ce82dd736591649abd9139b9f8e7bf3564460f46d852591bbe75aa502bcec` |
| “I see models being a whole other thing”: an empirical study of pre-trained model naming conventions and a tool for enhancing naming consistency | Empirical Software Engineering 2025, 30:155; DOI `10.1007/s10664-025-10711-4` | `sources/dara.pdf`, preserved Springer version of record | `67c547af18d1083ff15971e144d9f30554d6825fd47eab91b707555af83ab6f4` |

`retrieval-results.json` records exact request/final URLs, HTTP results and PDF/text conversion commands. `version-pinning.json` verifies that the explicit arXiv version URLs return bytes identical to the initially downloaded PDFs. DARA was copied from preserved evidence at `/workspace/metadata-contract-paper/sources/dara-paper.pdf`, verified against its old `results/literature-downloads.json`; its recorded original URL is `https://link.springer.com/content/pdf/10.1007/s10664-025-10711-4.pdf`. It was not freshly downloaded or represented as a new retrieval.

## Closest-work matrix

“Not demonstrated” means absent from the described method and evaluation of the reviewed version; it is not a claim about every possible adaptation or later version of that project.

| Work | Analysis input and source of constraints | Static/dynamic treatment | Wrapper or enforcement role | Complete artifact-to-getter join | Consequence for our claim |
|---|---|---|---|---|---|
| MLGuard | Developer-supplied contract specification, schema and probabilistic validation configuration; optional trained validation models | Proposed runtime pre/post checks, invariants, probabilistic violation handling | Explicitly proposes generated guard wrappers from code templates | Not demonstrated; the paper proposes a framework, not an implemented analysis of generated model bindings and associated label resources | “ML contracts”, “generated enforcement wrappers”, and “runtime validation” are existing ideas. Our executed characterization may differ from this vision, but cannot claim those ideas as new. |
| DocTer | API documentation, dependency parses, manually annotated abstract constraints; learned extraction rules | Offline extraction followed by concrete valid/invalid input generation and execution | Test harness invokes DL APIs; no deployment enforcement wrapper is demonstrated | Not demonstrated; dependency graph connects parameter constraints within APIs, not the focal model-package/getter chain | Automatic extraction of tensor shape/type/value constraints and constraint-guided testing already exist. A new contribution must be more specific than automatic shape checking. |
| ACETest | Actual DL operator validation code, error paths, user-controllability propagation, library-specific property summaries | Static LLVM/SVF constraint extraction; Z3 solves constraints to generate concrete execution tests | Python test scripts invoke operators; no deployment guard or residual runtime-obligation system is demonstrated | Not demonstrated; it follows operator code and API metadata, not the focal graph/resource/generated-interface chain | Deriving conditions from implementation is substantial prior art, including manual summaries and path reasoning. Merely moving a known check or adding a DEFER flag is not an established increment over it. |
| DARA | Computational-graph architecture, layer/parameter/connectivity features; learned classifiers versus supplied `model_type`, `architecture`, and `task` metadata | Dummy-input tracing for dynamic graphs, direct parsing for static graphs, then model classification | Assessment/warning use cases; no decoder guard wrapper | Not demonstrated; model-to-metadata comparison is central, but generated getter/label-resource/decoder compatibility is not the evaluated target | DARA cannot be dismissed as only documentation checking. Reference-backed output association and exact-consumer compatibility differ from its probabilistic architecture assessment. |

## Full-text observations and limitations

### MLGuard

- **Method:** §3.1, PDF p. 3, defines a developer-written contract specification and probabilistic detection/response configuration. §3.2 describes a proposed trainer for validation models, including possible AutoML support.
- **Wrapper mechanism:** §3.3, pp. 3–4, proposes selecting and instantiating contract code templates to produce wrappers containing model, validation models and checking/handling code.
- **Implementation/evaluation status:** §5, p. 4, is explicitly titled “FUTURE PLANS.” Prototype construction is in Phase 2 and industry evaluation in Phase 3. Thus the reviewed paper supports a design/vision attribution, not a claim that an empirically validated general wrapper implementation already solves our problem.
- **Scope:** uncertainty, distribution assumptions, schema, pre/post conditions and configurable responses. It is not a study of metadata-associated label order or actual code-generator tensor bindings.
- **Comparison caution:** absence of an implemented evaluation in this paper does not remove it as conceptual prior art; this audit did not inspect subsequent work or repositories.

### DocTer

- **Method:** §2.1, p. 3, describes rule construction, constraint extraction and testing. §2.2, pp. 4–5, normalizes API descriptions and annotates a sample with abstract constraints. §2.3, pp. 5–6, learns mappings from dependency-tree patterns to constraints. §2.4, pp. 6–7, instantiates them and handles constraint dependencies between API parameters.
- **Constraints:** structure, dtype, shape/dimensionality and valid values; this is more than a fixed set of manual per-API checks.
- **Execution:** §2.5, pp. 7–8, generates both conforming and violating inputs and executes target APIs. Its crash oracle is distinct from the caught getter exception or successful changed association in this project.
- **Implementation/evaluation:** §3, p. 8, names TensorFlow 2.1.0, PyTorch 1.5.0, MXNet 1.6.0 and Ubuntu 18.04, describes filtered APIs and annotation/tuning effort. §4 evaluates extracted constraints and test generation. These are paper-reported experiments, not rerun here.
- **Limitations:** §5, pp. 11–12, says complex nested or indirect parameter constraints are unsupported, documents manual annotation, and discusses parsing/coverage. §4.4, p. 11, attributes remaining low valid-input coverage partly to incomplete API documents.
- **Comparison caution:** it neither demonstrates our deployment-artifact join nor claims to accept arbitrary `.tflite` fixtures. Inability to feed it such a fixture must not be counted as a detection failure.

### ACETest

- **Method:** §3.1, p. 3, takes operator source and produces crash-inducing tests through validation-path extraction, constraint extraction and testing. §3.2, pp. 4–5, finds validation blocks through backward CFG traversal from error-handling calls and retains paths toward core functionality.
- **Condition derivation:** §3.3, pp. 5–7, identifies user-controllable values and restricts propagation to a constraint model, including tensor properties. Specific library accessors are mapped to property operations; some functions require manual handling. This is a direct technical predecessor to any proposed implementation-derived condition extraction.
- **Implementation:** §4, p. 7, uses an LLVM compiler pass, SVF graphs and Z3. Loops are unrolled once and loop continuation is ignored. New libraries require extraction/adaptation code and manually specified property functions. It is not a fully automatic arbitrary-library analyzer.
- **Evaluation:** §5.1, p. 8, evaluates operator-level TensorFlow 2.9.0 and PyTorch 1.13.0 APIs with defined exclusions and baselines. §5.2.2, p. 9, manually checks a sample of extracted constraints; §6, pp. 10–11, limits detected bugs to crashes. None of these numbers are our evaluation results.
- **Limitations:** §5.2.2 reports missing constraints due to loops, incomplete linking, pointers and constraints outside the implemented model. §6 notes randomness, analysis subjectivity and reliance on SVF. Avoid treating its extraction as complete or universally sound.
- **Comparison caution:** residual runtime checks for deployment consumers are not demonstrated here. Nevertheless, our proposed analyzer would still need a defensible technical difference from its source-derived constraints, rather than only a new application name.

### DARA

- **Method:** §7.2.1, p. 31, begins from pretrained weights and constructs graph architecture for feature extraction and classification. §7.2.2, p. 32, distinguishes dummy-input tracing for dynamic graphs from direct parsing of static graph definitions; §7.2.3, p. 33, represents layers, parameters, dimensions and connectivity.
- **Decision basis:** §7.3.3, p. 40, compares predicted architecture-related labels with supplied metadata. This is learned assessment, not an independent class-index specification or a decoder precondition proof.
- **Evaluation:** §7.3.1, p. 39, obtains target labels from `config.json` and model-card metadata, reports loading/exclusion constraints and dataset construction. §7.4 evaluates naming-related predictions, not generated public getter behavior.
- **Limits:** §8, pp. 46–49, discusses feature information loss, imbalanced data and ecosystem scope. §9.2, pp. 50–51, frames the tool as assessment with potential warning/integration use cases, not mandatory name correction or a complete solution.
- **Comparison caution:** never characterize it as just a model-card tool or claim graph-versus-metadata consistency is a new general principle. Architecture/task metadata labels in this paper are also not the same object as classifier display strings in E2.

## Implications for the current manuscript and next work

1. Add the three missing direct references, with MLGuard explicitly identified as a vision and DocTer/ACETest as implemented constraint-extraction/testing approaches.
2. Retain **executed, preserving interventions through an actual generated public interface** as the current empirical contribution. Do not turn literature absence into a new algorithm claim.
3. State the candidate method increment precisely: join the selected getter to its actual tensor, postprocessing and associated resource, then instantiate exact-library preconditions. Our complete-chain coverage, handling of unknown syntax and runtime obligations still need implementation and evaluation evidence.
4. A static/dynamic/semantic-unknown distinction is useful reporting vocabulary; DEFER or ABSTAIN labels alone do not establish novelty. Do not attribute arbitrary semantic inference to these prior methods or to our checker.
5. Use official comparable consumers and reasonable count/decoder baselines experimentally. Use these papers for technical positioning unless a justified common evaluation task is built; do not record unsupported-input tool invocations as failures.

## Audit limits

- This bounded review examined four requested full texts and their bibliographic metadata. It did not systematically search all executable-interface, contract-inference, model-packaging or software-contract work.
- It did not inspect or rerun the papers' repositories, validate their empirical findings, or establish whether later releases have additional capabilities.
- MLGuard, DocTer and ACETest were reviewed in the exact arXiv versions identified above; publisher PDFs were not independently compared.
- Poppler 26.05.0 converted PDFs. DocTer conversion emitted three “Badly formatted number” warnings in each text mode; conversion exited 0 and the relevant prose was available. We do not rely on its extracted tables for a numerical comparison.
- DARA was recovered from old preserved evidence, while the other PDFs and all four Crossref responses were freshly retrieved.
- Human verification remains pending. No novelty score or submission-readiness gate is assigned.
