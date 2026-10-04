package org.example.contract;

import android.app.Instrumentation;
import android.content.Context;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.util.Log;
import java.io.File;
import java.io.FileOutputStream;
import java.io.PrintWriter;
import java.io.StringWriter;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.security.MessageDigest;
import java.util.List;
import org.json.JSONArray;
import org.json.JSONObject;
import org.tensorflow.lite.DataType;
import org.tensorflow.lite.support.image.TensorImage;
import org.tensorflow.lite.support.label.Category;
import org.tensorflow.lite.support.model.Model;

/** Actual generated public API; raw-buffer access observes without replacing decoding. */
public final class ContractInstrumentation extends Instrumentation {
  private Bundle arguments;
  private JSONObject report;
  private File directory;
  @Override public void onCreate(Bundle arguments) { super.onCreate(arguments); this.arguments=arguments; start(); }
  private static String hash(byte[] b) throws Exception {
    byte[] d=MessageDigest.getInstance("SHA-256").digest(b);StringBuilder s=new StringBuilder();
    for(byte x:d)s.append(String.format("%02x",x&255));return s.toString();
  }
  private void write(String name,byte[] data) throws Exception {
    try(FileOutputStream f=new FileOutputStream(new File(directory,name))){f.write(data);}
  }
  private void flush() throws Exception { write("result.json",report.toString(2).getBytes("UTF-8")); }
  private static void failure(JSONObject target,String stage,Throwable error) throws Exception {
    StringWriter s=new StringWriter();error.printStackTrace(new PrintWriter(s));
    target.put("earliest_failing_stage",stage);target.put("exception_type",error.getClass().getName());
    target.put("exception_message",error.getMessage());target.put("stack_trace",s.toString());
    target.put(stage+"_status","FAIL");
  }
  @Override public void onStart() {
    ContractModel model=null;String stage="model_loading";
    try {
      Context context=getTargetContext();directory=new File(context.getFilesDir(),"evidence");directory.mkdirs();
      report=new JSONObject().put("variant",arguments.getString("variant","unknown"))
        .put("interface","ContractModel.newInstance -> process -> Outputs.getProbabilityAsCategoryList")
        .put("runtime","TensorFlow Lite 2.13.0; Support 0.4.4; CPU one thread")
        .put("platform",android.os.Build.FINGERPRINT).put("api",android.os.Build.VERSION.SDK_INT);
      flush();
      model=ContractModel.newInstance(context,"model.tflite",
          new Model.Options.Builder().setDevice(Model.Device.CPU).setNumThreads(1).build());
      report.put("model_loading_status","PASS");report.put("loaded_label_count",model.getMetadata().getProbabilityLabels().size());
      JSONArray observations=new JSONArray();report.put("observations",observations);flush();
      for(String name:new String[]{"gray127","rgb_pattern"}) {
        JSONObject row=new JSONObject().put("input",name);observations.put(row);stage="input_preparation";
        try {
          int width=224,height=224;int[] pixels=new int[width*height];byte[] rgb=new byte[width*height*3];
          for(int i=0;i<pixels.length;i++) {
            int r=name.equals("gray127")?127:((37*(3*i)+17)&255);
            int g=name.equals("gray127")?127:((37*(3*i+1)+17)&255);
            int b=name.equals("gray127")?127:((37*(3*i+2)+17)&255);
            pixels[i]=0xff000000|(r<<16)|(g<<8)|b;rgb[3*i]=(byte)r;rgb[3*i+1]=(byte)g;rgb[3*i+2]=(byte)b;
          }
          Bitmap bitmap=Bitmap.createBitmap(pixels,width,height,Bitmap.Config.ARGB_8888);
          TensorImage input=new TensorImage(DataType.UINT8);input.load(bitmap);
          write(name+"-input.rgb",rgb);row.put("input_sha256",hash(rgb));row.put("input_preparation_status","PASS");flush();
          stage="inference";ContractModel.Outputs output=model.process(input);
          row.put("inference_status","PASS");flush();
          stage="raw_output_observation";
          ByteBuffer buffer=((ByteBuffer)output.getBuffer().get(0)).duplicate().order(ByteOrder.nativeOrder());
          buffer.rewind();byte[] raw=new byte[buffer.remaining()];buffer.get(raw);write(name+"-output-0.f32",raw);
          row.put("raw_output_sha256",hash(raw));row.put("raw_output_bytes",raw.length);
          float[] scores=new float[raw.length/4];ByteBuffer.wrap(raw).order(ByteOrder.nativeOrder()).asFloatBuffer().get(scores);
          JSONArray top=new JSONArray();boolean[] used=new boolean[scores.length];
          for(int k=0;k<5;k++){int best=-1;for(int j=0;j<scores.length;j++)if(!used[j]&&(best<0||scores[j]>scores[best]))best=j;
            used[best]=true;top.put(new JSONObject().put("index",best).put("score",scores[best]).put("score_float_bits",Float.floatToIntBits(scores[best])));}
          row.put("top5_raw",top);row.put("raw_output_observation_status","PASS");flush();
          stage="generated_getter";
          List<Category> categories=output.getProbabilityAsCategoryList();
          JSONArray decoded=new JSONArray();
          for(int i=0;i<categories.size();i++){Category c=categories.get(i);decoded.put(new JSONObject().put("list_position",i).put("category_index_field",c.getIndex()).put("label",c.getLabel()).put("score",c.getScore()).put("score_float_bits",Float.floatToIntBits(c.getScore())));}
          write(name+"-decoded.json",decoded.toString(2).getBytes("UTF-8"));
          row.put("category_count",categories.size());row.put("generated_getter_status","PASS");
        } catch(Throwable error) {failure(row,stage,error);Log.e("ContractEvidence",stage,error);}
        flush();
      }
    } catch(Throwable error) {
      try{if(report!=null){failure(report,stage,error);flush();}}catch(Exception ignored){}
      Log.e("ContractEvidence",stage,error);
    } finally {
      if(model!=null)model.close();
      Bundle end=new Bundle();end.putString("evidence","files/evidence/result.json");finish(0,end);
    }
  }
}
