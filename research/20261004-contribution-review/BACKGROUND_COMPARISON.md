# Documentation and supply-chain background

This comparison follows the [protocol](PROTOCOL.md). It distinguishes freshly
read recovered full text from a freshly retrieved abstract. Neither paper's
empirical results were reproduced, and neither tool was run.

## AIBOM completeness: recovered full text

Md Erfan, Ahmed Ryan, and Md Rayhanur Rahman, *A Large-Scale Measurement of AI
Bill of Materials Completeness in Hugging Face Models*,
[arXiv:2607.17242v1](https://arxiv.org/abs/2607.17242v1), is treated as a preprint.
The recovered PDF matches the historical download record exactly:
`674ee9127a82f3b5541f1685defbc216f0b38e727e550d226edb2c8432c55035`.
It was freshly converted and inspected in this task; it was not freshly
downloaded. Locators below are one-based PDF pages.

- Section III.A–B, p. 4: the inputs are HF repository metadata; the study filters
  repositories before generating documentation artifacts.
- Section III.C–E, p. 5: the pipeline runs the OWASP AIBOM Generator, checks JSON
  and expected CycloneDX fields, and extracts the generator's completeness
  scores. The authors explicitly use an existing scoring method. Their sample
  inspection checks consistency between extracted scores and generator reports.
- Section VI, p. 10: field presence is distinguished from substantive quality;
  the findings are not presented as a full assessment of model quality, safety,
  fairness or performance. Section VII places richer semantic documentation
  quality in future work.

**Overlap:** generating and inspecting machine-readable model documentation,
distinguishing structural presence from stronger guarantees, and warning that a
successful completeness check is insufficient are already established here.

**Bounded difference:** the inspected method and evaluation concern repository
documentation and its completeness. They do not demonstrate a label-resource
intervention propagated through an actual generated classifier getter while
holding graph computation and generated code fixed. This difference in the
evaluated object supports technical positioning; it does not establish that the
present study is the first or that S/I/D is a novel taxonomy. AIBOM completeness
and our S population acceptance are also different measurements.

The current manuscript still describes this comparison as abstract-based. A
later rewrite can update that source-level statement using this audit; the
manuscript itself is unchanged by this task.

## Stalnaker et al.: abstract and publication record only

*An Empirical Analysis of Machine Learning Model and Dataset Documentation,
Supply Chain, and Licensing Challenges on Hugging Face*,
[DOI 10.1145/3776739](https://doi.org/10.1145/3776739), is identified by the
freshly retrieved Crossref record as a TOSEM journal article, volume 35, issue 8.
The returned record is byte-identical to the recovered historical record,
SHA-256 `3d5631e75402573eee2bcc33010d13d71feca92bf0853abded4d701b2e9c45e3`.
The publisher PDF request returned HTTP 403; no alternate-host attempt was made.

The abstract describes documentation shortcomings, supply-chain relationships
and licensing, and motivates automated inconsistency checking and validation.
This supports broad contextual overlap. It does **not** support asserting that
the full study lacks executable-interface analysis, or that it covers only
external references. Its detailed method/evaluation overlap remains unresolved
in this round and must remain a limit of the novelty comparison.

## Provenance and interpretation

[background-sources.json](background-sources.json) records the exact recovered
and requested sources, hashes and inspection levels. Raw PDFs, extracted text,
Crossref/Atom payloads and retrieval logs remain outside Git at
`/workspace/contribution-review-20261004/background/`. The first-party
[inspection script](scripts/inspect_background.py) records failures as well as
successes and refuses to overwrite an existing output directory.

Documentation-quality problems motivate care in model reuse. They do not, by
themselves, establish how often the focal getter failure occurs naturally or its
practical impact. The separate significance TODO remains open.
