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

## Repository review follow-up

The [earlier editorial source](work/review-followup-20261004/manuscript/paper.tex)
is preserved unchanged. The new [current manuscript](work/paper-rewrite-20261004/manuscript/paper.tex)
has a [source/parent digest index](docs/CURRENT_MANUSCRIPT.json) that distinguishes it from
the preserved P2/P3 revision identified below. The follow-up clarifies E5 naming,
the E4 denominator flow, payload/behavior restoration and abstract-only
background citations. It changes no experimental outcome. The
[review disposition](docs/REVIEW_FOLLOWUP.md) and
[English audit summary](docs/AUDIT_SUMMARY_EN.md) distinguish repository checks
from the excluded runtime evidence and pending human review.

The original source check passed. The extended check covers current document
navigation, warning-only historical README locators, imported bytes/sizes,
the historical manuscript hash in this note and both indexed manuscript sources.
Nine regression tests cover navigation, imported bytes and manuscript provenance,
including protocol-relative external links and the P2/P3 parent import.
This does not verify external `SHA256SUMS` bytes or recover the evidence archive.
This editorial follow-up performs no new model execution. P2 and the bounded P3
reference inquiry are already complete on main; their results are retained in
the current working manuscript. Human audit remains open; the subsequent bounded
contribution/significance assessments and local rewrite are recorded below.

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
differential tests and all original 65-fixture decisions pass in that recorded
reconstruction. The current manuscript now discloses the parser counterexamples
and corrected implementation separately from the historical evaluation. Other confirmed
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

P2 and the bounded P3 reference inquiry are complete. The active priorities in
`TODO.md` now follow the completed bounded assessments and local rewrite.
The [bounded contribution comparison](research/20261004-contribution-review/CONTRIBUTION_COMPARISON.md)
is now complete: official checks already enforce the focal predicates; prior
methods cover contracts, constraint extraction, mutation and differential testing.
The supported current framing is controlled empirical characterization, with E5
as a supporting diagnostic. This does not certify field-wide novelty or venue fit.
The separate [practical-significance assessment](research/20261004-significance-review/SIGNIFICANCE_ASSESSMENT.md)
is also complete within its declared scope. It supports integration-test coverage
and consumer-specific diagnosis, not prevalence, demonstrated operational benefit
or a superior method. Both assessments inform the new controlled empirical
framing; no method novelty or venue readiness is presumed.
The [documented reproduction handoff](docs/reproduction/README.md) is now complete
as an inventory and command guide; delivery of a portable external package and
fresh-machine validation remain open. Actual human verification remains pending;
venue selection and formatting follow the contribution decision. The P0
comparisons do not complete those tasks.

This contribution-review task freshly inspected seven full texts: five recovered
PDFs with historical matching hashes (MLGuard, DocTer, ACETest, DARA, AIBOM), plus
new DeepMutation and NNSmith downloads. Stalnaker remains abstract-only after
HTTP 403; Meyer full-text access was unresolved. Fixed Support 0.4.4 source was
also inspected. The current manuscript and experiment records were not changed
or rerun. Some historical E1/P2/P3 raw paths are visible on this host, correcting
any assumption that all old bytes remain absent; this was an existence check,
not archive authentication. The `/workspace/repro-*` records identified in the
previous reconstruction remain unavailable at the checked locations.

The subsequent significance review followed a same-session protocol: six official
workflow pages and eight fixed GitHub queries. It triaged 30 unique issues and
inspected all seven eligible reports plus 69 comments. Support #770 documents a
2022 generated segmentation getter/TensorLabel failure; a repository-member reply
says that model's Android Studio generation path is unsupported and recommends
Task Library. It supports engineering relevance AND constrains first-discovery
claims. It is not our reproduction of a supported natural defect. Other selected
reports retain existing-check, asset-selection and input-configuration explanations.
No issue model was downloaded or executed; zero natural artifacts were reproduced.

That task also read back a fixed selection of 59 old E1/E2/P2/P3 records/payloads:
14 successful lists retain score bits, two caught getter failures remain recorded,
and permutation changes 999 labels per input. This is old-record inspection, not a
new build/run or authentication of the entire sealed evidence/reference chain.
Independent agent review found no blocking inconsistency; it is not human review.
Raw retrieval/readback evidence stays outside Git under
`/workspace/significance-review-20261004/`; committed source indexes record hashes.

Full-package hash pinning would detect both associated-resource interventions;
Task initialization and exact-path simple checks already reject deletion. Getter
tests and qualified reference-map comparisons address the demonstrated remaining
properties. Do not claim these ordinary protections are absent, or that earlier
rejection saved time, energy or incidents. The two P0 assessments themselves did
not edit the manuscript; the subsequent rewrite incorporates their conclusions.

## Local manuscript rewrite, 2026-10-04

The [new source area](work/paper-rewrite-20261004/README.md) contains the rewritten
paper and [claim–evidence ledger](work/paper-rewrite-20261004/CLAIM_EVIDENCE.md).
The argument follows contracts → E1 actual getter failure → E2 successful but
changed association and qualified P3 reference → same-Android enforcement stages
→ Hand boundary → external checks and preflight limits. Controlled execution and
configured stage comparison carry the contribution; E5 remains supporting, with
zero incremental rejection over the matched baseline in the core set. Support
#770 supplies context and prior engineering evidence. Existing package hashes,
Task initialization, getter tests and reference-map checks remain explicit.

