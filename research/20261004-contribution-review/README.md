# Contribution review

Start with [the decision and claim–evidence–prior-work matrix](CONTRIBUTION_COMPARISON.md).
This completes the bounded P0 contribution comparison. The separate significance
assessment, full rewrite and human audit remain open.

| Document | Purpose |
|---|---|
| [Protocol](PROTOCOL.md) | Fixed questions, purposive source set, retrieval budget and stopping rule |
| [Claim inventory](CLAIM_INVENTORY.md) | Current evidence claims versus implemented checks and remaining limits |
| [Official baselines](OFFICIAL_BASELINES.md) | Versioned schema, population, generation, loader and consumer paths |
| [Four method papers](METHOD_COMPARISON.md) | MLGuard, DocTer, ACETest and DARA, with inspected passages |
| [Mutation and differential testing](MUTATION_COMPARISON.md) | DeepMutation, NNSmith and unresolved Meyer full-text access |
| [Documentation background](BACKGROUND_COMPARISON.md) | Recovered AIBOM full text and Stalnaker abstract-only boundary |

The provenance indexes are [official-sources.json](official-sources.json),
[method-sources.json](method-sources.json),
[mutation-sources.json](mutation-sources.json) and
[background-sources.json](background-sources.json). They identify exact versions,
hashes, source levels, locations and failed retrievals. They are documentation
indexes, not raw experimental results or a complete evidence archive.

Five full texts were recovered and hash-checked, and two were freshly retrieved.
Stalnaker full text remained unavailable; Meyer's original article was not
recovered. All third-party source bytes, papers, extracts and response logs are
outside Git under `/workspace/contribution-review-20261004/` or the historical
paths listed by the indexes. A checksum identifies bytes; it does not certify
source authority or paper findings.

New retrieval scripts record ordinary public requests and preserve failures:

```sh
python research/20261004-contribution-review/scripts/inspect_background.py \
  --output-dir /path/outside/repository/new-background-directory
python research/20261004-contribution-review/scripts/retrieve_mutation_sources.py --help
```

The four-method index records the exact PDF-to-text commands used on recovered
PDFs. Consult the other source indexes for their requests and local inputs. No
paper tool, model inference, generator or Android execution is part of this
review. Agent interpretation is not human verification. No systematic or
exhaustive novelty search is claimed.

Validation in this task: the repository source/navigation/provenance check and
`git diff --check` pass; all 354 imported files and both manuscript hashes remain
unchanged. Separate byte checks match 31 literature/retrieval/extraction objects
to their recorded digests, and the official-source verifier matches all 17 source
and provenance objects. These checks cover review sources, not model execution
records or the excluded experiment archive.
