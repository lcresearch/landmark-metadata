# Related-work and engineering-significance integration notes

This editorial input uses the completed repository comparisons. It adds no
literature search, experiment or tool evaluation. The paragraphs below are a
candidate manuscript insert; the source-level notes preserve the boundaries
needed when integrating them.

## Candidate related-work insert

```latex
\section{Relationship to Existing Work}
Executable preconditions are established design-by-contract practice~\cite{meyer},
and official tooling explicitly supports metadata-driven interface
generation~\cite{codegen-doc}. MLGuard proposes developer-specified ML contracts,
probabilistic validation models, and generated wrappers with violation
handlers~\cite{mlguard}; its reviewed paper presents an implementation and
evaluation agenda. Our empirical object is an existing generated interface and
the model-package resources it actually consumes. This lets us characterize
interface behavior while preserving the computation and generated code, rather
than introducing contracts or wrappers as new mechanisms.

DocTer learns documentation-to-constraint rules from annotated API descriptions
and uses the resulting constraints and parameter dependencies to generate
conforming and violating inputs~\cite{docter}. ACETest extracts conditions from
operator validation code, propagates controllable properties, and solves
constraints to generate tests, with library-specific handling~\cite{acetest}.
These establish both constraint-guided testing and implementation-derived
conditions. Our E5 procedure recognizes limited generated-code patterns and
encodes selected decoder conditions. Its role is supporting diagnosis; the core
comparison establishes no additional rejection over the matched simple baseline
or Task initialization.

DeepMutation alters training data/programs or trained model parameters and
structure to assess test-data quality~\cite{deepmutation}. Its label-error
operator changes training-example labels. Our focal intervention instead changes
an associated display-label resource in a deployed model package. NNSmith
composes operator constraints to generate valid graphs and compares compiled
outputs with a numerical reference, including conversion and optimization
boundaries~\cite{nnsmith}. The specific intervention--oracle pairing here holds
graph/weights and generated code fixed, checks numerical preservation, and then
observes public getter failure or changed display association. It complements
numerical testing with an interface observation; mutation, differential testing,
and constraint composition are established techniques.

DARA uses model-derived architecture features to assess supplied naming and
architectural metadata~\cite{dara}. The AIBOM preprint studies documentation
completeness and explicitly distinguishes field presence from substantive
quality~\cite{aibom}. Stalnaker et al.'s abstract describes documentation,
supply-chain, and licensing challenges~\cite{stalnaker}; detailed overlap with
that study remains unresolved because its full text was unavailable. These
works place our output/resource association within a broader consistency
problem. S/I/D organize the properties measured in this study; P separately
checks preservation under intervention.

A closer engineering antecedent is Support issue \#770, opened in 2022: a user
reported that an Android Studio generated segmentation getter reached
\code{TensorLabel} and rejected 21 labels for a tensor with shape
\code{[1,257,257,21]}~\cite{support-770}. A repository-member reply states that
this model cannot use that generated API and recommends Task
Library~\cite{support-770-reply}. The report supports the relevance of consumer
selection and establishes that generated-getter incompatibility was already
public. It describes an unsupported consumer/model combination according to that
reply; we did not reproduce the reported artifact. Our contribution is the
controlled characterization: preservation and reversal around actual interface
execution, a successful reference-disagreeing display association, and measured
enforcement stages in two configurations on the same Android device.

This positioning rests on a bounded comparison of the inspected versions.
The resulting evidence addresses which property a test establishes and which
public operation exposes a condition. It does not establish a general
contract-inference method or a field-wide firstness claim.
```

## New bibliography entries

The existing MLGuard, DocTer, ACETest, DARA, AIBOM, Stalnaker and Meyer entries
retain their current author/title identifiers. DeepMutation is cited as the
inspected arXiv version because a publisher identity was not authenticated in
the bounded review. NNSmith's publication and DOI below are stated on the
inspected arXiv PDF's first page; its publisher PDF was not separately retrieved.
The issue title intentionally retains the reporter's spelling, `Segementation`.

