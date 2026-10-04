# Research significance: evidence and limits

## Assessment

The study has **concrete engineering relevance to interface integration testing,
resource-association regression and consumer-specific diagnosis**. Its controlled
examples show which assurance claims are not supplied by successful loading,
unchanged model computation, unchanged generated code, or a successful decoder
call alone. Official workflows and a closely related public integration report
connect those questions to actual developer interfaces.

The evidence does **not** establish frequent natural defects, widespread resource
drift, production exposure, developer time saved, prevented incidents, latency
savings or user harm. Nor does it establish that E5 improves on the strongest
existing checks. The appropriate current framing remains a bounded empirical or
experience study. A broader impact claim or methods-paper framing would require
additional evidence, not a larger count of similar mutants.

This closes the declared [bounded assessment](PROTOCOL.md), not a publication
readiness gate. The findings below include limitations that reduce the importance
and novelty claims; a favorable verdict was not a completion requirement.

## Evidence basis

| Evidence level | What this task obtained | What it establishes |
|---|---|---|
| Existing controlled outcomes, partly read back now | [Measured outcomes](MEASURED_OUTCOMES.md): selected primary E1/E2 input/raw/decoded bytes and stages; P2 deletion records; P3 stored comparison. No new execution or complete archive authentication | Concrete observed interface differences and the scope of tests that would observe them |
| Official workflow documentation | [Workflow evidence](WORKFLOW_EVIDENCE.md): six official guides/examples, with redirects, hashes and current-versus-historical scope | These are documented integration tasks and APIs; this is not evidence of adoption rate or measured benefit |
| Public reports | [Public-report review](PUBLIC_REPORTS.md): the fixed search and its retained inclusion/exclusion decisions | Reports and selected project-member explanations provide contextual evidence; they are not independently reproduced model defects |
| Source mechanism and prior work | The preceding [contribution comparison](../20261004-contribution-review/CONTRIBUTION_COMPARISON.md), particularly fixed Support 0.4.4 code | Explains existing predicates, resource loading and observation boundaries; does not establish deployment incidence |
| Engineering implication | The checks and decisions below, derived from the preceding evidence | Actionable reasoning, explicitly separate from an experiment measuring developer productivity or operational benefits |

## Scenario–check–consequence matrix

The scenarios are documented workflows or explicit test-design decisions. The
study's mutations are controlled interventions; they are not observations that
an organization made the same resource edit in production.

| Scenario and decision | Existing protection or test | Observed consequence / evidence level | Supported action and remaining gap |
|---|---|---|---|
| Package or update a model plus associated labels | Metadata reading/population, source compilation and load checks | Recorded E1 deletion passes these stages and inference, then fails at the actual category getter; selected old outputs/stages read back now | Exercise the public getter the application relies on. A load/process-only test does not establish that getter's compatibility. We did not measure whether developers commonly omit this test |
| Approve a release because graph, generated code and raw outputs match | Graph/code identity and raw numerical regression | Recorded E2 permutation preserves those properties and decoder success while changing exposed labels; P3 provides a qualified display-order reference | Test the actual label–score–position association if it is a release requirement. An approved resource update may legitimately change labels; baseline difference alone is not incorrectness |
| Pin a released model package against unintended changes | Trusted full-artifact digest, covering the appended associated ZIP, verified at packaging/loading | **Analytical coverage, not a new run:** both deletion and permutation change the complete model file, so this protection would detect departure from the pinned file | Retain full-package identity checks. The study does not show a hash-pinning bypass. Hashes cannot judge a newly approved package's association without a trusted reference |
| Select generic binding or a task-specific consumer | Official compatibility requirements and the selected consumer's initialization/output checks | Recorded P2 rejects the same deletion at different stages; public Support #770 reports a segmentation generated-getter failure and a member directs the user to Task Library | Treat compatibility as a property of artifact plus selected consumer/configuration. The public segmentation path was described as unsupported; it does not prove a supported official path has a natural defect |
| Interpret a Task initialization exception | Cause-chain logging and fixed implementation checks | P2's recorded outer native-address exception contains a nested label-count diagnostic | Preserve nested diagnostics to localize this failure. No measured debugging-time improvement or general rule about native-address errors follows |
| Add preflight or move a check earlier | Exact-path label-count/axis baseline and official Task initialization | The recorded five-condition comparison gives E5 zero additional rejected conditions over either comparator | Preflight can provide a selected-path diagnostic before construction. Neither new detection capability nor cost/safety superiority was demonstrated |
| Implement preflight in another language | Parsing approximation versus the selected runtime loader | Recorded VT/U+2028 probes expose opposite errors in this study's historical checker and simple baseline; raw parser-probe evidence remains unavailable at its checked locator | Audit resource selection, encoding, line parsing and decoder assumptions against the actual library. This is a checker's modeling defect, not an established natural defect of the official loader |

The strongest supported importance claim is about **test coverage and evidence
interpretation**. It is not that routine protections are unavailable. The
counterexamples show why a successful check of one property must not be reported
as assurance of a different property.

## Public antecedent: relevant, but also a limit on novelty

Eight fixed queries returned 31 occurrences, representing 30 unique issues.
All were triaged by title/body; all seven eligible reports and their 69 comments
were inspected. Each query was limited to its first five oldest matches, so these
denominators describe a deliberately truncated inquiry, not a representative
sample. No report model was downloaded or executed.

