#!/usr/bin/env bash
set -euo pipefail
TASK_AUDIT_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
case "${1:-verify}" in
  verify)
    python3 - "$TASK_AUDIT_ROOT" <<'PY'
import hashlib,json,pathlib,sys
root=pathlib.Path(sys.argv[1]);bad=[];count=0
for line in (root/'SHA256SUMS').read_text().splitlines():
    expected,name=line.split('  ',1);p=root/name;count+=1
    if not p.is_file():bad.append({'path':name,'reason':'MISSING'});continue
    with p.open('rb') as f:got=hashlib.file_digest(f,'sha256').hexdigest()
    if got!=expected:bad.append({'path':name,'reason':'HASH_MISMATCH'})
print(json.dumps({'status':'FAIL' if bad else 'PASS','entries':count,'failures':bad,'human_verification':'PENDING'},indent=2))
sys.exit(bool(bad))
PY
    ;;
  *)
    echo 'Usage: bash commands.sh verify; see README.md for fresh-run scope.' >&2
    exit 2
    ;;
esac
