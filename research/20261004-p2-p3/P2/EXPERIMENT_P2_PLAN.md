# P2: same-Android consumer-stage comparison

Frozen before model execution. One canonical EfficientNet graph, five existing byte-distinct model conditions, two real consumer configurations. The intervention models are pinned in ../INPUTS.json. No new mutations or model search.

## Question and hypotheses
Does the earlier cross-platform observation of different rejection stages persist when generated Java and the official Android Java Task ImageClassifier execute in the same Android API 30 x86_64 AVD? Deletion might be rejected at either constructor, inference, output access, or build; report the earliest actual boundary. No result is assumed.

## Consumers and unit
A: Support codegen 0.4.4 unmodified ContractModel, Java/native TFLite 2.13.0, CPU, one thread. API sequence newInstance -> process(TensorImage) -> Outputs.getProbabilityAsCategoryList().
B: official tensorflow-lite-task-vision:0.4.4 and task-base:0.4.4; createFromFileAndOptions(Context,"model.tflite", options with BaseOptions CPU default and one thread; maxResults1000) -> classify(TensorImage). Task includes its published native library; do not force another runtime into it.
Two separate APK packages prevent conflicting native/Java integration. Same fresh AVD, API30/default/x86_64, software CPU emulation. SDK/JDK reused read-only; all writable state local. The primary unit is model variant x consumer configuration: 10 units, one canonical graph. Two identical deterministic inputs repeat observations within each unit, not independent models. Deletion constructor rejection may prevent input observations.

## Conditions and controls
Original, one-character description-control, one-label deletion, fixed predeclared left cyclic label permutation, restored associated labels. Use exact saved bytes. Preserve original control and restoration; no favorable version search, generated-source repair, or replacement getter.

## Inputs and observation
Two synthetic 224x224 RGB inputs from E1/E2: gray127 and rgb_pattern byte[k]=(37*k+17) mod256. Both harnesses create identical ARGB8888 Bitmap -> TensorImage UINT8. Save RGB bytes/hash. Wrapper raw bytes read using duplicate buffer before actual generated getter; all successful getter category score bits retained. Task public classify combines inference and postprocessing: mark ATOMIC inference+decoding success/failure; never infer separate hidden stage passes. Task returns class index, score bits, label and display name. No claim of raw-tensor equality across consumers without access to native raw tensors. Cross-consumer returned scores can be compared by explicit class index, reporting exact differences.

## Preservation and identity checks
Verify source fixture SHA256, copied model, APK asset and pre-load AssetManager read. Asset probe does not intercept native interpreter buffer. Compare canonical graph, all non-metadata buffers, embedded metadata, associated filenames and bytes separately. Compare generated source and generated classes bytewise across variants. Compare per-consumer DEX across variants; never use whole APK equality as graph evidence. Input byte equality across consumers, within-consumer numeric invariance and original/restoration equality required for related interpretations.

## Stage records
Metadata read/populate; generation (wrapper only); javac; DEX/package/sign; install; pre-load asset identity; public constructor/loading+initialization; input preparation; inference (wrapper process only); actual getter (wrapper); classify atomic inference+decoding (Task); returned categories or caught throwable with full stack. Non-reached stages remain NOT_REACHED, inapplicable stages INAPPLICABLE.

## Exact commands (from this directory)
```
PYTHONDONTWRITEBYTECODE=1 /workspace/hand-contract-repro/.venv/bin/python scripts/prepare.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/build.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/start_emulator.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/run.py
PYTHONDONTWRITEBYTECODE=1 /workspace/hand-contract-repro/.venv/bin/python scripts/analyze.py
```
SDK symlinks target /workspace/metadata-contract-e2e-20261004T030536Z/sdk. JDK /workspace/hand-contract-repro/toolchains/jdk-17.0.12+7. Expanded actual commands and stdout/stderr preserved per operation in commands-executed.sh and logs. Fetches recorded by fetch_dependencies.py/downloads.json; manual classpath with explicit resolved dependencies, no Gradle implicit resolver. Reused AndroidX annotation1.3.0 satisfies provided1.1.0 compile dependency and is pinned identically; record declared and selected versions.

## Stop and interpretation
One primary pass. A supported consumer rejection is a result, not a reason to alter it. Dependency/build failure remains recorded. Same-stage outcome weakens earlier timing contrast; different stage on same OS/API/ABI supports tested-consumer-configuration contrast with remaining native/build integration differences. Initialization exception is caught by harness: no application crash claim. Permutation success establishes original-relative label association change, not semantic error absent independently tied reference. No latency/accuracy/prevalence claim. No human audit implied.
