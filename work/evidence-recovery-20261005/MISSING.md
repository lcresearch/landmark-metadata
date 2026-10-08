# Unrecovered material and intentional exclusions

Bounded local search on 2026-10-05 found none of the nine exact reconstruction
locators below. This does not establish absence on other machines or backups.

| Missing object | Consequence / recovery requirement |
|---|---|
| `/workspace/repro-android` | Later Android build/execution records are unavailable as a set. Recover their original archive and provenance. |
| `/workspace/repro-task` | Later Linux Task observations remain unavailable. |
| `/workspace/repro-hand` | Later Hand observations remain unavailable. |
| `/workspace/repro-external` | Later external/checker fixture and probe evidence remains unavailable. |
| `/workspace/repro-claims` | Later recomputed claim records remain unavailable. |
| `/workspace/repro-audit` | Later audit/probe records remain unavailable. |
| `/workspace/repro-control` | Later controls remain unavailable. |
| `/workspace/reproduction-evidence-index-20261004.json` | The later evidence-set index is unrecovered. |
| `/workspace/repro-external/E5/results.json` | Required separately pinned catalog is unrecovered; expected SHA-256 `bf49a475696eec4b38fb17587f6541a8393da14297e5dca1d433a051ba166e79`. |

The earlier E5 file has digest
`46f27b8245216c37537f9a995fb87dbb0d44eca300c582fdb5fbe2f5807f4872`.
It cannot replace the missing pinned catalog. A catalog made from newly generated
fixtures would not supply that historical trust anchor either.

## Search bounds and partial matches

The search enumerated 9,229 filenames under `/workspace`, hashed 1,873 candidate
files, searched 5,373 safe text files and inspected six ZIP central directories
with bounded candidate-member hashing. The two previously named evidence ZIPs
match their historical digests, but contain earlier packages. Scratch and
library-files were empty; shared contained an empty downloads directory.

Eight of 38 recorded reconstruction-file pins match older/shared source,
metadata, static or deterministic result bytes; 30 have no scoped match. Byte
identity does not locate the later execution or recover its complete provenance.
No files were placed into the absent `repro-*` paths or relabeled as that run.

SDK/dependency/environment/Git/credential paths, other machines, remote stores,
nested archives and over-limit files were not exhaustively searched. Two JSON
files above 8 MiB and three toolchain/image archives above 128 MiB were skipped;
the candidate-count limit was not reached. Exact arguments, paths, skips and
hash matches are retained under the external recovery root's `search/` directory,
indexed by [delivery-record.json](delivery-record.json).

## Other uncompleted work

- Hand, E4/E5 and baseline/literature raw payloads are intentionally outside the
  focal package. They are not declared missing merely because they were omitted.
- SDK/emulator/dependency binaries and signing keys are excluded by design.
  Text identities/acquisition records support later preparation, but this is
  not a standalone offline build environment.
- P3 bodies and saved comparisons are included; source authority and the full
  computational bridge were not independently rederived this turn.
- No durable deposit destination was selected. The user chose local staging;
  future storage/upload and retrieval verification remain separate.
- Actual human verification and a fresh build/inference run remain pending.

Recover the later archive from its original workspace/backup if available, then
compare its own recorded identities. If only a fresh rerun is possible, create
a new evidence history and state that it does not authenticate the lost run.
