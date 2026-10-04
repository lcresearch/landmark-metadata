# Contribution and related-work comparison

## Decision

The defensible current position is a **bounded empirical characterization of
model-package associations at executable consumer boundaries**, with E5 as a
supporting diagnostic. The comparison does not establish a novel general
validator or contract-inference algorithm. It also does not establish that the
empirical distinction is sufficient for a particular venue: the separate
significance assessment remains open.

The distinctive experimental object is the relationship between an ordered
model output, an associated resource, an actual generated public getter, and a
pinned consumer implementation. E1/E2 vary the resource while recording
preservation of graph/weights, generated code and tested numerical outputs;
P2 locates enforcement in two consumer configurations on one Android device.
The reviewed work constrains broad claims about each ingredient. Combining
established ingredients is not, by itself, a novelty proof.

## What this review actually checked

The [protocol](PROTOCOL.md) fixes the scope. The starting revision is
`81af34b10f8093e646179e51e658d597e6acc84b`; the current manuscript SHA-256 is
`6e77175d25ff0834978463bdb2359ab82e6cf62bc8e2d611960c23dcf8b48537`.

- **Primary research sources:** methods/evaluation/limitations passages in
  seven full texts: MLGuard, DocTer, ACETest, DARA, DeepMutation, NNSmith and the
  AIBOM preprint. Five were recovered and hash-checked; DeepMutation and NNSmith
  were freshly downloaded. This is not a systematic search.
- **Limited research sources:** Stalnaker et al. remain abstract/publication
  record only after a publisher HTTP 403. Meyer's original full text was not
  recovered; design by contract is treated as background, without a new detailed
  technical comparison to that article.
- **Official implementation:** fixed Support 0.4.4 source, including the
  schema, metadata reader/populator, generator, label loader, TensorLabel and
  Task ImageClassifier. Source inspection establishes where the conditions are
  written; it does not establish binary/source-build equivalence.
- **Our implementation and evidence:** the current manuscript, experiment and
  audit scripts, E5 implementation, and preserved reports. The experiment
  observations in the matrix are recorded findings, not fresh executions or a
  complete raw-byte audit in this task. Some historical evidence roots are
  visible on this machine; visibility alone does not authenticate their contents.

Exact sources, versions, hashes and passage/function locators are in the linked
comparison notes and JSON indexes. No paper tool or model experiment was run.

## Claim–evidence–prior-work–remaining-difference matrix

“Keep” means the bounded claim has a place in the paper; it does not mean novelty
or significance has been certified. Details of our evidence are in the
[claim inventory](CLAIM_INVENTORY.md).

| Candidate claim | Evidence currently available | Existing work or official capability | Remaining difference and disposition |
|---|---|---|---|
| Metadata and associated resources influence generated interfaces | Schema and generator source; Hand binding record; classifier resource-loading path | Official schema/codegen explicitly implement this. MLGuard also proposes generated contract guards | **Drop as a standalone novelty claim.** Use it to define the problem and the two distinct mechanisms: changed generated binding versus unchanged code loading changed resources |
| A resource intervention can produce an actual getter failure while model computation and generated code remain fixed | E1 recorded original/control/deletion/restoration executions, preservation comparisons and caught getter stack | TensorLabel already checks cardinality and axis suitability. DocTer/ACETest already use constraints to drive concrete tests | **Keep as controlled empirical evidence.** The increment is the observed package-to-public-interface path and causal controls, not a newly discovered cardinality rule. It remains an injected condition in one focal classifier |
| Successful output access can disagree with a specified display association while scores and positions remain fixed | E2 recorded permutation/reversal and numerical preservation; P3 publisher display-order bridge | Resource-index association is implicit in the official decoding path. DARA already compares model content and metadata, but evaluates learned architecture/naming labels | **Keep, narrowly.** Characterize interface-visible display-association disagreement against the qualified reference. Do not claim stable class-ID correctness, prediction error, accuracy loss or a new semantic-inference method |
| The same injected condition is exposed at different consumer stages | P2 recorded same-Android wrapper getter failure after process and Task construction rejection; official call-path inspection | Official implementations already contain the checks at those locations. MLGuard and ordinary contracts already motivate runtime enforcement | **Keep as a configuration-specific boundary comparison.** Pair observations with source explanation; neither delayed checking nor early rejection is invented here. Native integrations differ, and no latency or safety benefit was measured |
| Metadata-role changes do not necessarily propagate to task output | Hand reference-backed role/binding witness; unchanged official Task result on one fixed image | Model-derived metadata assessment predates this work; task-specific and generic consumers can use different paths | **Keep as a short boundary case.** It limits propagation claims. Do not infer universal Task insensitivity, full model repair or a second established end-to-end failure |
| E5 automatically derives consumer contracts | Actual E5 uses recognized getter patterns, naming conventions and encoded decoder conditions; five-condition baseline finds zero additional rejections | ACETest already analyzes implementation validation paths with library-specific summaries; DocTer learns constraints and parameter dependencies; official consumers enforce the focal rule | **Withhold the method claim.** Describe scoped diagnostics and their limitations. No general data-flow analysis or residual runtime-obligation generator has been demonstrated |
| Preflight compatibility must model the selected resource parser | Recorded VT/U+2028 probes show opposite wrong judgments by the historical Python checker/baseline; maintained valid-UTF-8 parser correction | Java FileUtil already defines its loader behavior; differential and constraint-based testing are established methods, including NNSmith's different target | **Keep as a scoped audit finding and engineering lesson.** The defects are in the studied checks. These probes do not show a natural official-tool bug, new Android inference failure or new differential-testing algorithm |
| The study introduces a novel mutation/differential-testing approach | Description controls, resource deletion/permutation and reversal; graph/code/numeric preservation records | DeepMutation mutates training data/programs or trained models; NNSmith composes operator constraints to generate graphs and compares compiled/reference numerical behavior | **Drop the broad method claim.** Our preserved computation plus changed resource/decoded association is a different intervention/oracle pairing. That specificity supports empirical positioning, not ownership of mutation or cross-transformation testing |
| S/I/D with separate P is a new general correctness framework | Definitions and experiments distinguish population acceptance, supplied-reference agreement and selected-decoder compatibility; P checks the intervention | Existing contracts, documentation completeness, consistency analysis and runtime checks already address related distinctions | **Keep as analytical vocabulary.** Do not claim an exhaustive taxonomy, certification hierarchy or semantic oracle; P belongs to causal validity |
| External fixtures establish generalization or detector superiority | E4 static scope records and E5 outcomes with exclusions/abstentions; no external runtime study in that evaluation | DARA and documentation studies evaluate different populations/tasks; comparable official/simple core baselines already reject deletion | **Narrow to applicability and coverage reporting.** Mutations, aliases and inputs are not independent models. No prevalence, detector-accuracy or broad superiority result follows |

