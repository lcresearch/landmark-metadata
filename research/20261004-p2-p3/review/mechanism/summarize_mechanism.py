#!/usr/bin/env python3
"""Generate auditable line anchors and static facts for the bounded P2 paths."""
import hashlib, json, pathlib
R = pathlib.Path(__file__).resolve().parent
S = R/'sources/tensorflow_lite_support'
P2 = R.parents[1]/'P2'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def anchor(p, text):
    lines=p.read_text().splitlines(); found=[i+1 for i,l in enumerate(lines) if text in l]
    assert found, (str(p),text)
    return {'path':str(p),'sha256':sha(p),'needle':text,'lines':found}
def main():
    tasks = [
      ('java_create',S/'java/src/java/org/tensorflow/lite/task/vision/classifier/ImageClassifier.java','public static ImageClassifier createFromFileAndOptions('),
      ('java_init_jni',S/'java/src/java/org/tensorflow/lite/task/vision/classifier/ImageClassifier.java','return initJniWithModelFdAndOptions('),
      ('java_classify',S/'java/src/java/org/tensorflow/lite/task/vision/classifier/ImageClassifier.java','public List<Classifications> classify(TensorImage image)'),
      ('java_classify_native',S/'java/src/java/org/tensorflow/lite/task/vision/classifier/ImageClassifier.java','return classifyNative('),
      ('java_exception_wrap',S/'java/src/java/org/tensorflow/lite/task/core/TaskJniUtils.java','} catch (RuntimeException e)'),
      ('jni_vision_namespace',S/'java/src/native/task/vision/classifier/image_classifier_jni.cc','using ::tflite::task::vision::ImageClassifier;'),
      ('jni_create',S/'java/src/native/task/vision/classifier/image_classifier_jni.cc','ImageClassifier::CreateFromOptions(options,'),
      ('jni_init_error',S/'java/src/native/task/vision/classifier/image_classifier_jni.cc','Error occurred when initializing ImageClassifier:'),
      ('jni_classify',S/'java/src/native/task/vision/classifier/image_classifier_jni.cc','auto results_or = classifier->Classify(*frame_buffer, roi);'),
      ('jni_conversion',S/'java/src/native/task/vision/classifier/image_classifier_jni.cc','return ConvertToClassificationResults(env, results_or.value());'),
      ('jni_invalid_argument',S/'cc/utils/jni_utils.cc','case StatusCode::kInvalidArgument:'),
      ('cpp_create_init',S/'cc/task/vision/image_classifier.cc','RETURN_IF_ERROR(image_classifier->Init('),
      ('cpp_init_outputs',S/'cc/task/vision/image_classifier.cc','RETURN_IF_ERROR(CheckAndSetOutputs());'),
      ('cpp_output_labels',S/'cc/task/vision/image_classifier.cc','BuildClassificationHead(*metadata_extractor, *output_tensor,'),
      ('cpp_label_count',S/'cc/task/vision/image_classifier.cc','if (num_classes != num_label_map_items)'),
      ('cpp_label_error',S/'cc/task/vision/image_classifier.cc','Got %d class(es) for output index %d, expected %d '),
      ('cpp_label_selection',S/'cc/task/vision/core/classification_head.cc','ModelMetadataExtractor::FindFirstAssociatedFileName('),
      ('cpp_selection_rule',S/'metadata/cc/metadata_extractor.cc','if (locale.empty() ||'),
      ('cpp_label_parse',S/'cc/task/vision/core/label_map_item.cc',"std::vector<absl::string_view> labels = absl::StrSplit(labels_file, '\\n');"),
      ('tensorlabel_ctor_count',S/'java/src/java/org/tensorflow/lite/support/label/TensorLabel.java','shape[axis] == entry.getValue().size(),'),
      ('tensorlabel_ctor_list',S/'java/src/java/org/tensorflow/lite/support/label/TensorLabel.java','this(makeMap(getFirstAxisWithSizeGreaterThanOne(tensorBuffer), axisLabels), tensorBuffer);'),
      ('tensorlabel_category',S/'java/src/java/org/tensorflow/lite/support/label/TensorLabel.java','public List<Category> getCategoryList()'),
      ('tensorlabel_axis',S/'java/src/java/org/tensorflow/lite/support/label/TensorLabel.java','labeledAxis == shape.length - 1,'),
      ('tensorlabel_first_axis',S/'java/src/java/org/tensorflow/lite/support/label/TensorLabel.java','if (shape[i] > 1)'),
    ]
    generated=P2/'variants/original/generated/src/main/java/org/example/contract/ContractModel.java'
    for ident,text in [
      ('generated_getter','return new TensorLabel(probabilityLabels, postprocessProbability(probability)).getCategoryList();'),
      ('generated_output','outputs.put(0, probability.getBuffer());'),
      ('generated_label_selection','extractor.getOutputTensorMetadata(0).associatedFiles(0).name();'),
      ('generated_label_read','probabilityLabels = FileUtil.loadLabels('),
      ('generated_process','model.run(inputBuffers, outputs.getBuffer());'),
      ('generated_postprocessor','private TensorProcessor buildDefaultProbabilityPostprocessor()')]: tasks.append((ident,generated,text))
    anchors={i:anchor(p,t) for i,p,t in tasks}
    (R/'line-anchors.json').write_text(json.dumps(anchors,indent=2)+'\n')
    old=pathlib.Path('/workspace/metadata-contract-e2e-20261004T030536Z/E1/variants/original/generated/src/main/java/org/example/contract/ContractModel.java')
    generated_versions=[{'variant':p.relative_to(P2/'variants').parts[0], 'path':str(p),'sha256':sha(p),'same_as_original':p.read_bytes()==generated.read_bytes()} for p in (P2/'variants').glob('*/generated/src/main/java/org/example/contract/ContractModel.java')]
    md=json.loads((P2/'variants/original/metadata.json').read_text())
    output=md['subgraph_metadata'][0]['output_tensor_metadata'][0]
    native=(R/'binary/native_strings.txt').read_text(errors='replace')
    checks={
       'five_generated_sources_available_and_equal':len(generated_versions)==5 and all(p['same_as_original'] for p in generated_versions),
       'new_original_source_equals_historical':sha(old)==sha(generated),
       'one_axis_labels_resource':output['associated_files']==[{'name':'labels_without_background.txt','description':'Labels for objects that the model can recognize.','type':'TENSOR_AXIS_LABELS'}],
       'native_has_init_diagnostic':'Error occurred when initializing ImageClassifier: %s' in native,
       'native_has_cardinality_diagnostic':'Got %d class(es) for output index %d, expected %d according to the label map.' in native,
       'support_jars_byte_identical':(P2/'dependencies/tensorflow-lite-support-api/classes.jar').read_bytes()==pathlib.Path('/workspace/hand-contract-repro/deps/tensorflow-lite-support-api-0.4.4.jar').read_bytes(),
    }
    assert all(checks.values()), checks
    result={'status':'PASS_STATIC_MECHANISM_REVIEW','runtime_executed_by_this_review':False,
            'source_commit':'133228616ca14e1b64c03f6a0ea8610f41a60783','checks':checks,
            'generated_sources':generated_versions,'source_anchors_path':str(R/'line-anchors.json'),
            'android_source_path':'vision::ImageClassifier::CreateFromOptions -> Init -> CheckAndSetOutputs',
            'source_path_correction':'Do not attribute this Android JNI route to ClassificationPostprocessor::Init; that is a different v0.4.4 implementation path.',
            'stage_observation_boundary':'Public Task createFromFileAndOptions combines model opening/loading and initialization. Public classify combines preprocessing, inference, postprocessing and Java result conversion. No internal runtime hooks here.',
            'binary_boundary':'Java bytecode inspected directly. Native JNI exported symbols and matching diagnostic strings inspected; complete native binary-source equivalence not established.'}
    (R/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'anchors':len(anchors),'checks':checks}))
if __name__=='__main__': main()