[TensorFlow Lite Support #770](https://github.com/tensorflow/tflite-support/issues/770),
opened in March 2022, reports importing a linked segmentation model through
Android Studio, calling the generated `getSegmentationMasksAsCategoryList`, and
receiving a TensorLabel exception. The issue body gives 21 labels, tensor shape
`[1,257,257,21]`, the first-nonunit-axis selection, and a stack through the
generated getter. This is considerably closer to our consumer-contract question
than a general complaint about model quality.

In a [project-member reply](https://github.com/tensorflow/tflite-support/issues/770#issuecomment-1108777779),
the member states that this segmentation model cannot be used through that
Android Studio generated API and directs the user to Task Library. The recorded
GitHub association is `MEMBER`; this is an attributed explanation, not our
independent validation of the reporter's artifacts. The issue does not pin the
complete binary/toolchain inputs needed for our replay, and no replay was
attempted here.

This report has two consequences for the paper:

1. **It supports practical relevance.** A developer reported a generated public
   getter/decoder incompatibility while following an integration route; consumer
   selection and the meaning of a successful import are concrete decisions.
2. **It narrows novelty.** Generated TensorLabel getter failure and a Task
   alternative were already public in 2022. The manuscript must not describe
   that phenomenon as a first discovery. Any remaining empirical contribution
   must rest on the controlled preservation/reversal, the successful association
   case and the measured configuration comparison, with this antecedent cited.

Its cause also differs from E1: a segmentation tensor is not the focal
single-classifier vector with one deleted label. It is not evidence that the
published EfficientNet original is defective, that all generated wrappers fail,
or that Task and generated binding are interchangeable. The other selected
reports and negative/configuration explanations are retained in
[PUBLIC_REPORTS.md](PUBLIC_REPORTS.md); they are not pooled into a natural-bug
count. **No new artifact-reproduced natural model failure is established here.**

## Challenge the importance claim with ordinary strong baselines

These coverage judgments combine previously measured outcomes with source and
logical reasoning. This table is not a new head-to-head experiment.

| Ordinary defense | What it addresses in the focal cases | Why it does not settle every question |
|---|---|---|
| Trusted full-package hash | Detects both resource interventions as changed artifacts, including associated ZIP bytes | It detects change; it does not validate the association in a newly approved package. Graph/code hash equality is a different property |
| Official Task initialization | Already rejects the focal nonempty 999-label condition | Accepts the count-preserving permutation; does not supply an independent display-order reference |
| Actual selected-getter smoke test | Would observe E1's demonstrated exception on the tested path | Checking only successful return would not detect E2; this says nothing about untested inputs, getters or configurations |
| Full selected label-map comparison against a trustworthy, artifact-linked specification | Can expose E2/P3 display-order disagreement without relying on image recognition accuracy | A baseline list alone only identifies change. Reference authority, artifact linkage, parsing and repeated display names need separate treatment |
| Raw-score regression | Checks the numerical property it was designed to check, and remains equal in E1/E2 | It does not check the later association/getter property. This is a scope boundary, not an erroneous numerical-test result |

The research should therefore explain the **assurance property of each test**.
It should not contrast a sophisticated new checker with deliberately weak
baselines, imply that changing labels evades all integrity protection, or claim
that only a novel analyzer can catch these conditions.

## Supported, narrowed and unsupported importance statements

**Supported:** In the tested generated classifier, successful computation does
not establish successful output access or agreement of exposed display labels
with a supplied reference. Explicit getter and association observations make
these distinctions testable. Official guides establish that models, metadata,
label resources and generated/task APIs participate in documented integration
workflows. The related public report supplies a concrete historical example of
consumer-selection difficulty at a generated getter.

**Narrowed:** Enforcement stage matters for which public operation a test must
exercise and where a diagnostic is observed. We have not measured its effect on
latency, energy, availability, repair time or migration cost. The parser probes
show that a preflight approximation can be wrong in both directions; they do not
show that these separators are common in released label resources. E5 is a
supporting diagnostic and regression artifact with known coverage limits.

**Unsupported:** This problem is widespread; most model users are exposed; the
study found new supported natural Android failures; the injected permutation
caused wrong image classifications; existing official tools lack the focal
count check; E5 improves detector accuracy; early rejection reduced costs or
prevented production incidents. Issue search totals and documentation availability
are not measurements of any of those claims.

## Paper decision and next work

Proceed with a **bounded empirical/experience-paper framing** if the authors
judge that the controlled characterization and test-scope lessons meet the
selected venue's expectations. The evidence now supports a more concrete
motivation than “metadata matters”: identify exactly what load tests, raw-output
regressions, integrity pins, getter tests and reference comparisons do and do not
establish in these configurations. Explain existing protections fairly.

The assessment does not justify promoting the current E5 into a new method or
calling the study a high-prevalence industrial failure investigation. Public
antecedent #770 should enter the later rewrite as both motivation and related
engineering work. Keep the approved manuscript order and E5's supporting role.

Both P0 review deliverables can now be treated as complete within their declared
scope. Full rewrite, reproduction handoff, actual human audit and venue selection
remain separate TODOs. Do not extend this search or add models merely to improve
counts. A future natural-case reproduction or practitioner-benefit study would
need a separately declared question and budget; neither is silently assumed
necessary or complete by this assessment.
