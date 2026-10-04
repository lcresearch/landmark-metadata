# E1 results

Fresh Android instrumentation execution of the byte-unmodified generated public interface. Recovered host-JVM probes are not pooled into these results. Same-environment replay is separate from the primary observations.

| Variant | S | Generate | Compile | Package | Load | Inference | Actual getter | Earliest failure |
|---|---|---|---|---|---|---|---|---|
| original | PASS | PASS | PASS | PASS | PASS | PASS | PASS | — |
| description_control | PASS | PASS | PASS | PASS | PASS | PASS | PASS | — |
| label_deletion | PASS | PASS | PASS | PASS | PASS | PASS | FAIL | generated_getter |
| label_restoration | PASS | PASS | PASS | PASS | PASS | PASS | PASS | — |

## Preservation and actual observations

- original: canonical graph preserved=True; embedded metadata equal=True; source equal=True; generated classes equal=True; DEX equal=True.
  - gray127: raw equality=True; score-bit equality=True; changed label positions=0.
  - rgb_pattern: raw equality=True; score-bit equality=True; changed label positions=0.
  - Replay: stage outcomes=True; raw equality=True; decoded equality=True.
- description_control: canonical graph preserved=True; embedded metadata equal=False; source equal=True; generated classes equal=True; DEX equal=True.
  - gray127: raw equality=True; score-bit equality=True; changed label positions=0.
  - rgb_pattern: raw equality=True; score-bit equality=True; changed label positions=0.
  - Replay: stage outcomes=True; raw equality=True; decoded equality=True.
- label_deletion: canonical graph preserved=True; embedded metadata equal=True; source equal=True; generated classes equal=True; DEX equal=True.
  - gray127: raw equality=True; score-bit equality=NOT_REACHED; changed label positions=NOT_REACHED.
  - rgb_pattern: raw equality=True; score-bit equality=NOT_REACHED; changed label positions=NOT_REACHED.
  - Exact failure: `java.lang.IllegalArgumentException: Label number 999 mismatch the shape on axis 1`.
  - Replay: stage outcomes=True; raw equality=True; decoded equality=True.
- label_restoration: canonical graph preserved=True; embedded metadata equal=True; source equal=True; generated classes equal=True; DEX equal=True.
  - gray127: raw equality=True; score-bit equality=True; changed label positions=0.
  - rgb_pattern: raw equality=True; score-bit equality=True; changed label positions=0.
  - Replay: stage outcomes=True; raw equality=True; decoded equality=True.

## Evidence paths and boundaries

`E1/results.json` contains one record per variant/configuration with nested primary and replay evidence. See `variants/<variant>/generated`, `variants/<variant>/build`, and `executions/<run>/<variant>/device` plus `logs`. Exact subprocesses are in `commands-executed.sh` and each `.command.json`. Full dependencies and downloads: `prerequisites/`.

The generated historical Gradle project was not used. The pinned minimal Android APK harness compiles the unmodified Java with official Java/native dependencies. Whole-APK byte differences are not treated as code differences. No deployment, real-user impact, task-accuracy, prevalence, semantic-truth or general detector-accuracy claim follows. Class-order semantics remain ABSTAIN absent an independent artifact-tied reference.

The restored associated payload matches the original; archive container bytes need not match the publisher ZIP. A successful label-order intervention changes association relative to original only. If a stage is NOT_REACHED, no later-stage outcome is inferred.

## Deviations

```json
[
  {
    "stage": "harness preparation before first Android execution",
    "observation": "The initial APK build succeeded. POM inspection identified declared ODML image and annotation dependencies not yet packaged. They were recovered and archived before any model execution. The complete dependency configuration is rebuilt in a separate build directory; initial build artifacts retained.",
    "generated_source_modified": false,
    "initial_apks_executed": false
  }
]
```
