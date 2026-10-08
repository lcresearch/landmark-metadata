# Bounded parser follow-up protocol — 8 October 2026

This is a fresh, known-result agent probe, not recovery or authentication of the
4 October reconstruction, model inference, or human verification. This protocol
is saved before the fresh library calls. Historical source/evidence is read only.

## Question and stopping rule

Determine whether actual Support 0.4.4 `FileUtil.loadLabels` and
`TensorLabel(List, TensorBuffer).getCategoryList` disagree with Python
`splitlines()` on the previously described VT and U+2028 inputs, with an ordinary
LF control. Separately check the maintained valid-UTF-8 parser against actual
FileUtil on the existing 22 valid cases and its three malformed-input abstentions.
Stop after these fixed cases; no model collection, Android build, inference,
Task initialization, E5 expansion, or 65-fixture regression is authorized by this
protocol. Missing dependencies or mismatched pins block execution; do not replace
the actual library with a handwritten decoder or change library versions.

## Bounded recovery before execution

Check the four exact historical paths under `/workspace/repro-audit` and
`/workspace/repro-external` named by HA09c, the six existing archive-entry indexes
under `/workspace/evidence-recovery-20261005T170453Z/search`, the saved file
inventory, and the three top-level workspace ZIP central directories. Compare
any E5 catalog candidate to the separately recorded SHA-256
`bf49a475696eec4b38fb17587f6541a8393da14297e5dca1d433a051ba166e79`.
Do not extract archives or search broad model payload collections. Negative
results establish absence only within these locators and indexes.

## Inputs and actual consumers

- Read the unchanged classifier with SHA-256
  `6c7ab0a6e5dcbf38a8c33b960996a55a3b4300b36a018c4545801de3a3c8bde0`
  only to extract `labels_without_background.txt`; do not write a model mutant.
- Reuse the exact historical transformations from
  `sources/repro-audit-20261004/probes/probe_label_parser.py`: original bytes;
  replace the first LF with VT; replace the first LF with UTF-8 U+2028 followed
  by `suffix` and LF. Reuse the fixed little-endian 1,000 float values `i/1000`.
- Compile and run byte-identical copies of historical `DecoderProbe.java` and
  maintained `LabelOracle.java`. These call actual fixed library APIs. The
  unchanged decoder probe records a caught Java exception as JSON and exits
  zero; distinguish that `FAIL` observation from process failure.
- Use installed JDK 17.0.12+7 and the eight historical Java classpath JARs. Match
  each JAR to its prior pin in `docs/reproduction/toolchain.json`; especially
  Support API 0.4.4
  `15d59ab34528d75908306432715e522a278f781ba6f4802d6b41917a5838a59d`.
- Import, without modification, `CASES`/`MALFORMED` and `java_labels.py` from the
  maintained source. Record complete FileUtil output strings via the unchanged
  base64 oracle transport. Malformed input must make the helper abstain; no
  equivalence with Java replacement decoding is claimed.

## Declared comparisons and expected observations

These expectations already appear in historical reports; this is not blind.

| Condition | Python splitlines count | Actual FileUtil count | TensorLabel |
|---|---:|---:|---|
| Original LF | 1,000 | 1,000 | 1,000 categories |
| First LF replaced by VT | 1,000 | 999 | Label-count exception |
| U+2028 plus suffix inside first label | 1,001 | 1,000 | 1,000 categories |

Require exact counts/status/exception text for these three cases. Require exact
string-list equality for all 22 maintained valid cases and helper abstention for
all three malformed cases. A failed comparison stays failed and produces a
nonzero controller exit; never silently reduce the denominator.

## Evidence and scope adaptation

Write all raw inputs, synthetic scores, copied source, dependency identities,
compiled classes, version output, commands, timestamps, exit codes and unedited
stdout/stderr into a new timestamped external directory. Copy this protocol and
runner before execution; record their hashes. Keep only first-party source,
this protocol, a concise report and a path/digest index in Git.

The new driver reuses the historical Java probe, transformations and score
construction, but intentionally omits historical preflight/code generation,
model rewriting, preservation checks and Task initialization. It adds per-call
logging, identity checks and the existing 22+3 differential cases. Thus it can
support fresh isolated FileUtil/TensorLabel observations and bounded helper
checks, but cannot reestablish the old end-to-end checker/baseline decisions,
Task results, generated-source equivalence or missing 65-fixture regression.
