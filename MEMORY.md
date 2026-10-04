# Project continuation

This repository is the source-code handoff for **From Model Metadata to Executable Interfaces: A Controlled Study of Tensor Binding and Decoder Contracts**. Read `TODO.md` before planning new work. This note records conclusions and working preferences, not a substitute for raw evidence.

## Repository preference

The user requested that future project work be kept in this GitHub repository, then narrowed the upload to code. Keep project source code, necessary manuscript/source documentation, TODO updates, and concise decisions/continuation notes here. Exclude SDKs, emulators/AVDs, installed environments, dependency binaries, model binaries, APKs, classes/DEX, rendered PDFs, logs, and other build/runtime products. Keep new research evidence outside this source-only repository unless the user later changes that scope. Update these notes when findings or next steps change; do not promise unattended background synchronization.

## Verified state

- **E1:** The original EfficientNet generated Java runs without a source repair. Removing one associated label preserves graph/weights, generated model code, and tested raw outputs. Loading and inference succeed; the actual generated `getProbabilityAsCategoryList()` then throws `IllegalArgumentException: Label number 999 mismatch the shape on axis 1`. The harness catches it; this is not an application-crash result.
- **E2:** A predeclared label-order permutation preserves tested raw outputs and score bits while changing 999 of 1,000 displayed label strings. Generated output access succeeds. Restoration returns the observed outputs and associations to baseline. No independent class-order reference has been tied to the exact artifact, so the claim is an exposed association change, not incorrect prediction or accuracy loss.
- **Agent audit:** Fresh generated sources, builds, and a new AVD reproduced E1/E2 using the already installed pinned toolchain. Eight phase/variant execution records represent five distinct artifact–consumer configurations, one graph, and 16 input observations: 14 successful category lists and two caught getter exceptions. This was not a toolchain-from-archive installation or independent human replication.
- **Preservation:** Five model-byte conditions preserve 165 non-metadata buffers. Label interventions also preserve embedded metadata and the pre-ZIP prefix. The description control changes metadata. Working model, APK asset, and a pre-load AssetManager read match; the audit did not intercept the native interpreter buffer. Generated model classes match historical classes. Fresh-variant DEX files match each other, but are not claimed equal to historical DEX because the audit added a harness hash observation.
- **Official/simple baselines:** On five core conditions, metadata reading and population succeed. The version-specific simple decoder baseline, E5, and Task initialization reject only label deletion. E5 has **zero additional rejections** over that baseline or Task initialization in this set; retain it as supporting diagnostics, not a demonstrated novel detection algorithm.
- **Remaining boundaries:** E3 compares Android generated Java with Linux Task, so configuration differences remain. E4 is bounded external static examination, not a prevalence or natural runtime-defect study. Hand is a reference-backed binding witness plus unchanged Task output on one fixed image, not a second established end-to-end failure. E5 uses limited regex/template association and cannot guarantee correct abstention for every unknown getter or processor syntax.
- The manuscript was revised after the audit. Four specified full-text related-work comparisons were completed; this is not an exhaustive novelty proof. Independent human verification remains pending.

## Repository review follow-up

The [current editorial source](work/review-followup-20261004/manuscript/paper.tex)
is a new working copy; imported snapshots remain unchanged. Its
[source/parent digest index](docs/CURRENT_MANUSCRIPT.json) distinguishes it from
the historical revision identified below. The follow-up clarifies E5 naming,
the E4 denominator flow, payload/behavior restoration and abstract-only
background citations. It changes no experimental outcome. The
[review disposition](docs/REVIEW_FOLLOWUP.md) and
[English audit summary](docs/AUDIT_SUMMARY_EN.md) distinguish repository checks
from the excluded runtime evidence and pending human review.

The original source check passed. The extended check covers current document
navigation, warning-only historical README locators, imported bytes/sizes,
the historical manuscript hash in this note and both indexed manuscript sources.
Seven regression tests exercise failures that the previous check could miss.
This does not verify external `SHA256SUMS` bytes or recover the evidence archive.
The historical evidence roots and Android execution tools were unavailable in
the follow-up environment, so P2 was not executed. Next remains P2, with human
audit and contribution/novelty assessment still open.

## Analysis and next action

Keep **S** (structural acceptance), **I** (reference-backed association agreement), and **D** (compatibility with the actual decoder path) distinct. **P** is intervention-preservation evidence, not a fourth correctness category. Never count mutated fixtures or repeated inputs as independent models.

Next is **P2: generated wrapper versus Android Task ImageClassifier in the same Android environment**, using identical model bytes and inputs and recording each stage. Retain remaining dependency/integration differences. Then perform bounded P3 reference and natural-case searches. Do not broaden model collection or repeat P0/P1 without a new change or unresolved contradiction. An E5 method expansion is conditional on demonstrated value beyond a strong baseline.

## Evidence availability

Full sealed evidence remains in the original workspace; it is **not uploaded in this code-only repository**. The paths below are local provenance locators, not portable downloads:

| Local package | Identity |
|---|---|
| `/workspace/metadata-contract-e2e-20261004T030536Z` | `SHA256SUMS` SHA-256: `aba0739ac893ee69795556d43384029d20cc096a584156d0f0c37638fdc8751d` |
| `/workspace/metadata-contract-audit-20261004T062010Z` | `SHA256SUMS` SHA-256: `b73388bf6ce263d9fff7659a90166d80ae56544d540a12620768a1bc8a8af89d` |
| `/workspace/metadata-contract-paper-revision-20261004T065132Z` | Revised `manuscript/paper.tex` SHA-256: `390445a494c24cf9e9069ca3d5ab62e4d0174587f631856b764846d54908782d` |

Do not claim a future rerun merely from these hashes or this summary. Recover the required inputs, inspect actual artifacts, and record missing prerequisites explicitly. New evidence belongs in a new timestamped directory; never overwrite sealed historical evidence.
