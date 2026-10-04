# E1 — EfficientNet generated-interface execution

Written before new E1 generation/build/inference. Starting artifact and recovered results are in CURRENT_STATE.md and phase0/results.json. Experimental unit: component × variant × pinned Android consumer configuration. Inputs are repeated observations.

## Hypothesis and intervention

Test whether deletion of the last associated label is reachable as a failure through the unmodified generated public interface. Do not presume the failure stage or a successful original.

- A original: exact frozen EfficientNet Lite0 float32 version-1 artifact, SHA-256 `6c7ab0a6e5dcbf38a8c33b960996a55a3b4300b36a018c4545801de3a3c8bde0`.
- B description_control: reproduce the existing one-character description mutation, matching the preserved variant bytes.
- C label_deletion: reproduce the established deterministic ZIP label rewrite, removing the final line of `labels_without_background.txt` (1000 → 999). Require equality to the frozen deletion artifact.
- D label_restoration: put the saved original label bytes back into C using the same deterministic ZIP writer. Require original graph, metadata and all associated payloads; whole-file equality is not assumed because ZIP container fields may differ from the original publisher archive.

## Fixed consumer and inputs

Generator: official tflite-support 0.4.4. Runtime: TensorFlow Lite Java/native 2.13.0; Support/Support API/metadata 0.4.4. Existing JDK 17.0.12+7, Java 8 target. Android SDK platform 30 revision 3, build-tools 35.0.0, platform-tools 37.0.1; Android 30 default x86_64 image revision 11. Emulator stable 37.2.12 (build 16428233), software CPU (`-accel off`). Downloads must be preserved and checked against official repository checksums, with SHA-256 additionally recorded. No Android Studio claim.

An ordinary `android.app.Instrumentation` harness, in the generated class's package, will call:

```java
ContractModel m = ContractModel.newInstance(context, "model.tflite",
    new Model.Options.Builder().setDevice(Model.Device.CPU).setNumThreads(1).build());
ContractModel.Outputs out = m.process(image);
// Observe a duplicate of out.getBuffer().get(0); do not modify it.
List<Category> categories = out.getProbabilityAsCategoryList();
```

Two inputs are fixed now, before E1 output inspection: (1) a 224×224 ARGB_8888 bitmap with RGB=(127,127,127) everywhere; (2) a 224×224 bitmap whose RGB byte stream is `(37*i+17) mod 256`, i increasing in row-major RGB order. Both use the generated default image preprocessing. They are not accuracy tests. Inference stage includes the generated preprocessing performed inside `process`; any failure there must be localized from its stack, not asserted to be the interpreter without evidence.

## Exact intended orchestration commands

Working directory: `/workspace/metadata-contract-e2e-20261004T030536Z`.

```bash
PYTHONDONTWRITEBYTECODE=1 /workspace/hand-contract-repro/.venv/bin/python scripts/prepare_e1.py
python scripts/setup_android.py
python scripts/start_emulator.py
PYTHONDONTWRITEBYTECODE=1 /workspace/hand-contract-repro/.venv/bin/python scripts/build_android.py --experiment E1
python scripts/run_android.py --experiment E1 --run primary
python scripts/run_android.py --experiment E1 --run replay
```

Build uses javac, D8, aapt2, zipalign and apksigner directly with pinned dependencies, avoiding the generated obsolete/nightly Gradle configuration. Each actual subprocess argument vector, stdout/stderr and return code will be retained. The final installation/execution commands are:

```bash
sdk/platform-tools/adb -s emulator-5554 install -r E1/variants/<variant>/build/consumer.apk
sdk/platform-tools/adb -s emulator-5554 shell am instrument -w -e variant <variant> org.example.contract.consumer/org.example.contract.ContractInstrumentation
```

The command list is intended, not evidence of execution. Missing prerequisites will be recorded before any dependent command. No repair or editing of generated Java is allowed.

## Required preservation comparisons

For each variant against A: exact canonical graph; every non-metadata buffer; shapes, tensor indices and quantization; embedded metadata bytes (C and D must be identical); original TFLite prefix before appended ZIP (C/D); associated filename and other payloads; generated Java byte equality; all generated class hashes; DEX code equality when deterministic. Compare actual raw output byte arrays for each identical input and category scores, not APK hashes. Observe actual output buffers before calling the actual getter. Save all returned categories or exact exception and stack trace.

## Stage record and interpretation

Record structural population, generation, javac, DEX/package build, install, model loading, input preparation, process/inference, output-buffer observation, generated getter/decoding, cleanup. Keep NOT_REACHED distinct from FAIL. Record first failing stage and diagnostic. Structural population acts on a separate in-memory buffer; it must not replace the experimental model bytes.

If A fails, report the actual failure; do not mutate the generated implementation to obtain success. If C fails before the getter, attribute only that observed stage. If C reaches the getter and fails while A/B/D succeed, this establishes reachability for this generated Android interface and toolchain, not deployed application impact or prevalence. If all succeed, preserve that negative result. Failure of graph preservation aborts the corresponding unit.

Primary and replay execution use separate output directories. A replay reuses the pinned APK/toolchain on the same operator/environment; it is not independent human replication. E2/E3 depend on a reproducible working baseline.
