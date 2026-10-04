# Official implementation comparison

The official implementation already defines metadata-driven interfaces, ordered
label associations and label-count preconditions. This study must not claim to
invent those rules. Its candidate empirical contribution is the controlled
execution and comparison of their consequences at particular consumer boundaries.
Whether that characterization is sufficiently novel also depends on the research
comparisons in this review.

## Source status

This review freshly retrieved Support `v0.4.4`, resolved the tag to commit
`133228616ca14e1b64c03f6a0ea8610f41a60783`, and checked every downloaded source's
Git blob identity against that commit's recursive tree. The API responses equal
the historical pinned responses. Relevant historical source copies, including
the installed `metadata.py` snapshot, also match the freshly downloaded bytes.
Exact SHA-256 digests, URLs, function/line locators, retrieval timestamps and
historical comparisons are in [official-sources.json](official-sources.json).

The 17 indexed objects comprise two provenance responses and 15 source files.
Fourteen source files received targeted function inspection; `codegen/utils.cc`
was downloaded and hash-verified only. Raw downloads and HTTP response logs are
outside Git under `/workspace/contribution-review-20261004/official/`.
This is source inspection, not a new execution of generation, inference or Task
initialization. A source version does not establish exact Maven/native binary
equivalence. Existing execution findings remain recorded experiment findings.

The following command freshly verified all 17 indexed objects, the tag resolution
and source blob membership. Omitting `--verify-only` retrieves missing objects
from their fixed primary URLs; it never overwrites existing evidence.

```sh
python research/20261004-contribution-review/scripts/inspect_official.py \
  --directory /workspace/contribution-review-20261004/official --verify-only
```

## What each official entry point already does

| Entry point | Freshly inspected mechanism | Boundary and contribution consequence |
|---|---|---|
| Metadata schema (`OFF03`, lines 87–103, 632–649) | Declares ordered output metadata correspondence and equal tensor-metadata cardinality. `TENSOR_AXIS_LABELS` explicitly requests a labels/probabilities mapping in generated interfaces. | Ordered association and metadata-based code generation are documented design, not newly discovered capabilities. Schema comments specify relationships; their existence is not proof every entry point enforces them. |
| `MetadataDisplayer` (`OFF04`, 686–756) | Checks model/metadata identifiers, requires metadata, enumerates ZIP resources and returns named file bytes. | A reading/display entry point; no label-count or class-order check appears in the inspected path. Its successful use must not be renamed comprehensive validation. |
| `MetadataPopulator.load_metadata_buffer` / `_validate_metadata` (`OFF04`, 285–321, 610–642) | Checks metadata identifier, exactly one subgraph metadata object and equal numbers of graph input/output tensors and tensor metadata records. Loading also inserts minimum parser version and normalizes resource basenames. | **Tensor metadata count is not label-entry count.** Removing an output metadata record exercises an existing structural check. Repacking can change metadata bytes, so intervention preservation still requires separate comparison. |
| `MetadataPopulator.populate` / `_assert_validate` (`OFF04`, 361–397) | Requires recorded associated filenames to be supplied or already packed; rejects duplicate packing; warns but allows unrecorded resources. | Checks resource presence/packing, not cardinality of the labels inside a resource or external class-order agreement. Calling this a label-count validator would be incorrect. |
| Generic Java code generator (`OFF05`, `OFF14`, `OFF17`) | Derives names from tensor metadata, iterates metadata positions, selects an associated file index, emits output tensor bindings and a `TensorLabel(...).getCategoryList()` getter for supported axis-label tensor outputs. | Generated names, ordered bindings, resource selection and decoder calls already exist. The checked generator path operates on metadata declarations; label bytes are loaded later by generated code. Source/class invariance under a resource-only intervention is still an experiment assertion, not a measurement made here. |
| Generated `newInstance` / metadata constructor (`OFF05`, 495–544, 647–650) | Creates a `Model`; metadata constructor obtains actual output tensor shape/type and loads labels through `FileUtil` from the named associated file. | **Label loading already occurs during construction.** Do not write that the getter is the first access to the label file. In this path the label-count comparison is deferred to the decoder. |
| Generated `process` and category getter (`OFF05`, 393–398, 682–690) | `process` allocates `Outputs`, preprocesses inputs, calls `model.run`, then returns. Getter separately postprocesses the output and constructs `TensorLabel`. | Explains how inference can precede category-decoder rejection. Whether a particular run reaches it is established by the preserved E1/P2 records, not by reading the template. |
| `FileUtil.loadLabels` (`OFF06`, 87–113) | InputStream overload uses `Charset.defaultCharset()`. A `BufferedReader` supplies lines; `line.trim().length() > 0` controls inclusion, while the original untrimmed `line` is retained. | Correct preflight needs the selected parser and charset assumptions. Python `splitlines()` is not this implementation. The maintained fix and the recorded VT/U+2028 probes are supporting tool evidence, not a new official decoder rule. |
| `TensorLabel` (`OFF07`, 74–105, 189–215) | List overload selects the first axis of size greater than one. Constructor compares axis size with label count. Category conversion requires that selected axis to be the final axis and label count to equal float-array length. | Cardinality and axis requirements are existing checks. Merely moving them earlier is not a new rule. They are also more specific than “last dimension equals number of text lines.” |
| Task `ImageClassifier` (`OFF09`, 52–83, 121–261) | Construction calls `Init`, which calls `CheckAndSetOutputs`. This checks metadata/output count, supported output dimensions and label-map count against class count. | Provides an existing initialization-time compatibility check. The observed same-Android comparison should be explained with this actual call chain. |
| Task `ClassificationPostprocessor` (`OFF08`, 43–137) | Its own `Create` calls `Init`, which checks supported shape, label count and type. | A second official location for an analogous rule. It must not be substituted for the `ImageClassifier::CheckAndSetOutputs` call chain without proving that consumer uses it. |
| Task label-map construction (`OFF12`, 32–61; `OFF13`, 31–75; `OFF16`, 162–178) | Selects the first named axis-label file, and a matching locale file for display names. Splits file bytes on LF, drops one final empty element, and checks display-name/label counts. | Resource selection and parsing are consumer-specific. This is not Java `FileUtil` behavior for arbitrary inputs. No new parser-mutant execution or equivalence claim is made here. |

