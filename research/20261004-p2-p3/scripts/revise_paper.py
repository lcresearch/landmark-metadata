"""Rebuild the targeted P2/P3 manuscript revision from the sealed prior paper.

Reads completed experiment results; writes only manuscript/paper.tex and
manuscript-changes.patch in this work root. No experiments are run.
"""
import argparse
import difflib
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = Path('/workspace/metadata-contract-paper-revision-20261004T065132Z/manuscript/paper.tex')
BASE_SHA256 = '390445a494c24cf9e9069ca3d5ab62e4d0174587f631856b764846d54908782d'

def replace(text, old, new):
    count = text.count(old)
    assert count == 1, (count, old[:100])
    return text.replace(old, new, 1)

def apply_p3(text):
    result = json.loads((ROOT / 'P3/results.json').read_text())
    review = json.loads((ROOT / 'review/reference-audit/results.json').read_text())
    assert result['status'] == 'COMPLETE_WITH_QUALIFIED_DISPLAY_REFERENCE'
    primary = result['primary_result']
    assert primary['stable_class_id_reference'] == 'ABSTAIN'
    assert primary['prediction_correctness'] == 'NOT_EVALUATED'
    assert (primary['original_position_matches'], primary['permutation_position_mismatches'],
            primary['restoration_position_matches']) == (1000, 999, 1000)
    assert result['bridge']['equal_nonmetadata_buffers'] == 165
    assert result['bridge']['all_nonbuffer_nonmetadata_model_fields_equal']
    assert result['bridge']['ordered_outputs_equal']
    assert result['bridge']['metadata_buffer_not_tensor_referenced']
    assert review['status'] == 'PASS_DISPLAY_REFERENCE_ONLY'
    assert review['original_display_matches'] == review['restored_display_matches'] == 1000
    assert len(review['mutant_display_mismatches']) == 999

    text = replace(text,
        'A fresh build and new Android virtual device reproduce both outcomes.',
        'A fresh build and new Android virtual device reproduce both outcomes. An external publisher reference, linked through identical graph/weights, establishes that the permutation disagrees with the prescribed display-label order at 999 positions; stable class-ID provenance remains unresolved.')
    text = replace(text,
        'E1/E2 answer through an executed failure, a successful association change, and reversals.',
        'E1/E2 answer through an executed failure, a successful association change, and reversals; a subsequent publisher-reference comparison establishes disagreement with the prescribed display-label order.')
    text = replace(text,
        "The reference must be tied to the tested artifact or to a documented graph-equivalence bridge. Unknown mappings and absent references yield abstention. A class-order judgment similarly requires an artifact-tied class-index reference; the original artifact's own label list is only a comparison baseline. Our Hand mapping is extracted from official integration source with knowledge of the case and remains subject to human audit. I neither infers arbitrary tensor meanings nor evaluates prediction correctness.",
        r"The reference must be tied to the tested artifact or to a documented graph-equivalence bridge. Unknown mappings and absent references yield abstention. The reference's granularity is part of the judgment: $I_{\mathrm{display}}$ compares positions within a classification output tensor with prescribed display strings, whereas stable class identifiers require their own provenance. The original artifact's label list alone supplies neither reference. Section~\ref{sec:p3} establishes a publisher display-order reference; the complete stable-ID chain remains unresolved. Our Hand role mapping is extracted from official integration source with knowledge of the case. Both reference interpretations remain subject to human audit; I does not evaluate prediction correctness.")
    text = replace(text,
        'These observations establish a successful change in exposed association relative to the original artifact. No independent class-order reference is tied to this exact EfficientNet version, so I abstains. The result is neither a demonstrated incorrect class assignment nor evidence of reduced prediction accuracy. Passing the permutation under D is an intended boundary of a count/shape precondition, not a false negative for a semantic detector.',
        r'These executions establish a successful change in exposed association relative to the original artifact. A subsequent reference comparison (Section~\ref{sec:p3}) establishes disagreement with publisher-prescribed display-label order. Passing the permutation under D remains an intended boundary of a count/shape precondition; neither result evaluates prediction accuracy.')

    p3_section = r'''\subsection{A publisher display-order reference (P3)}
\label{sec:p3}
P3 separately retrieves a reference outside the mutated model package. The versioned TFHub Lite0 fp32/2 artifact has a different whole-file hash from the focal EfficientNet model, but all 165 non-metadata buffers, computational fields, tensor descriptors, and ordered outputs agree. Both contain 166 buffers; only metadata buffer 165 differs, and no graph tensor references it. The shared output is tensor 163 with shape \code{[1,1000]}. This independently recomputed graph/weight bridge supports transferring an output-order specification without asserting byte-identical packages or reconstructing the export history.

The exact Lite card, pinned at catalog commit \code{81fdea8ffa53}, identifies \code{lite0/classification/1} as its parent~\cite{tfhub-lite-card}. That parent explicitly prescribes the external \code{ImageNetLabels.txt} file and instructs readers to omit its first background line, making output index 0 ``tench''~\cite{tfhub-parent-card,imagenet-display}. The offset follows the publisher's instruction rather than an alignment fitted to the focal labels. The saved reference has 1,001 lines and SHA-256 prefix \code{536feacc519d}; it is a separately retrieved object, not the focal labels relabeled as ground truth.

All 1,000 original and restored display associations agree with that reference. The predetermined cyclic permutation disagrees at 999 positions, including position 904: prescribed ``window screen'' becomes ``window shade'' despite successful E2 decoding and unchanged score bits. The complete position-wise comparison is preserved. Duplicate strings ``crane'' at 134/517 and ``maillot'' at 638/639 demonstrate why display strings are not stable class IDs; the adjacent maillot pair accounts for the sole unchanged permuted string. Thus $I_{\mathrm{display}}$ reports agreement, disagreement, and restored agreement, respectively.

The full output-index-to-stable-synset-ID provenance chain remains \textsc{abstain}. Ancillary generic ImageNet/checkpoint lists agree in their names but do not establish the missing exact-artifact training lineage. The catalog commit preserves documentation retrieved for this study, not a verified release-time snapshot; the external label URL is unversioned and its retained bytes/hash define the reference used here. P3 performs no inference. It establishes a violation of the documented display-order specification, not an incorrect prediction on an image, accuracy loss, or a natural EfficientNet defect. Earlier E5 reports were produced without this reference and remain unchanged.

'''
    text = replace(text, r'\subsection{Fresh construction audit of E1/E2}', p3_section + r'\subsection{Fresh construction audit of E1/E2}')
    text = replace(text,
        'The secondary Hand case supplies reference-backed association evidence not established by the classifier experiments: a graph-specific output-role reference.',
        'The secondary Hand case supplies a different reference-backed association: graph-specific output roles, paired with a task-specific consumer boundary.')
    text = replace(text,
        'The later Hand supplied-reference checks are separate.',
        'The later Hand supplied-reference checks and P3 display-order comparison are separate; neither retroactively changes these frozen outcomes.')
    text = replace(text,
        'The count-preserving permutation passes, with I still abstaining. These baseline runs stop at Task initialization and add no Task classification or Android execution.',
        'The count-preserving permutation passes, with I abstaining in these runs because no reference was supplied. These baseline runs stop at Task initialization and add no Task classification or Android execution.')
    text = replace(text,
        'No class-order reference is supplied. The separate structural negative control is described in the text.',
        'No class-order reference was supplied to these runs; the later P3 comparison is separate. The structural negative control is described in the text.')
    text = replace(text,
        'E2 establishes changed association, not independently established class-order correctness.',
        'E2 establishes changed association, and P3 establishes its disagreement with a publisher display-order specification through a checked graph/weight bridge. Stable class-ID provenance and prediction correctness remain unestablished; documentary source interpretation still requires human review.')
    text = replace(text,
        'Preparing this revision launches no further model experiments.',
        'The P3 reference inquiry adds retrieval and offline comparison of independently supplied documentation/resources; it adds no inference.')
    text = replace(text,
        'a count-preserving permutation instead succeeds while changing the exposed association. Restoration reverses both outcomes, and fresh same-toolchain construction reproduces them.',
        'a count-preserving permutation instead succeeds while disagreeing with an independently supplied publisher display-order specification at 999 positions. Restoration recovers execution success and reference agreement, and fresh same-toolchain construction reproduces the runtime outcomes. Stable class-ID provenance and image prediction correctness remain outside these conclusions.')
    text = replace(text, r'\begin{thebibliography}{14}', r'\begin{thebibliography}{17}')
    new_references = r'''\bibitem{tfhub-lite-card} TensorFlow Hub. \emph{EfficientNet Lite0 fp32/2 model card}. Catalog commit \code{81fdea8ffa53b5acbd66a012d17fb8f9602c714b}. \url{https://github.com/tensorflow/tfhub.dev/blob/81fdea8ffa53b5acbd66a012d17fb8f9602c714b/assets/docs/tensorflow/models/efficientnet/lite0/fp32/lite/2.md}.
\bibitem{tfhub-parent-card} TensorFlow Hub. \emph{EfficientNet Lite0 classification/1 model card}. Same catalog commit; explicit output-index mapping and background rule. \url{https://github.com/tensorflow/tfhub.dev/blob/81fdea8ffa53b5acbd66a012d17fb8f9602c714b/assets/docs/tensorflow/models/efficientnet/lite0/classification/1.md}.
\bibitem{imagenet-display} TensorFlow. \emph{ImageNetLabels.txt}. Retrieved reference snapshot, SHA-256 prefix \code{536feacc519d}; full bytes, digest, and storage generation preserved. \url{https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt}.
'''
    text = replace(text, r'\bibitem{task-classifier}', new_references + r'\bibitem{task-classifier}')
    return text

