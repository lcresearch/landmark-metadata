import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.charset.StandardCharsets;
import java.util.List;
import org.tensorflow.lite.DataType;
import org.tensorflow.lite.support.common.FileUtil;
import org.tensorflow.lite.support.label.Category;
import org.tensorflow.lite.support.label.TensorLabel;
import org.tensorflow.lite.support.tensorbuffer.TensorBuffer;

/** Isolated library precondition probe; does not execute an Android wrapper. */
public class DecoderProbe {
  private static String escape(String x) {
    return x.replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", "\\n");
  }
  public static void main(String[] args) throws Exception {
    String[] dimensions=args[0].split(",");
    int[] shape=new int[dimensions.length];int size=1;
    for(int i=0;i<shape.length;i++){shape[i]=Integer.parseInt(dimensions[i]);size*=shape[i];}
    byte[] bytes=Files.readAllBytes(Paths.get(args[1]));
    if(bytes.length!=size*4)throw new IllegalArgumentException("Input buffer size mismatch");
    float[] values=new float[size];
    ByteBuffer.wrap(bytes).order(ByteOrder.LITTLE_ENDIAN).asFloatBuffer().get(values);
    TensorBuffer buffer=TensorBuffer.createFixedSize(shape,DataType.FLOAT32);buffer.loadArray(values);
    List<String> labels=FileUtil.loadLabels(Files.newInputStream(Paths.get(args[2])),StandardCharsets.UTF_8);
    try {
      List<Category> categories=new TensorLabel(labels,buffer).getCategoryList();
      System.out.println("{\"status\":\"PASS\",\"categories\":"+categories.size()+",\"labels\":"+labels.size()+"}");
    } catch(RuntimeException e) {
      System.out.println("{\"status\":\"FAIL\",\"exception\":\""+e.getClass().getName()+"\",\"message\":\""+escape(e.getMessage())+"\",\"labels\":"+labels.size()+"}");
    }
  }
}
