#!/usr/bin/env python3
"""Stage selected historical bytes outside Git; never execute model code.

The plan pins historical manifest digests. New package integrity is separate
from historical identity, evidence completeness and experimental truth.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat


def digest(path):
    value = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            value.update(chunk)
    return value.hexdigest()


def safe_relative(value):
    path = PurePosixPath(value)
    if (not value or value == '.' or path.is_absolute() or '..' in path.parts
            or str(path) != value or '\\' in value or '\n' in value
            or any(ord(char) < 32 or ord(char) == 127 for char in value)):
        raise ValueError(f'Unsafe/noncanonical relative path: {value!r}')
    return path


def read_manifest(path, expected):
    if path.is_symlink() or digest(path) != expected:
        raise ValueError(f'Historical manifest identity mismatch: {path}')
    rows = {}
    for line in path.read_text().splitlines():
        match = re.fullmatch(r'([0-9a-f]{64}) [ *](.+)', line)
        if not match:
            raise ValueError(f'Malformed manifest entry in {path}')
        name = str(safe_relative(match[2]))
        if name in rows:
            raise ValueError(f'Duplicate manifest path: {name}')
        rows[name] = match[1]
    return rows


def exclusion(name, root, plan):
    parts = safe_relative(name).parts
    if name in root.get('include_metadata_files', []):
        return None
    if any(p in plan['excluded_directory_names'] for p in parts[:-1]):
        return 'EXCLUDED_TOOLCHAIN_CACHE_OR_DEPENDENCIES'
    if parts[-1] in plan['excluded_file_names']:
        return 'EXCLUDED_REDUNDANT_APK_INTERMEDIATE'
    if Path(parts[-1]).suffix.lower() in plan['excluded_file_suffixes']:
        return 'EXCLUDED_KEY_OR_CACHE_FILE'
    if len(parts) == 1:
        return None if root['include_root_files'] else 'OUTSIDE_SELECTED_SCOPE'
    if parts[0] not in root['include_directories']:
        return 'OUTSIDE_SELECTED_SCOPE'
    return None


def list_files(source, root, plan):
    """No symlink traversal; record excluded directories without opening them."""
    paths, skipped = [], []
    for base, dirs, files in os.walk(source, followlinks=False):
        base = Path(base)
        keep = []
        for name in sorted(dirs):
            p = base/name
            rel = p.relative_to(source).as_posix()
            if p.is_symlink():
                reason = 'EXCLUDED_SYMLINK'
            elif name in plan['excluded_directory_names']:
                reason = 'EXCLUDED_TOOLCHAIN_CACHE_OR_DEPENDENCIES'
            elif base == source and name not in root['include_directories']:
                reason = 'OUTSIDE_SELECTED_SCOPE'
            else:
                keep.append(name)
                continue
            skipped.append({'path':rel, 'reason':reason, 'kind':'directory'})
        dirs[:] = keep
        for name in sorted(files):
            p = base/name
            rel = p.relative_to(source).as_posix()
            reason = 'EXCLUDED_SYMLINK' if p.is_symlink() else exclusion(rel, root, plan)
            if reason:
                skipped.append({'path':rel, 'reason':reason, 'kind':'file'})
            else:
                paths.append(rel)
    for name in root.get('include_metadata_files', []):
        p = source/str(safe_relative(name))
        if p.is_symlink() or any(parent.is_symlink() for parent in p.parents):
            skipped.append({'path':name, 'reason':'EXCLUDED_SYMLINK', 'kind':'file'})
        elif p.is_file() and name not in paths:
            paths.append(name)
    return sorted(paths), skipped


def dump(path, value):
    with path.open('x') as output:
        output.write(json.dumps(value, indent=2) + '\n')


def stage(plan_path, destination):
    plan = json.loads(plan_path.read_text())
    repo = Path(__file__).resolve().parents[2]
    if destination.is_symlink() or any(p.is_symlink() for p in destination.parents):
        raise ValueError('Output path must not contain symlinks')
    destination = destination.resolve()
    if destination.is_relative_to(repo) or destination.exists():
        raise ValueError('Use a new output directory outside the source repository')
    prefixes = [str(safe_relative(r['destination_prefix'])) for r in plan['roots']]
    if len(prefixes) != len(set(prefixes)):
        raise ValueError('Duplicate destination prefix')
    contexts = []
    for root in plan['roots']:
        for name in root.get('include_metadata_files', []):
            p = safe_relative(name)
            if p.suffix not in {'.json', '.xml', '.pom', '.txt'} and p.name != 'LICENSE':
                raise ValueError('Dependency metadata exception is not a supported text type')
        source = Path(root['source_root'])
        if source.is_symlink() or not source.is_dir():
            raise ValueError(f'Unavailable/non-direct source root: {source}')
        if destination.is_relative_to(source.resolve()) or source.resolve().is_relative_to(destination):
            raise ValueError('Source and destination must be separate trees')
        manifest = source/str(safe_relative(root['manifest']))
        if any(p.is_symlink() for p in manifest.parents):
            raise ValueError('Historical manifest ancestors must not be symlinks')
        contexts.append((root, source, read_manifest(manifest, root['manifest_sha256'])))
    supplements = []
    by_id = {r['id']:(r, s, m) for r, s, m in contexts}
    for extra in plan.get('supplementary_files', []):
        name = str(safe_relative(extra['destination']))
        if not name.startswith('SUPPLEMENTARY_SOURCE/'):
            raise ValueError('Supplementary sources need a separate payload namespace')
        if any(name == p or name.startswith(p + '/') for p in prefixes):
            raise ValueError('Supplementary source overlaps a root prefix')
        _, source, anchored = by_id[extra['reference_root_id']]
        ref_name = str(safe_relative(extra['reference_record']))
        ref = source/ref_name
        if ref.is_symlink() or any(p.is_symlink() for p in ref.parents):
            raise ValueError('Supplementary reference must not use symlinks')
        if ref_name not in anchored or digest(ref) != anchored[ref_name]:
            raise ValueError('Supplementary source reference is not historically anchored')
        value = json.loads(ref.read_text())
        for key in extra['digest_selector']:
            value = value[key]
        if value != extra['expected_sha256']:
            raise ValueError('Supplementary digest differs from its historical reference')
        original = Path(extra['source_path'])
        if original.is_symlink() or not original.is_file() or any(p.is_symlink() for p in original.parents):
            raise ValueError('Supplementary source must be an existing non-symlink file')
        supplements.append((extra, original, name))
    destination.mkdir(parents=True, exist_ok=False)
    rows, issues, omitted, roots = [], [], [], []
    for root, source, expected in contexts:
        names, skipped = list_files(source, root, plan)
        omitted.extend({'root_id':root['id'], **item} for item in skipped)
        actual = set(names)
        for name, sha in expected.items():
            reason = exclusion(name, root, plan)
            if reason:
                omitted.append({'root_id':root['id'], 'path':name,
                                'reason':reason, 'kind':'manifest_entry', 'expected_sha256':sha})
            elif name not in actual:
                issues.append({'root_id':root['id'], 'path':name,
                               'issue':'EXPECTED_SELECTED_FILE_MISSING_OR_SYMLINK', 'expected_sha256':sha})
        for name in names:
            original = source/name
            if not stat.S_ISREG(original.lstat().st_mode):
                raise ValueError(f'Non-regular source file: {original}')
            target_rel = f"payload/{root['destination_prefix']}/{name}"
            target = destination/target_rel
            target.parent.mkdir(parents=True, exist_ok=True)
            before = original.stat()
            # Copy, never move, hard-link or edit the preserved original.
            with original.open('rb') as src, target.open('xb') as dst:
                shutil.copyfileobj(src, dst, 1024 * 1024)
            current_sha = digest(target)
            after = original.stat()
            stable = ((before.st_size, before.st_mtime_ns, before.st_ino)
                      == (after.st_size, after.st_mtime_ns, after.st_ino))
            historical = root['manifest_sha256'] if name == root['manifest'] else expected.get(name)
            status = ('MATCH_HISTORICAL_MANIFEST' if historical == current_sha else
                      'UNLISTED_CURRENT_COPY' if historical is None else 'HISTORICAL_DIGEST_MISMATCH')
            row = {'path':target_rel, 'source_path':str(original), 'root_id':root['id'],
                   'bytes':target.stat().st_size, 'sha256':current_sha,
                   'historical_expected_sha256':historical, 'identity_status':status,
                   'source_stat_unchanged_during_copy':stable}
            rows.append(row)
            if status != 'MATCH_HISTORICAL_MANIFEST' or not stable:
                issues.append({'root_id':root['id'], 'path':name, 'issue':status if stable else 'SOURCE_CHANGED_DURING_COPY'})
        roots.append({'id':root['id'], 'source_root':str(source),
                      'manifest_sha256':root['manifest_sha256'],
                      'historical_manifest_entries':len(expected), 'selected_files':len(names)})
    for extra, original, name in supplements:
        target_rel = f'payload/{name}'
        target = destination/target_rel
        target.parent.mkdir(parents=True, exist_ok=True)
        before = original.stat()
        with original.open('rb') as src, target.open('xb') as dst:
            shutil.copyfileobj(src, dst, 1024 * 1024)
        current_sha = digest(target)
        after = original.stat()
        stable = ((before.st_size, before.st_mtime_ns, before.st_ino)
                  == (after.st_size, after.st_mtime_ns, after.st_ino))
        status = ('MATCH_HISTORICAL_REFERENCE' if current_sha == extra['expected_sha256']
                  else 'HISTORICAL_DIGEST_MISMATCH')
        rows.append({'path':target_rel, 'source_path':str(original), 'root_id':'SUPPLEMENTARY_SOURCE',
                     'bytes':target.stat().st_size, 'sha256':current_sha,
                     'historical_expected_sha256':extra['expected_sha256'], 'identity_status':status,
                     'reference_root_id':extra['reference_root_id'], 'reference_record':extra['reference_record'],
                     'digest_selector':extra['digest_selector'], 'source_stat_unchanged_during_copy':stable})
        if status != 'MATCH_HISTORICAL_REFERENCE' or not stable:
            issues.append({'root_id':'SUPPLEMENTARY_SOURCE', 'path':name,
                           'issue':status if stable else 'SOURCE_CHANGED_DURING_COPY'})
    manifest = {'schema_version':1, 'created_utc':datetime.now(timezone.utc).isoformat(),
                'scope':plan['scope'], 'plan_sha256':digest(plan_path),
                'source_repository_base_commit':plan['repository_base_commit'],
                'status':'IDENTITY_ISSUES' if issues else 'SELECTED_HISTORICAL_BYTES_MATCH',
                'roots':roots, 'files':rows, 'issues':issues,
                'exclusion_record':'EXCLUSIONS.json',
                'limits':['Selected saved-byte identity only; no model execution or human verification.',
                          'Intentional exclusions prevent a complete/offline reproduction claim.',
                          'Local staging is not a durable external deposit.']}
    dump(destination/'MANIFEST.json', manifest)
    dump(destination/'EXCLUSIONS.json', omitted)
    dump(destination/'PACKAGE_PLAN.json', plan)
    with (destination/'SHA256SUMS').open('x') as output:
        for row in rows:
            output.write(f"{row['sha256']}  {row['path']}\n")
        for name in ['MANIFEST.json','EXCLUSIONS.json','PACKAGE_PLAN.json']:
            output.write(f'{digest(destination/name)}  {name}\n')
    print(json.dumps({'status':manifest['status'], 'files':len(rows),
                      'bytes':sum(r['bytes'] for r in rows), 'issues':len(issues),
                      'manifest_sha256':digest(destination/'MANIFEST.json'),
                      'checksum_file_sha256':digest(destination/'SHA256SUMS')}, indent=2))
    return bool(issues)


def verify(package, expected_checksums):
    package = package.resolve()
    expected = read_manifest(package/'SHA256SUMS', expected_checksums)
    actual = set()
    for base, dirs, files in os.walk(package, followlinks=False):
        for name in dirs + files:
            path = Path(base)/name
            if path.is_symlink():
                raise ValueError(f'Symlink in staged package: {path}')
        for name in files:
            actual.add((Path(base)/name).relative_to(package).as_posix())
    if actual != set(expected) | {'SHA256SUMS'}:
        raise ValueError('Package inventory differs from checksum inventory')
    for name, sha in expected.items():
        p = package/name
        if not p.is_file() or digest(p) != sha:
            raise ValueError(f'Package byte mismatch: {name}')
    manifest = json.loads((package/'MANIFEST.json').read_text())
    manifest_paths = [row['path'] for row in manifest['files']]
    if len(manifest_paths) != len(set(manifest_paths)):
        raise ValueError('Duplicate package manifest path')
    if set(manifest_paths) != {p for p in expected if p.startswith('payload/')}:
        raise ValueError('Payload and structured manifest disagree')
    for row in manifest['files']:
        path = package/str(safe_relative(row['path']))
        if row['sha256'] != expected[row['path']] or path.stat().st_size != row['bytes']:
            raise ValueError('Structured manifest byte identity mismatch')
    print(json.dumps({'package_integrity':'PASS', 'payload_files':len(manifest_paths),
                      'historical_identity_status':manifest['status'],
                      'identity_counts':dict(Counter(r['identity_status'] for r in manifest['files'])),
                      'historical_identity_issues':len(manifest['issues']),
                      'experimental_truth_verified':False}, indent=2))
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    create = sub.add_parser('stage')
    create.add_argument('--plan', type=Path, required=True)
    create.add_argument('--output', type=Path, required=True)
    check = sub.add_parser('verify')
    check.add_argument('--package', type=Path, required=True)
    check.add_argument('--checksums-sha256', required=True)
    args = parser.parse_args()
    try:
        code = (stage(args.plan, args.output) if args.command == 'stage'
                else verify(args.package, args.checksums_sha256))
    except (ValueError, OSError, KeyError) as exc:
        parser.exit(1, f'{type(exc).__name__}: {exc}\n')
    raise SystemExit(code)


if __name__ == '__main__':
    main()