def apply_p2(text):
    result = json.loads((ROOT / 'P2/results.json').read_text())
    assert (result['primary_units'], result['unique_graphs'], result['variants'],
            result['consumers'], result['observed_input_runs']) == (10, 1, 5, 2, 18)
    assert len(result['records']) == len(result['stage_matrix']) == 10
    stages = {(r['consumer'], r['variant']): r['stages'] for r in result['stage_matrix']}
    variants = ['original', 'description_control', 'label_deletion', 'label_permutation', 'restoration']
    for variant in variants:
        w = stages['wrapper', variant]; t = stages['task', variant]
        assert w['public_constructor'] == w['inference'] == 'PASS'
        assert w['generated_getter'] == ('FAIL' if variant == 'label_deletion' else 'PASS')
        if variant == 'label_deletion':
            assert t['public_constructor'] == 'FAIL'
            assert t['input_preparation'] == t['inference'] == t['classify_inference_and_decoding'] == 'NOT_REACHED'
        else:
            assert t['public_constructor'] == t['classify_inference_and_decoding'] == 'PASS'
            assert t['inference'] == t['decoder'] == 'NOT_SEPARATELY_OBSERVED'
    assert all(result['source_classes_dex'].values())
    assert all(r['source_copy_apk_preload_equal'] for r in result['identity_checks'])
    paired = result['cross_consumer_returned_score_comparisons']
    assert len(paired) == 8
    assert all(r['compared_indices'] == r['equal_score_bit_count'] == r['equal_label_count'] == 1000 for r in paired)
    assert all(r['max_abs_returned_score_difference'] == 0 for r in paired)
    for row in result['numeric_comparisons']:
        if row['consumer'] == 'wrapper':
            assert row['raw_equal_original']
        if row['decoded_available']:
            assert row['score_bits_equal_original']
            assert row['changed_label_count'] == (999 if row['variant'] == 'label_permutation' else 0)
    task_failure = json.loads((ROOT / 'P2/executions/primary/task/label_deletion/device/result.json').read_text())
    assert task_failure['exception_type'] == 'java.lang.IllegalStateException'
    assert task_failure['exception_message'] == 'Error getting native address of native library: task_vision_jni'
    assert task_failure['cause_chain'][1]['type'] == 'java.lang.IllegalArgumentException'
    assert task_failure['cause_chain'][1]['message'] == 'Error occurred when initializing ImageClassifier: Got 1000 class(es) for output index 0, expected 999 according to the label map.'
    assert (ROOT / 'P2/EXPERIMENT_P2_RESULTS.md').is_file()

    text = replace(text,
        'An official Task classifier rejects the identical deletion artifact during initialization, establishing different enforcement stages for the two configured consumers.',
        'On the same Android virtual device, an official Task classifier rejects the identical deletion artifact during public construction, while the generated interface rejects it at output access after inference. Native integrations remain different.')
    text = replace(text,
        'E3 compares two official paths, while Hand bounds the reach of an output-role witness through a task-specific consumer.',
        'E3/P2 compare two official paths, including on the same Android device, while Hand bounds the reach of an output-role witness through a task-specific consumer.')
    text = replace(text,
        'Combined E1/E2 evidence relative to the original.',
        'Combined E1/E2 generated-wrapper evidence relative to the original.')
    start = text.index(r'\section{E3: Different Stages of Contract Enforcement}')
    end = text.index(r'\section{Hand: Reference Agreement and Consumer Reach}', start)
    replacement = r'''\section{E3/P2: Consumer Enforcement Boundaries}
\label{sec:e3}
P2 tests whether the earlier cross-platform stage contrast persists on the same Android device. The unmodified generated wrapper and official Task Vision/Base 0.4.4 execute as separate APK configurations on one fresh API-30 default x86\_64 AVD. The wrapper retains TFLite Java/native 2.13.0; Task uses its published native library. Both request CPU execution and one thread. Task calls \code{createFromFileAndOptions} with a 1,000-result limit and then \code{classify(TensorImage)}. The five exact original, description, deletion, permutation, and restored artifacts and the two E1/E2 RGB inputs are unchanged. Ten variant--consumer units cover one computational graph and 18 actual input observations; Task deletion fails before its two planned inputs are reached.

All ten configurations compile, package, and install. Generated Java is byte-identical across the five variants; compiled classes and DEX are equal within each consumer. Source-model, copied-model, APK-asset, and pre-construction AssetManager hashes agree. This checks the supplied resource before public creation, not an intercepted native interpreter buffer. Both harnesses create the same UINT8 TensorImage from identical ARGB8888 bitmap inputs. Separate APKs preserve the published native integrations rather than forcing Task onto the wrapper's interpreter.

The wrapper loads and completes \code{process} for every variant, then only deletion fails in its actual generated getter with the E1 label-cardinality exception. Task creates and classifies the other four variants, returning 1,000 categories for each input, but rejects deletion during its public creation call (Table~\ref{tab:stages}). The recorded public exception is \code{IllegalStateException}: ``Error getting native address of native library: task\_vision\_jni.'' Its preserved cause is \code{IllegalArgumentException}: ``Error occurred when initializing ImageClassifier: Got 1000 class(es) for output index 0, expected 999 according to the label map.'' The outer message wraps this cardinality rejection; it is not evidence of a missing native library. All exceptions are caught by instrumentation.

\begin{table*}[t]
\centering\small
\setlength{\tabcolsep}{8pt}
\begin{tabular}{@{}llllll@{}}
\toprule
 & \multicolumn{3}{c}{Generated wrapper / Android} & \multicolumn{2}{c}{Official Task / same Android AVD}\\
\cmidrule(lr){2-4}\cmidrule(l){5-6}
Artifact & Create & Process & Getter & Create & Classify\\
\midrule
Original & pass & pass & pass & pass & pass\\
Description control & pass & pass & pass & pass & pass\\
Label deletion & pass & pass & fail & fail & not reached\\
Label permutation & pass & pass & pass & pass & pass\\
Restoration & pass & pass & pass & pass & pass\\
\bottomrule
\end{tabular}
\caption{Fresh P2 executions on the same API/ABI/AVD. Each successful creation reaches both prescribed inputs. Task creation combines loading and initialization; its classify call combines preprocessing, inference, and result decoding. No separate Task internal inference or decoder stage is observed. Wrapper process and getter are distinct public calls.}
\label{tab:stages}
\end{table*}

The mechanism review connects the Android JNI path to \code{vision::ImageClassifier::CreateFromOptions}, then \code{Init} and \code{CheckAndSetOutputs}~\cite{task-classifier}. That function builds the output label map and compares its length with the class dimension during initialization. The actual Java \code{TaskJniUtils} bytecode explains the outer exception and retained cause. The generated path instead constructs \code{TensorLabel} during getter access. For these single-resource artifacts, Task's first \code{TENSOR\_AXIS\_LABELS} selection and the generated metadata/file-index selection resolve to the same resource. These observations do not establish equivalent behavior for arbitrary multiple-resource or locale configurations.

Within each consumer, permutation preserves all returned score bits by output/class index while changing 999 labels; restoration recovers the original decoded result. Wrapper raw outputs agree across all five variants. In the eight successful paired condition/input comparisons, all 1,000 returned score bit patterns and labels also agree between consumers after matching Task class indices to wrapper output positions. Task ranked-list position is not used as an output index. These are returned-value comparisons: the Task API exposes no separately captured raw tensors, and \code{classify} remains an atomic public call for this study.

The same Android device removes the earlier OS/API/ABI difference, but consumer APIs and native integrations remain different. The routes share ecosystem components, including an identical Support API jar; they are not established as independent implementations. Exact Maven/native hashes and the source mechanism are preserved, without claiming a reproducible native source build or inferring Task's embedded interpreter version from the wrapper's 2.13.0 dependency. The result is a contrast between these configured consumers, not isolated interpreter-version causality.

\paragraph{Earlier Linux comparison (E3).}
The preserved Task Library 0.4.4 Python/C++ runs on Linux also rejected the same deletion during initialization with a \code{ValueError}, while original, description, and permutation initialized and classified successfully. Those earlier Android comparison rows reused E1/E2 execution. E3 therefore varied both consumer and platform; P2 adds the same-Android comparison rather than relabeling or duplicating those historical observations.

'''
    text = text[:start] + replacement + text[end:]
    text = replace(text,
        'E3 records enforcement stages in two configurations.',
        'E3/P2 record enforcement stages in two consumer configurations, including a same-Android comparison.')
    text = replace(text,
        'E3 changes both consumer and platform/toolchain, so its contrast is descriptive at that configuration level.',
        'The historical E3 comparison changes both consumer and platform/toolchain. P2 fixes the Android device, API and ABI while native integrations and public interfaces still differ; it does not isolate a single implementation variable.')
    text = replace(text,
        'The later construction audit uses new outputs and a new AVD with the same installed toolchain (Section~\\ref{sec:rebuild}).',
        'The later construction audit uses new outputs and a new AVD with the same installed toolchain (Section~\\ref{sec:rebuild}). P2 likewise retains both successful pre-execution build attempts; its final rebuild separates API-return status from observation serialization without changing generated Java, artifacts, or the frozen consumer/input choices.')
    text = replace(text,
        'The companion claim map distinguishes historical executions, checks of their retained bytes, and the subsequent construction and baseline runs.',
        'The companion claim map distinguishes historical executions, checks of their retained bytes, the subsequent construction/baseline runs, and P2 same-Android execution.')
    text = replace(text,
        'The tested Task configuration rejects the cardinality mismatch earlier, while the secondary Hand Task preserves its result on the prescribed input.',
        'The Task configuration rejects the cardinality mismatch earlier on the same Android device; native integrations still differ. The secondary Hand Task preserves its result on the prescribed input.')
    text = replace(text,
        r'\bibitem{task-classifier} TensorFlow Lite Support. \emph{ImageClassifier interface and implementation}, v0.4.4. Header, source, and Python binding preserved. \url{https://github.com/tensorflow/tflite-support/blob/v0.4.4/tensorflow_lite_support/cc/task/vision/image_classifier.cc}.',
        r'\bibitem{task-classifier} TensorFlow Lite Support. \emph{ImageClassifier Java/JNI/C++ implementation}, v0.4.4, commit \code{133228616ca14e1b64c03f6a0ea8610f41a60783}. Source, bindings, and selected binaries preserved. \url{https://github.com/tensorflow/tflite-support/blob/133228616ca14e1b64c03f6a0ea8610f41a60783/tensorflow_lite_support/cc/task/vision/image_classifier.cc}.')
    return text

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--p3-only', action='store_true', help='Stage completed P3 edits while P2 execution is pending.')
    args = parser.parse_args()
    base_bytes = BASE.read_bytes()
    assert hashlib.sha256(base_bytes).hexdigest() == BASE_SHA256
    base = base_bytes.decode()
    text = apply_p3(base)
    if not args.p3_only:
        text = apply_p2(text)
    (ROOT / 'manuscript/paper.tex').write_text(text)
    patch = ''.join(difflib.unified_diff(base.splitlines(keepends=True), text.splitlines(keepends=True),
                                       fromfile=str(BASE), tofile='manuscript/paper.tex'))
    (ROOT / 'manuscript-changes.patch').write_text(patch)
    print(json.dumps({'source_sha256': hashlib.sha256(text.encode()).hexdigest(),
                      'phase': 'P3-only staging' if args.p3_only else 'P2/P3 complete revision',
                      'base_sha256': BASE_SHA256, 'new_experiments_run_by_editor': 0}, indent=2))

if __name__ == '__main__':
    main()
