# E1/E2 getter, harness, and deployed bytecode audit

**Conclusion:** The inspected artifacts support the actual generated API call chain, actual Support-library decoding, non-mutating raw observation, and a caught getter-time label-cardinality exception after successful inference. The Java source, four application class files, and DEX are byte-identical across all eight E1/E2 variant builds. Each APK contains that same DEX. No core execution-claim contradiction was found. **The archived logcat dumps are cumulative and must not be attributed wholesale to the variant directory containing them.**

This is an AI-assisted read-only audit of saved artifacts and logs, not human audit or an independent execution. No emulator, inference, model editing, recompilation, or dependency installation was performed. All new files were written only under this report's directory. The evidence root is `/workspace/metadata-contract-e2e-20261004T030536Z`. The obsolete `build-before-dependency-closure` trees were excluded. The existing JDK executable under `/workspace/hand-contract-repro/toolchains/jdk-17.0.12+7/bin/javap` was used as a tool; no evidence from that older workspace was substituted for this evidence root.

## Evidence and reproducible commands

- `audit.py` recomputes artifact hashes, opens the eight APKs as ZIP files, runs fresh `javap -c -p -l` on the four class files, runs the saved SDK's `dexdump -d -f -h` on the DEX, and reads the 16 saved device result files and their six associated log/command files. Invoke with `python /workspace/metadata-contract-audit-20261004T062010Z/preservation/bytecode/audit.py`.
- `commands.json` records the exact disassembler arguments and exit codes. `javap-version.stdout` records version `17.0.12`. All disassembler commands exited 0.
- `input-manifest.json` records exact paths, byte counts, and freshly computed SHA-256 values of all audited source, class, DEX, APK, device result and log inputs.
- `results.json` contains the eight-build hash matrix, the APK DEX matches, per-execution stages, full exception stacks, and logcat attribution intervals.
- `javap-ContractInstrumentation.stdout`, `javap-ContractModel.stdout`, `javap-ContractModel-Metadata.stdout`, and `javap-ContractModel-Outputs.stdout` are fresh class disassemblies.
- `dexdump-full.stdout` is the complete fresh DEX disassembly. `dexdump-selected.txt` extracts the four application classes plus actual bundled `TensorLabel`, `FileUtil`, `Model`, and `DequantizeOp`. Additional exact library extracts are `dexdump-TensorBuffer.txt`, `dexdump-Category.txt`, and `dexdump-MetadataExtractor.txt`.

The eight builds are E1 original/description_control/label_deletion/label_restoration and E2 original/description_control/label_permutation/permutation_restoration. Original and description-control conditions appearing in E1 and E2 are not additional independent models.

## Unchanged executable artifacts

The following SHA-256 values are shared by all eight current builds:

| Artifact relative to each variant | SHA-256 |
| --- | --- |
| `generated/src/main/java/org/example/contract/ContractModel.java` | `60c1fb6022891cc2bd41b5bacdd2194361eb0ca40e37da2eddf6cba963279670` |
| `build/classes/org/example/contract/ContractInstrumentation.class` | `480d9b03e2160150bc765f6cc2f142067693074254cc626bb9d734617555bf34` |
| `build/classes/org/example/contract/ContractModel.class` | `bbf74b8a5b53e2efa47986a11c99b6c52ef533c7c6f149f7032c09adc5059145` |
| `build/classes/org/example/contract/ContractModel$Metadata.class` | `6fd67e5f9d764e833d0e8441850a708676dbd3128c736ffc72234742caf33e4b` |
| `build/classes/org/example/contract/ContractModel$Outputs.class` | `947d1073a42002d3aaa070e37a498d9a65a8244c3468bf945116e6cb205fcf44` |
| `build/dex/classes.dex` and APK `classes.dex` | `82ae7e4dafaeba6a1dcc4be479693cd1eb9cfc02ff04f661e801ac0466c5ee99` |

The E1 snapshot, E2 snapshot, and `scripts/ContractInstrumentation.java` are byte-identical. This supports the same application and library bytecode across conditions; it does not establish whole-APK equality, since the bundled model assets differ. Source inspection and line-number matching support consistency with the compiled classes; a fresh reproducible-source build was outside this audit.

