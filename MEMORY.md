# Project continuation

This repository is the source-code handoff for **From Model Metadata to Executable Interfaces: A Controlled Study of Tensor Binding and Decoder Contracts**. Read `TODO.md` before planning new work. This note records conclusions and working preferences, not a substitute for raw evidence.

## Repository preference

The user requested that future project work be kept in this GitHub repository, then narrowed the upload to code. Keep project source code, necessary manuscript/source documentation, TODO updates, and concise decisions/continuation notes here. Exclude SDKs, emulators/AVDs, installed environments, dependency binaries, model binaries, APKs, classes/DEX, rendered PDFs, logs, and other build/runtime products. Keep new research evidence outside this source-only repository unless the user later changes that scope. Update these notes when findings or next steps change; do not promise unattended background synchronization.

## Historical verified state recorded by the original workspace

These are the original handoff's conclusions. The fresh reconstruction below
checks the behaviors with new evidence; it does not authenticate excluded old
raw files, binary identities or chronology.

- **E1:** The original EfficientNet generated Java runs without a source repair. Removing one associated label preserves graph/weights, generated model code, and tested raw outputs. Loading and inference succeed; the actual generated `getProbabilityAsCategoryList()` then throws `IllegalArgumentException: Label number 999 mismatch the shape on axis 1`. The harness catches it; this is not an application-crash result.
- **E2:** A predeclared label-order permutation preserves tested raw outputs and score bits while changing 999 of 1,000 displayed label strings. Generated output access succeeds. Restoration returns the observed outputs and associations to baseline. No independent class-order reference has been tied to the exact artifact, so the claim is an exposed association change, not incorrect prediction or accuracy loss.
- **Historical agent audit:** Fresh generated sources, builds, and a new AVD reproduced E1/E2 using the already installed pinned toolchain. Eight phase/variant execution records represent five distinct artifact–consumer configurations, one graph, and 16 input observations: 14 successful category lists and two caught getter exceptions. This was not a toolchain-from-archive installation or independent human replication.
- **Historical preservation audit:** Five model-byte conditions preserve 165 non-metadata buffers. Label interventions also preserve embedded metadata and the pre-ZIP prefix. The description control changes metadata. Working model, APK asset, and a pre-load AssetManager read match; the audit did not intercept the native interpreter buffer. Generated model classes match historical classes. Fresh-variant DEX files match each other, but are not claimed equal to historical DEX because the audit added a harness hash observation.
- **Official/simple baselines:** On five core conditions, metadata reading and population succeed. The version-specific simple decoder baseline, E5, and Task initialization reject only label deletion. E5 has **zero additional rejections** over that baseline or Task initialization in this set; retain it as supporting diagnostics, not a demonstrated novel detection algorithm.
- **Remaining boundaries:** E3 compares Android generated Java with Linux Task, so configuration differences remain. E4 is bounded external static examination, not a prevalence or natural runtime-defect study. Hand is a reference-backed binding witness plus unchanged Task output on one fixed image, not a second established end-to-end failure. E5 uses limited regex/template association and cannot guarantee correct abstention for every unknown getter or processor syntax.
- The manuscript was revised after the audit. Four specified full-text related-work comparisons were completed; this is not an exhaustive novelty proof. Independent human verification remains pending.

## Analysis and next action

### Fresh cloud reconstruction, 2026-10-04

The user requested a complete rerun/audit and authorized PRs for problems.
New source and the authoritative report are in
`sources/repro-audit-20261004/`; imported historical snapshots remain unchanged.
Official assets and pinned Python/JDK/Android prerequisites were actually
recovered in this cloud machine. E1/E2 primary and replay completed with 16
records/32 inputs: 28 successful category lists and four expected caught deletion
getter exceptions. Five model-byte conditions share one graph and 165 preserved
nonmetadata buffers. Replay used the stable main AVD after a second AVD's package
service failed before model loading; this is not independent-device replication.
The base corpus, Linux Task, Hand, E4 and all 65 E5 fixtures also ran; see the
new report for denominators and independent evidence checks.

The old E5 and simple baseline both use Python `splitlines()`, which differs from
the actual Java FileUtil reader. New label-only fixtures demonstrate both false
compatibility (VT) and false incompatibility (U+2028). The new maintained copies
use Java-compatible valid-UTF-8 parsing and abstain on malformed UTF-8; real Java
differential tests and all original 65-fixture decisions pass. Manuscript line
58 needs correction beyond the existing regex limitation. Other confirmed
historical script defects include success prose on missing/empty evidence,
inconsistent aggregate exit codes, and optimization-sensitive assertions. New
strict readers verify actual files and complete denominators; these findings do
not establish that historical model results were false.

New evidence remains outside Git under `/workspace/repro-*` and the reconstructed
`/workspace/{hand-contract-repro,metadata-contract-paper}`. The original sealed
archives were not available in this machine. Fresh literature PDF recovery was
blocked by proxy CONNECT 403, so the historical full-text review above has not
been independently repeated. Human audit, historical evidence authentication,
same-Android Task comparison and artifact-tied class-order references remain
open. A cloud configuration draft is not a published/tested future snapshot.

Keep **S** (structural acceptance), **I** (reference-backed association agreement), and **D** (compatibility with the actual decoder path) distinct. **P** is intervention-preservation evidence, not a fourth correctness category. Never count mutated fixtures or repeated inputs as independent models.

Next is **P2: generated wrapper versus Android Task ImageClassifier in the same Android environment**, using identical model bytes and inputs and recording each stage. Retain remaining dependency/integration differences. Then perform bounded P3 reference and natural-case searches. Do not broaden model collection or repeat P0/P1 without a new change or unresolved contradiction. An E5 method expansion is conditional on demonstrated value beyond a strong baseline.

## Evidence availability

The historical handoff recorded sealed evidence in the original workspace; it is
**not uploaded in this code-only repository and was unavailable in the fresh cloud
machine**. The paths below are historical provenance locators, not verified
current locations or portable downloads:

| Local package | Identity |
|---|---|
| `/workspace/metadata-contract-e2e-20261004T030536Z` | `SHA256SUMS` SHA-256: `aba0739ac893ee69795556d43384029d20cc096a584156d0f0c37638fdc8751d` |
| `/workspace/metadata-contract-audit-20261004T062010Z` | `SHA256SUMS` SHA-256: `b73388bf6ce263d9fff7659a90166d80ae56544d540a12620768a1bc8a8af89d` |
| `/workspace/metadata-contract-paper-revision-20261004T065132Z` | Revised `manuscript/paper.tex` SHA-256: `390445a494c24cf9e9069ca3d5ab62e4d0174587f631856b764846d54908782d` |

Do not claim a future rerun merely from these hashes or this summary. Recover the required inputs, inspect actual artifacts, and record missing prerequisites explicitly. New evidence belongs in a new timestamped directory; never overwrite sealed historical evidence.
