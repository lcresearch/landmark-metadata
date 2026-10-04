# Java label reader maintenance patch

Add `java_labels.py` next to the maintained Python entry points. It mirrors the
selected Support 0.4.4 `FileUtil.loadLabels(InputStream, UTF_8)` line and blank-line
semantics for valid UTF-8. CR, LF and CRLF terminate lines; VT/FF/NEL/U+2028/U+2029
do not. Nonblank label strings retain their leading/trailing whitespace. A BOM
is ordinary label content. Java's trim test removes characters only through
U+0020 when deciding whether to discard an empty line.

Malformed UTF-8 explicitly requires abstention. Java's replacement decoding and
Python's `errors='replace'` do not always produce the same strings. For example,
`ED A0 80` becomes one replacement character in the tested Java decoder, but
three in Python. We preserve that boundary instead of introducing an untested
replacement decoder.

For the maintained copy of E5 `check`, replace the line-93 comprehension:

```python
from java_labels import LabelEncodingUnsupported, load_java_utf8_labels

try:
    labels = load_java_utf8_labels(files[filename])
except LabelEncodingUnsupported as error:
    finding['diagnostic'] = str(error)
    findings.append(finding)  # initial finding status is ABSTAIN
    continue
```

For the maintained simple baseline, replace its lines 97–98:

```python
from java_labels import LabelEncodingUnsupported, load_java_utf8_labels

try:
    labels = load_java_utf8_labels(payload)
except LabelEncodingUnsupported as error:
    report.update(status='ABSTAIN', diagnostic=str(error))
    return report
```

The legacy frozen E4/static checker also shares the original line parser. Keep
that historical snapshot unchanged; a future maintained version must use the
helper with its own explicit ABSTAIN result. Supplied-reference class-order
comparison in preflight has another parser occurrence at line 34: if maintaining
that optional feature, apply the helper and return an I ABSTAIN on unsupported
encoding. Do not claim that patching D automatically fixes the I branch.

Run actual-library differential regression:

```bash
PYTHONDONTWRITEBYTECODE=1 python test_java_labels.py \
  --output-dir /workspace/repro-audit/java-label-regression-next
```

This checks 22 valid UTF-8 fixtures by exact returned strings against the pinned
real FileUtil API, plus three malformed inputs that explicitly require
abstention. It includes both EfficientNet cardinality counterexamples. Missing
JDK/JARs or a changed oracle JAR digest fail instead of silently skipping tests.
The JARs/classes/output results stay outside the source repository.
