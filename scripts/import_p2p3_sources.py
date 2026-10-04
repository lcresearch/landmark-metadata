"""Import only first-party P2/P3 source and necessary text documentation.

Requires the sealed local workspace; excludes raw evidence and build products.
Refuses to overwrite a changed existing import. No experiment is executed.
"""
from pathlib import Path
import hashlib
import json
import shutil

REPOSITORY = Path(__file__).resolve().parents[1]
SOURCE = Path('/workspace/metadata-contract-p2p3-20261004T073824Z')
DESTINATION = REPOSITORY / 'research/20261004-p2-p3'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    if not (SOURCE / 'SHA256SUMS').is_file():
        raise SystemExit('Finalize the local evidence package first')
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
        selected.update(p for p in SOURCE.glob(pattern) if p.is_file())
    rows = []
    for source in sorted(selected):
        assert not source.is_symlink()
        relative = source.relative_to(SOURCE)
        target = DESTINATION / relative
        data = source.read_bytes()
        data.decode('utf-8')
        assert b'\0' not in data and len(data) < 1_000_000
        if target.exists() and target.read_bytes() != data:
            raise SystemExit('Refusing changed existing import: ' + str(target))
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            shutil.copyfile(source, target)
        rows.append({'source_path': str(source),
                     'repository_path': str(target.relative_to(REPOSITORY)),
                     'sha256': digest(data), 'bytes': len(data)})
    manifest = {'scope': 'Selected first-party sources and necessary text documents; raw evidence excluded.',
                'local_evidence_root': str(SOURCE),
                'local_evidence_manifest_sha256': digest((SOURCE / 'SHA256SUMS').read_bytes()),
                'full_evidence_uploaded': False, 'files': rows}
    manifest_path = REPOSITORY / 'docs/SOURCE_P2P3.json'
    encoded = json.dumps(manifest, indent=2) + '\n'
    if manifest_path.exists() and manifest_path.read_text() != encoded:
        raise SystemExit('Refusing changed existing source manifest')
    manifest_path.write_text(encoded)
    print(json.dumps({'selected_files': len(rows), 'bytes': sum(row['bytes'] for row in rows),
                      'manifest': str(manifest_path)}, indent=2))


if __name__ == '__main__':
    main()
