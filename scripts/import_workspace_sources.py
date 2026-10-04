"""Import first-party source snapshots, never runtime or build artifacts.

Existing snapshots are immutable: an identical source is skipped; a changed
source at an imported path is an error. New experiments need a new source root.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil

REPO = Path(__file__).resolve().parents[1]
ROOT_NAMES = [
    'hand-contract-repro',
    'hand-contract-fresh-qrh65aao',
    'metadata-contract-paper',
    'metadata-contract-e2e-20261004T030536Z',
    'metadata-contract-audit-20261004T062010Z',
    'metadata-contract-paper-rewrite-20261004T052625Z',
    'metadata-contract-paper-revision-20261004T065132Z',
]
EXCLUDED_DIRS = {
    '.git', '.venv', 'venv', 'toolchains', 'sdk', 'downloads', 'wheels',
    'deps', '__pycache__', 'sources', 'classes', 'generated', 'patched',
    'runs', 'checks', 'variants', 'executions', 'aar', 'replay-evidence',
    'hand-evidence', 'outputs', 'conditions', 'demo-deletion', 'logs',
    'preview', 'runtime', 'build', 'binding-audit',
}
SOURCE_SUFFIXES = {'.py', '.java', '.sh', '.tex', '.md', '.patch', '.gradle', '.toml', '.yml', '.yaml'}
EXTRA_NAMES = {'requirements.txt', 'requirements.lock', 'Makefile', 'Dockerfile', 'REPRODUCE.txt', 'README.txt', 'REVISION_NOTES.txt', '研究说明.txt'}
CONFIG_PATHS = {
    'hand-contract-repro/experiment-plan.json',
    'metadata-contract-paper/contracts.json',
    'metadata-contract-paper/protocol.json',
    'metadata-contract-e2e-20261004T030536Z/E4/protocol/candidates.json',
    'metadata-contract-e2e-20261004T030536Z/E4/protocol/contracts.json',
    'metadata-contract-e2e-20261004T030536Z/E4/protocol/mutation-rules.json',
    'metadata-contract-e2e-20261004T030536Z/E4/protocol/prior-exclusions.json',
    # These are text inputs consumed by the manuscript editor, not raw results.
    'metadata-contract-paper-revision-20261004T065132Z/review/rebuild-evidence-proposal.txt',
    'metadata-contract-paper-revision-20261004T065132Z/review/related-work-proposal.txt',
}

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def select(workspace):
    for name in ROOT_NAMES:
        base = workspace/name
        if not base.is_dir():
            raise FileNotFoundError(base)
        for folder, dirs, files in os.walk(base):
            dirs[:] = sorted(d for d in dirs if d not in EXCLUDED_DIRS)
            for filename in sorted(files):
                source = Path(folder)/filename
                relative = source.relative_to(workspace)
                if source.is_symlink() or filename == 'commands-executed.sh':
                    continue
                if (source.suffix in SOURCE_SUFFIXES or filename in EXTRA_NAMES
                        or relative.as_posix() in CONFIG_PATHS):
                    yield source, relative

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', type=Path, default=Path('/workspace'))
    args = parser.parse_args()
    rows = []
    for source, relative in select(args.workspace):
        content = source.read_bytes()
        content.decode('utf-8')  # Reject binary data despite an allowed suffix.
        if len(content) > 1_000_000 or b'\x00' in content:
            raise ValueError(f'Unexpected binary or large source: {source}')
        target = REPO/'sources'/relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            if target.read_bytes() != content:
                raise ValueError(f'Refusing to overwrite imported source: {target}')
        else:
            shutil.copy2(source, target)
        rows.append({'repository_path':target.relative_to(REPO).as_posix(),
                     'original_path':str(source), 'sha256':digest(source), 'bytes':len(content)})
    rows.sort(key=lambda row:row['repository_path'])
    manifest = {'scope':'Source code and necessary text documentation only; NOT the complete experimental evidence package.',
                'workspace_roots':ROOT_NAMES, 'files':rows,
                'excluded':'SDKs, installed dependencies, emulator images/state, third-party source copies, generated wrappers, model assets, raw results, execution logs, build outputs, archives, keys and credentials.'}
    destination = REPO/'docs/SOURCE_IMPORT.json'
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(manifest, indent=2, ensure_ascii=False)+'\n')
    print(json.dumps({'imported_files':len(rows),'source_bytes':sum(r['bytes'] for r in rows),'manifest':str(destination)}))

if __name__ == '__main__':
    main()
