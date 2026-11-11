"""Import only first-party P2/P3 source and necessary text documentation.

Requires the sealed local workspace; excludes raw evidence and build products.
Refuses to overwrite a changed existing import. No experiment is executed.
"""
from pathlib import Path
import hashlib
import json

REPOSITORY = Path(__file__).resolve().parents[1]
SOURCE = Path('/workspace/metadata-contract-p2p3-20261004T073824Z')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def import_sources(source_root=SOURCE, repository=REPOSITORY):
    """Validate the complete immutable selection before any destination writes."""
    source_root, repository = Path(source_root), Path(repository)
    destination = repository / 'research/20261004-p2-p3'
    manifest_path = repository / 'docs/SOURCE_P2P3.json'
    historical_manifest = source_root / 'SHA256SUMS'
    if not historical_manifest.is_file():
        raise ValueError('Finalize the local evidence package first')
    if any(p.is_symlink() for p in [historical_manifest, *historical_manifest.parents]):
        raise ValueError('Historical source root and manifest must not use symlinks')
    selected = set()
    patterns = [
        '*.md', 'commands.sh', 'build_manuscript.sh', 'manuscript-changes.patch',
        'EVIDENCE_INDEX.json', 'CLAIM_EVIDENCE_FOLLOWUP.json', 'INPUTS.json',
        'scripts/*.py', 'manuscript/paper.tex', 'manuscript/BASE_SOURCE.json',
        'P2/*.md', 'P2/commands.sh', 'P2/scripts/*.py', 'P2/scripts/*.java',
        'P2/source-attempt-1/*.java', 'P2/dependencies/resolved-lock.json',
        'P3/*.md', 'P3/commands.sh', 'P3/scripts/*.py', 'P3/initial-candidates.json',
        'P3/additional-initial-candidates.json', 'P3/followups-*.json',
        'review/*.py', 'review/*.md', 'review/mechanism/*.py',
        'review/mechanism/commands.sh', 'review/mechanism/MECHANISM_REVIEW.md',
        'review/reference-audit/audit_candidate.py', 'review/reference-audit/AUDIT_REPORT.md',
        'review/reference-audit/attempt-1-header-assumption/audit_candidate.py',
        'review/reference-audit/attempt-1-header-assumption/PRESERVATION_NOTE.txt',
    ]
    for pattern in patterns:
        selected.update(p for p in source_root.glob(pattern) if p.is_file() or p.is_symlink())
    rows = []
    pending = []

    def destination_path(path):
        if (not path.resolve().is_relative_to(repository.resolve()) or
                any(p.is_symlink() for p in [path, *path.parents] if p.is_relative_to(repository))):
            raise ValueError('Refusing linked import destination: ' + str(path))
        if any(p.exists() and not p.is_dir() for p in path.parents):
            raise ValueError('Import destination parent is not a directory: ' + str(path))

    for source in sorted(selected):
        if any(p.is_symlink() for p in [source, *source.parents]) or not source.is_file():
            raise ValueError('Refusing linked/non-file source: ' + str(source))
        relative = source.relative_to(source_root)
        target = destination / relative
        destination_path(target)
        data = source.read_bytes()
        data.decode('utf-8')
        if b'\0' in data or len(data) >= 1_000_000:
            raise ValueError('Unexpected binary or large source: ' + str(source))
        if target.exists():
            if not target.is_file() or target.read_bytes() != data:
                raise ValueError('Refusing changed existing import: ' + str(target))
        else:
            pending.append((target, data))
        rows.append({'source_path': str(source),
                     'repository_path': str(target.relative_to(repository)),
                     'sha256': digest(data), 'bytes': len(data)})
    manifest = {'scope': 'Selected first-party sources and necessary text documents; raw evidence excluded.',
                'local_evidence_root': str(source_root),
                'local_evidence_manifest_sha256': digest(historical_manifest.read_bytes()),
                'full_evidence_uploaded': False, 'files': rows}
    destination_path(manifest_path)
    encoded = json.dumps(manifest, indent=2) + '\n'
    if manifest_path.exists() and (not manifest_path.is_file() or manifest_path.read_text() != encoded):
        raise ValueError('Refusing changed existing source manifest')
    indexed = {row['repository_path'] for row in rows}
    for path in destination.rglob('*'):
        if (path.is_file() or path.is_symlink()) and str(path.relative_to(repository)) not in indexed:
            raise ValueError('Refusing unindexed imported source: ' + str(path))
    for target, data in pending:
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('xb') as output:
            output.write(data)
    if not manifest_path.exists():
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        with manifest_path.open('x') as output:
            output.write(encoded)
    return {'selected_files': len(rows), 'bytes': sum(row['bytes'] for row in rows),
            'manifest': str(manifest_path)}


def main():
    try:
        result = import_sources()
    except (OSError, ValueError) as error:
        raise SystemExit(str(error))
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
