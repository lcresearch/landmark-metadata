# Evidence-checking repairs

The user requested fixes after a comprehensive review of merged main
`c0cd67307d89a74394c7d0deb1f425e608906aef`. These changes address verifier
false passes, input attribution and current navigation. They do not alter the
manuscripts, historical experiment records, import manifests or research claims.
No Android, model or JVM execution is performed by this repair.

| Review finding | Maintained repair |
|---|---|
| A directory could replace an authenticated archive file during extraction | [Archive verifier](../evidence-recovery-20261005/verify_archive.py) checks every member name/type and rejects file/parent collisions |
| A damaged or absent gzip trailer passed archive verification | The same verifier consumes the gzip stream through EOF and validates CRC/length |
| E5 baseline rows could name other fixtures with the same status | [Observation reader](../observation-review-20261004/verify_observations.py) binds each variant/mode to its actual Android core model before comparison |
| Hand could count explicitly failed preparation as completed | The observation reader checks preparation/controller completion and counts only validated records |
| P2's old total PASS omitted preservation and coverage | [P2 reader](verify_p2_records.py) separates validity, coverage and historical outcomes; all must pass |
| Nested current deliverable pins were unchecked | [Source checker](../../scripts/check_source_tree.py) checks the current companion, claim map and handoff as well as source/predecessor pins |
| Reimport could remove existing files from the hash index | [Importer](../../scripts/import_workspace_sources.py) validates the existing inventory before writes; the checker detects unindexed snapshot files |
| Recovered inputs were described as freshly downloaded | [Android initializer](../../scripts/initialize_android_run.py) records local inputs without asserting acquisition it did not observe |
| P2 instructions incorrectly said INPUTS.json was absent | [Commands](../../docs/reproduction/COMMANDS.md) points to the preserved input manifest and explains path adaptation |
| Current entries said PR #15 was open after it merged | README, TODO, MEMORY and the current manuscript index record its verified squash merge; dated history stays intact |

The previously disclosed parser-verifier reuse limitation is also addressed by
a [maintained parser reader](verify_parser_probe.py). It checks trusted case,
payload, source and dependency identities rather than accepting counts and
self-declared pins alone. The executed October 8 runner/verifier and its reports
remain unchanged as historical sources.

Use the current [reproduction commands](../../docs/reproduction/COMMANDS.md) for
prerequisites and setup. All paths below assume the repository root:

```sh
# Read a saved P2 round; never write into it.
PYTHONDONTWRITEBYTECODE=1 python3 work/review-fixes-20261021/verify_p2_records.py \
  --round-root /path/to/recovered-p2-round \
  --output /path/outside/round-and-repository/new-p2-readback.json

# Read the saved October 8 parser evidence without running Java.
PYTHONDONTWRITEBYTECODE=1 python3 work/review-fixes-20261021/verify_parser_probe.py \
  --evidence /path/to/parser-evidence \
  --report /path/outside/evidence-and-repository/new-parser-readback.json

# Copy sources for a future Android run; no downloads, builds or inference.
PYTHONDONTWRITEBYTECODE=1 python3 scripts/initialize_android_run.py \
  --repo "$PWD" --root /path/to/new-external-android-round
```

P2 expects INPUTS.json and P2/ containing frozen inputs, build records, APKs and
device observations. Overall PASS requires the expected ten configurations,
18 observations, 16 decoded lists and ten wrapper tensors as well as status,
identity and comparison checks. Comparisons concern returned Task scores;
no native Task tensors are inferred. Failed or missing conditions are retained
as failures, not converted into successful observations.
The freeze must cover the plan, dependency/static/build records, APKs and
preparation/runtime sources. Known postprocessing tools are not presumed to have
existed before execution; if listed in the freeze, their bytes are still checked.

The parser reader's default original-label anchor is the independently recorded
historical evidence-manifest digest. For a newly captured probe, supply
`--model /path/to/original.tflite`; the fixed model SHA must match before its
associated labels can serve as the anchor. A self-reported model hash is not an
independent anchor. Saved stdout consistency does not authenticate that a
library actually ran; no human verification is established.

The archived P2 and parser readers are preserved, but their old PASS fields
must not substitute for these maintained checks. Historical counts and reports
have not been regenerated. Raw evidence remains outside Git and unavailable at
its original paths in this environment.

Regression validation uses temporary synthetic files and copy-only setup:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_source_tree.py
git diff --check
```

Validation on 21 October 2026: all **144 regression tests passed** (83 before
this repair). The source checker passed for 553 files, including 257 Python
syntax checks, 17 shell scripts, 47 JSON files, 354 imported source identities
and seven current/predecessor artifact pins. Navigation and whitespace checks
passed; historical missing-locator and unchecked external-evidence warnings remain.
Logs are outside Git at `/workspace/landmark-builds/review-fixes-20261021/`.

Independent source reviews checked the initializer/observation formats, repository
integrity changes and both new readers. The P2 freeze inventory was corrected
to require execution inputs without presuming later postprocessing existed
before execution. Actual historical P2/parser packages were not available for
a fresh readback, so compatibility validation is against preserved producers
and synthetic positive controls.

`git diff` against the review base confirms no changes to `sources/`, the
imported P2/P3 tree, the current paper revision, the original parser supplement
or either source import manifest. Paper builds were not repeated because
manuscript bytes are unchanged. Delivered for review in
[PR #16](https://github.com/lcresearch/landmark-metadata/pull/16), from feature
branch `fix/review-integrity-20261021`. Consult the live PR for its subsequent
state; delivery does not authorize a merge.
