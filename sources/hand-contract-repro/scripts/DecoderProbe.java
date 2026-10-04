import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.List;
import org.tensorflow.lite.DataType;
import org.tensorflow.lite.support.common.TensorProcessor;
import org.tensorflow.lite.support.common.ops.DequantizeOp;
import org.tensorflow.lite.support.label.Category;
import org.tensorflow.lite.support.label.TensorLabel;
import org.tensorflow.lite.support.tensorbuffer.TensorBuffer;

/** Isolated host-JVM probe of the generated getter's library expression.
 * Does not instantiate the Android wrapper or run its interpreter.
 */
public final class DecoderProbe {
  public static void main(String[] args) throws Exception {
    String variant = args[0];
    int size = Integer.parseInt(args[1]);
    byte[] raw = Files.readAllBytes(Paths.get(args[2]));
    if (raw.length != size * 4) throw new IllegalArgumentException("Unexpected raw buffer size");
    ByteBuffer bytes = ByteBuffer.wrap(raw).order(ByteOrder.LITTLE_ENDIAN);
    float[] values = new float[size];
    bytes.asFloatBuffer().get(values);
    TensorBuffer buffer = TensorBuffer.createFixedSize(new int[]{1,size}, DataType.FLOAT32);
    buffer.loadArray(values);
    List<String> labels = Files.readAllLines(Paths.get(args[3]));
    TensorProcessor postprocessor = new TensorProcessor.Builder().add(new DequantizeOp(0,0)).build();
    System.out.println("variant=" + variant + " shape=" + Arrays.toString(buffer.getShape()) + " labels=" + labels.size());
    try {
      List<Category> categories = new TensorLabel(labels, postprocessor.process(buffer)).getCategoryList();
      System.out.println("status=ok categories=" + categories.size());
    } catch (RuntimeException e) {
      System.out.println("status=exception class=" + e.getClass().getName() + " message=" + e.getMessage());
    }
  }
}
