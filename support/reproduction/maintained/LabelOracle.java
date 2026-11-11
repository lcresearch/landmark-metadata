import java.io.ByteArrayInputStream;
import java.nio.charset.StandardCharsets;
import java.util.Base64;
import java.util.List;
import org.tensorflow.lite.support.common.FileUtil;

/** Calls the actual pinned API; outputs base64 labels to preserve all content. */
public final class LabelOracle {
  public static void main(String[] args) throws Exception {
    byte[] payload = Base64.getDecoder().decode(args[0]);
    List<String> labels = FileUtil.loadLabels(
        new ByteArrayInputStream(payload), StandardCharsets.UTF_8);
    System.out.println(labels.size());
    for (String label : labels) {
      System.out.println(Base64.getEncoder().encodeToString(label.getBytes(StandardCharsets.UTF_8)));
    }
  }
}
