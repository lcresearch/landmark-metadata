# Fresh isolated parser evidence — 8 October 2026

Actual Support 0.4.4 FileUtil/TensorLabel calls reproduce both previously
described line-parser disagreements. This is fresh, known-result agent execution;
the old reconstruction's raw results were not recovered. It is not human review.

## Observations

The classifier's pinned original label payload and the two exact historical
byte transformations were supplied to unchanged `DecoderProbe.java`, using
synthetic `[1,1000]` float scores. No model was executed or rewritten.

| Input | Python `splitlines()` count | Actual FileUtil count | Actual TensorLabel result |
|---|---:|---:|---|
| Original LF control | 1,000 | 1,000 | 1,000 categories |
| First LF replaced by VT | 1,000 | 999 | `java.lang.IllegalArgumentException: Label number 999 mismatch the shape on axis 1` |
| U+2028 plus suffix inside first label | 1,001 | 1,000 | 1,000 categories |

The maintained helper also matches the complete actual FileUtil string lists in
all 22 existing valid-UTF-8 cases, and abstains on all three existing malformed
cases. Malformed Java replacement output is retained without claiming equivalent
Python replacement decoding. These are 28 declared comparisons (3+22+3), not
28 independent models. The expected VT exception is a library failure recorded
by the unchanged Java probe, whose process exits zero; controller PASS means
the expected observation matched, not that VT decoding succeeded.

All eight JARs match previously recorded pins; actual Java reports Temurin
17.0.12+7. The unchanged Support API JAR has SHA-256
`15d59ab34528d75908306432715e522a278f781ba6f4802d6b41917a5838a59d`.
The current controller used Python 3.12.14; this is not a claim to recreate the
historical Python environment. Dependency/source/input/output identities and
versions are in the [evidence index](evidence-index.json).

## Recovery and limits

The four exact later parser/catalog paths are absent. Six saved archive-name
indexes, the saved file inventory and central directories of the three current
top-level workspace ZIPs yielded no parser result candidate. This was bounded
local recovery, not a global absence proof or archive authentication.

Original E5 records are present at the earlier `metadata-contract-e2e` location.
Its results digest is `46f27b8245216c37537f9a995fb87dbb0d44eca300c582fdb5fbe2f5807f4872`,
which does not match the required later catalog
`bf49a475696eec4b38fb17587f6541a8393da14297e5dca1d433a051ba166e79`.
No substitution was made. The old parser/Task records, later pinned catalog and
65-fixture maintained regression remain unrecovered/unverified.

The fresh run confirms the selected actual Java behavior and bounded helper
cases. It does not rerun the old full E5 checker or simple-baseline decisions,
Task initialization, code generation, model preservation, Android inference or
the 65-fixture regression. Historical reconstruction statements about those
activities remain report-attributed. No current-version claim, prevalence,
prediction accuracy, natural defect or production crash follows.

## Raw evidence and verification

Raw evidence is outside Git at `/workspace/parser-followup-20261008T032600Z`.
The directory suffix is a provisional identifier selected before execution;
it is not an execution timestamp. `invocation.json` records actual start
`2026-10-08T03:23:56.053118+00:00`; `completion.json` records finish
`2026-10-08T03:23:58.483161+00:00`. Per-command timestamps are authoritative.
The [protocol](PROTOCOL.md) and executed runner were saved before library calls,
copied into the raw directory, and hashed there.

All 35 subprocess calls retain exact argument arrays, stdout, stderr and exit
codes: 28 FileUtil oracle calls, three decoder calls and four version/compile
calls. Oracle base64 transport preserves every label string. The 151-entry
`evidence-files.json` covers the exact remaining file set, including raw inputs,
scores, source copies and classes; it excludes itself to avoid a circular hash.
Its own digest is recorded in the source index. No raw artifact is committed.

`verify_probe.py` freshly verified all 151 file sizes/hashes and the exact file
set, actual stdout, labels/counts, sources and declared denominators: 379 checks,
zero failures. Its report is outside the frozen experiment directory at
`/workspace/parser-followup-readback-20261008T032714Z/report.json`. A second agent
also read the raw manifest, command payloads, output transport and original
source/JAR pins; shared infrastructure and inputs mean this is not independent
human verification.

Exact controller command (the saved invocation omits the interpreter's `-B`
flag because it records `sys.argv`; this command supplies that outer detail):

```bash
python -B work/preaudit-followup-20261008/parser/run_probe.py \
  --output-dir /workspace/parser-followup-20261008T032600Z
```

The command ran from `/workspace/landmark-preaudit-followup`, exit 0. For another
run choose a new external path; the runner refuses to overwrite an existing one.
The [source driver](run_probe.py) discloses its bounded adaptation of the
historical probe. Source snapshots and old evidence remain unchanged.
