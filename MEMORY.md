# Project continuation

This repository is the source-code handoff for **From Model Metadata to Executable Interfaces: A Controlled Study of Tensor Binding and Decoder Contracts**. Read `TODO.md` before planning new work. This note records conclusions and working preferences, not a substitute for raw evidence.

## Repository preference

All future changes use **feature branch → pull request → user review**. Push
only the feature branch; never update `main`/the default branch directly, whether
through Git or an API. Do not merge or enable auto-merge without an explicit user
instruction. This applies to source, manuscript, TODO, memory and policy edits,
and supersedes the earlier direct-push synchronization preference.

The user requested that future project work be kept in this GitHub repository, then narrowed the upload to code. Keep project source code, necessary manuscript/source documentation, TODO updates, and concise decisions/continuation notes here. Exclude SDKs, emulators/AVDs, installed environments, dependency binaries, model binaries, APKs, classes/DEX, rendered PDFs, logs, and other build/runtime products. Keep new research evidence outside this source-only repository unless the user later changes that scope. Update these notes when findings or next steps change; do not promise unattended background synchronization.

## Historical verified state recorded by the original workspace

These are the original handoff's conclusions. The fresh reconstruction below
checks the behaviors with new evidence; it does not authenticate excluded old
raw files, binary identities or chronology.

- **E1:** The original EfficientNet generated Java runs without a source repair. Removing one associated label preserves graph/weights, generated model code, and tested raw outputs. Loading and inference succeed; the actual generated `getProbabilityAsCategoryList()` then throws `IllegalArgumentException: Label number 999 mismatch the shape on axis 1`. The harness catches it; this is not an application-crash result.
- **E2:** A predeclared label-order permutation preserves tested raw outputs and score bits while changing 999 of 1,000 displayed label strings. Generated output access succeeds. Restoration returns the observed outputs and associations to baseline. The later P3 inquiry now supports disagreement with a publisher-prescribed external display-order reference; stable class-ID lineage and image prediction correctness remain unverified.
- **Historical agent audit:** Fresh generated sources, builds, and a new AVD reproduced E1/E2 using the already installed pinned toolchain. Eight phase/variant execution records represent five distinct artifact–consumer configurations, one graph, and 16 input observations: 14 successful category lists and two caught getter exceptions. This was not a toolchain-from-archive installation or independent human replication.
- **Historical preservation audit:** Five model-byte conditions preserve 165 non-metadata buffers. Label interventions also preserve embedded metadata and the pre-ZIP prefix. The description control changes metadata. Working model, APK asset, and a pre-load AssetManager read match; the audit did not intercept the native interpreter buffer. Generated model classes match historical classes. Fresh-variant DEX files match each other, but are not claimed equal to historical DEX because the audit added a harness hash observation.
- **Official/simple baselines:** On five core conditions, metadata reading and population succeed. The version-specific simple decoder baseline, E5, and Task initialization reject only label deletion. E5 has **zero additional rejections** over that baseline or Task initialization in this set; retain it as supporting diagnostics, not a demonstrated novel detection algorithm.
- **P2 same Android:** Ten configurations (one graph, five model-byte conditions, two consumers) ran on one fresh API-30 x86_64 AVD with the installed pinned tools. Task ImageClassifier 0.4.4 rejects deletion during construction; generated Support 0.4.4/TFLite 2.13.0 wrapper completes process and rejects at the actual getter. Original/description/permutation/restoration succeed in both. There are 18 actual input observations, 16 category lists and ten wrapper raw tensors. A separate script passed 152 checks. Across eight successful shared condition/input pairs, all 1000 returned score bits and labels agree by class index; native Task raw tensors were not observed. Task classify is atomic and its embedded interpreter version is unknown; native integrations still differ.
- **P3 qualified reference:** The focal model and a versioned official TFHub Lite0 fp32/2 artifact have identical complete computation fields, ordered outputs and all 165 non-metadata buffers. The commit-pinned fp32/2 card identifies classification/1 as parent; that exact card prescribes an external 1001-line ImageNetLabels file with background removed. Original/restoration match all 1000 positions; permutation disagrees at 999. This establishes reference-disagreeing display associations, not incorrect image predictions, stable-ID semantic correctness or a natural defect. The full stable-ID chain remains ABSTAIN. The 30-request bounded search is complete; a separate 38-check agent audit passed. Old E5 abstentions were not retroactively changed.
- **Remaining boundaries:** Historical Linux E3 is retained as context; P2 strengthens the stage comparison on Android but does not isolate all library/runtime effects. E4 is bounded external static examination, not a prevalence or natural runtime-defect study. Hand is a reference-backed binding witness plus unchanged Task output on one fixed image, not a second established end-to-end failure. E5 uses limited regex/template association and cannot guarantee correct abstention for every unknown getter or processor syntax.
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
been independently repeated. Human audit and historical evidence authentication remain open for this fresh
reconstruction. Main separately records completed P2 and the qualified P3
display-order reference; those results and their limits are retained above. A cloud configuration draft is not a published/tested future snapshot.