## Official capabilities are separate baselines

The [implementation comparison](OFFICIAL_BASELINES.md) supplies exact source
links and explains these distinct boundaries:

1. **Metadata reading** extracts metadata and resources. Readability is not a
   promise of all downstream validations.
2. **Metadata population** checks metadata structure and tensor-metadata
   cardinality. Counting output-metadata entries is different from counting
   labels inside an associated file.
3. **Generated interface construction and processing** load resources and run
   the model; **category getter evaluation** constructs the selected TensorLabel
   path and reaches its cardinality/axis checks.
4. **Task ImageClassifier initialization** checks its output/label compatibility
   in its own initialization path. Its check must be located in the actual
   ImageClassifier call chain, not attributed solely to another classification
   postprocessor that happens to enforce a similar predicate.

Consequently, “the official validator missed the error” is too vague. Name the
entry point, version, promised condition and observed stage. The label-count
requirement and its implementation are prior capability. The study contributes
the measured relationship among paths and interventions within the tested scope.

## Technical positioning by research family

The [four-method comparison](METHOD_COMPARISON.md) rules out broad firstness for
ML contracts/guards (MLGuard), documentation-derived shape/type/value constraints
and dependencies (DocTer), implementation-derived validation conditions and
manual library summaries (ACETest), and graph-versus-metadata assessment (DARA).
The current paper already cites these four; adding their names again would not
resolve the novelty question.

The [mutation comparison](MUTATION_COMPARISON.md) adds two specific constraints
on the framing. DeepMutation's label-error operator changes training sample
labels and leads to a new trained model; that is not the same resource as a
released classifier's display-label file. NNSmith already tests numerical
behavior across compilation backends using valid generated graphs. Thus
“contracts across deployment transformations” would be an overly broad claim
unless a separately implemented method and comparison justified it. Here the
specific object is the resource-to-output association exposed by a public API,
including successful calls whose returned association changes.

The [background comparison](BACKGROUND_COMPARISON.md) establishes that AIBOM
completeness explicitly distinguishes field coverage from stronger substantive
quality. Our S measurement is a different official population path, not an AIBOM
score. The inaccessible Stalnaker full text prevents a stronger negative
comparison to that work. These studies cannot supply practical-impact evidence
for our particular injected failures merely because they concern model reuse.

## Recommended contribution wording for a later rewrite

**Primary empirical contribution:**

> We characterize how associated-label interventions propagate through an actual
> generated classifier interface under fixed graph/weights and generated code.
> In the tested configuration, one intervention reaches a getter exception after
> inference, while a count-preserving permutation completes and exposes a
> display association that disagrees with the qualified publisher reference.
> Controls and reversal bound the attribution to the intervened resource.

**Second empirical contribution:**

> We compare where the relevant condition is enforced by two official consumer
> configurations on the same Android device and explain the observed stages
> using their versioned implementation paths. A secondary Hand witness bounds
> how far metadata changes propagate through a task-specific consumer.

Treat the checker, source/evidence indexes, S/I/D vocabulary and parser repair as
supporting methods, artifacts and lessons. Neither item above claims firstness;
the contributions describe what was established empirically. A reviewer may
still regard the behavior as expected from existing implementations. The
significance assessment must address why this characterization is useful beyond
reproducing a known check, using evidence rather than a broader title.

## Open issues and decisions that this task does not close

- **Research significance remains pending.** This review does not establish
  naturally occurring resource drift, frequency, user impact or reduced costs.
- **Novelty remains bounded.** The selected papers differ in their reported
  object/oracle; unseen deployment-packaging, resource-versioning, schema or
  contract-analysis work may overlap. The Stalnaker full-text comparison and
  detailed Meyer reading are incomplete. No field-wide absence is claimed.
- **Methods-paper framing remains unsupported by current E5.** A future analyzer
  needs an actual incremental capability and evaluation on supported structures
  unused in its design. Renaming checks, adding ABSTAIN/DEFER states, or
  accumulating more similar mutants would not establish that increment.
- **Evidence and human boundaries remain.** Primary experiments and prior-tool
  evaluations were not rerun; source inspection does not authenticate all saved
  binary records. Human verification and portable evidence handoff remain open.
- **Manuscript action is deferred to its own TODO.** Retain the two bounded
  empirical contributions, shorten Hand, add the precise mutation/testing
  comparisons, and update the AIBOM reading level. Do not rewrite historical
  results or claim completion of the separate P1 rewrite in this PR.

This completes the protocol's bounded contribution-comparison deliverable. It
does not mark novelty, publication readiness, significance, or human audit as
passed.
