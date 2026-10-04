# Bounded contribution and related-work comparison

This protocol defines the P0 contribution-comparison task before fresh source
retrieval. It does not execute the separate significance assessment, rewrite the
manuscript, or rerun model experiments. The starting repository commit is
`81af34b10f8093e646179e51e658d597e6acc84b`.

## Questions and fixed scope

1. Which candidate claims are already documented or implemented by the official
   Support 0.4.4 schema, population, generation, label-loading and decoder paths?
2. Which ideas and methods overlap with MLGuard, DocTer, ACETest and DARA, the
   four already identified closest method papers?
3. Do the previously raised mutation/differential-testing comparisons,
   DeepMutation and NNSmith, restrict the proposed empirical distinction?
4. What can the documentation/supply-chain study by Stalnaker et al. and the
   AIBOM completeness preprint support at their actually accessible source level?
   Meyer design by contract is conceptual background, not a new algorithm claim.
5. What bounded contribution remains in the actual implementation and preserved
   research record, and what must be narrowed, withheld or dropped?

Use the current manuscript and supplied code as the claim inventory. The eight
named research works above plus design-by-contract background form a purposive
comparison set, not a systematic search or an exhaustive nearest-work set.
Official schema/populator, generator, FileUtil, TensorLabel and Task classifier
implementations are implementation baselines. Do not label all of them one
validator or count unrelated tools' unsupported inputs as detection failures.

## Retrieval and evidence rules

- Prefer exact versions already recorded; record version, URL, retrieval status,
  digest and passage/function locator for newly inspected primary sources.
- Start with the recorded primary URLs. At most four ordinary public retrieval
  requests per named paper are allowed; successful retrieval ends source hunting
  for that version. A policy denial ends attempts to retrieve that content through
  alternate hosts. No proxy bypass or credential workaround is allowed.
- An unavailable full text stays unavailable. Historical audit notes may inform
  a qualified comparison but are not a fresh reading of the paper. Distinguish
  full text, abstract, official code, historical report and unresolved claims.
- Inspect methods and evaluation sections before claiming that a particular
  mechanism is not demonstrated. Even then, restrict the statement to the
  inspected version and its reported scope; do not infer field-wide absence.
- Preserve downloaded papers, third-party code and response logs outside Git in
  `/workspace/contribution-review-20261004/`. Commit only first-party protocols,
  retrieval scripts if used, concise source indexes and analytical documents.
- No paper tool or model experiment is executed. Do not authenticate unavailable
  runtime evidence from source scripts or manuscript prose. Distinguish recorded
  experiment findings from source mechanisms inspected in this task.

## Deliverables and stopping condition

Produce a claim–evidence–prior-work–remaining-difference matrix, an official
implementation comparison, source-level provenance, and keep/narrow/drop/defer
recommendations. Record any unresolved overlap and a conditional paper framing.
Stop after this bounded source set and implementation paths have been examined
or their access limits documented. Do not expand models, introduce an analyzer,
or search for natural defects in this task. Independent human verification and
practical-significance assessment remain open.
