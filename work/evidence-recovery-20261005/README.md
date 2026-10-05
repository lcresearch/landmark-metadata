# Local saved-evidence recovery

The user selected a **local evidence package and missing-material list**. The
selected original E1/E2, installed-toolchain build-audit and P2/P3 bytes have been
copied and verified outside Git. Later reconstruction records remain missing.
No model was generated, built or executed, and no human audit was completed.

## Delivered locally

Root: `/workspace/evidence-recovery-20261005T170453Z/`

| Item | Location / identity |
|---|---|
| Selected package | `package-v2/`: 2,749 payload files, 2,285,772,379 bytes |
| Compressed copy | `delivery/focal-saved-evidence.tar.gz`: 1,924,911,456 bytes |
| Archive SHA-256 | `1e6f9737ecdaf426b8e4a30391fd1298b6f503e39d8c17423c521376b86c746e` |
| Package `SHA256SUMS` SHA-256 | `a689674abb65452d8eb02a17d6af3f097884bd8c2ad4cb4a8353e33914197a3c` |
| Package `MANIFEST.json` SHA-256 | `ba9592c8f49735c5f8e2f53ba3af1c560e51b674050cdf7b6c64dc6d8b87f0ba` |

[delivery-record.json](delivery-record.json) records exact external report paths,
hashes, counts and exclusions. These local paths are not persistent download
URLs. The full delivery directory checksum file has SHA-256
`8350edd06a05a284e0ff028d154909ea1f45b293534f79b22a5ad10ab6f29a76`. It covers the archive, tools, missing
list and verification/search reports. No upload, Release/LFS publication or external
storage configuration was performed. Only scripts, the selection plan and necessary text records enter Git.

The package contains 2,746 files checked against three independently pinned
historical manifests, plus three algorithm/schema source files whose expected
digests come from records covered by those manifests. All matched. The archive
was read member by member without extraction: all 2,749 payload files and four
package metadata files matched its separately pinned checksum index.

## What the saved-record checks cover

| Evidence family | Complete saved records | Actual input observations | Decoded lists |
|---|---:|---:|---:|
| Original E1/E2 primary, replay and separate recovery | 16 | 32 | 28 |
| Installed-toolchain build audit | 8 | 16 | 14 |
| Same-Android P2 | 10 | 18 | 16 |

These are repeated observations/configurations, not independent models. The
original interrupted E2 replay remains a separate incomplete attempt with three
install-log files. Task deletion remains a construction failure with no reached
input observation. Wrapper deletion remains a caught getter exception.

The new [coverage reader](check_focal_coverage.py) checks all 26 executed APKs
against working/staged model bytes, recorded APK hashes and saved installation
commands. Fourteen initial build APKs are checked separately. It checks exact
saved payload sets, input/raw identities and lengths, stages, category indices,
score bits and eight successful shared P2 score/label pairs. It does not inspect
a newly device-pulled APK or intercept the interpreter's buffer.

The existing finite reader also ran against the relocated package: 59 selected
files, no false comparison booleans, and P3's stored display table recount of
1,000 original agreements, one permutation agreement and 1,000 restoration
agreements. That recount does not independently establish reference authority.
Neither reader rederives graph preservation, disassembles all compiled bindings
or performs new inference. These checks do not sign any human-audit item.

## Selection and exclusions

[package-plan.json](package-plan.json) is the exact selection and trust-anchor
plan. Original roots, relative paths and file bytes remain distinct in the
payload. Each staged file records its original path and expected historical
digest. Original evidence was copied, never edited, moved or hard-linked.

SDKs, virtual environments, dependency binaries, AVD state and signing keys are
excluded. Explicit text exceptions preserve resolved dependencies, acquisition
records, POMs and licenses. Generated Java/classes/DEX, executed APKs, raw tensors,
decoded lists and logs are retained **only in the external local package**.
Unsigned/aligned APK intermediates are omitted; initial build attempts and their
logs remain visible. Historical test-signing command arguments remain verbatim;
this local bundle has not undergone public-redistribution review.

Root-level historical reports/manifests can describe deliberately unpackaged
Hand, E4/E5, baseline or literature units. Use the new package inventory for
completeness; running every old `SHA256SUMS` over this subset is not appropriate.
The full later reconstruction reader remains blocked by its own prerequisites.

An initial `package/` omitted 29 dependency text records. Cross-review found the
gap; `package-v2/` adds them and matches the independently proposed 2,746-file
scope plus the three supplemental sources. The earlier preparation directory
is retained and is not the delivery target.

## Tool and documentation validation

All 43 new synthetic staging/archive tests pass, together with the 40 existing
repository tests (83 total). Negative cases include tampering, missing/extra
files, wrong historical anchors, links/traversal and overwrite attempts; they
also distinguish package integrity from historical identity. The coverage
reader rejects a missing APK under ordinary Python and `-O`.

Source checks pass with 354 imported files and all 48 editorial source hashes
unchanged. The 12 existing historical-locator/external-digest warnings remain.
Agent code and scope reviews found no remaining blocker for this local task;
these reviews do not constitute human research verification.

## Use the package

From the repository root, verify the compressed copy without extraction:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 work/evidence-recovery-20261005/verify_archive.py \
  --archive /workspace/evidence-recovery-20261005T170453Z/delivery/focal-saved-evidence.tar.gz \
  --checksums-sha256 a689674abb65452d8eb02a17d6af3f097884bd8c2ad4cb4a8353e33914197a3c
```

For an extracted/relocated package, pass its actual root to:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 work/evidence-recovery-20261005/stage_evidence.py verify \
  --package /path/to/focal-saved-evidence \
  --checksums-sha256 a689674abb65452d8eb02a17d6af3f097884bd8c2ad4cb4a8353e33914197a3c
PYTHONDONTWRITEBYTECODE=1 python3 work/evidence-recovery-20261005/check_focal_coverage.py \
  --package /path/to/focal-saved-evidence \
  --output /path/to/new-external-directory/coverage.json
```

Use a new output path. See [COMMANDS.md](COMMANDS.md) for the performed staging,
archive and readback commands. The two [discovery scripts](discovery/README.md)
are fixed-path command snapshots, not portable rerun entry points.

## Remaining work

The [missing-material list](MISSING.md) distinguishes unrecovered later records
from intentionally omitted payloads. Local preservation is complete for the
selected scope. Durable external delivery, dependency recovery/fresh-workspace
build and execution, secondary evidence coverage and actual human verification
remain open. No manuscript claim was strengthened by this packaging task.
