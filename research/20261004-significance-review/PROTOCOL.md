# Bounded research-significance assessment

Starting source revision: `f090668b8f50b51d2ca2aecbabfabd143d61f0ca` (the
contribution comparison in PR #6, still open when this task began). This is a
separate follow-up PR based on that branch. The protocol is written before the
public-issue search; it is a same-session scope declaration, not independent
preregistration.

## Questions

1. Which documented engineering workflows actually consume these resources and
   interfaces, and what developer decisions could the recorded results inform?
2. What consequences are directly observed in this study, which public reports
   describe related situations, and which impact claims remain hypotheses?
3. Which checks already address the problem, and what does the study add for
   testing/assurance or diagnosis without claiming a novel detector?
4. Is there evidence of natural occurrences or practical impact strong enough
   to change the paper's positioning? An absence of such evidence is acceptable.

## Evidence levels and exclusions

- **Measured study outcome:** a recorded controlled experiment, with this task's
  inspection scope explicitly stated. Source code or a report alone does not
  prove all preserved binary evidence. This task does not rerun experiments.
- **Documented workflow / source mechanism:** an official guide or pinned
  implementation describing intended integration. Documentation is not adoption,
  prevalence, or a measured benefit to developers.
- **Public report:** an issue/PR reports a problem or explanation. Record whether
  a maintainer confirms a cause, whether exact artifact/version data are present,
  and whether reproduction occurred. A closed issue is not a verified fix.
- **Artifact-reproduced natural case:** requires exact public input artifacts,
  supported configuration and reproduced observed failure. No report in this
  task receives that label without these requirements; no model execution is
  planned in this bounded task.
- **Hypothesis:** an engineering implication without direct outcome evidence,
  such as time saved, incident frequency, user harm or production exposure.

Do not use injected label failures as natural defects. Do not infer prediction
accuracy, uncaught application crashes, latency savings, security/privacy impact
or user harm. Keep S/I/D separate and P as intervention preservation. Keep Hand
as its scoped source-backed/bounded consumer witness; do not count it as a new
external natural runtime case found by this search.

## Official workflow scope

Inspect at most six official guides or examples: metadata/codegen, Android ML
Model Binding, Support image labeling, Task ImageClassifier, metadata associated
files, and metadata writer usage. Use existing fixed-version source provenance
from the contribution review when possible. Follow no more than two first-party
source links per guide to clarify a selected resource or public call. Record
unavailable and redirected documents. Current guides describe intended workflows,
not the exact historical behavior of every version.

## Public-report search protocol

Use GitHub's issue search on the three named official repositories. Run exactly
these eight queries (append `created:<=2026-10-04` to each), ordered as listed:

1. `repo:tensorflow/tflite-support is:issue "Label number"`
2. `repo:tensorflow/tensorflow is:issue "Label number"`
3. `repo:google-ai-edge/mediapipe is:issue "label map"`
4. `repo:tensorflow/tflite-support is:issue "label map"`
5. `repo:tensorflow/tensorflow is:issue metadata label order`
6. `repo:tensorflow/tflite-support is:issue label order`
7. `repo:google-ai-edge/mediapipe is:issue metadata output`
8. `repo:tensorflow/tflite-support is:issue metadata output`

For each query request the first five results, sorted by creation ascending.
Preserve total count, incomplete-results flag, returned order, issue IDs and
response digest. This deliberate truncation favors old reports and is a search
coverage limit, not an estimate of all relevant incidents. Deduplicate by issue
URL/number and repository, retaining the first occurrence in query order.

Triage every returned unique item using its title/body. Include reports that
explicitly concern label/tensor cardinality, association/order, resource parsing
or selection, generated binding, or an output-metadata consumer compatibility
issue. Exclude generic prediction-quality, training, unrelated build/device
errors and requests without a relevant contract mechanism; record reasons.
Uncertain but mechanism-relevant reports are eligible, not silently discarded.

Inspect the first eight eligible reports in the resulting fixed order, whether
they confirm, contradict or fail to establish the intended mechanism. Retrieve
each issue and at most its first 100 comments. Record omitted comments and any
remaining eligible reports as not inspected under the budget. At most one linked
first-party implementation/PR page per selected report may be inspected for a
claimed explanation; do not recursively search, download models, run code from
issues or replace inconvenient candidates. Exact issue reports can remain
unresolved. No confirmed natural failure is an acceptable outcome.

If access fails, record it and continue independent work. Do not bypass proxy or
access controls, alter queries to obtain desired cases, or broaden repositories.

## Deliverables and stopping rule

Produce a scenario–existing check–observed consequence–evidence level–remaining
gap matrix; a transparent public-report disposition table; source/version/hash
indexes; and supported/narrowed/unsupported importance statements with a paper
framing recommendation. Close this bounded TODO when those judgments and limits
are documented, not only when favorable public cases are found.

Downloads, full third-party text and raw search/comments remain outside Git at
`/workspace/significance-review-20261004/`. Commit first-party scripts and concise
review/provenance documents only. Preserve the manuscript, prior comparison and
historical source snapshots. Independent human review, a portable evidence
deposit, actual industrial benefit and venue acceptance remain separate tasks.
