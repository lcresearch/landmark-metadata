package org.example.contract;
import android.app.Instrumentation;
import android.content.Context;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.util.Log;
import java.io.*;
import java.security.MessageDigest;
import java.util.List;
import org.json.*;
import org.tensorflow.lite.DataType;
import org.tensorflow.lite.support.image.TensorImage;
import org.tensorflow.lite.support.label.Category;
import org.tensorflow.lite.task.core.BaseOptions;
import org.tensorflow.lite.task.vision.classifier.ImageClassifier;
import org.tensorflow.lite.task.vision.classifier.Classifications;

/** Real published Android Task API; classify is an atomic public inference+decode boundary. */
public final class TaskInstrumentation extends Instrumentation {
  private Bundle arguments;private JSONObject report;private File directory;
  @Override public void onCreate(Bundle b){super.onCreate(b);arguments=b;start();}
  private static String hash(byte[] b)throws Exception{StringBuilder s=new StringBuilder();for(byte x:MessageDigest.getInstance("SHA-256").digest(b))s.append(String.format("%02x",x&255));return s.toString();}
  private void write(String n,byte[] b)throws Exception{try(FileOutputStream f=new FileOutputStream(new File(directory,n))){f.write(b);}}
  private void flush()throws Exception{write("result.json",report.toString(2).getBytes("UTF-8"));}
  private static void failure(JSONObject j,String stage,Throwable t)throws Exception{StringWriter w=new StringWriter();t.printStackTrace(new PrintWriter(w));JSONArray chain=new JSONArray();for(Throwable c=t;c!=null;c=c.getCause())chain.put(new JSONObject().put("type",c.getClass().getName()).put("message",c.getMessage()));j.put("cause_chain",chain);j.put("earliest_failing_stage",stage).put(stage+"_status","FAIL").put("exception_type",t.getClass().getName()).put("exception_message",t.getMessage()).put("stack_trace",w.toString());}
  @Override public void onStart(){ImageClassifier classifier=null;String stage="asset_identity";
    try{Context context=getTargetContext();directory=new File(context.getFilesDir(),"evidence");directory.mkdirs();report=new JSONObject().put("variant",arguments.getString("variant","unknown")).put("interface","ImageClassifier.createFromFileAndOptions -> classify(TensorImage)").put("runtime","Task Vision0.4.4 published native; CPU default one thread; bundled interpreter version not inferred from standalone JNI").put("platform",android.os.Build.FINGERPRINT).put("api",android.os.Build.VERSION.SDK_INT);flush();
      final String asset="model.tflite";try(InputStream in=context.getAssets().open(asset);ByteArrayOutputStream copy=new ByteArrayOutputStream()){byte[] chunk=new byte[8192];int n;while((n=in.read(chunk))!=-1)copy.write(chunk,0,n);report.put("loaded_asset_name",asset).put("loaded_asset_sha256",hash(copy.toByteArray())).put("loaded_asset_bytes",copy.size()).put("asset_identity_status","PASS");}flush();
      stage="model_initialization";ImageClassifier.ImageClassifierOptions options=ImageClassifier.ImageClassifierOptions.builder().setBaseOptions(BaseOptions.builder().setNumThreads(1).build()).setMaxResults(1000).build();classifier=ImageClassifier.createFromFileAndOptions(context,asset,options);report.put("model_initialization_status","PASS");JSONArray observations=new JSONArray();report.put("observations",observations);flush();
      for(String name:new String[]{"gray127","rgb_pattern"}){JSONObject row=new JSONObject().put("input",name);observations.put(row);stage="input_preparation";
        try{int width=224,height=224;int[] pixels=new int[width*height];byte[] rgb=new byte[width*height*3];for(int i=0;i<pixels.length;i++){int r=name.equals("gray127")?127:((37*(3*i)+17)&255);int g=name.equals("gray127")?127:((37*(3*i+1)+17)&255);int b=name.equals("gray127")?127:((37*(3*i+2)+17)&255);pixels[i]=0xff000000|(r<<16)|(g<<8)|b;rgb[3*i]=(byte)r;rgb[3*i+1]=(byte)g;rgb[3*i+2]=(byte)b;}
          Bitmap bitmap=Bitmap.createBitmap(pixels,width,height,Bitmap.Config.ARGB_8888);TensorImage image=new TensorImage(DataType.UINT8);image.load(bitmap);write(name+"-input.rgb",rgb);row.put("input_sha256",hash(rgb)).put("input_preparation_status","PASS");flush();
          stage="classify_inference_and_decoding";List<Classifications> heads=classifier.classify(image);row.put("classify_inference_and_decoding_status","PASS");JSONArray decoded=new JSONArray();for(Classifications h:heads){JSONArray cats=new JSONArray();for(Category c:h.getCategories())cats.put(new JSONObject().put("category_index_field",c.getIndex()).put("label",c.getLabel()).put("display_name",c.getDisplayName()).put("score",c.getScore()).put("score_float_bits",Float.floatToIntBits(c.getScore())));decoded.put(new JSONObject().put("head_index",h.getHeadIndex()).put("categories",cats));}write(name+"-decoded.json",decoded.toString(2).getBytes("UTF-8"));row.put("head_count",heads.size());
        }catch(Throwable t){failure(row,stage,t);Log.e("ContractEvidence",stage,t);}flush();}
    }catch(Throwable t){try{if(report!=null){failure(report,stage,t);flush();}}catch(Exception ignored){}Log.e("ContractEvidence",stage,t);}finally{if(classifier!=null)classifier.close();Bundle end=new Bundle();end.putString("evidence","files/evidence/result.json");finish(0,end);}}
}