## Exact Java decoder condition

For the inspected expression
`new TensorLabel(labels, postprocessOutput(buffer)).getCategoryList()`, let
`shape` describe the **postprocessed** tensor and let `labels` be the result of
the selected `FileUtil` call. The inspected implementation requires:

1. an axis `a`, the first axis for which `shape[a] > 1`;
2. `labels.size() == shape[a]` in the constructor;
3. `a == shape.length - 1` in `getCategoryList()`;
4. `labels.size() == tensorBuffer.getFloatArray().length` before emitting results.

The output combines each retained label with the float at its enumeration
position (`OFF07`, 197–203). Thus changing label order while keeping count does
not violate these checks. These checks supply no independent class-order oracle.
The list overload's implementation is the authority here: its behavior must not
be generalized from a looser Javadoc example or from another TensorLabel overload.

Preflight may use graph shape only where the actually selected postprocessor and
shape behavior justify doing so. Custom processors, unsupported generated
patterns, dynamic shapes, malformed encodings and absent semantic references
are distinct limitations; a general correctness verdict does not follow.

## Task initialization requires separate attribution

At this fixed commit the inspected vision `ImageClassifier` has its own output
validation code. Its concrete source chain is:

`CreateFromOptions` → `Init` → `CheckAndSetOutputs`
→ `vision::core::BuildClassificationHead` / `BuildLabelMapFromFiles`.

Within `CheckAndSetOutputs`, lines 212–241 constrain rank to 2 or 4, batch to 1,
and spatial dimensions of a rank-4 output to 1. Lines 242–261 take the final
dimension as the class count and compare it with the nonempty label map. When no
label map is present, a default map can instead be constructed. A model without
labels is therefore not interchangeable with a model containing a nonempty
999-entry label file for a 1000-class output. An empty selected file has its own
error in `BuildLabelMapFromFiles`.

`ClassificationPostprocessor::Init` contains analogous logic, but is a distinct
implementation location using the `task::core` label helpers. The source tree
contains both core and vision/core helper versions. Similar function names and
messages do not demonstrate independent implementations, identical runtime
integrations or a particular binary call chain. The recorded P2 mechanism/binary
analysis is a separate source of those narrower runtime claims.

## Remaining comparison, without novelty inflation

| Candidate statement | Decision against these official baselines |
|---|---|
| “We introduce output/metadata order, label count or metadata-driven wrappers.” | **Drop.** Already specified or implemented in these sources. |
| “Official validation misses label deletion.” | **Narrow.** Identify the actual reading/population entry point; Task initialization and TensorLabel already check it. |
| “The getter first reads the label file.” | **Correct.** Construction loads the file; the getter constructs/checks the decoder. |
| “All structural acceptance implies consumer compatibility.” | **Reject this inference.** The inspected entry points check different obligations; the experiments characterize selected cases. |
| “Resource-only interventions reach an unmodified generated public API, with computation preserved and reversal controls.” | **Retain as a bounded empirical contribution candidate.** Source explains the mechanism; the actual controlled executions and preservation records provide the case evidence. Closest-work comparison still decides novelty. |
| “Different official consumers enforce this condition at different stages.” | **Retain with configuration scope.** Source confirms the differing locations; recorded P2 supplies the same-Android observation. Do not infer universal earlier-is-better safety or performance. |
| “The preflight checker invents stronger label validity.” | **Drop.** It implements a modeled path's existing preconditions. Useful extras must be measured separately against an implementation-faithful baseline. |
| “The parser counterexamples establish a new official-library defect.” | **Drop.** The reported mismatch was in the project's former approximation; official implementations define different parsing behavior. Its value is showing the cost of an inaccurate consumer model. |
| “Label-count compatibility establishes correct class meaning.” | **Drop.** A supplied, artifact-linked reference remains a separate I check; D does not provide one. |

This comparison supports an empirical characterization and a supporting preflight
artifact. It does not by itself establish a novel analysis algorithm, a natural
EfficientNet defect, practical prevalence, task accuracy impact or completed human
verification.
