# Support #770 reconstruction results

One frozen setup was used after the user authorized execution. The full unmodified
linked model matches the reported shape/resource description. Actual AGP ML Model
Binding generation, explicit compilation and both APK builds succeeded. This is
a reconstruction of a known reported mechanism with missing historical identities,
not an exact replay of the reporter's Android Studio session.

## Asset and generated interface

The acquired metadata/2 asset is 2,780,051 bytes, SHA-256
`9711334db2b01d5894feb8ed0f5cb3e97d125b8d229f8d8692f625801818f5ef`.
Its one subgraph has 70 operators and 186 buffers; float32 input is
`[1,257,257,3]`, output `[1,257,257,21]`. Associated `labelmap.txt` has 21 lines,
141 bytes and SHA-256 `d9efa78274f1799ddbcab1f87263e19dae338c1697de47a5b270c9526c45d364`.
No labels, graph or metadata were edited. The reporter did not provide a digest,
so matching names and shapes do not identify exact 2022 bytes.

AGP generated `LiteModelDeeplabv31Metadata2.java` through its real
`:app:generateDebugMlModelClass` task. The unchanged generated getter calls
TensorLabel. We compiled that source using the explicit Android instrumentation
harness; Android Studio's UI and a complete AGP application build were not replayed.
The same original model is packaged in both APKs, and device-side identities agree.

## Version interpretation

| Layer | Selected identity | What this establishes |
|---|---|---|
| Actual ML Model Binding generator | AGP 7.4.2 with Gradle 7.5.1 | One generator configuration; not the unknown reporter version |
| Build-time metadata dependency | `tensorflow-lite-metadata:0.1.0-rc2` | AGP-resolved parser dependency; not runtime Support 0.4.4 |
| Wrapper runtime and decoder | TFLite 2.13.0, Support 0.4.4 | The observed process/getter behavior in this combination |
| Task consumer | Task Vision/Base 0.4.4, Support API 0.4.4 | One Task configuration; embedded native interpreter version remains unknown |
| Host/device | Temurin 17.0.12+7, SDK/API 30 x86_64 software AVD, build tools 35.0.0 | Fixed reconstruction environment, not historical equivalence |

The wrapper exception occurs in Java Support's TensorLabel after process returned.
That localizes the observed failing layer; it does not show that LiteRT runtime
version caused the problem or that upgrading fixes it. Generator, Support and
Task changes can independently alter behavior. The [official LiteRT migration
guide](https://developers.google.com/edge/litert/migration) documents the runtime/API
transition, but this experiment executes the pinned TFLite stack and contains no
LiteRT version comparison. No version search or alternative configuration was run.

## Observed public stages

| Consumer | Construction | Computation call | Output access | Retained result |
|---|---|---|---|---|
| Actual AGP-generated wrapper | PASS | `process`: PASS | Category getter: FAIL | Complete caught TensorLabel exception and raw float32 tensor |
| Task ImageSegmenter | PASS | `segment`: PASS | Category-mask access: PASS | One 257×257 UINT8 mask and 21 labels |

Both arms have identical model/input hashes and completed instrumentation records.
The wrapper and Task instrumentation commands took 125.1 and 83.7 seconds on this
software AVD; these include harness/transport work and are **not performance
benchmarks**. No complete scientific result was retried.

### Wrapper

On the one 257×257 gray-127 RGB input, construction and process returned. The
read-only observer saved 5,548,116 raw output bytes with shape `[1,257,257,21]`,
SHA-256 `029b8cd2f0a4425f5300e76c6bac998948684f986e57af29eed08e27c11e650a`.
Then the **actual generated category getter failed** with
`java.lang.IllegalArgumentException: Label number 21 mismatch the shape on axis 1`.
The stack includes TensorLabel and the generated getter. The complete scientific
FAIL, raw output, class/DEX/APK identities and collection records are retained.
The harness caught the exception; no production application crash was observed.

The device-side input SHA-256 is
`0dfa666c3ad18209900fbd68463f933e349b0e06a1b06e3833c5e7906d43b6c0`.
It is our fixed synthetic input, not the reporter's unavailable bitmap.

### Task

Task returned one `CATEGORY_MASK` segmentation: 66,049 bytes, shape `[257,257]`,
SHA-256 `d7bccfd47ff005e33710bc793ad07fdc8ce61c1e9be1fcabec939de22352ee3d`,
with 21 colored-label entries. Construction, segment and mask access all passed.
A returned mask is a smoke-test result, not an accuracy assessment. Task native
raw scores were not exposed; no equality comparison to wrapper scores is claimed.

### Bounds and retained failures

One asset, one configuration, one AGP generation (26.4 seconds), one build per
consumer (6.9 seconds for both), one fresh AVD boot (291.2 seconds to ready), and
one invocation per consumer. All finished within their declared bounds. Acquisition
needed one request per URL. No version sweep, model mutation, alternative input,
restart or scientific retry was used. The protocol's stop conditions were not hit.
The owned emulator was stopped and its process/console port confirmed absent.

The wrapper getter FAIL remains a completed scientific observation. Gradle's
ordinary missing-repository responses, boot-time offline/empty adb observations,
emulator warnings and one incomplete progress snapshot remain in the raw logs;
none is silently relabeled as a model failure or a second experiment.

## Scope and evidence

The [original report](https://github.com/tensorflow/tflite-support/issues/770)
and [consumer-selection reply](https://github.com/tensorflow/tflite-support/issues/770#issuecomment-1108777779)
describe an unsupported segmentation/generated-interface combination. Reproducing
its mechanism does not establish a supported-path framework bug, a natural
EfficientNet defect, prevalence or prediction accuracy. It adds a bounded example
of why acceptance should exercise the actual output endpoint and select the
appropriate consumer. It is not discovery of the TensorLabel count rule.

Evidence root: `/home/hsz/landmark-evidence/support770-reconstruction-20261111`.
Exact selected paths/hashes and verified local retention are recorded in the
[delivery receipt](delivery-record.json); [validation](VALIDATION.md) distinguishes
scientific outcomes from identity/readback checks. The current short manuscript and its evidence
pins remain unchanged; this is a separate reconstruction record. Human review,
persistent reviewer access and a second independently retained copy remain open.
