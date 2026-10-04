"""Check source-only scope and imported bytes without running experiments."""
from pathlib import Path
import ast
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_SUFFIXES = {
    '.apk','.aab','.aar','.jar','.class','.dex','.so','.dll','.dylib','.o','.a',
    '.exe','.tflite','.task','.onnx','.pb','.npz','.npy','.bin','.img','.qcow2',
    '.zip','.gz','.zst','.tar','.whl','.pdf','.png','.jpg','.jpeg','.webp',
    '.log','.stdout','.stderr','.pyc','.keystore','.jks','.pem','.key','.p12','.pfx',
    '.aux','.out','.fls','.fdb_latexmk',
}
FORBIDDEN_DIRS = {'.venv','venv','sdk','toolchains','downloads','deps','wheels',
                  'build','dist','target','generated','patched','preview',
                  'executions','outputs','runtime','__pycache__'}
SECRET_PATTERNS = [
    re.compile(rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
    re.compile(rb'\bgh[pousr]_[A-Za-z0-9]{30,}\b'),
    re.compile(rb'\bgithub_pat_[A-Za-z0-9_]{40,}\b'),
    re.compile(rb'\bAKIA[A-Z0-9]{16}\b'),
]

def main():
    rows = json.loads((ROOT/'docs/SOURCE_IMPORT.json').read_text())['files']
    failures = []
    for row in rows:
        p = ROOT/row['repository_path']
        if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=row['sha256']:
            failures.append({'path':row['repository_path'],'issue':'imported bytes differ'})
    counts = {'files':0,'python_syntax':0,'shell_syntax':0,'json_parse':0}
    for p in sorted(ROOT.rglob('*')):
        rel=p.relative_to(ROOT)
        if '.git' in rel.parts or not p.is_file():
            continue
        counts['files']+=1
        if p.is_symlink() or p.suffix.lower() in FORBIDDEN_SUFFIXES or FORBIDDEN_DIRS.intersection(rel.parts):
            failures.append({'path':str(rel),'issue':'excluded artifact type/path'})
            continue
        data=p.read_bytes()
        if len(data)>1_000_000 or b'\x00' in data:
            failures.append({'path':str(rel),'issue':'unexpected large/binary content'})
        for pattern in SECRET_PATTERNS:
            if pattern.search(data):
                failures.append({'path':str(rel),'issue':'credential-like content; value suppressed'})
        try:
            source=data.decode('utf-8')
            if p.suffix=='.py':
                ast.parse(source,filename=str(rel));counts['python_syntax']+=1
            elif p.suffix=='.sh':
                checked=subprocess.run(['bash','-n',str(p)],capture_output=True)
                if checked.returncode:
                    failures.append({'path':str(rel),'issue':'bash syntax check failed'})
                else: counts['shell_syntax']+=1
            elif p.suffix=='.json':
                json.loads(source);counts['json_parse']+=1
        except (UnicodeError,SyntaxError,ValueError) as exc:
            failures.append({'path':str(rel),'issue':type(exc).__name__})
    # Root navigation must point to actual files/directories. Historical imported
    # reports intentionally retain external paths and are not made portable here.
    for name in ['README.md','MEMORY.md','TODO.md']:
        for target in re.findall(r'\]\(([^)]+)\)', (ROOT/name).read_text()):
            if '://' not in target and not target.startswith('#') and not (ROOT/target.split('#')[0]).exists():
                failures.append({'path':name,'issue':'broken root navigation','target':target})
    print(json.dumps({'status':'FAIL' if failures else 'PASS','checks':counts,
                      'imported_files_verified':len(rows),'failures':failures,
                      'model_experiments_run':False},indent=2))
    raise SystemExit(bool(failures))

if __name__=='__main__':
    main()