## Actual consumer call chain

Directly inspected source is E1 `implementation-snapshot/ContractInstrumentation.java` and `variants/original/generated/src/main/java/org/example/contract/ContractModel.java`. Identical-source hashes transfer these observations to the other seven builds; bytecode and APK DEX were independently checked.

1. Harness lines 52–53 call `ContractModel.newInstance(context, "model.tflite", CPU/one-thread options)`. Fresh class bytecode invokes this static method at offset 119; DEX invokes it at method-local offset `0x006f` in `ContractInstrumentation.onStart`.
2. Generated `newInstance` lines 176–184 call `Model.createModel`, construct `Metadata` from `model.getData()`, and install the generated default preprocessor and postprocessor. The actual bundled `Model.run` DEX calls `InterpreterApi.runForMultipleInputsOutputs`.
3. Harness line 69 calls `model.process(input)`. Generated `process` lines 197–201 allocate `Outputs`, preprocess the input, and call `model.run(inputBuffers, outputs.getBuffer())` before returning. Class offset 552 and DEX offset `0x017c` in `onStart` invoke the generated process method. `inference_status=PASS` is written only after that return.
4. Harness line 81 calls `output.getProbabilityAsCategoryList()`. Class offset 876 and DEX offset `0x026c` invoke the actual generated getter. The getter's own class/DEX constructs `TensorLabel(probabilityLabels, postprocessProbability(probability))` and calls `TensorLabel.getCategoryList()`. This is not a hand-written replacement decoder.
5. Harness lines 82–85 serialize the returned `Category` objects. The separate raw-score top-five computation operates on a copied byte array and is observational; it does not supply categories or labels to the generated getter.

## Associated labels and actual decoder

Generated `Metadata` lines 97–99 obtain `getOutputTensorMetadata(0).associatedFiles(0).name()`, open that name with `MetadataExtractor.getAssociatedFile`, and pass its stream to `FileUtil.loadLabels`. This exact sequence appears in fresh class bytecode (offsets 181–200) and DEX. It does not load an independent hard-coded label mapping from the harness.

The bundled `MetadataExtractor.getAssociatedFile` DEX asserts that a ZIP is available, obtains its `zipFile` field, and calls `ZipFile.getRawInputStream(name)`. The bundled `FileUtil.loadLabels(InputStream, Charset)` reads lines in order, skips lines whose trimmed length is zero, and appends each retained original line. There is no class-order oracle here.

The actual `TensorLabel` constructor in the APK compares the size of each axis-label list against the corresponding tensor shape dimension and calls `SupportPreconditions.checkArgument`, constructing `Label number <count> mismatch the shape on axis <axis>`. The list constructor delegates to this constructor. `getCategoryList` subsequently obtains the tensor float array and constructs `Category(label, score)` in label-list order. This constructor sets the category index to `-1` (confirmed in `dexdump-Category.txt`), so a raw/list position such as 904 must not be called `Category.getIndex()`.

## Raw observation does not mutate the inference output

This conclusion includes the getters before `.duplicate()`:

- Generated `Outputs.getBuffer()` creates a new `HashMap`, retrieves `probability.getBuffer()`, inserts that object at key 0, and returns the map. Its class and DEX contain no buffer-position or data write.
- The exact bundled `TensorBuffer.getBuffer()` DEX consists solely of `iget-object ... buffer` followed by `return-object` (`dexdump-TensorBuffer.txt`, method-local offsets `0x0000` and `0x0002`, original source line 157). It does **not** rewind, clear, or otherwise alter the buffer position.
- Harness line 72 calls `.duplicate().order(ByteOrder.nativeOrder())`. Lines 73–75 rewind and read the duplicate into a newly allocated byte array, then read that copy into a newly allocated float array. Bytecode confirms `duplicate`, `order`, `rewind`, `remaining`, and `get(byte[])`; the harness has no `ByteBuffer.put` call.
- A duplicate shares the backing bytes but has independent position/limit/mark. It is not made intrinsically read-only with `asReadOnlyBuffer`; the supported conclusion is that these operations perform no backing-data writes and no original-buffer position changes. The generated decoder receives the original `TensorBuffer`, not the observation copy.

