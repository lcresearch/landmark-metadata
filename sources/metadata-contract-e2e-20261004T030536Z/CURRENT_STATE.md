# Current state before E1

Fresh byte/hash/array audit of recovered evidence; no new generation, compilation, inference, or decoder execution in phase 0.

All 691 entries of the existing workspace evidence manifest match. Read-only artifact inventory: 930 files. No old evidence was modified.

## Starting files and exact hashes

- `/workspace/metadata-contract-paper/manuscript/paper.tex` — SHA-256 `16385b61700ff2b89a9f1dfe40bd6a44b19e8b30db48b777f6c361d787b6b06c`
- `/workspace/metadata-contract-paper/manuscript/paper.pdf` — SHA-256 `42bfe3416425d534885ed9252bae55e1858ad7b2c83d58205a03d61ac92a639b`
- `/workspace/metadata-contract-paper/WORKSPACE-EVIDENCE-MANIFEST.json` — SHA-256 `bcb5766c5bc9bc0549709eb1da148d66ee285049c1e1e924f5edc5f75104d1c9`
- `/workspace/metadata-contract-paper/results/summary.json` — SHA-256 `df0e94b36061b38dca078e54ed53abf82fb0d867a87c6a023340f6fb35bcfa8c`
- `/workspace/metadata-contract-paper/scripts/suite_static.py` — SHA-256 `e0e3e023bdf01e1294626c85f61ae2ed340be67421670118b5bccb46d2648970`
- `/workspace/metadata-contract-paper/scripts/codegen_one.py` — SHA-256 `e4a2ef490591691ec6518c2d957fe7511cc3b89562574497cdd8fa82c6c7252e`
- `/workspace/metadata-contract-paper/scripts/suite_compile.py` — SHA-256 `4f55e37cda7f512cece13d98edc0f80b97883d08d3ad305eafebc106d4bcc286`
- `/workspace/metadata-contract-paper/scripts/DecoderProbe.java` — SHA-256 `97337d45c866a22461bc6857a48661147d5dba013488e84f4d09490a73f14604`
- `/workspace/hand-contract-evidence.zip` — SHA-256 `0ddb27f56496dbdc6ed0bb6d6922717ef26bfeb35ce537b0c3014e42c8f8afa1`
- `/workspace/metadata-contract-paper-sources.zip` — SHA-256 `776c3c800f0ec1feae7b41049f11f416e0e99dcea482cbfc998af1b34589fd31`

## Recovered evidence, freshly checked bytes

```json
{
  "metadata_components": 11,
  "metadata_graph_groups": 10,
  "variants": 46,
  "count_reductions_rejected": 11,
  "accepted_variants": 35,
  "recovered_cpu_invocations": 105,
  "isolated_decoder_probes": 23,
  "unmodified_original_compile_success_ids": [
    "62a87ded76da",
    "6c7ab0a6e5dc",
    "ff36e24d4054"
  ]
}
```

For EfficientNet and Gesture, original/description/deletion sources, compiled classes and saved output arrays match byte-for-byte. Canonical graphs and non-metadata buffers match. Saved JVM decoder logs/records show original and description success, deletion failure. Exact model, metadata, label, source, class and output hashes and paths: `phase0/results.json`. Full artifact/script inventory: `phase0/inventory.json`.

| EfficientNet variant | Model SHA-256 |
|---|---|
| original | `6c7ab0a6e5dcbf38a8c33b960996a55a3b4300b36a018c4545801de3a3c8bde0` |
| description_control | `ed16d9573d8fe3e489c27637036a4e5c8476d15f013b7116f89864d55432f51d` |
| count_minus_one | `510da3d77d2d11124a6a8eb91ec7699bdee5f9f3851d2120c5f57c21ca06b4c2` |
| label_drop_1 | `739f08462e831806db6a9bce7ed5b70a037fce593003028e5d6911dbd284fd83` |

Canonical graph SHA-256: `73e57df01115600419abb72de4b2c3257200e12eb205d335bcbfc203a589bee8`.

## Versions

Python 3.11.16 (main, Sep 24 2026, 17:56:40) [Clang 22.1.3 ]

openjdk version "17.0.12" 2024-07-16
OpenJDK Runtime Environment Temurin-17.0.12+7 (build 17.0.12+7)
OpenJDK 64-Bit Server VM Temurin-17.0.12+7 (build 17.0.12+7, mixed mode, sharing)

```json
{
  "tflite-support": "0.4.4",
  "tflite-runtime": "2.14.0",
  "numpy": "1.26.4",
  "flatbuffers": "25.12.19",
  "protobuf": "3.20.3"
}
```

Java libraries: tensorflow-lite and tensorflow-lite-api 2.13.0; support, support-api and metadata 0.4.4; flatbuffers-java 2.0.0; android stubs 4.1.1.4; androidx.annotation 1.3.0. Their absolute paths and SHA-256 values are in phase0/results.json. Compilation used JDK 17.0.12+7 with --release 8.

## Exact generated API

`/workspace/metadata-contract-paper/runs/6c7ab0a6e5dc/original/generated/src/main/java/org/example/contract/ContractModel.java`:

```java
ContractModel m = ContractModel.newInstance(context, "model.tflite", options);
ContractModel.Outputs out = m.process(tensorImage);
List<Category> categories = out.getProbabilityAsCategoryList();
```

Metadata construction loads labels through MetadataExtractor and FileUtil. The getter executes the actual TensorLabel path. The package-private Outputs.getBuffer() can expose a duplicate raw output buffer for observation without replacing the public getter.

## Not yet verified / missing prerequisites

- No fresh generation, compilation, inference or decoder execution in phase 0. Hash and saved-array checks do not make historical runs new experiments.
- No Android SDK/emulator/native AARs/APK harness existed at the start; /dev/kvm is absent. Software emulation is an unverified prerequisite.
- The generated Gradle project has historical experimental/nightly dependencies. E1 proposes a pinned APK harness with byte-unmodified generated Java, not an unchanged generated Gradle project.
- Hand records and official graph source are preserved and hash-verified, including disclosed syntax repair; an exact source-release-to-artifact linkage remains to be scrutinized.
- No independently supplied EfficientNet class-order reference has been tied to the exact artifact. Original labels are a baseline, not semantic truth.
- R15–R17 historical files and 41-agent review are unavailable; human verification remains pending.
- No prevalence, general detector accuracy, task accuracy, Android application/user impact, or current Android Studio result is established.
- First phase-0 audit-script attempt stopped on absent-metadata entries having no original compile row; the audit script was corrected to handle this abstention. Both logs remain. No experimental result was changed.
