# E3 results

The official Task classifier rejects the deletion during initialization. The generated Android interface reaches its getter before rejecting the same model bytes. The permutation succeeds in both configurations with changed label associations.

| Variant | Configured consumer | S baseline | Generate | Compile/package | Initialize | Inference | Decode | Earliest failure |
|---|---|---|---|---|---|---|---|---|
| original | Task Library 0.4.4 Python/C++ on Linux | PASS | NOT_APPLICABLE | PREBUILT_WHEEL/PREBUILT_WHEEL | PASS | PASS | PASS | — |
| original | Support 0.4.4 generated Java / Android API 30 / TFLite 2.13.0 | PASS | PASS | PASS/PASS | PASS | PASS | PASS | — |
| description_control | Task Library 0.4.4 Python/C++ on Linux | PASS | NOT_APPLICABLE | PREBUILT_WHEEL/PREBUILT_WHEEL | PASS | PASS | PASS | — |
| description_control | Support 0.4.4 generated Java / Android API 30 / TFLite 2.13.0 | PASS | PASS | PASS/PASS | PASS | PASS | PASS | — |
| label_deletion | Task Library 0.4.4 Python/C++ on Linux | PASS | NOT_APPLICABLE | PREBUILT_WHEEL/PREBUILT_WHEEL | FAIL | NOT_REACHED | NOT_REACHED | task_initialization |
| label_deletion | Support 0.4.4 generated Java / Android API 30 / TFLite 2.13.0 | PASS | PASS | PASS/PASS | PASS | PASS | FAIL | generated_getter |
| label_permutation | Task Library 0.4.4 Python/C++ on Linux | PASS | NOT_APPLICABLE | PREBUILT_WHEEL/PREBUILT_WHEEL | PASS | PASS | PASS | — |
| label_permutation | Support 0.4.4 generated Java / Android API 30 / TFLite 2.13.0 | PASS | PASS | PASS/PASS | PASS | PASS | PASS | — |

Exact Task initialization diagnostic: `ValueError: Got 1000 class(es) for output index 0, expected 999 according to the label map.` Inference and decoding were not reached for that unit. The Android diagnostic remains `IllegalArgumentException: Label number 999 mismatch the shape on axis 1` at the actual generated getter.

Original, description and permutation Task paths returned all 1000 categories on both inputs. Per-index score bits agree with the Task original; the permutation changes 999 label strings. Primary and same-environment Task replay agree. Returned Task category scores are not raw interpreter tensors. No cross-platform raw-tensor equality is claimed.

## Implementation and compatibility evidence

Official v0.4.4 image_classifier.h documents RGB batch-one UINT8/FLOAT32 inputs, required float normalization metadata, and [1,N] or [1,1,1,N] output heads. Exact original inspection satisfies these requirements (compatibility.json). The archived native binary is identified by SHA-256 in implementation.json; its separate embedded interpreter version is not established and is not assumed to equal Android 2.13.0.

The Python binding calls the C++ ImageClassifier::CreateFromOptions (_pywrap_image_classifier.cc). The matching release implementation calls CheckAndSetOutputs during Init, including label-map cardinality validation (image_classifier.cc). This is not the Java TensorLabel implementation. Both share TensorFlow Lite foundations and metadata schemas; the command-line generator and its Android wrapper are one generation path, not two independent implementations. The additional classification_postprocessor.cc source is related but is not asserted to be this Python binding’s called implementation.

## Boundaries and deviations

Android entries reuse sealed E1/E2 records; Task entries are fresh Linux executions. Platform and consumer both differ, so this is a comparison of these configured paths, not a controlled platform-effect study. The optional Android Studio / Gradle binding frontend was not evaluated; no universal support claim follows. Source discovery retained a 404 for an initial classification_head.cc candidate. API inspection corrected the planned factory spelling to create_from_array before any Task execution. No model was adapted after a failure.

No independent class-order semantic reference is supplied by a second consumer reading the same labels. Structural acceptance, initialization requirements, decoder compatibility and semantic correctness remain separate.