Keep **S** (structural acceptance), **I** (reference-backed association agreement), and **D** (compatibility with the actual decoder path) distinct. **P** is intervention-preservation evidence, not a fourth correctness category. Never count mutated fixtures or repeated inputs as independent models.

P2 and the bounded P3 reference inquiry are complete. Next prioritize actual human audit, final technical positioning, venue selection/formatting and an independently usable evidence-deposit plan. No natural-case search was conducted this round; any such search is optional and needs predefined scope/stopping conditions. Do not broaden model collection or repeat P0/P1 without a new change or unresolved contradiction. An E5 method expansion is conditional on demonstrated value beyond a strong baseline.

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
| `/workspace/metadata-contract-p2p3-20261004T073824Z/P2` | Same-Android `SHA256SUMS` SHA-256: `d903826e8d6f666921ba9e6e9247fe541cb3b7c6b8170113c4b5c572f82f58d5` |
| `/workspace/metadata-contract-p2p3-20261004T073824Z/P3` | Reference inquiry `SHA256SUMS` SHA-256: `77345fcadf085095d23722ac7a16ef7c4d5d34c202e4f32b7046750cad919de3` |
| `/workspace/metadata-contract-p2p3-20261004T073824Z` | Final 1,159-entry `SHA256SUMS` SHA-256: `aed26d18de158a3eebf5dcd7a3996356da99419779b689addd1f083a6a0cec27`; excludes P2 SDK/AVD operational state |

The current revised manuscript and P2/P3 first-party code/documents are indexed
under [the latest follow-up](research/20261004-p2-p3/README.md). The full local
round preserves both successful build attempts and the reference audit's first
failed Git-tree-header assumption, resolved by reconstructing all committed tree
objects. These are not hidden or relabeled runtime failures. All 3,207 entries in
the three protected old manifests were independently rechecked unchanged.
The current manuscript source SHA-256 is
`118ccc9820454f8ac1d3b0416ba456401e5ef3f9e9d0199ba1c59991103ec5a9`.
Its generic reading PDF rendered to nine pages and all pages were agent-inspected;
PDF/build products remain local and no venue-length compliance is claimed.

Do not claim a future rerun merely from these hashes or this summary. Recover the required inputs, inspect actual artifacts, and record missing prerequisites explicitly. New evidence belongs in a new timestamped directory; never overwrite sealed historical evidence.

## Reproduction checker review repair

PR #1 now rejects incomplete or duplicate evidence identities and mismatched
fixture digests, requires a separately pinned 65-artifact manifest, creates Hand
asset/result directories, and preserves retrieval records on conversion timeout.
Eleven synthetic regressions pass; this is a verifier repair, not a new model run.
The complete external fixture identity list and raw assets remain unavailable
in this source-only checkout. P2/P3 completion and current research priorities
above are unchanged.
