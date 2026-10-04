# Continuation state

User objective: strengthen the existing manuscript “From Model Metadata to Executable Interfaces: A Controlled Study of Tensor Binding and Decoder Contracts,” preserving S (structure), I (reference-backed index semantics), D (selected decoder compatibility), and P (graph/weight preservation) as separate claims. No prevalence, general detector accuracy, task accuracy or production-user consequences without direct evidence.

All requested phases have now been completed within their documented scope. Start with RESULTS_OVERVIEW.md, results.json, REPORTING_CLARIFICATIONS.md and MANUSCRIPT_IMPACT.md. Do not restart the experiments merely to add invocations.

Old evidence is unchanged at `/workspace/metadata-contract-paper` and `/workspace/hand-contract-repro`. The original paper.tex hash remains `16385b61700ff2b89a9f1dfe40bd6a44b19e8b30db48b777f6c361d787b6b06c`. The final audit matched all 930 inventoried old files, the 691-entry paper manifest and the 188-entry Hand manifest.

New evidence root: `/workspace/metadata-contract-e2e-20261004T030536Z`. E1/E2/E3/E4/E5/E7 are sealed with SHA256SUMS and must not be edited. Root reporting clarifications supplement, rather than overwrite, sealed results. New work needs another timestamped directory. The emulator has been shut down.

- E1: actual unmodified generated EfficientNet Android interface succeeds for original/description/restoration. Label deletion preserves graph, metadata, code and raw outputs but throws from the actual generated getter after inference. Same-environment replay agrees.
- E2: predeclared left cyclic label shift preserves all scores and raw positions; actual getter succeeds with 999 changed label strings. Restoration reverses it. No independent EfficientNet class-order reference. One interrupted replay unit was separately recovered; retain the original incomplete attempt.
- E3: official Task ImageClassifier 0.4.4 rejects the same deletion during initialization, earlier than the Android getter. Task and Android platforms differ. Android Studio omitted, not tested-and-failed. Separate embedded Task TFLite version unknown; exact wheel/native hashes preserved.
- E4: locally frozen rules/candidates before inspection; 20 URLs, 16 downloads, 4 unavailable, 15 new canonical groups after exclusions. No new supported end-to-end natural failure or reference-backed semantic mismatch. All semantic judgments abstain; runtime not executed.
- E5: scoped preflight implemented/evaluated on 65 byte-distinct fixtures. Structural count failures and actual EfficientNet getter failure detected; permutation compatible under D. Dynamic-signature Gesture cases abstain, including its known isolated deletion failure. Do not claim precision/recall. Later CLI smoke checks confirmed original exit 0 and deletion exit 2.
- E7: source v0.10.14/commit `4cf89a70942ca3252e46ace7e4552f53be9bef2e` pins a different Hand component hash whose graph/weights equal focal `6acda7…`. The explicit bridge supports output roles. Actual MediaPipe Task results are identical before/after metadata exchange on one source-pinned image. Generic repaired compilation remains historical; fresh javap checked the preserved binding. Metadata exchange is not a complete repair.

Toolchain: Python 3.11.16; generator/Support 0.4.4; Android TFLite 2.13.0; JDK 17.0.12+7 targeting Java 8; API-30 x86_64 software emulator 37.2.12/build16428233. System-image archive r11 internally reports properties r10; both identities are disclosed. Task MediaPipe 0.10.14 has its own preserved environment.

No human verification has occurred. HUMAN_AUDIT.md remains unchecked. The old manuscript was intentionally not rewritten; focused proposed changes are ready for review. Public archival release, independent human audit, broader novelty/venue assessment and any manuscript revision remain subsequent work. This local package still relies on the two existing workspace roots; do not call it a standalone offline release.