## Saved execution records and failure attribution

All 16 saved `device/result.json` files report model-loading PASS. Each contains both `gray127` and `rgb_pattern` observations with input preparation, inference, and raw-output observation PASS; each raw result is 4000 bytes. Twelve control/restoration/original execution records plus the two permutation records report generated-getter PASS and 1000 categories. The two deletion records report 999 loaded labels and generated-getter FAIL for both inputs.

The exception in all four deletion observations is:

```text
java.lang.IllegalArgumentException: Label number 999 mismatch the shape on axis 1
  at ...SupportPreconditions.checkArgument(SupportPreconditions.java:104)
  at ...TensorLabel.<init>(TensorLabel.java:86)
  at ...TensorLabel.<init>(TensorLabel.java:104)
  at org.example.contract.ContractModel$Outputs.getProbabilityAsCategoryList(ContractModel.java:47)
  at org.example.contract.ContractInstrumentation.onStart(ContractInstrumentation.java:81)
```

The same stacks appear in time-correlated logcat entries:

| Saved execution | Instrument start → logcat dump start | Exception timestamps | PID / TID |
| --- | --- | --- | --- |
| E1 primary deletion | `03:26:48.318` → `03:27:46.364` | `03:27:19.945`, `03:27:44.585` | `2995 / 3015` |
| E1 replay deletion | `03:31:45.160` → `03:32:40.162` | `03:32:14.237`, `03:32:38.390` | `3239 / 3260` |

All timestamps are on the archived run date, October 4. The two stacks in each interval share the current process/thread IDs. The other 14 execution intervals contain zero matching label-cardinality exceptions. Intervals were derived from the saved instrumentation and logcat command timestamps, not from summary claims; their calculation and retained lines are in `results.json`.

**Cumulative logcat caveat:** Successful E1 restoration and subsequent E2 dumps contain old deletion exceptions. Counts across entire log files grow from two to four because the dumps retain earlier runs. They are not evidence that the successful conditions threw these exceptions. The saved device JSON and method control flow support success stages; logcat does not independently print every successful stage. Timestamp correlation assumes the recorded host/device clocks are comparable and is not a cryptographic run attestation.

Harness line 86 catches `Throwable`, records the stage and complete stack, logs the error, and continues to the next input. The class exception table covers the getter in this catch region. It closes the model and invokes `finish(0, bundle)` in the outer `finally`. All saved instrumentation commands exit 0 and print `INSTRUMENTATION_CODE: 0`; that code alone is not a success oracle because caught getter failures deliberately finish with it. The correct claim is a **caught generated-getter exception after inference**, not an application crash. No `FATAL EXCEPTION` appears in the inspected filtered logcat dumps; those dumps are not a complete device log.

## Limits and handoff

- No new Android execution, independent reproduction, human sign-off, current-device state check, or original publisher authenticity check was performed.
- This audit establishes consistency of saved source, class/DEX behavior, saved device reports, and time-attributed log entries. It does not independently attest which exact APK was installed at historical execution time; installation/asset preservation belongs to the parent audit.
- Graph, weight, metadata-table, ZIP-payload, raw-score equality, and decoded-label permutation comparisons are owned by the parent preservation audit. This report does not infer those from unchanged DEX.
- A getter has postprocessing as well as label construction. The observed exception stack localizes this failure to the TensorLabel constructor; it is not a failure of numerical model execution or a returned decoded value.
- E1/E2 use the same generated code to consume changed associated resources. This evidence therefore supports resource-dependent interface behavior, not an E1/E2 change in generated-code text.
- The saved replay-recovery directory supplies E2 permutation-restoration replay; it is explicitly retained under that name in the results. The initial `E2/executions/replay/permutation_restoration` directory contains only install logs and has no `device/result.json`; its runtime result is **UNCLASSIFIED / UNVERIFIABLE**, not a getter pass or failure. The 16 complete records counted here are phase/run/variant records including repeats and recovery, not 16 independent experimental units. None of these repetitions creates a new independent model or consumer.
