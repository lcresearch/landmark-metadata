# P2 consumer mechanism review

Status: **PASS for the inspected static relationships**. This review executed no
Android tests or model inference. Runtime outcomes belong to the separate P2
execution records. The source and dependency observations below were made fresh;
historical generated source was used only for an explicit byte comparison.

## Result that changes the attribution

The Android Task path in the inspected `v0.4.4` source is
`vision::ImageClassifier::CreateFromOptions → Init → CheckAndSetOutputs`.
Its output/label cardinality rejection must not automatically be attributed to
`ClassificationPostprocessor::Init`. Both implementations exist in this release
and contain similar diagnostics, but the Android JNI file names the former
`vision::ImageClassifier` explicitly.

The actual Maven Java bytecode also exposes an exception-wrapping boundary:
`TaskJniUtils.createHandleFromLibrary` catches `RuntimeException` and throws an
`IllegalStateException` with the original exception as its cause. A report should
therefore retain both the public exception and the native/JNI cause rather than
rename the public failure as only `IllegalArgumentException`.

## Exact inspected versions and identities

Source tag `tensorflow/tflite-support v0.4.4` resolved to commit
`133228616ca14e1b64c03f6a0ea8610f41a60783` through the preserved GitHub commit and
tree responses. Source URLs use this commit, not a mutable branch. Collection
records retain one absent exploratory path (`vision/utils/label_map_utils.cc`);
the actual parser is `vision/core/label_map_item.cc`.

| Actual Java/native input | SHA-256 |
|---|---|
| Task Vision 0.4.4 `classes.jar` | `922e51623a3e5a4e5f21e372d44de392d5c82d9dd8a8ea195d9f7d348ac005de` |
| Task Base 0.4.4 `classes.jar` | `bfd29de8d3e85c87e7b15287eeca42103f1a940680e3a8d4716221228952acf8` |
| Support API 0.4.4 `classes.jar`, identical to the wrapper's Support API jar | `15d59ab34528d75908306432715e522a278f781ba6f4802d6b41917a5838a59d` |
| Task Vision x86_64 `libtask_vision_jni.so` | `3d30020f2352e0144c5fb87c2740dcab95548d81786b3c8d8db9435ed7347fe3` |

`binary-provenance.json` contains absolute paths and executed commands.
`source-provenance.json` contains every source URL, path, and SHA-256.
`line-anchors.json` provides 30 freshly checked function/statement anchors.
The complete classpaths and native selections are recorded in
`../../P2/dependencies/resolved-lock.json`.

The native artifact exports the expected ImageClassifier JNI entry points and
contains both the initialization diagnostic and cardinality diagnostic. This
supports consistency with the reviewed implementation. It is not a reproducible
native rebuild or proof that the entire Maven native binary is equivalent to the
tagged source. The Task library's embedded TensorFlow Lite implementation version
is not established just because the Java compile classpath includes Lite API
2.13.0. The wrapper separately uses Lite 2.13.0 JNI. Do not describe these runtime
integrations as identical.

## Generated wrapper path

All five freshly generated `ContractModel.java` files are byte-identical, and the
fresh original also equals the historical original source. The focal source
relationships are:

1. `Metadata` reads graph output 0's shape/type/quantization (lines 93–96), then
   selects `getOutputTensorMetadata(0).associatedFiles(0).name()` and loads that
   associated resource with `FileUtil.loadLabels` (98–99).
2. `Outputs` creates the output buffer from that recorded shape/type and obtains
   the label list (50–53). Its buffer map binds the probability buffer to graph
   output position 0 (58).
3. `process(TensorImage)` prepares inputs, calls `model.run`, and returns the
   `Outputs` object (197–201). It does not call the category getter.
4. The actual public `getProbabilityAsCategoryList` (46–47) applies the configured
   postprocessor and then executes
   `new TensorLabel(probabilityLabels, postprocessProbability(probability)).getCategoryList()`.
   The default postprocessor is a `DequantizeOp` built from the output's
   quantization parameters (228–232). The contract is about the buffer after this
   selected processor, not an arbitrary assumption that all processors preserve
   shape.

