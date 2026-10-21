"""Check source-only scope and imported bytes without running experiments."""
from pathlib import Path
import ast
import hashlib
import json
import re
import subprocess
from urllib.parse import unquote, urlsplit

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

def local_targets(source):
    """Read ordinary inline Markdown links, ignoring fenced examples."""
    source = re.sub(r'^```.*?^```[^\n]*$', '', source, flags=re.M | re.S)
    pattern = r'\]\((?:<([^>]+)>|([^\s)]+))(?:\s+["\'][^\n]*?["\'])?\)'
    for match in re.finditer(pattern, source):
        target = match[1] or match[2]
        parsed = urlsplit(target)
        if not parsed.scheme and not parsed.netloc and not target.startswith('#'):
            yield unquote(parsed.path)


def check_navigation(root, counts, failures, warnings):
    """Current documentation fails on missing targets; imports warn only."""
    for p in sorted(root.rglob('*')):
        rel = p.relative_to(root)
        if '.git' in rel.parts or not p.is_file() or p.is_symlink():
            continue
        historical = rel.parts[0] == 'sources'
        if historical:
            if not p.name.startswith('README') or p.suffix not in {'.md', '.txt'}:
                continue
        elif p.suffix != '.md':
            continue
        try:
            source = p.read_text(encoding='utf-8')
        except UnicodeError:
            continue  # The content/syntax check already reports this.
        targets = set(local_targets(source))
        if historical:
            # Historical READMEs also use backticks for excluded evidence files.
            # Inspect file-like locators, not commands or prose in code spans.
            for target in re.findall(r'`([^`\n]+)`', source):
                if (not re.search(r'\s', target) and not urlsplit(target).scheme
                        and ('/' in target or '.' in Path(target).name
                             or target == 'SHA256SUMS')):
                    targets.add(target)
        for target in sorted(targets):
            counts['navigation_targets'] += 1
            resolved = (p.parent / target).resolve()
            portable = resolved.is_relative_to(root.resolve())
            if not portable or not resolved.exists():
                item = {'path':str(rel), 'issue':'unavailable historical locator'
                        if historical else 'broken documentation navigation',
                        'target':target}
                (warnings if historical else failures).append(item)


def check_memory_hashes(root, rows, counts, failures, warnings):
    """Cross-check import-backed MEMORY digests without trusting external paths."""
    original_rows = {row.get('original_path', row.get('source_path')):row for row in rows}
    source = (root/'MEMORY.md').read_text(encoding='utf-8')
    pattern = r'^\| `([^`]+)` \| [^\n]*?`([^`]+)` SHA-256: `([0-9a-f]{64})`'
    for package, name, expected in re.findall(pattern, source, flags=re.M):
        original = str(Path(package) / name)
        row = original_rows.get(original)
        if row is None:
            item = {'path':'MEMORY.md', 'issue':'external evidence digest not checked',
                    'target':original}
            if name == 'SHA256SUMS':
                warnings.append(item)
            else:
                item['issue'] = 'MEMORY source locator absent from import index'
                failures.append(item)
            continue
        counts['memory_import_hashes'] += 1
        imported = root/row['repository_path']
        if (row['sha256'] != expected or not imported.is_file()
                or hashlib.sha256(imported.read_bytes()).hexdigest() != expected):
            failures.append({'path':'MEMORY.md', 'issue':'MEMORY/import/source hash mismatch',
                             'target':row['repository_path']})


