# November short-paper evidence and author handoff

Use the [new short source](manuscript/paper.tex), [claim map](CLAIM_EVIDENCE.md) and
[evidence identity index](evidence-index.json), pinned together in
[CURRENT_MANUSCRIPT.json](../../docs/CURRENT_MANUSCRIPT.json). The October short,
full companion, ledger and unsigned human-audit targets remain historical and
unchanged. The full companion has not been rewritten for the November run.

## What can be inspected now

The new local execution is `/home/hsz/landmark-evidence/focal-rerun-20261110`.
Its archive is `/home/hsz/landmark-evidence/focal-rerun-20261110-evidence.tar.gz`:
3,321,366,905 bytes, SHA-256
`57970b8ff5a4127caf11b13bdc9837ed2479c13dbb488cfc5262506a76535afd`.
All 2,120 members and the embedded manifest were freshly read back for this
revision. The selected index binds 1,036 live files to their archived identities;
this is a file count, not a sample size. The [run receipt](../focal-rerun-20261110/delivery-record.json)
remains unchanged. No binary material is uploaded to Git, Releases or LFS.

New editorial readbacks are retained at
`/home/hsz/landmark-evidence/paper-revision-20261111/` under `core-readback/` and
`archive/`. They are byte-preserved copies of actual readbacks first written under
`/tmp/landmark-paper-review-20261111/`; recorded command paths retain that origin.
The index pins both their current retained locations and copied bytes. These
outputs postdate the experiment archive and are not falsely labeled its members.

| Author inspection | Start at these evidence groups |
|---|---|
| Loss versus new execution provenance | N0 availability/recovery; N1 initial freeze/environment; the new run is known-outcome, not the recovered old run |
| Actual generated getter and preservation | N2 models/generated source/classes/DEX/APKs; N3/N4 complete device files, install commands and controller records |
| E1/E2 results and record selection | N3/N4 selected primary/replay; N7 interruptions, previous results, relocation and continuation identities; do not double-count aliases or excluded initial attempts |
| Same-Android comparison and reader correction | N5 actual-file P2 readback and its 112 identified inputs; N8 before/after reader and failed/successful readbacks; unchanged device cause chain |
| Qualified reference order | N6 six input bodies, card/parent rule, bridge and complete positional map; no full search, synset, stable-ID or accuracy claim |
| Archive retention | N9 receipt/manifest/readback; local integrity is not external backup or anonymous access |

[recheck_core.py](recheck_core.py) redirects only pinned audit report destinations
into a fresh external directory and reuses the maintained P2/P3 readers. It does
not run models or write into the original run. Adapted source/patch hashes and
original-record preservation checks are saved. [verify_new_archive.py](verify_new_archive.py)
reads without extraction. Commands, source/build identities and actual checks
are in [VALIDATION.md](VALIDATION.md). Source tests are separate from these
saved-byte checks, which remain separate from fresh inference and human review.

## Six author questions — all unsigned

Reviewer name/role: **PENDING**. Date: **PENDING**. Inspected manuscript/index
SHA-256 values: **PENDING**. Record the actual values from the current pointer
when reviewing, with observations and a conclusion for each item.

| Question | Evidence route | Human observation / conclusion |
|---|---|---|
| 1. Do generated source, compiled classes and attributed device records establish the actual getter call after process, without a replacement decoder? | N2/N3/N4; C3 | PENDING |
| 2. Do model/resource/APK identities and separate G/W/O, M, F and H comparisons support the stated intervention and restoration scope? | N1/N2; C2 | PENDING |
| 3. Do complete E1 stages, raw outputs and exception stacks establish the four caught getter failures after successful inference? | N3; C3 | PENDING |
| 4. Do full E2 mappings/score bits and restoration support 999 changed strings, and are the known outcomes, excluded first attempt and two interrupted/continued collections disclosed correctly? | N4/N7; C4 | PENDING |
| 5. Do P2 stages and complete cause chains support the comparison, with reader correction separated from unchanged device observations and Task/native limits retained? | N5/N8; C6 | PENDING |
| 6. Do the six pinned P3 inputs, bridge and explicit mapping support only the stated display-order result, without implying a repeated full search, stable IDs or accuracy? | N6; C5 | PENDING |

Agent checks and PR review cannot supply these signatures. Author verification,
independent human audit and independent human reproduction are distinct. The
historical human-review templates remain unsigned; this revision supplies a new
target rather than changing their status retrospectively.

## Still open

- The old cloud archive/execution records remain unavailable. Hashes and matching
  fresh results do not reconstruct old provenance; a bounded search is not proof
  that every backup is gone.
- E5's zero additional rejection is an explicitly historical result. Hand,
  external static examination, development counts, the later E5 catalog and
  parser history were not newly recreated or raw-verified. The old companion
  cannot substitute for available supporting bytes in a submitted claim.
- A second verified evidence copy and persistent anonymous reviewer delivery
  remain open. Choose destination/access and redistribution/anonymization scope
  before an external upload; the source-only rule remains in force.
- Venue/category, final author verification and submission remain undecided.
