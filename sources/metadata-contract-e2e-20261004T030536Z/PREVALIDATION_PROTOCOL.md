# Frozen-rule external validation protocol — E4

Freeze this protocol, candidate URL list, prior-artifact exclusions, unchanged checker/helper source, exact existing mutation procedures and environment identities in a local Git commit and SHA-256 record before downloading any E4 candidate. This is a same-session local freeze, not independent preregistration. E1–E3 are already observed and are development evidence.

## Units and selection

The sampling frame is a fixed list of 20 version-1 candidate locations on the official mediapipe-models storage host, chosen for classification, detection, segmentation, audio and pose diversity plus quantization variants. The list is in E4/protocol/candidates.json. A candidate address is not a verified publisher-catalog entry; an unavailable URL is reported as such, not as a missing promised release. No replacement, new URL, latest fallback or version substitution is permitted. No candidate model metadata has been inspected before this freeze.

Recursively extract .tflite members from successfully retrieved .task ZIPs. Retain occurrences; deduplicate component bytes and canonical graphs. Exclude any exact component or canonical graph already seen in the prior 13-component corpus, E1 or E2. Record these as PRIOR_COMPONENT or PRIOR_GRAPH, not independent new models. Within the new set, choose the first occurrence in fixed candidate/member lexical order per canonical graph. Approximately 15–20 new canonical graphs is a working target, not a quota; all failed addresses, duplicates and abstentions remain in the denominator flow. No opportunistic replacement.

Download limit: 128 MiB per candidate, HTTPS, 90-second request timeout; one retry is permitted only for transport/HTTP 5xx failures, never for 404/403. Record URL, HTTP outcome, bytes and SHA-256. Archives with unsafe paths or inaccessible/corrupt structures are recorded and not repaired.

## Frozen checks and scope

Run the exact previous check_model.py, inspect_suite.py, suite_static.py, codegen_one.py and contracts.json copies identified by the freeze. No changes to their detection logic after candidate inspection. The test controller may add logging and classification of unsupported cases but may not change a failed prediction into a pass. Unexpected checker errors are outcomes; fixes require a separate post-freeze version and cannot be pooled into this validation.

- S: actual official MetadataPopulator load/populate result, not metadata JSON parsing.
- I: existing exact-digest role references only. New semantics require an independently supplied official output-role/class-order source tied to the exact artifact/version. No shape/name heuristics, original labels as truth, or reference annotations authored after inspecting an outcome. No new such reference has been supplied; expected missing-reference outcomes are explicit abstentions, not passes.
- D: inspect the actually emitted TensorLabel(List, TensorBuffer).getCategoryList path using the frozen implementation. Report first-nonunit-axis, label cardinality and last-axis requirements only. No category getter means INAPPLICABLE, not universally compatible. Restrict an unconditional D verdict to fully static positive output shapes and signatures; dynamic signatures yield ABSTAIN even if the unchanged raw checker prints a conditional stored-shape result. Preserve both the raw checker result and the scope-filtered verdict.
- Eligibility: preserve all downloads/components; checker can inspect any readable TFLite component. Missing metadata, unsupported generation, nonpositive/dynamic shape, unsupported input/output and absent semantic reference are explicit statuses. Input/output dtype/shape is recorded, not guessed. No inference is required for an original-only static external observation.
- Compilation: attempt raw javac for every generated Java source with the same pinned JDK 17.0.12+7 --release 8 and archived jars. No generated-source repair. Capture diagnostics, especially existing unsupported-type/fallback warnings. A D failure in an already uncompilable or warned unsupported path is a consumer-compatibility observation, not a demonstrated supported end-to-end natural defect.

## Mutations and validation limits

Freeze the established description edit, metadata-count decrement, first differing-shape index exchange, final-label deletion, cyclic-left label permutation and inverse restoration procedures/specifications alongside the checker. E4's external observations use originals only. Controlled mutation evaluation in E5 reuses preserved development/control fixtures; it will not inflate the natural external denominator. Original artifacts are never replaced with mutants, and no mutation-induced failure is called a natural finding.

Preserve every output and exception. A newly observed static incompatibility alone does not establish a natural semantic error or deployed failure. A new supported generated-interface failure would require its own unmodified baseline execution with a prior plan; no such follow-up is promised in the denominator. Zero new natural defects is acceptable. No precision, recall, general detector accuracy or population defect rate will be reported.

## Commands and outputs

```bash
python scripts/freeze_e4.py
PYTHONDONTWRITEBYTECODE=1 /workspace/hand-contract-repro/.venv/bin/python scripts/external_validation.py
python scripts/summarize_e4.py
```

The freeze must complete before external_validation.py is launched. Save per-component machine records, unmodified raw checker JSON/stdout/stderr, generated source, javac logs/classes, download provenance, protocol commit/digest and SHA256SUMS. Previously observed examples are explicitly development data; an independent human audit remains pending.
