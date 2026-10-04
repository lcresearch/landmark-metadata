# P1-A results: existing checks and the simple baseline

**The five core artifact conditions show no detection increment for E5 over either the simple selected-decoder baseline or official Task initialization.** All three identify the injected 999-label deletion, and all three accept the modeled preconditions of the other four conditions. E5 provides a static, generated-path-specific diagnostic; the condition itself already exists in the library and Task consumer.

This is a fresh AI-agent execution audit on the existing environment, not an independent human audit, independent clean build, or Android replay. No emulator was launched, and no Task `classify` call was made. Prior evidence files were read only.

## Fixed inputs and outcomes

The eight E1/E2 phase aliases deduplicate to five complete file hashes. E1 label restoration and E2 inverse-permutation restoration are one byte-identical artifact; the two original aliases and two description aliases also coincide. `inputs.json` retains all aliases and full digests. The restored artifact differs from the publisher original in container bytes, so it remains a separate file condition.

| Core condition | Output metadata entries / graph outputs | Label strings | Displayer | Populator | Simple decoder baseline | Existing E5 D | Task initialization |
|---|---:|---:|---|---|---|---|---|
| Original | 1 / 1 | 1,000 | readable | accepted | compatible | compatible | pass |
| Description control | 1 / 1 | 1,000 | readable | accepted | compatible | compatible | pass |
| Final-label deletion | 1 / 1 | 999 | readable | accepted | incompatible | incompatible | fail |
| Cyclic permutation | 1 / 1 | 1,000 | readable | accepted | compatible | compatible | pass |
| Label restoration | 1 / 1 | 1,000 | readable | accepted | compatible | compatible | pass |

Here “compatible” means only the stated static decoder preconditions. Display success means JSON/resource readability. Task pass means successful initialization, not inference or prediction correctness. All E5 reference judgments abstain because this audit supplies no independent class-order reference.

The simple baseline selects the single graph output and its unique TENSOR_AXIS_LABELS resource, then checks positive static shape/signature, the first axis greater than one, label count on that axis, the exact last-axis requirement, and flattened cardinality. It does not infer an arbitrary getter binding. For each of these five artifacts, its selected output 0, metadata position 0, associated-file position 0 and `labels_without_background.txt` are independently compared with the actual bindings extracted by unchanged E5; they agree. E5-generated source bytes also agree across all five audit runs. This comparison is limited to the selected core classifier path.

The deletion's Task exception is `ValueError: Got 1000 class(es) for output index 0, expected 999 according to the label map.` It arises in initialization; classification is not reached. The simple baseline and E5 detect the same mismatch without constructing a Task classifier. E5's actual message names `getProbabilityAsCategoryList`, output 0, axis 1, size 1,000 and 999 labels.

## Separate structural negative control

The pre-existing EfficientNet `count_minus_one` fixture has one graph output and zero output-metadata entries. Its original label archive remains readable and contains the unchanged 1,000-label payload. Displayer reads it successfully, but MetadataPopulator rejects it at `load_metadata_buffer` / `_validate_metadata` with `The number of output tensors (1) should match the number of output tensor metadata (0)`. The raw result records the broader “populator” stage and preserves the stack trace that identifies this substage.

This is an entry-cardinality defect, unlike deleting one label string inside an associated resource. The structural control is reported separately and was not forced through a nonexistent selected getter binding. Only Displayer and Populator were run for this control.

## What the comparison adds

| Comparison on the five core conditions | Observed additional rejection by E5 | Interpretation |
|---|---:|---|
| E5 D versus simple exact-path baseline | 0 | No added detection on this set; both implement the selected existing library constraints. |
| E5 D versus official Task initialization | 0 | Same rejected artifact, at different configured analysis/execution stages. |
| E5 D versus MetadataPopulator | 1 | The deletion satisfies metadata-entry cardinality but violates the selected decoder's label cardinality. This is scope separation, not a claim that official tools lack the condition. |
| E5 D versus Displayer | 1 | Readability is not contract validation; this is not a detector-accuracy comparison. |

The permutation passes every tested check above. None of these checks supplies an independent class-order oracle, so this outcome is not a proven semantic false negative. No precision, recall, prevalence, or overall superiority estimate follows from these five deliberately constructed conditions.

## Source and used-binary audit

Sources and exact line anchors are preserved in `source-anchors.json`; snapshots are in `sources/`. `versions.json` records Python 3.11.16, tflite-support 0.4.4, NumPy 1.26.4, FlatBuffers 25.12.19 and protobuf 3.20.3, plus the actual native extension hashes. The Task wrapper/native hashes agree with those already recorded for E3. No separately embedded Task interpreter version or source-build equivalence is established.

