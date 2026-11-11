package org.example.support770;

import java.lang.reflect.Field;
import java.util.List;
import org.json.JSONArray;
import org.json.JSONObject;
import org.example.support770.ml.LiteModelDeeplabv31Metadata2;
import org.tensorflow.lite.support.image.TensorImage;
import org.tensorflow.lite.support.label.Category;
import org.tensorflow.lite.support.model.Model;
import org.tensorflow.lite.support.tensorbuffer.TensorBuffer;

public final class WrapperInstrumentation extends EvidenceInstrumentation {
  @Override protected void exercise(TensorImage input) throws Exception {
    stage = "construction";
    LiteModelDeeplabv31Metadata2 model = LiteModelDeeplabv31Metadata2.newInstance(getTargetContext(),
        new Model.Options.Builder().setDevice(Model.Device.CPU).setNumThreads(1).build());
    try {
      passed(stage); stage = "process";
      LiteModelDeeplabv31Metadata2.Outputs outputs = model.process(input);
      passed(stage); stage = "raw_observation";
      // Observe the filled raw buffer without substituting for the generated decoder.
      Field field = outputs.getClass().getDeclaredField("segmentationMasks"); field.setAccessible(true);
      TensorBuffer raw = (TensorBuffer)field.get(outputs);
      tensor("raw_output", raw.getBuffer(), raw.getShape()); passed(stage);
      stage = "category_getter";
      List<Category> categories = outputs.getSegmentationMasksAsCategoryList();
      JSONArray list = new JSONArray();
      for (Category category : categories) list.put(new JSONObject().put("label", category.getLabel())
          .put("score", category.getScore()).put("index", category.getIndex()));
      report.put("categories", list); passed(stage);
    } finally {
      try { model.close(); } catch (Throwable error) { report.put("close_error", error.toString()); }
    }
  }
}
