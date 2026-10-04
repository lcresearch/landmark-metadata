"""Isolated process boundary for the native generator."""
from pathlib import Path
import json
import sys
from tensorflow_lite_support.codegen.python import _pywrap_codegen

model=Path(sys.argv[1]);dest=Path(sys.argv[2]);status=Path(sys.argv[3])
generator=_pywrap_codegen.AndroidJavaGenerator(str(dest))
result=generator.generate(model.read_bytes(),'org.example.contract','ContractModel','model.tflite')
files=[]
for file in result.files:
    p=Path(file.path);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(file.content)
    files.append(str(p))
status.write_text(json.dumps({'files':files,'diagnostics':generator.get_error_message(),'success':bool(files)},indent=2))