```latex
\bibitem{deepmutation} Lei Ma et al.
DeepMutation: Mutation Testing of Deep Learning Systems.
\href{https://arxiv.org/abs/1805.05206v2}{arXiv:1805.05206v2}, 2018.

\bibitem{nnsmith} Jiawei Liu et al.
NNSmith: Generating Diverse and Valid Test Cases for Deep Learning Compilers.
In \emph{Proceedings of the 28th ACM International Conference on Architectural
Support for Programming Languages and Operating Systems (ASPLOS)}, Volume 2,
2023.
\href{https://doi.org/10.1145/3575693.3575707}{doi:10.1145/3575693.3575707}.
Inspected version: \href{https://arxiv.org/abs/2207.13066v2}{arXiv:2207.13066v2}.

\bibitem{support-770} TensorFlow Lite Support issue \#770.
Semantic Segementation Example ``Label number 21 mismatch'' exception.
Opened March 28, 2022; issue and comments retrieved October 4, 2026.
\url{https://github.com/tensorflow/tflite-support/issues/770}.

\bibitem{support-770-reply} lu-wang-g.
Reply to TensorFlow Lite Support issue \#770, April 25, 2022.
GitHub author association: MEMBER; retrieved October 4, 2026.
\url{https://github.com/tensorflow/tflite-support/issues/770#issuecomment-1108777779}.
```

The member comment was also read from the retained raw response during this
editorial task. Its complete short text is:

> The Segmentation model can not be drag-and-dropped into Android Studio. The
> API generated won't work. Please use Task Library to inference the model. See
> the instruction here.

The final `here` links to the then-current official Task ImageSegmenter guide.
`MEMBER` is GitHub's repository-organization association, not independently
verified employment or responsibility for the model.

## Candidate engineering-implications insert

```latex
\paragraph{Match the check to the release property.}
The controlled results distinguish useful integration tests. A load/process
test covers model execution; the generated getter must also be exercised when
its category interface is required. E2 further requires observing the returned
position--score--label association: successful decoding and unchanged raw scores
do not establish agreement with a display-order specification. Compare the
selected, actually parsed label map with an artifact-linked reference when that
agreement is a release requirement. A baseline map alone establishes change.

These recommendations complement ordinary protections. A trusted digest of the
complete model package, including its associated-file archive, would detect both
resource interventions as changed files. Official Task initialization already
rejects the tested deletion. Package pinning checks identity; a reference map
checks the association in a newly approved package. Our results identify their
different assurance properties. They do not measure how often developers omit
these checks or whether earlier rejection saves time, energy or incidents.
```

This is an implication of recorded experiments and implementation inspection,
not a newly run comparison of engineering practices. Use #770 in motivation as
well as related work; the same report supports relevance and limits firstness.
Do not count it as a newly reproduced natural defect or as evidence that the
published EfficientNet original fails.

## Source locators and integration checks

| Text element | Checked repository basis | Scope to preserve |
|---|---|---|
| MLGuard, DocTer, ACETest, DARA mechanisms | [Method comparison](../../research/20261004-contribution-review/METHOD_COMPARISON.md) and [source index](../../research/20261004-contribution-review/method-sources.json) | Specific inspected full texts; none of their tools was run for comparison |
| DeepMutation label meaning; NNSmith numerical oracle | [Mutation comparison](../../research/20261004-contribution-review/MUTATION_COMPARISON.md) and [source index](../../research/20261004-contribution-review/mutation-sources.json) | Deployment display-label resources differ from training labels; computation-preservation testing already exists |
| AIBOM reading level; Stalnaker limit | [Background comparison](../../research/20261004-contribution-review/BACKGROUND_COMPARISON.md) | AIBOM recovered full text was read; Stalnaker remains abstract/publication-record only |
| Meyer | Mutation source index, `meyer` record | Inherited background citation; full text and a fresh bibliographic authentication were unavailable |
| #770 body and member reply | [Public reports](../../research/20261004-significance-review/PUBLIC_REPORTS.md) and [source index](../../research/20261004-significance-review/public-report-sources.json), R1 | Unsupported route according to reply; unpinned artifact/version; no reproduction |
| Strong ordinary defenses and engineering value | [Significance assessment](../../research/20261004-significance-review/SIGNIFICANCE_ASSESSMENT.md) | Coverage reasoning, not measured adoption, productivity or operational benefit |

Update the old manuscript's literature-scope paragraph: **seven** full texts
were inspected in the completed comparison (MLGuard, DocTer, ACETest, DARA,
DeepMutation, NNSmith and AIBOM). Stalnaker remains abstract-only; Meyer remains
background without recovered full text. Do not keep the old statement that
AIBOM positioning was abstract-only. The comparison is bounded, and no
comparative execution of these research tools is claimed.

Keep the positive thesis in the introduction and conclusion: the experiments
separate successful computation, successful public output access, and supported
display association under controlled resource interventions. Group the limits
on prevalence, task accuracy, natural defects and operational benefits once in
validity rather than repeating the full list after each observation. Keep local
qualifiers where they change interpretation: reference is display-order scoped;
P2 integrations differ; Hand concerns one fixed image; #770 is a public report.
