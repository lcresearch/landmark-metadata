# Research significance review

Start with the [assessment and scenario–check–consequence matrix](SIGNIFICANCE_ASSESSMENT.md).
The bounded P0 significance assessment is complete. The evidence supports concrete
integration-test and diagnostic relevance; prevalence, industrial benefits and
user impact remain unmeasured. It does not certify novelty or venue readiness.
The manuscript was not rewritten and no model experiment was run in this task.

| Document | Purpose |
|---|---|
| [Protocol](PROTOCOL.md) | Same-session scope, evidence levels, six official guides, eight fixed queries and stopping rules |
| [Measured outcomes](MEASURED_OUTCOMES.md) | Readback of selected old E1/E2/P2/P3 records, engineering implications and unavailable evidence |
| [Workflow evidence](WORKFLOW_EVIDENCE.md) | Documented developer tasks, existing protections and the limits of current documentation |
| [Public reports](PUBLIC_REPORTS.md) | All 30 issue dispositions, seven selected reports with 69 comments, counterexamples and source qualifications |

Support [#770](https://github.com/tensorflow/tflite-support/issues/770) is relevant
both as practical context and as prior engineering evidence: a generated
segmentation getter failure and Task alternative were public in 2022. The member
reply describes an unsupported model/frontend combination. It is not a newly
reproduced supported-path defect. No model from a report was downloaded or run;
artifact-reproduced natural cases in this task number zero.

The source indexes are [outcome-sources.json](outcome-sources.json),
[workflow-sources.json](workflow-sources.json) and
[public-report-sources.json](public-report-sources.json). They record versions,
paths, hashes, source status and selection decisions. Raw evidence, third-party
text, API responses and logs stay outside this source-only repository under
`/workspace/significance-review-20261004/` and the historical paths in those
indexes. These provenance documents are not a portable evidence deposit.

## Source entry points

The collectors require Python 3, `gh` for public issue API requests, `curl` for
guides and `lxml` for extraction. Versions actually used are in the indexes.
Use new external directories. Live pages/searches can change, so a later fetch
does not guarantee the same bytes, ordering or findings.

```sh
python research/20261004-significance-review/scripts/search_public_reports.py --help
python research/20261004-significance-review/scripts/retrieve_workflows.py --help
python research/20261004-significance-review/scripts/extract_workflows.py --help
python research/20261004-significance-review/scripts/read_existing_outcomes.py --help
```

Exact retrieval commands are in the workflow and public-report documents. Issue
eligibility is a recorded manual agent decision between search and inspection,
not an automatic detector or human-annotator result. The extraction script is
deterministic for its saved HTML inputs; the documented article selection still
needs inspection if future page layouts change.

The old-outcome reader requires the excluded historical files; defaults and
override flags are documented in [Measured outcomes](MEASURED_OUTCOMES.md).
The maintained reader preserves the finite comparison logic but differs from
the external script actually used by adding CLI/output protections. Both hashes
and that distinction are recorded. A report's booleans must be inspected; process
exit zero is not certification of the complete archive. Do not describe this
readback as a new inference, build, preservation audit or human verification.

The preceding contribution-review directory remains an unchanged record of its
own completion state. The current [TODO](../../TODO.md) closes both bounded P0
assessments; full rewrite, reproduction handoff, human audit and venue selection
remain open.

## Verification of this review

`git diff --check` and `PYTHONDONTWRITEBYTECODE=1 python scripts/check_source_tree.py`
passed: 457 files, 232 Python syntax checks, 34 JSON documents and 154 navigation
targets; all 354 imported files and both manuscript hashes remain unchanged.
Twelve existing warnings identify historical locators or unchecked excluded
archive digests. These are source checks, not model experiments.

Separate byte checks matched the 59 old input/result files selected for readback,
40 workflow/retrieval/prior-source objects and 44 public-response/stderr files to
their indexed digests. An independent agent reviewed the synthesis, raw query
counts, selected issue replies, readback witnesses and strong-baseline treatment,
finding no blocking inconsistency. This is an agent review of the stated scope,
not human verification or authentication of the complete historical archive.
