# Lost cloud evidence: current input recovery

Current executable entry: [maintained source](../../experiment/inputs/README.md). The commands below
record the original layout; removed originals are available in the fixed Git archive.

Date: 10 November 2026 (America/Los_Angeles). Source base:
`fa8a318eabff681ee061e55a7908a20a7fda2113`, the verified PR #17 squash commit.
The user requested original-material review, then reported losing the material
from the former cloud `/workspace` environment.

**The original execution evidence is still unavailable. The core input bytes
have been recovered and checked against previously recorded hashes.** Matching
input bytes do not recover old APKs, logs, observations or their execution history.

## Availability checked now

All 39 inventoried external paths were absent, including the selected archive,
extracted package, original roots, models, P3 bodies, manifests, two older ZIPs,
later reconstruction locators and separate parser run. `/workspace` itself does
not exist on this machine. These exact-path checks returned absence, not access
errors. A separate bounded filename search inspected 829 entries under Downloads,
Documents, Desktop, `/tmp`, `/mnt` and `/media`, descending at most four directory
levels below each root; it found no named
candidate or archive of at least 64 MiB. Nine protected system/mount directories
were inaccessible. Hidden/dependency directories and other roots were excluded.
This is not an exhaustive filesystem, remote-workspace or backup search.

The [historical delivery record](../evidence-recovery-20261005/delivery-record.json)
contains a local path and hash for the 1,924,911,456-byte focal archive, but no
persistent download URL. The earlier `hand-contract-evidence.zip` and
`metadata-contract-paper-sources.zip` are partial older packages, not substitutes
for the missing E1/E2/P2/P3 package. Their exact recorded paths are absent too.

## Actual recovery results

| Material | Current result | What remains unestablished |
|---|---|---|
| Official EfficientNet version-1 model | Fresh HTTPS download, 18,582,189 bytes; complete SHA-256 matches `6c7ab0a6…c8bde0` | Original retrieval/execution provenance |
| Description, deletion, permutation, restoration conditions | Deterministically rebuilt from the verified original; all four whole-model hashes and label payload hashes match | Original build, installation and execution |
| Gray127 and RGB-pattern inputs | Both 150,528-byte payloads match the recorded hashes | Old device input preparation or inference |
| Six P3 input bodies | Five new HTTPS retrievals plus reuse of the freshly acquired original; all six size/hash pins match | Old HTTP records, full computational bridge and source-chain re-audit |
| Old APKs, class/DEX files, logs, raw tensors and decoded results | Not recovered | E1/E2/P2 outcome revalidation remains blocked |

The P3 set includes the TFHub bridge model, two cards at commit
`81fdea8ffa53b5acbd66a012d17fb8f9602c714b`, and two published copies of the same
label text. These are six retrieval identities, not six independent models.
The five classifier conditions are interventions on one model, not five models.
All expected full digests remain in [inputs.json](../../docs/reproduction/inputs.json),
whose unchanged SHA-256 is
`b297d7b0756a8f10f8488f2b2bbe8b15a51239e9de354983ca17d264127069cf`.

After the recovery tools finished, a separate disk-readback command rehashed all
seven generated/copied files, all five model label members and all six P3 bodies
directly against that index; every comparison matched. No stored success boolean
was used as a substitute for reading the bytes. No graph/weight bridge was
recomputed, model was executed, emulator was started or human item signed.

## Local retention and reproducible tools

Data remains outside Git in these local directories:

- `/home/hsz/landmark-evidence/input-recovery-20261110/`: five `models/*.tflite`,
  two `inputs/*-input.rgb`, recovery/acquisition records and availability inventory.
- `/home/hsz/landmark-evidence/reference-recovery-20261110/`: six P3 body folders,
  new transfer/response records for the five network requests, and summary.

The original model was downloaded using `curl --fail --location` from the
official versioned URL in the input index and passed its historical hash before
use. That first download did not save HTTP headers; its separate acquisition
record states this. P3 acquisitions retain curl transfer JSON, response headers,
stderr, requested URL and checked body identity. New records use current times;
they are never represented as recovered October retrieval logs.

| Retained external record | SHA-256 |
|---|---|
| `input-recovery-20261110/input-recovery.json` | `9f2e7617f67b03429d5b2634038750c8afb1c789510cd73b94ebfd12056737d1` |
| `input-recovery-20261110/independent-readback.json` | `d5b5d174a04a819d69aafdd988a17ddcbf03524cc0bf9ff7d249b48cb70556b9` |
| `input-recovery-20261110/original-acquisition.json` | `1e9932943e5c7188da18b31c5cdd67666a42b80e2de5963c58c3ebfd9a12e079` |
| `input-recovery-20261110/availability-before-recovery.json` | `59bbf5fd61cf07af26fa05eea5643b2ec94889acd681d80e3e45e5d84c72af1c` |
| `reference-recovery-20261110/reference-recovery.json` | `7f243fcaddd3bc89c003a9bd71d2fc55c777632483fbc6784476befdfd0251b1` |

These copies avoid dependence on the old cloud `/workspace` and temporary output
directories. They are still local copies, not a remote backup or reviewer deposit.
No raw material is committed, uploaded, added to LFS or attached to a Release.

[recover_inputs.py](https://github.com/lcresearch/landmark-metadata/blob/e9da459f6043684cdecba913c9c711433371909d/work/input-recovery-20261110/recover_inputs.py) uses the standard library to verify the
historical index and original model, perform the recorded deterministic byte
changes, and verify all seven outputs before creating a new external directory.
[retrieve_references.py](https://github.com/lcresearch/landmark-metadata/blob/e9da459f6043684cdecba913c9c711433371909d/work/input-recovery-20261110/retrieve_references.py) uses that pinned index and curl
for the bounded reference acquisition. Both refuse existing output directories
and repository destinations. Failed requests/mismatches remain in the new
acquisition directory and produce a nonzero exit; they are not replaced by other
models or label lists. Interrupted writes can leave an incomplete new directory.

From the repository root, using actual paths and **new** external outputs:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 work/input-recovery-20261110/recover_inputs.py \
  --original-file /path/to/downloaded/efficientnet_lite0.tflite \
  --output-dir /path/outside/repository/new-input-recovery
PYTHONDONTWRITEBYTECODE=1 python3 work/input-recovery-20261110/retrieve_references.py \
  --original-file /path/outside/repository/new-input-recovery/models/original.tflite \
  --output-dir /path/outside/repository/new-reference-recovery
```

Both commands were actually executed against the retained directories above.
All **170** repository tests pass, including five new refusal/preservation tests.
The source checker and diff checks pass; the 354 preserved imports, historical
input index, manuscript sources and seven artifact pins remain unchanged.

## Consequences for the paper and next execution

The original saved-record audit remains incomplete. Keep earlier audit reports
as dated reports and disclose unavailable underlying execution material. Do not
describe a fresh run as verification or recovery of the lost run. Existing
manuscripts and human PENDING statuses were not changed by this recovery.

If no original workspace/backup can be recovered, the next empirical step is a
new, separately identified E1/E2/P2 execution plus P3 bridge analysis. Before that
run, verify pinned toolchain availability, adapt historical absolute paths in new
working copies, freeze the new protocol/configuration and choose durable retention.
Record all deviations and failures and then update the paper against the new raw
results. The broader Hand/E4/E5 histories remain separate; recreating a catalog
does not recreate the missing frozen E5 identity anchor. Human verification and
external distribution remain separate steps. No new model/Android run is claimed
or started here.