The actual Support API jar was disassembled with JDK 17.0.12+7 `javap -c -p`.
The list overload of `TensorLabel` selects the **first axis with size greater
than 1**, constructs an axis map, and checks the supplied label count against
that selected dimension. The exact constructor diagnostic includes
`Label number ... mismatch the shape on axis ...`. `getCategoryList` additionally
requires the selected axis to equal `rank - 1` and the label count to equal the
float array length. These are separate constructor and conversion conditions;
the strict last-axis equality comes from implementation, even though the Javadoc
uses the phrase “effectively the last axis.” A shape with no axis larger than 1
is rejected by this constructor path.

For the focal `[1,1000]` output and shape-preserving default path, the selected
axis is 1. A 999-entry list violates the constructor count condition. This is a
static explanation; the actual exception stage must still be taken from the P2
harness record, not assumed from this review.

## Android Task creation and classification

The inspected Java bytecode and pinned source agree on this public path:

`ImageClassifier.createFromFileAndOptions(context, assetName, options)`
→ `TaskJniUtils.createHandleFromFdAndOptions`
→ `AssetManager.openFd`
→ load `task_vision_jni`
→ `ImageClassifier$1.createHandle`
→ `initJniWithModelFdAndOptions`.

In the pinned source, JNI passes the file descriptor, length, offset and options
to `vision::ImageClassifier::CreateFromOptions`. Creation constructs the engine
and invokes `Init`; `Init` calls `CheckAndSetInputs` and `CheckAndSetOutputs`.
`CheckAndSetOutputs` builds a classification head from each output's metadata,
validates supported output rank/batch/spatial dimensions, determines the number
of classes from the last dimension, and compares this with the label map length.
The relevant count branch is `image_classifier.cc:253`; its diagnostic at 256 is:

> Got %d class(es) for output index %d, expected %d according to the label map.

The status is `kInvalidArgument` with the metadata-inconsistency support code.
JNI maps invalid argument to Java `IllegalArgumentException`, prefixes
`Error occurred when initializing ImageClassifier:`, and the inspected Java
`TaskJniUtils` wrapper can expose that as an `IllegalStateException` cause chain.

Resource selection differs in general from the generated code. Task
`BuildClassificationHead` chooses the first associated file whose type is
`TENSOR_AXIS_LABELS`; it separately selects a matching locale for optional display
names. An empty locale argument does not require the resource's locale itself to
be empty. The parser splits on newline and removes one final empty entry. In
these focal artifacts, the sole output resource is
`labels_without_background.txt`, type `TENSOR_AXIS_LABELS`, so both routes select
the same label resource. No conclusion about all multiple-resource/locale
configurations follows from this single-resource case.

The public Task `classify(TensorImage)` calls the base vision processing route
and ultimately `classifyNative`. The pinned JNI source invokes `Classify`, then
converts the classification result to Java categories before returning. It does
not expose separate public calls for raw inference and decoder output access.
Task categories should be aligned by their class index, not their returned list
rank, when compared with generated output positions.

## Observable stages and remaining scope

| Instrumented public boundary | What an execution record can directly establish |
|---|---|
| Wrapper `newInstance` | Generated model/metadata construction returned or threw |
| Wrapper `process` | The inference-containing generated call returned or threw; raw buffer observation can separately establish recorded values |
| Wrapper generated category getter | The actual category conversion returned or threw |
| Task `createFromFileAndOptions` | Combined asset opening/model creation/initialization returned or threw; a preserved diagnostic identifies the reported internal rejection |
| Task `classify` | Combined preprocessing/inference/postprocessing/result conversion returned or threw |

Do not mark Task internal inference and decoding as independently instrumented
stages. If Task creation throws, its later classify/inference/output stages are
not reached. Merely reading and hashing the asset before creation is not proof
that native model loading completed. A successful Task classify returns decoded
output, but supplies no separately captured raw tensors through this public API.

Same emulator/API/ABI removes the earlier OS and device-environment difference.
It does not isolate a single code component: native integrations and public
interfaces still differ. The routes are not established as wholly independent
implementations; they share ecosystem components and, here, a byte-identical
Support API jar. The analysis justifies source-linked explanation of the tested
paths, not comparative safety, performance, prevalence, task accuracy, or a
general invalid-model claim.

## Reproduction of this review

Run `collect_sources.py`, `inspect_binaries.py`, and `summarize_mechanism.py`
with the preserved P2 inputs and JDK available. Network collection is needed only
to reacquire sources; source checks can use the hashed preserved snapshots.
`commands.sh` records the exact review sequence. These scripts perform static
inspection, not an Android execution. All referenced generated artifacts,
third-party binaries, raw command outputs, and source snapshots remain outside
the source-only project repository.
