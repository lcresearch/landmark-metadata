#!/usr/bin/env python3
"""Read-only bounded local evidence search; writes only this report directory."""
import collections
import datetime
import fnmatch
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tarfile
import zipfile

ROOT = Path('/workspace')
OUT = ROOT / 'evidence-recovery-20261005T170453Z/search'
REPO = ROOT / 'landmark-evidence-recovery'
LIMIT = 8 * 1024 * 1024
ARCHIVE_LIMIT = 128 * 1024 * 1024
MEMBER_LIMIT = 20000
HASH_LIMIT = 4000
PIN = 'bf49a475696eec4b38fb17587f6541a8393da14297e5dca1d433a051ba166e79'
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
inputs = json.loads((REPO / 'docs/reproduction/inputs.json').read_text())
claim_source = REPO / 'sources/repro-audit-20261004/claims/claim-map.json'
claims = json.loads(claim_source.read_text())
expected = {}
def collect(obj):
    if isinstance(obj, dict):
        p = obj.get('path', '')
        if p.startswith('/workspace/repro-') and obj.get('sha256'):
            expected[p] = obj['sha256']
        for value in obj.values():
            collect(value)
    elif isinstance(obj, list):
        for value in obj:
            collect(value)
collect(claims)
by_hash = collections.defaultdict(list)
for p, h in expected.items():
    by_hash[h].append(p)
target_names = {Path(p).name for p in expected}
target_names.add('reproduction-evidence-index-20261004.json')
excluded_dirs = [
    '.git', '.venv*', 'venv*', '*-venv*', 'site-packages', 'dist-packages',
    'node_modules', '__pycache__', '.pytest_cache', '.mypy_cache', '.cache',
    '.gradle', 'gradle-cache*', 'gradle-home*', 'dependencies', 'deps',
    'android-sdk*', '*-android-sdk*', 'sdk', 'sdk-*', 'sdk_root', 'android_sdk',
    'sdk-home', 'sdk_home', 'avd', 'avds', '*-avd*', '*.avd', 'avd-home',
    '.android', 'system-images', 'platform-tools', 'build-tools',
    'jdk*', 'openjdk*', 'toolchain*', '.ssh', '.aws', '.azure', '.gcloud',
    '.config', 'credentials', 'secrets', 'evidence-recovery-20261005T170453Z',
]
excluded_files = [
    '.env', '.env.*', '*credential*', '*secret*', '*token*', '*.pem', '*.key',
    '*.p12', '*.pfx', 'id_rsa*', 'id_ed25519*', '.netrc', '.git-credentials',
    '*publish-state*', '*publication*', 'publish_*.py',
]
globs = ['!**/' + x + '/**' for x in excluded_dirs]
globs += ['!**/' + x for x in excluded_files]
cmd = ['rg', '--files', '--hidden', '--no-ignore', '-0']
for g in globs:
    cmd += ['-g', g]
cmd.append(str(ROOT))
scan = subprocess.run(cmd, capture_output=True, check=False)
paths = sorted({Path(p.decode()) for p in scan.stdout.split(b'\0') if p})
(OUT / 'scanned-file-paths.txt').write_text(''.join(str(p) + '\n' for p in paths))
(OUT / 'rg-enumeration-stderr.txt').write_bytes(scan.stderr)
top_counts = collections.Counter(p.relative_to(ROOT).parts[0] for p in paths)
safe_suffixes = {'.json', '.jsonl', '.ndjson'}
archive_suffixes = ('.zip', '.tar', '.tar.gz', '.tgz', '.tar.xz', '.txz', '.tar.bz2')
path_pattern = re.compile(r'(repro-(?:android|task|hand|external|claims|audit|control)(?:/|$)|reproduction-evidence-index|(?:^|/)E5/(?:results|replay-summary|core-baseline-comparison)\.json$)')
candidate_paths = [p for p in paths if path_pattern.search(str(p))]
hashes = []
hash_skips = []
matches = []
errors = []
for p in paths:
    if not (p.suffix.lower() in safe_suffixes or p.name in target_names):
        continue
    if p.is_symlink():
        hash_skips.append({'path': str(p), 'reason': 'symlink_not_followed'})
        continue
    try:
        size = p.stat().st_size
        if size > LIMIT or len(hashes) >= HASH_LIMIT:
            hash_skips.append({'path': str(p), 'bytes': size, 'reason': 'size_or_count_limit'})
            continue
        digest = hashlib.sha256(p.read_bytes()).hexdigest()
        entry = {'path': str(p), 'bytes': size, 'sha256': digest}
        hashes.append(entry)
        if digest in by_hash:
            matches.append({**entry, 'matching_recorded_paths': by_hash[digest]})
    except OSError as e:
        errors.append({'path': str(p), 'error': str(e)})
