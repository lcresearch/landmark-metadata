package org.example.support770;

import java.util.List;
import org.json.JSONArray;
import org.json.JSONObject;
import org.tensorflow.lite.support.image.TensorImage;
import org.tensorflow.lite.task.core.BaseOptions;
import org.tensorflow.lite.task.vision.segmenter.ColoredLabel;
import org.tensorflow.lite.task.vision.segmenter.ImageSegmenter;
import org.tensorflow.lite.task.vision.segmenter.OutputType;
import org.tensorflow.lite.task.vision.segmenter.Segmentation;

public final class TaskInstrumentation extends EvidenceInstrumentation {
  @Override protected void exercise(TensorImage input) throws Exception {
    stage = "construction";
    report.put("requested_output_type", "CATEGORY_MASK");
    ImageSegmenter model = ImageSegmenter.createFromFileAndOptions(getTargetContext(), ASSET,
        ImageSegmenter.ImageSegmenterOptions.builder().setBaseOptions(BaseOptions.builder().setNumThreads(1).build())
          .setOutputType(OutputType.CATEGORY_MASK).build());
    try {
      passed(stage); stage = "segment";
      List<Segmentation> results = model.segment(input);
      report.put("segmentations", results.size()); passed(stage); stage = "mask_observation";
      JSONArray descriptions = new JSONArray(); int s = 0;
      for (Segmentation result : results) {
        JSONArray labels = new JSONArray();
        for (ColoredLabel label : result.getColoredLabels()) labels.put(new JSONObject()
            .put("label", label.getlabel()).put("display_name", label.getDisplayName()).put("argb", label.getArgb()));
        descriptions.put(new JSONObject().put("output_type", result.getOutputType().toString())
            .put("mask_count", result.getMasks().size()).put("labels", labels));
        int m = 0;
        for (TensorImage mask : result.getMasks()) {
          tensor("mask_" + s + "_" + m, mask.getBuffer(), mask.getTensorBuffer().getShape()); m++;
        }
        s++;
      }
      report.put("outputs", descriptions); passed(stage);
    } finally {
      try { model.close(); } catch (Throwable error) { report.put("close_error", error.toString()); }
    }
  }
}