**Official structural path.** Installed `metadata.py` checks input/output metadata-entry counts in `_validate_metadata` (610–644). Display JSON/resource access is a separate API. The new structural control directly demonstrates why “Displayer succeeded” must not be written as “official validation accepted.”

**Actual Task path.** Installed Python `ImageClassifier.create_from_options` calls the native `_CppImageClassifier.create_from_options`; the preserved pybind source calls `ImageClassifier::CreateFromOptions` (line 66). The release `image_classifier.cc` calls `Init` (line 80), then `CheckAndSetOutputs` (line 132), where output/label-map cardinality is checked at lines 242–260. This is the relevant source route for the exercised ImageClassifier interface; the separately preserved `classification_postprocessor.cc` is not used as a substitute call-path proof. Runtime observations are consistent with this route, but the C++ source was not independently rebuilt into the wheel.

**Exact TensorLabel conditions.** Fresh `javap -c -p` reads the Support API jar named in the original Android build commands. That jar has SHA-256 `15d59ab34528d75908306432715e522a278f781ba6f4802d6b41917a5838a59d`. Its bytecode confirms first-nonunit-axis selection, label cardinality, a strictly last labeled axis, and category-list length equality. In particular, the implementation rejects shape `[1,4,1]` with four labels even though trailing axes are unit sized. The JavaDoc's “effectively last” wording does not override this explicit guard. This is binary disassembly, not a new runtime shape experiment or complete source-build-equivalence claim.

## E5 automatic extraction and limits

The existing implementation is more than a metadata-only shape heuristic, but it is a fixed-template parser rather than a general program analyzer:

- Lines 65–76 invoke the official generator, read the generated Java, and use regular expressions to extract actual getter names, tensor fields, `model.getOutputTensor(i)`, metadata/file positions, and postprocess-name suffixes. Lines 80–83 join these to the selected associated resource. No model-name, Gesture-name, or fixture-hash decision rule selects the D answer; digests identify evidence and supplied semantic references.
- Lines 84–87 inspect a matching default-postprocessor body and the operation names captured by `.add(new Word(`. This supports the known generated DequantizeOp template. It does not prove that every unknown processing expression is recognized and rejected: variable/factory expressions or unrecognized syntax can be missed by this pattern.
- The parser does not trace `Outputs` field assignments, `outputs.put(i, buffer)`, `model.run`, actual postprocess method calls, or default-processor installation through a full dataflow graph. Matching naming conventions supply those bridges. It does not reason about runtime reset methods, aliases, Java control flow or types.
- At line 104, an unmatched getter pattern can produce `INAPPLICABLE_NO_SELECTED_GETTER`; that status alone cannot distinguish a genuinely absent selected getter from a getter written in unrecognized syntax. Therefore the manuscript's blanket assertion that all “unrecognized processing require abstention” is stronger than the implementation guarantee. A bounded formulation is: “The checker abstains for dynamic signatures and for unsupported operations it recognizes within its modeled generated templates; unrecognized syntax is outside its demonstrated analysis scope.”
- Lines 88–90 abstain when any concrete shape/signature dimension is nonpositive. The preserved Gesture shape `[1,8]` / signature `[-1,8]` therefore triggers the three previously recorded abstentions before cardinality evaluation. E5 has no DEFER state, symbolic shape obligation, runtime obligation generation or discharge. These cases were inspected in preserved evidence and were not rerun here. Old abstentions must not be rewritten as new detections.

No parser counterexample model or arbitrary new Java program was created in this audit. The parser limitations above follow from source inspection; the successful baseline comparison concerns only the five actual fixed-template artifacts.

## Execution adaptation and preservation

Directly launching old E5 would append codegen logs to the sealed evidence tree through `common.run`. `launch_e5.py` therefore loads the unchanged original `scripts/preflight.py` with `runpy` and replaces only that imported logger. It executes the same codegen command with a new evidence directory, records stdout/stderr/exit status here, uses this new audit directory as subprocess working directory, and omits the sealed-log append. The rule code, official generator and old helpers are not edited. The old `E5/preflight.py` and `scripts/preflight.py` both hash to `8a149290196809e7cc0ed2ac642e212223f71ca4d46fb15dbd1976ce5c976166`.

`plan-freeze.json` predates the 27 core/control check invocations. Each command has separate stdout, stderr and command JSON; E5 also retains nested codegen logs. Additional source-audit commands record version discovery and javap. MetadataPopulator writes only new copies under `conditions/*/populator/`.

`protected-before.json`, `protected-after.json` and final checks record unchanged original model/script bytes and an unchanged old `commands-executed.sh` hash. There were no blocked core checks and no unexplained failed invocation: the observed nonzero exits are the expected deletion incompatibilities and the structural negative-control rejection. These new results add baseline comparison and source/binary auditing, not a human audit, clean-environment reproduction, new Android execution or new task-accuracy evidence.
