# E3 — configured official consumers and rejection stages

E1 and E2 primary/replay evidence is complete and sealed before this experiment. No Gesture repetition is needed to establish the already observed mechanism.

Use exact original, description, deletion and permutation model bytes from E1/E2. Compare the official Support 0.4.4 generator/structural path and the already executed generated Android interface against official Task Library Python ImageClassifier in the archived tflite-support 0.4.4 CPython-3.11 Linux wheel. The Task API is a different configured consumer on a different platform, not a platform-controlled timing experiment. Do not claim all implementations are independent: inspect the Python binding and corresponding C++ validation/decoder source; both ecosystems share metadata schemas and TensorFlow Lite foundations.

The Android Studio / Gradle ML Model Binding frontend has no prepared, pinned project or IDE configuration in this workspace. It is not evaluated in this bounded comparison. This is an omission, not proof that a model is unsupported by that frontend or that it could not be configured.

Before running Task inference, preserve official release header/documentation specifying ImageClassifier compatibility and match the original artifact's input/output types, shapes, RGB metadata and normalization options to those requirements. If the original does not qualify or fails initialization, retain the negative result and do not adapt the model to get success.

For Task Library, call its actual `ImageClassifier.create_from_options` with BaseOptions(file_name=exact_variant, num_threads=1, use_coral=False) and ClassificationOptions(max_results=-1). Call `classify` on Task TensorImage.create_from_array using the exact RGB bytes saved by E1. The factory name was checked against installed source before execution. Do not implement a substitute decoder. Record initialization separately from classify. Classify combines inference and postprocessing; a classify failure without additional evidence cannot be localized to one of those internal stages. Initialization rejection is NOT_REACHED for inference/decoding.

Save every category with index, label and score bits, raw stdout/stderr, full exception trace, exact wheel/native-library hashes, source files, parameters and source diagnostics. No raw Task interpreter tensor is exposed by this public API; returned category scores are decoded results and will not be mislabeled raw tensors. Compare per-index returned scores/labels within this Task configuration across variants, not presumed bitwise equivalence across Linux and Android runtimes.

Use the existing E1/E2 records for the generated Android consumer and generator stages; do not add redundant Android inference calls. These entries are explicitly reused results, while Task entries are fresh executions. Run the four Task units once and repeat the set in a separate directory for reproducibility. Exact entry commands:

```bash
PYTHONDONTWRITEBYTECODE=1 /workspace/hand-contract-repro/.venv/bin/python scripts/task_consumer.py --run primary
PYTHONDONTWRITEBYTECODE=1 /workspace/hand-contract-repro/.venv/bin/python scripts/task_consumer.py --run replay
python scripts/summarize_e3.py
```

The expected rejection stage is not assumed. A consumer-specific acceptance/rejection outcome never establishes universal model validity. No independent EfficientNet class-order semantic reference is introduced by another consumer reading the same labels.
