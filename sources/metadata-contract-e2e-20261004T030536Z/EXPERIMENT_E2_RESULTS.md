# E2 results

Fresh Android instrumentation execution of the byte-unmodified generated public interface. Recovered host-JVM probes are not pooled into these results. Same-environment replay is separate from the primary observations.

| Variant | S | Generate | Compile | Package | Load | Inference | Actual getter | Earliest failure |
|---|---|---|---|---|---|---|---|---|
| original | PASS | PASS | PASS | PASS | PASS | PASS | PASS | — |
| description_control | PASS | PASS | PASS | PASS | PASS | PASS | PASS | — |
| label_permutation | PASS | PASS | PASS | PASS | PASS | PASS | PASS | — |
| permutation_restoration | PASS | PASS | PASS | PASS | PASS | PASS | PASS | — |

## Preservation and actual observations

- original: canonical graph preserved=True; embedded metadata equal=True; source equal=True; generated classes equal=True; DEX equal=True.
  - gray127: raw equality=True; score-bit equality=True; changed label positions=0.
  - rgb_pattern: raw equality=True; score-bit equality=True; changed label positions=0.
  - Replay: stage outcomes=True; raw equality=True; decoded equality=True.
- description_control: canonical graph preserved=True; embedded metadata equal=False; source equal=True; generated classes equal=True; DEX equal=True.
  - gray127: raw equality=True; score-bit equality=True; changed label positions=0.
  - rgb_pattern: raw equality=True; score-bit equality=True; changed label positions=0.
  - Replay: stage outcomes=True; raw equality=True; decoded equality=True.
- label_permutation: canonical graph preserved=True; embedded metadata equal=True; source equal=True; generated classes equal=True; DEX equal=True.
  - gray127: raw equality=True; score-bit equality=True; changed label positions=999.
  - rgb_pattern: raw equality=True; score-bit equality=True; changed label positions=999.
  - Replay: stage outcomes=True; raw equality=True; decoded equality=True.
- permutation_restoration: canonical graph preserved=True; embedded metadata equal=True; source equal=True; generated classes equal=True; DEX equal=True.
  - gray127: raw equality=True; score-bit equality=True; changed label positions=0.
  - rgb_pattern: raw equality=True; score-bit equality=True; changed label positions=0.
  - Replay: stage outcomes=True; raw equality=True; decoded equality=True.

## Evidence paths and boundaries

`E2/results.json` contains one record per variant/configuration with nested primary and replay evidence. See `variants/<variant>/generated`, `variants/<variant>/build`, and `executions/<run>/<variant>/device` plus `logs`. Exact subprocesses are in `commands-executed.sh` and each `.command.json`. Full dependencies and downloads: `prerequisites/`.

The generated historical Gradle project was not used. The pinned minimal Android APK harness compiles the unmodified Java with official Java/native dependencies. Whole-APK byte differences are not treated as code differences. No deployment, real-user impact, task-accuracy, prevalence, semantic-truth or general detector-accuracy claim follows. Class-order semantics remain ABSTAIN absent an independent artifact-tied reference.

The restored associated payload matches the original; archive container bytes need not match the publisher ZIP. A successful label-order intervention changes association relative to original only. If a stage is NOT_REACHED, no later-stage outcome is inferred.

## Deviations

```json
[
  {
    "stage": "same-environment replay controller",
    "observation": "Execution-tool transport disconnected while awaiting the long-running controller. Original, description and permutation replay records were already complete. Restoration APK installation succeeded, but the controller process was no longer running, no complete instrumentation log existed, and no device result.json was recovered for that last unit. Its outcome is INCOMPLETE_TRANSPORT, not a consumer failure or success.",
    "recovery": "Retain partial replay directory unchanged. Run only permutation_restoration using the same APK and parameters in replay-recovery-20261004T034600Z. Combine completed records explicitly, without overwriting a completed unit.",
    "generated_source_modified": false,
    "runtime_configuration_modified": false
  }
]
```
