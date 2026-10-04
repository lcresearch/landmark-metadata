# P2/P3 completed follow-ups

Completed 2026-10-04 (America/Los_Angeles). This round answers the authorized
same-Android consumer comparison and bounded independent reference inquiry.
No new model corpus or natural-defect search was conducted. Human audit remains
pending. `CURRENT_STATE.md` records the pre-experiment state, not the final result.

## P2: the rejection-stage difference survives the same Android environment

Ten component × variant × consumer configurations cover one canonical graph,
five model-byte conditions and two official consumer configurations. Two fixed
synthetic RGB inputs give 18 completed input observations: the Task deletion
configuration rejects before input preparation. There are 16 returned category
lists, 10 wrapper raw tensors, two caught getter exceptions and one caught Task
constructor exception. These are not ten models or independent replications.

| Condition | Generated wrapper | Android Task ImageClassifier |
|---|---|---|
| Original | Constructor, process and getter succeed | Constructor and classify succeed |
| Description control | Same success | Same success |
| Label deletion | Constructor and process succeed; getter throws | Constructor rejects; classify not reached |
| Label permutation | Success; 999 displayed labels change | Success; 999 displayed labels change |
| Restoration | Original scores and associations restored | Original scores and associations restored |

The wrapper exception is `java.lang.IllegalArgumentException: Label number 999
mismatch the shape on axis 1`. The Task public exception is
`java.lang.IllegalStateException: Error getting native address of native library:
task_vision_jni`, with cause `java.lang.IllegalArgumentException: Error occurred
when initializing ImageClassifier: Got 1000 class(es) for output index 0,
expected 999 according to the label map.` The cause and stack establish metadata
cardinality rejection; the generic outer message must not be described as a
missing native library. Instrumentation catches both failures.

All variants preserve the canonical graph and 165 non-metadata buffers. Generated
Java, compiled classes and DEX are equal across variants within each consumer
configuration. The graph-preserving canonical SHA-256 is
`73e57df01115600419abb72de4b2c3257200e12eb205d335bcbfc203a589bee8`.
Working model, APK asset and pre-load AssetManager hashes match for every unit.
This does not intercept the native interpreter's memory buffer.

All ten wrapper raw tensors match their corresponding original-input bytes.
For the eight successful condition/input pairs shared by the consumers, all
1,000 returned score bit patterns and labels match after alignment by Task
category index and wrapper output position. Task list rank is not class index.
Task internal raw tensors were not observed; public `classify` combines inference
and decoding, so its internal stages are not independently marked successful.

Both consumers use one fresh API-30/default/x86_64 AVD. The wrapper uses Support
0.4.4 and TFLite Java/native 2.13.0; Task uses Task Vision/Base 0.4.4 and its
published JNI library. Its embedded interpreter version is unknown. This reduces
the prior OS/device difference but does not isolate all runtime/integration
differences. Source and actual-bytecode review locate the Task check in
`ImageClassifier::CheckAndSetOutputs`, reached during `Init`; the wrapper checks
in `TensorLabel` on getter access. No latency or safety superiority was measured.

The first ten APK builds succeeded. Before any execution, instrumentation was
refined to distinguish successful API return from subsequent result-file IO;
all ten were rebuilt. Both build attempts are retained. Generated source and
dependency versions were unchanged. Only the final ten configurations executed.

## P3: qualified external display-order reference established

The bounded search retained 30 candidate requests: 25 HTTP 200 and five HTTP
404. No inference was performed in P3. A separate TFHub Lite0 fp32/2 model has
different whole-file bytes but equal complete computation fields, ordered
outputs and all 165 non-metadata buffers to the focal model. Its commit-pinned
publisher card explicitly identifies `classification/1` as parent. That exact
parent card prescribes the external ImageNetLabels file and explicitly excludes
the leading background line for its 1,000 output classes.

External reference SHA-256:
`536feacc519de3d418de26b2effb4d75694a8c4c0063e36499a46fa8061e2da9`.
Catalog commit: `81fdea8ffa53b5acbd66a012d17fb8f9602c714b`.

Original and restored resources agree with the reference at 1,000/1,000
positions; the predeclared cyclic permutation disagrees at 999/1,000. At
position 904, the reference/original/restoration say `window screen`; the
permutation says `window shade`. P2 again returns that position with score
`0.23542051017284393` for the patterned input in both consumers.

This strengthens E2 to **successful decoding with a reference-disagreeing
display-label association**. It does not establish image prediction error,
accuracy loss or a natural EfficientNet defect. The full output-index → stable
class-ID → display-name lineage requested by the original P3 protocol remains
ABSTAIN: duplicate `crane` and `maillot` strings are not unique class IDs. The
external mapping is independent of the mutated package, but its publisher
statement is not independently revalidated training history. The unversioned
label object is preserved as a hashed retrieval snapshot, not asserted immutable
for its entire history. Historical E5 runs without this reference remain unchanged.

## Verification and evidence locations

- `P2/EXPERIMENT_P2_RESULTS.md`, `P2/results.json`: completed device observations.
- `P3/EXPERIMENT_P3_RESULTS.md`, `P3/results.json`: bounded reference search and
  complete mapping comparison.
- `review/mechanism/MECHANISM_REVIEW.md`: version-pinned source and used binaries.
- `review/reference-audit/AUDIT_REPORT.md`: independent-script reference review;
  38 final checks pass. The initial Git-tree-header assumption failure and its
  resolution through all 3,411 reconstructed tree hashes remain preserved.
- `verification/runtime-record-review.json`: separate script recomputes 152
  passing checks from raw model/APK/device records, without rerunning inference.
- `verification/protected-evidence-review.json`: all 2,191 original, 970 audit
  and 46 previous-manuscript manifest entries, plus five input hashes, still match.
- `HUMAN_AUDIT.md`: uncompleted human review requirements.

Full evidence remains at `/workspace/metadata-contract-p2p3-20261004T073824Z`.
Source-only GitHub synchronization excludes models, raw results, dependencies,
SDK/AVD state, generated wrappers, APK/classes/DEX, logs and rendered papers.
Manifests and exact dependency identities are evidence, not proof of a portable
toolchain-from-archive reproduction.
