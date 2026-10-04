# E3 manuscript impact

The paper must scope the sentence “it checks tensor-metadata cardinality but does not establish the selected semantic and decoder contracts” to the tested MetadataPopulator/codegen path. The official Task ImageClassifier already enforces the tested label-count requirement during initialization.

New justified comparison: the exact same 999-label EfficientNet artifact is accepted by the structural baseline, loads and runs through the generated Android interface, then fails its getter; the Task 0.4.4 Python/C++ classifier rejects it during initialization with a class/label-map inconsistency diagnostic. No inference or decoder call is reached in that Task unit. The original qualifies under the Task API’s documented shape/type/normalization requirements and actually succeeds.

This supports consumer-specific enforcement-stage differences. It does not establish universal model invalidity, independent implementations for every frontend, or a novel condition absent from official tools. A proposed pre-flight guard would move an already-known library precondition earlier for the selected generated-Java path. Keep the two platforms and exact consumer versions explicit. The optional Android Studio binding frontend remains unevaluated.