def check_current_manuscript(root, rows, counts, failures):
    index = root/'docs/CURRENT_MANUSCRIPT.json'
    if not index.is_file():
        return
    try:
        current = json.loads(index.read_text())
        entry = re.search(r'\[Current manuscript source\]\(([^)]+)\)',
                          (root/'README.md').read_text())
        if entry is None or entry[1] != current['repository_path']:
            failures.append({'path':'README.md', 'issue':'current manuscript navigation/index mismatch'})
        by_path = {row['repository_path']:row for row in rows}
        parent = current['derived_from_repository_path']
        if (parent not in by_path
                or current['derived_from_sha256'] != by_path[parent]['sha256']):
            failures.append({'path':str(index.relative_to(root)),
                             'issue':'current manuscript/import parent mismatch'})
        required_pins = ['full_companion', 'claim_crosswalk', 'artifact_handoff']
        if 'editorial_predecessor_companion' in current:
            required_pins.append('editorial_predecessor_companion')
        for required in required_pins:
            pin = current.get(required)
            if not isinstance(pin, dict) or not {'path', 'sha256', 'bytes'} <= pin.keys():
                failures.append({'path':str(index.relative_to(root)),
                                 'issue':'missing current artifact pin', 'target':required})

        def verify_pin(path, expected, size):
            if (not isinstance(path, str) or not isinstance(expected, str)
                    or not re.fullmatch(r'[0-9a-f]{64}', expected)
                    or not isinstance(size, int) or isinstance(size, bool) or size < 0):
                raise ValueError('Invalid current artifact pin')
            p = root/path
            counts['manuscript_hashes'] += 1
            if (Path(path).is_absolute() or not p.resolve().is_relative_to(root.resolve())
                    or not p.is_file() or p.is_symlink()
                    or hashlib.sha256(p.read_bytes()).hexdigest() != expected
                    or p.stat().st_size != size):
                failures.append({'path':path, 'issue':'manuscript digest mismatch'})

        verify_pin(current['repository_path'], current['sha256'], current['bytes'])
        verify_pin(parent, current['derived_from_sha256'], by_path[parent]['bytes'])
        for key, path in current.items():
            if key.endswith('_repository_path') and key != 'derived_from_repository_path':
                prefix = key[:-len('_repository_path')]
                # Older predecessor pins omit size; the digest still pins all bytes.
                p = root/path
                size = current.get(prefix+'_bytes', p.stat().st_size if p.is_file() else 0)
                verify_pin(path, current[prefix+'_sha256'], size)

        def nested_pins(value):
            if isinstance(value, dict):
                if 'path' in value or 'sha256' in value:
                    verify_pin(value['path'], value['sha256'], value['bytes'])
                for child in value.values():
                    nested_pins(child)
            elif isinstance(value, list):
                for child in value:
                    nested_pins(child)
        for value in current.values():
            nested_pins(value)
    except (KeyError, TypeError, ValueError, OSError) as exc:
        failures.append({'path':str(index.relative_to(root)), 'issue':type(exc).__name__})


def check_tree(root):
    rows = []
    snapshot_roots = set()
    for name in ['SOURCE_IMPORT.json', 'SOURCE_P2P3.json']:
        manifest = json.loads((root/'docs'/name).read_text())
        rows.extend(manifest['files'])
        snapshot_roots.update(Path(*Path(row['repository_path']).parts[:2])
                              for row in manifest['files'])
        if name == 'SOURCE_IMPORT.json':
            snapshot_roots.update(Path('sources')/name for name in manifest.get('workspace_roots', []))
        else:
            # This import has a fixed destination in import_p2p3_sources.py.
            snapshot_roots.add(Path('research/20261004-p2-p3'))
    failures = []
    warnings = []
    indexed = set()
    for row in rows:
        if row['repository_path'] in indexed:
            failures.append({'path':row['repository_path'], 'issue':'duplicate imported path'})
        indexed.add(row['repository_path'])
        p = root/row['repository_path']
        if (not p.resolve().is_relative_to(root.resolve()) or not p.is_file()
                or p.is_symlink() or hashlib.sha256(p.read_bytes()).hexdigest()!=row['sha256']
                or p.stat().st_size != row['bytes']):
            failures.append({'path':row['repository_path'],'issue':'imported bytes differ'})
    for snapshot in sorted(snapshot_roots):
        if not (root/snapshot).resolve().is_relative_to(root.resolve()):
            failures.append({'path':str(snapshot), 'issue':'invalid imported snapshot root'})
            continue
        for p in sorted((root/snapshot).rglob('*')):
            if (p.is_file() or p.is_symlink()) and p.relative_to(root).as_posix() not in indexed:
                failures.append({'path':p.relative_to(root).as_posix(),
                                 'issue':'unindexed imported snapshot file'})
    counts = {'files':0,'python_syntax':0,'shell_syntax':0,'json_parse':0,
              'navigation_targets':0, 'memory_import_hashes':0, 'manuscript_hashes':0}
    for p in sorted(root.rglob('*')):
        rel=p.relative_to(root)
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
    check_navigation(root, counts, failures, warnings)
    check_memory_hashes(root, rows, counts, failures, warnings)
    check_current_manuscript(root, rows, counts, failures)
    return {'status':'FAIL' if failures else 'PASS', 'checks':counts,
            'imported_files_verified':len(rows) if not any(
                f['issue'] in {'imported bytes differ', 'duplicate imported path',
                              'invalid imported snapshot root', 'unindexed imported snapshot file'}
                for f in failures) else 0,
            'failures':failures, 'warnings':warnings, 'model_experiments_run':False}


def main():
    report = check_tree(ROOT)
    print(json.dumps(report, indent=2))
    raise SystemExit(bool(report['failures']))

if __name__=='__main__':
    main()