archive_results = []
archive_hash_matches = []
expected_archives = {a['path']: a for a in inputs['historical_archive_locators']}
def member_safe(name):
    parts = Path(name).parts
    return not any(fnmatch.fnmatchcase(part, pat) for part in parts for pat in excluded_dirs + excluded_files)
for p in paths:
    if not str(p).lower().endswith(archive_suffixes):
        continue
    result = {'path': str(p)}
    try:
        size = p.stat().st_size
        result['bytes'] = size
        if p.is_symlink() or size > ARCHIVE_LIMIT:
            result['status'] = 'SKIPPED_SYMLINK_OR_ARCHIVE_SIZE_LIMIT'
            archive_results.append(result)
            continue
        result['sha256'] = hashlib.sha256(p.read_bytes()).hexdigest()
        if str(p) in expected_archives:
            result['expected_sha256'] = expected_archives[str(p)]['expected_sha256']
            result['hash_matches_input_pin'] = result['sha256'] == result['expected_sha256']
        if zipfile.is_zipfile(p):
            with zipfile.ZipFile(p) as z:
                entries = z.infolist()
                names = [e.filename for e in entries]
                result['format'] = 'zip'
                if len(entries) <= MEMBER_LIMIT:
                    for e in entries:
                        name = e.filename
                        if (not e.is_dir() and member_safe(name) and e.file_size <= LIMIT
                                and (Path(name).suffix.lower() in safe_suffixes or Path(name).name in target_names)):
                            digest = hashlib.sha256(z.read(e)).hexdigest()
                            if digest in by_hash:
                                archive_hash_matches.append({'archive': str(p), 'member': name, 'bytes': e.file_size, 'sha256': digest, 'matching_recorded_paths': by_hash[digest]})
                    result['safe_target_members_hashed'] = sum(not e.is_dir() and member_safe(e.filename) and e.file_size <= LIMIT and (Path(e.filename).suffix.lower() in safe_suffixes or Path(e.filename).name in target_names) for e in entries)
        else:
            with tarfile.open(p, 'r:*') as t:
                entries = t.getmembers()
                names = [e.name for e in entries]
                result['format'] = 'tar'
                if len(entries) <= MEMBER_LIMIT:
                    for e in entries:
                        if e.isfile() and member_safe(e.name) and e.size <= LIMIT and (Path(e.name).suffix.lower() in safe_suffixes or Path(e.name).name in target_names):
                            with t.extractfile(e) as f:
                                digest = hashlib.sha256(f.read()).hexdigest()
                            if digest in by_hash:
                                archive_hash_matches.append({'archive': str(p), 'member': e.name, 'bytes': e.size, 'sha256': digest, 'matching_recorded_paths': by_hash[digest]})
                    result['safe_target_members_hashed'] = sum(e.isfile() and member_safe(e.name) and e.size <= LIMIT and (Path(e.name).suffix.lower() in safe_suffixes or Path(e.name).name in target_names) for e in entries)
        result['entry_count'] = len(names)
        result['top_level_names'] = sorted({name.split('/')[0] for name in names})
        result['target_name_matches'] = [name for name in names if path_pattern.search(name)]
        listing = 'archive-' + hashlib.sha256(str(p).encode()).hexdigest()[:12] + '-entries.txt'
        (OUT / listing).write_text(''.join(name + '\n' for name in names))
        result['entry_listing'] = listing
        result['status'] = 'DIRECTORY_LISTED_AND_SAFE_TARGET_MEMBERS_HASHED' if len(names) <= MEMBER_LIMIT else 'DIRECTORY_LISTED_MEMBER_HASHING_SKIPPED_COUNT_LIMIT'
    except (OSError, zipfile.BadZipFile, tarfile.TarError, RuntimeError) as e:
        result['status'] = 'ERROR'
        result['error'] = str(e)
    archive_results.append(result)
