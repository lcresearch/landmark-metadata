package org.example.support770;

import android.app.Instrumentation;
import android.graphics.Bitmap;
import android.os.Bundle;
import java.io.*;
import java.nio.ByteBuffer;
import java.security.MessageDigest;
import java.util.Arrays;
import org.json.JSONArray;
import org.json.JSONObject;
import org.tensorflow.lite.support.image.TensorImage;

/** Records stages before/after each actual public call, including complete failures. */
public abstract class EvidenceInstrumentation extends Instrumentation {
  protected static final String ASSET = "lite_model_deeplabv3_1_metadata_2.tflite";
  protected JSONObject report;
  protected String stage = "setup";
  protected File directory;
  @Override public void onCreate(Bundle arguments) { super.onCreate(arguments); start(); }
  protected abstract void exercise(TensorImage input) throws Exception;
  protected static String sha(byte[] bytes) throws Exception {
    StringBuilder result = new StringBuilder();
    for (byte b : MessageDigest.getInstance("SHA-256").digest(bytes)) result.append(String.format("%02x", b & 255));
    return result.toString();
  }
  protected void write(String name, byte[] bytes) throws Exception {
    try (FileOutputStream out = new FileOutputStream(new File(directory, name))) { out.write(bytes); }
  }
  protected void flush() throws Exception { write("result.json", report.toString(2).getBytes("UTF-8")); }
  protected void passed(String name) throws Exception { report.put(name + "_status", "PASS"); flush(); }
  protected void tensor(String name, ByteBuffer buffer, int[] shape) throws Exception {
    ByteBuffer copy = buffer.duplicate(); copy.rewind(); byte[] bytes = new byte[copy.remaining()]; copy.get(bytes);
    write(name + ".bin", bytes);
    JSONArray dims = new JSONArray(); for (int n : shape) dims.put(n);
    report.put(name, new JSONObject().put("bytes", bytes.length).put("sha256", sha(bytes)).put("shape", dims)); flush();
  }
  @Override public void onStart() {
    try {
      directory = new File(getTargetContext().getFilesDir(), "evidence");
      if (!directory.mkdir()) throw new IOException("Evidence directory must be absent");
      report = new JSONObject().put("instrumentation", getClass().getName())
          .put("platform", android.os.Build.FINGERPRINT).put("api", android.os.Build.VERSION.SDK_INT)
          .put("completed", false);
      flush(); stage = "asset_identity";
      try (InputStream in = getTargetContext().getAssets().open(ASSET); ByteArrayOutputStream bytes = new ByteArrayOutputStream()) {
        byte[] chunk = new byte[8192]; int n;
        while ((n = in.read(chunk)) != -1) bytes.write(chunk, 0, n);
        report.put("model_sha256", sha(bytes.toByteArray())).put("model_bytes", bytes.size());
      }
      passed(stage); stage = "input";
      byte[] rgb = new byte[257 * 257 * 3]; Arrays.fill(rgb, (byte)127);
      int[] pixels = new int[257 * 257]; Arrays.fill(pixels, 0xff7f7f7f);
      write("input.rgb", rgb); report.put("input_sha256", sha(rgb)).put("input_width", 257).put("input_height", 257);
      TensorImage input = TensorImage.fromBitmap(Bitmap.createBitmap(pixels, 257, 257, Bitmap.Config.ARGB_8888));
      passed(stage); exercise(input); report.put("scientific_status", "PASS");
    } catch (Throwable error) {
      try {
        StringWriter trace = new StringWriter(); error.printStackTrace(new PrintWriter(trace));
        report.put("scientific_status", "FAIL").put("earliest_failing_stage", stage)
            .put(stage + "_status", "FAIL").put("exception_type", error.getClass().getName())
            .put("exception_message", error.getMessage()).put("stack_trace", trace.toString());
        JSONArray causes = new JSONArray();
        for (Throwable cause = error; cause != null; cause = cause.getCause())
          causes.put(new JSONObject().put("type", cause.getClass().getName()).put("message", cause.getMessage()));
        report.put("causes", causes);
      } catch (Throwable recordingError) { recordingError.printStackTrace(); }
    } finally {
      try { report.put("completed", true); flush(); } catch (Throwable error) { error.printStackTrace(); }
      finish(-1, new Bundle());
    }
  }
}
