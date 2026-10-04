# Audit starting point and provenance

Source evidence (read-only): `/workspace/metadata-contract-e2e-20261004T030536Z`.
Recovered model/helper inputs (read-only): `/workspace/metadata-contract-paper/runs/6c7ab0a6e5dc` and `/workspace/metadata-contract-paper/scripts`.
Installed Python/JDK/Java library inputs (read-only): `/workspace/hand-contract-repro`.

The exact original EfficientNet component is SHA-256 `6c7ab0a6e5dcbf38a8c33b960996a55a3b4300b36a018c4545801de3a3c8bde0`. This audit regenerates the original description edit, one-label deletion, label-payload restoration, previously declared cyclic permutation, and its inverse using the preserved procedures. `INPUT_PROVENANCE.json` pins the copied orchestration scripts; `source-snapshots/` and root patches preserve the local audit changes.

Fresh versus recovered: model/source helper inputs and installed SDK/JDK/Python are recovered; new generated Java, compiled classes, new APKs, new AVD, runtime asset hashes, two input observations per phase/variant record and independent summary computations are fresh. Historical primary output files are only read for comparison. No fresh human verification or SDK archive reinstall is claimed.

Exact installed version commands and output: `versions/`; source and dependency hashes: `versions/files.json`, `versions/native-and-java-dependencies.json`, and each `E1|E2/build-results.json`. Generator: tflite-support 0.4.4; Java/native runtime: TensorFlow Lite 2.13.0; Support API/metadata 0.4.4; Temurin JDK 17.0.12+7, javac --release 8; Android API 30 x86_64 with CPU one thread. The copied SDK's internal system-image properties report revision 10; the historical archive provenance records `x86_64-30_r11.zip`. This audit does not normalize that discrepancy.

Final fresh evidence is reported in `results.json` and `AUDIT_REPORT.md` after execution. Independent class-order reference, human audit, supported untouched generated Gradle project build, SDK-from-archive installation, prediction correctness and generalization remain unverified by this audit.
