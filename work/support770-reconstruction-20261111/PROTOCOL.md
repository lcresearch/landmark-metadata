# Support #770: one bounded reconstruction

Authorized 11 November 2026 after PR #23 integration (`fd9ce5d`). Follow the
[screened plan](../case-screening-20261111/SHORTLIST.md). This protocol is frozen
before full model acquisition or generation. Raw outputs stay in the new external
root `/home/hsz/landmark-evidence/support770-reconstruction-20261111`.

Question: can one actual ML Model Binding configuration generate/import the
unmodified linked segmentation model, execute process, then fail at its category
getter? What public stages does Task ImageSegmenter reach on the same input?
Either success or failure is an observation; no result is required to match #770.
The report's consumer route is explicitly unsupported. Neither this nor the
classifier study establishes prevalence, accuracy or a new validator advantage.

## Fixed configuration and inputs

- Asset: the official example's exact `lite-model_deeplabv3_1_metadata_2.tflite`
  [download](https://storage.googleapis.com/download.tensorflow.org/models/tflite/task_library/image_segmentation/android/lite-model_deeplabv3_1_metadata_2.tflite).
  Acquire whole bytes, SHA-256, graph input/output descriptors, metadata and label
  payload. Require output `[1,257,257,21]` and 21 associated labels before proceeding.
  Preserve original bytes; do not edit or replace with metadata/1.
- Generator: Android Gradle plugin **7.4.2**, Gradle **7.5.1**,
  `buildFeatures { mlModelBinding true }`, model in `app/src/main/ml/`.
  Run the real AGP `generateDebugMlModelClass` task. Android Studio's GUI is not
  replayed. Do not replace this task with standalone CLI codegen or hand-written
  TensorLabel. Retain generated files and the resolved generator dependency.
- JDK **Temurin 17.0.12+7**, compile/target SDK **30**, build tools **35.0.0**,
  min SDK **23**, Java target **8**. Copy SDK components from the preceding verified
  local toolchain; read its JDK/Python without writing old evidence.
- Intended wrapper libraries: TFLite **2.13.0**, Support **0.4.4**. Intended Task
  Vision/Base **0.4.4**; Task's embedded interpreter is a separate, possibly unknown
  version. Record actual resolved dependencies/native hashes before runtime.
- One deterministic 257×257 RGB image: all channels 127; retain the bytes/hash.
  Use the same bitmap for both consumers, CPU/one thread, no accuracy judgment.
- If build succeeds: fresh API-30 x86_64 software AVD, `-accel off`; one call per
  consumer. Preserve construction/process/getter or construction/segment stages,
  complete exception causes, available raw output and selected Task output kind.

## Bounds and stop rules

One frozen configuration, **one AGP generation invocation (900-second timeout)**.
Acquisition budget: 20 minutes, at most two transport attempts per exact URL;
retain each response/error and partial download. Verify the Gradle distribution
against the publisher's SHA-256 response. Do not switch versions or repositories
after a dependency/generation failure. Stop if full asset linkage or actual AGP
generation cannot be established. A successful setup permits one build invocation
per consumer (600 seconds), one AVD boot (900 seconds), and one runtime invocation
per consumer (300 seconds). Retain complete scientific failures; do not rerun them
to seek success. Missing transport collection may be recovered with separate
records, without repeating completed inference. Stop the owned AVD afterward.

The original report does not pin Studio/AGP, runtime, Support/Task, model digest
or input. This is **mechanism reconstruction**, never exact historical replication.
Version choice is a fixed contemporary-to-library engineering configuration, not
an estimate of the reporter's versions or a LiteRT compatibility survey. A version
effect would require an independently authorized, matched comparison; this run
cannot show that a LiteRT upgrade fixes or causes the report.

## Primary configuration references

[Android Studio 4.1 notes](https://developer.android.com/studio/releases/past-releases/as-4-1-0-release-notes)
describe import into `ml/`, generated classes and the initial supported model
domains. [AGP 7.4 release notes](https://developer.android.com/build/releases/agp-7-4-0-release-notes)
document Gradle 7.5/JDK 11 minima; Gradle 7.5.1/JDK 17 are our explicit choices.
[LiteRT migration](https://developers.google.com/edge/litert/migration) distinguishes
the classic Interpreter API from newer API paths; renaming a dependency alone
does not identify generator or Task internals. Current pages are not 2022 snapshots.
