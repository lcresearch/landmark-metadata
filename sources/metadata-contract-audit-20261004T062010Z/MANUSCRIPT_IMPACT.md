# Manuscript impact of the agent audit

Target: the sealed `manuscript/paper.tex` in `/workspace/metadata-contract-paper-rewrite-20261004T052625Z`, SHA-256 `35c8dfe8173b84e7410e6d8ae348791a503351ce74d537368cededd2a62897bd`. This file proposes changes; the manuscript has not been edited in place.

## Retain the primary empirical contribution

The independent audit implementation re-parses the retained models, ZIP resources, APK entries, raw float arrays, decoded lists and actual APK bytecode. It supports the existing E1/E2 preserving-intervention claims, getter reachability, changed exposed association and restoration. This is an additional automated check, not another independent model or a human replication.

Any new reconstruction claim must cite `rebuild/AUDIT_REPORT.md` and distinguish fresh generated code/builds and a fresh AVD from the reused installed Python/JDK/SDK toolchain. The added asset digest is a pre-load read through the same Context and asset name, not an interception of native interpreter memory. The harness change must be disclosed, and new DEX must be compared within the new build set rather than assumed identical to historical DEX.

## Required scope correction: E5 extraction

The statement near line 58 that unrecognized processing requires abstention reads more strongly than the implementation guarantees. The intended policy and the actual template matcher must be separated. A getter that does not match the regular expression can be reported as inapplicable; an unrecognized processor-construction syntax can evade the operation matcher. This audit has not established a wrong classification on a newly executed natural artifact.

Suggested replacement:

> The implementation recognizes a limited set of generator templates. For recognized paths, it abstains on dynamic signatures and detected unsupported processors. Unmatched getter or processor syntax is outside the supported analysis scope; the current matcher does not establish that every such case is correctly classified as abstention.

Near lines 54 and 195, describe the mechanism as **template-based extraction of selected generated bindings and audited decoder conditions**, rather than implying complete data-flow verification. A future implementation could enforce the intended policy more comprehensively, but that work is not completed by this audit.

## Add the measured baseline comparison

Five byte-distinct EfficientNet conditions were freshly checked: original, description control, label deletion, label permutation and restored labels. Reader and population paths accept all five. The implementation-matched simple decoder baseline and E5 make the same decisions; Task initialization rejects the same deletion condition. Thus E5 establishes no additional rejected condition over those two comparisons in this family. It moves a known selected-path diagnostic earlier and identifies the getter/resource association; broader incremental capability remains unproved.

Suggested addition to the pre-flight discussion:

> On the five core artifact conditions, a baseline implementing the same selected TensorLabel preconditions and the pre-flight command produce identical compatibility decisions. Task initialization also rejects the deletion artifact. The pre-flight procedure is therefore a supporting means of early, path-specific diagnosis in this evaluation, rather than evidence of greater defect-detection capability.

The separate existing structural negative control has one graph output and zero output-metadata entries, while its label resource still has 1,000 entries. MetadataDisplayer can read it; MetadataPopulator rejects it in `load_metadata_buffer` validation before `populate`. Keep this distinct from deleting one label in an otherwise unchanged associated resource. Acceptance by a reader is not acceptance by a validator.

## Add the missing direct related work

The bounded full-text audit in `literature/AUDIT_REPORT.md` supplies preserved versions and page/section anchors for MLGuard, DocTer, ACETest and DARA.

- MLGuard proposes contract specifications and generated enforcement wrappers; the reviewed paper presents a vision and future implementation/evaluation plans.
- DocTer implements documentation-derived constraints and conforming/violating input generation.
- ACETest implements extraction from actual operator validation code with library summaries, static analysis and constraint solving. Deriving conditions from code is not new by itself.
- DARA analyzes model architecture features against supplied metadata. It must not be described as only a documentation checker.

These reviewed papers do not demonstrate the complete focal graph/resource/generated-getter/decoder connection in their reported methods and evaluations. That bounded difference neither proves exhaustive novelty nor establishes a new algorithm in the present E5 implementation. Keep the principal contribution as controlled execution evidence unless additional method results justify a change.

## Preserve the existing limits

- E3 remains a comparison of Android generated Java and Linux Task configurations; no same-Android Task experiment was performed in this audit.
- E4's static incompatibilities are not supported natural end-to-end defects. No external runtime execution is added here.
- E2 still lacks an artifact-tied independent class-order reference. Keep association change separate from prediction correctness.
- Hand remains a reference-backed association witness plus a consumer boundary observed on one image. Do not infer global metadata insensitivity.
- Keep the incomplete historical E2 replay attempt unclassified, the recovery separately identified, and restoration distinguished from full ZIP byte identity.
- Agent audits, fresh automated builds and full-text checks do not complete independent human verification or decide submission readiness.

## Reporting hygiene

Use per-run device records and attributed log time windows. Historical logcat dumps are cumulative and can contain another variant's exception. Do not treat the presence of an exception string in a log file as the current condition's outcome.

The final root `AUDIT_REPORT.md` and `results.json` distinguish completed fresh execution from checks of retained records. Update the manuscript only from their completed, qualified outcomes.