The editorial round checked repository sources, not new model executions. Agent
review corrected the description-control preservation wording, the scope of P2
Java-source equality, exact exception quotation and direct reconstruction/corpus
provenance. The paper compiled as an eight-page generic reading draft; all pages
were visually checked. PDF and build logs stay outside Git. Prior working and
imported manuscripts remain unchanged. Human verification, portable evidence
delivery and venue formatting are still open.

The branch is `paper/executable-contract-rewrite`, originally based on saved PR #8
head `87290c2f7571d1fdf5cc2e56286a0ecff5b984ac`. The initial HTTP 401 blocked
publication, so the user requested local completion first. On resumed delivery,
GitHub API access recovered and PR #8's merged state was verified at main
`ccf1a98eca39d49f06e54f4c3def675a90c10540`; its tree matches the saved #8 head.
That main revision was merged into the feature branch without manuscript edits.
Direct Git push still returned 401, but the authenticated GitHub API published
the feature branch while preserving exact local tree and commit identities.
[PR #9](https://github.com/lcresearch/landmark-metadata/pull/9) is now open for
review. No default-branch write, PR merge or new model experiment occurred.

Any new natural-artifact reproduction needs a separately declared scope and
stopping condition; the completed public-report review is not such a reproduction.
Do not broaden model collection or
repeat completed core audits and baseline comparisons without a new change or
unresolved contradiction. An E5 method expansion is conditional on demonstrated
value beyond a strong baseline. Priority labels in the active TODO are distinct
from the completed experiment/follow-up names.

## Reproduction handoff, 2026-10-04

The [entry point](docs/reproduction/README.md) separates source checks, finite
readback of original E1/E2/P2/P3 records, the later reconstructed corpus reader,
and future build/run steps. It indexes exact inputs and dependency identities,
recorded acquisition routes, current local observations and unresolved delivery
gaps. Public URLs were not fetched again. Selected original model, input,
reference and dependency files were rehashed; hashing a manifest file alone does
not authenticate all of its entries.

The maintained finite reader was actually exercised on 59 old files in this
handoff, with comparison booleans inspected. The later `/workspace/repro-*`
results remain absent at their checked locators and were not replaced with older
records. Source-only base copying and Android source initialization succeeded in
new external directories; neither installed a toolchain or ran inference.
The handoff host's Python 3.12.14 is distinct from the recorded experiment Python
3.11.16. Task's embedded interpreter remains unknown. The system-image archive
named r11 internally reports revision 10; this documented packaging discrepancy
is not evidence of a changed image. Exact archive identity is recorded separately.

Raw handoff logs stay outside Git in `/workspace/landmark-handoff-audit-20261004/`.
No model build, Android execution or full preservation/reference-chain rerun was
performed. Several historical scripts write at import time or depend on omitted
configuration and absolute paths; follow the gated command guide, not a blind
replay of `commands.sh`. The separate external-deposit plan remains to be executed;
source-only documentation is not a portable evidence archive or human audit.

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

The preserved P2/P3 manuscript and first-party code/documents are indexed
under [the latest follow-up](research/20261004-p2-p3/README.md). The full local
round preserves both successful build attempts and the reference audit's first
failed Git-tree-header assumption, resolved by reconstructing all committed tree
objects. These are not hidden or relabeled runtime failures. All 3,207 entries in
the three protected old manifests were independently rechecked unchanged.
The preserved P2/P3 parent manuscript source SHA-256 is
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

The final PR #1 review also found that the exported claim reader accepted empty
Hand manifests and incomplete Task/Android identity sets. The maintained reader
in `work/observation-review-20261004/` requires exact identities and writes to a
new output directory; the original reader and all five claim-export hashes stay
unchanged. Nine new regressions bring the repository total to 29 passing tests.
The historical 677-check result predates this repair; excluded model evidence
was not rerun. Use the maintained entry point linked from the root README.

## Remaining observation-reader gaps repaired

A subsequent review demonstrated two additional synthetic false-pass cases:
a substituted non-core E5 fixture could pass count/self-consistency checks, and
Task results with absent or contradictory per-input observations could be counted
as successful when decoded files remained. The maintained reader now gates E5
on a separately digest-pinned 65-artifact manifest and requires exact Task input
identities, recorded preparation/classify success, category counts, and input
bytes/hashes. Eleven new regressions cover failures and valid reordered evidence;
all 40 repository tests and the source checks pass. All 354 imported files and
five historical claim-export hashes remain unchanged.

The current paper now distinguishes the historical parser from the maintained
valid-UTF-8 fix and describes the VT/U+2028 cases as isolated decoder probes.
The historical 65-fixture and 677-check records, exported sources, and P2/P3
results remain unchanged. This repair adds no model inference or human review;
the fresh reconstruction's excluded raw evidence was not available for another
complete readback. See [repair scope](docs/OBSERVATION_REPAIR.md).
