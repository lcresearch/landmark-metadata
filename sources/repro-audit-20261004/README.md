# Fresh reproduction and checker audit

This source area records the October 4, 2026 reconstruction from official inputs,
the independently checked results, and confirmed checker/reporting defects.
Historical source snapshots remain byte-preserved. Models, SDKs, installed
dependencies, generated Java, APKs, raw arrays, logs and result records stay in
the external workspaces described by the reports.

Read `reports/CHECKER_AUDIT.md` for the executable label-parser counterexamples
and missing-evidence probes. `hand/REPORT.md` covers the fresh generic Hand and
MediaPipe Task reconstruction. The final overall report and claim map describe
which manuscript claims the new evidence supports and which historical claims
cannot be independently checked without the original sealed evidence.

## Maintained label checker

The preserved E5 checker and simple baseline use Python `splitlines()` to model
Java's label reader. This can produce both false compatible and false
incompatible decisions even on the supported, unchanged generated template.
`maintained/java_labels.py` uses CR/LF/CRLF line boundaries and Java's blank-line
rule for valid UTF-8. It preserves the actual nonblank label strings. Malformed
UTF-8 yields explicit abstention because Java's replacement-decoding semantics
are not implemented.

`maintained/preflight.py` and `maintained/baseline.py` apply this correction in a
new source area. The supplied-reference class-order branch uses the same reader.
The checker still has the documented template/processor-analysis limits; this
patch does not establish general Java data-flow analysis or semantic correctness.
The CLI preserves the historical convention: zero means command completion;
inspect the separate S, I and D judgments rather than treating zero as universal
compatibility. Explicit incompatibility exits 2; controller/generation errors
exit 3 in preflight.

The maintained entry points use the active Python interpreter and retained
generator source, and reject evidence paths inside this repository. Run them
with the recovered Python 3.11 environment:

```sh
/workspace/hand-contract-repro/.venv/bin/python \
  sources/repro-audit-20261004/maintained/preflight.py MODEL.tflite \
  --evidence-dir /workspace/new-preflight-evidence
```

Actual-library and fixture regression commands:

```sh
python sources/repro-audit-20261004/maintained/test_java_labels.py \
  --output-dir /workspace/new-java-label-regression
/workspace/hand-contract-repro/.venv/bin/python \
  sources/repro-audit-20261004/maintained/verify_fixture_regression.py \
  --output-dir /workspace/new-fixture-regression
```

The first command compares exact returned strings against the pinned real
Support 0.4.4 FileUtil JAR (22 valid text cases and three explicit malformed-input
abstentions). The second requires the external fresh E5 fixture catalog and
counterexample models; it checks all 65 retained fixture outcomes plus the
baseline and checker decisions on the original and both label counterexamples.
Missing prerequisites fail instead of being reported as skipped successes.

## Reproduction source

Use the existing isolated checkout; do not create a Git worktree unless asked.
Keep all generated evidence outside the repository, and use new directories for
new runs. The `hand/` source folder is intended to be copied to an external
workspace as described in `hand/REPRODUCE.md`.

`reproduction/run_task.py --output-dir /workspace/new-task-run` runs five exact
core conditions with primary/replay classification plus the historical official
and simple baselines. It constructs the prescribed RGB bytes and checks stages,
category counts, score bits, label changes, restoration and replay. These
historical-baseline results are distinct from tests of the maintained baseline.
The runner depends on the recovered base corpus and the pinned environment.
`reproduction/verify_corpus.py` independently reads the 105 CPU observations and
243 arrays from that corpus, verifies file digests and all nonmetadata buffers,
and requires the complete 23 decoder probes.

`probes/` contains the deliberately synthetic audit-failure tests and the new
label-only counterexamples. They are not natural model defects, historical
records, or additional independent models. The counterexample experiment calls
the real FileUtil/TensorLabel library on fixed scores and tests Task initialization;
it does not claim another Android-wrapper execution.

No independent human review or comparison against unavailable historical raw
archives is claimed. The source-only repository remains distinct from a public
reproduction/evidence deposit.
