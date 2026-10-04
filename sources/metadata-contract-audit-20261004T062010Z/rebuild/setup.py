from pathlib import Path
import shutil,json,hashlib,difflib
root=Path(__file__).resolve().parent
old=Path('/workspace/metadata-contract-e2e-20261004T030536Z')
(root/'scripts').mkdir();(root/'prerequisites').mkdir();(root/'sdk').mkdir();(root/'logs').mkdir();(root/'source-snapshots').mkdir()
for name in ['common.py','prepare_e1.py','prepare_e2.py','build_android.py','start_emulator.py','run_android.py','ContractInstrumentation.java']:
    shutil.copyfile(old/'scripts'/name,root/'scripts'/name)
    shutil.copyfile(old/'scripts'/name,root/'source-snapshots'/name)
for name in ['aar','extra-jars']:
    shutil.copytree(old/'prerequisites'/name,root/'prerequisites'/name)
for name in ['emulator','platform-tools','build-tools','platforms','system-images']:
    (root/'sdk'/name).symlink_to(old/'sdk'/name,target_is_directory=True)
for name in ['EXPERIMENT_E1_PLAN.md','EXPERIMENT_E2_PLAN.md']:
    shutil.copyfile(old/name,root/name)
h=root/'scripts/ContractInstrumentation.java'
s=h.read_text().replace('import java.io.File;','import java.io.File;\nimport java.io.InputStream;\nimport java.io.ByteArrayOutputStream;')
s=s.replace('      model=ContractModel.newInstance(context,"model.tflite",','''      stage="asset_identity";
      final String modelAsset="model.tflite";
      try(InputStream stream=context.getAssets().open(modelAsset);ByteArrayOutputStream copy=new ByteArrayOutputStream()) {
        byte[] chunk=new byte[8192];int count;
        while((count=stream.read(chunk))!=-1)copy.write(chunk,0,count);
        report.put("loaded_asset_name",modelAsset).put("loaded_asset_sha256",hash(copy.toByteArray()))
          .put("loaded_asset_bytes",copy.size()).put("asset_identity_status","PASS");
      }
      flush();stage="model_loading";
      model=ContractModel.newInstance(context,modelAsset,''')
h.write_text(s)
p=root/'scripts/prepare_e2.py'
s=p.read_text().replace('# Gate execution on complete E1 primary and replay, including all four variants.','# Audit scope: gate on complete fresh E1 primary; historical same-APK replay is not required.')
s=s.replace("for run in ['primary','replay']:","for run in ['primary']:")
p.write_text(s)
for name in ['ContractInstrumentation.java','prepare_e2.py']:
    a=(root/'source-snapshots'/name).read_text();b=(root/'scripts'/name).read_text()
    (root/(name+'.patch')).write_text(''.join(difflib.unified_diff(a.splitlines(True),b.splitlines(True),fromfile='sealed/'+name,tofile='audit/'+name)))
files=[old/'scripts'/p.name for p in (root/'source-snapshots').iterdir()]
(root/'INPUT_PROVENANCE.json').write_text(json.dumps([{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files],indent=2))