exact = []
for obj in inputs['reconstruction_evidence_locations']:
    p = Path(obj['path'])
    exact.append({'path': str(p), 'expected_sha256': obj.get('expected_sha256'), 'present': p.exists(), 'is_symlink': p.is_symlink(), 'status': 'PRESENT' if p.exists() else 'MISSING_AT_CHECKED_PATH'})
report = {
    'schema_version': 1,
    'started_at_utc': started,
    'finished_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'read_only_scope': 'No historical source/evidence changes; no historical scripts or models executed; no network or remote stores accessed. New output is confined to this search report directory.',
    'search_root': str(ROOT), 'explicit_requested_scopes': [{'path': str(ROOT / s), 'present': (ROOT / s).exists(), 'enumerated_files': top_counts.get(s, 0)} for s in ('scratch', 'shared', 'library-files')],
    'rg_enumeration_command': cmd, 'rg_returncode': scan.returncode,
    'excluded_directory_patterns': excluded_dirs, 'excluded_file_patterns': excluded_files,
    'symlink_policy': 'rg defaults: do not follow directory symlinks; candidate file symlinks are not hashed',
    'limits': {'eligible_hash_file_bytes': LIMIT, 'eligible_hash_file_count': HASH_LIMIT, 'archive_bytes': ARCHIVE_LIMIT, 'archive_entry_count_for_member_hashing': MEMBER_LIMIT},
    'hash_candidate_selection': 'All enumerated .json/.jsonl/.ndjson files and all basenames in the 38-file reconstruction claim-map; only regular files up to limits. Hash safe matching members inside inspected archives without extraction.',
    'top_level_enumerated_file_counts': dict(sorted(top_counts.items())), 'enumerated_files': len(paths),
    'inventory_file': 'scanned-file-paths.txt', 'exact_locator_results': exact,
    'recorded_hash_source': {'path': str(claim_source), 'sha256': hashlib.sha256(claim_source.read_bytes()).hexdigest()},
    'recorded_reconstruction_files': [{'path': p, 'sha256': h} for p, h in sorted(expected.items())],
    'path_name_candidates': [str(p) for p in candidate_paths], 'eligible_files_hashed': len(hashes),
    'hashes_file': 'candidate-hashes.json', 'hash_matches': matches, 'hash_skips': hash_skips,
    'archives': archive_results, 'archive_member_hash_matches': archive_hash_matches,
    'e5_manifest_pin': PIN,
    'e5_manifest_matches': [m for m in matches + archive_hash_matches if m['sha256'] == PIN],
    'errors': errors,
    'limits_statement': 'Negative results apply only to the enumerated local scope and safe candidate classes/limits. No universal absence claim; excluded toolchains/dependencies/AVD/Git/credential paths, unexamined formats, remote stores and other machines were not searched.'
}
(OUT / 'candidate-hashes.json').write_text(json.dumps(hashes, indent=2) + '\n')
(OUT / 'search-results.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({'enumerated_files': len(paths), 'hashed': len(hashes), 'hash_matches': matches, 'archive_member_hash_matches': archive_hash_matches, 'archive_summaries': [{k: v for k, v in a.items() if k != 'target_name_matches'} for a in archive_results], 'explicit_scopes': report['explicit_requested_scopes'], 'hash_skips': len(hash_skips), 'errors': errors}, indent=2))
