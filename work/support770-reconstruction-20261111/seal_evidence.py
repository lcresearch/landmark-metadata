"""Archive selected evidence and verify every member; retain toolchains locally."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import tarfile


def sha(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b''): digest.update(chunk)
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--archive', type=Path, required=True)
    parser.add_argument('--receipt', type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    if args.archive.exists() or args.receipt.exists(): raise FileExistsError('Delivery destination exists')
    if json.loads((root / 'stages/stop-device/command.json').read_text())['status'] != 'PASS':
        raise ValueError('Owned device stop not recorded')
    directories = ['initial-source','generation-source','runtime-source','execution-source',
        'model-download','model-inspection','model-graph-readback','gradle-checksum','stages','project','build',
        'runtime-dependencies','executions','boot','generator-inspection','versions','validation']
    files = [p for name in directories for p in (root / name).rglob('*')
             if p.is_file() and not p.is_symlink() and p.suffix != '.keystore']
    files += list(root.glob('*.json')) + list((root / 'gradle-download').glob('*.json'))
    files = sorted(set(files))
    entries = [{'path': str(p.relative_to(root)), 'bytes': p.stat().st_size, 'sha256': sha(p)} for p in files]
    manifest = root / 'selected-evidence-manifest.json'
    if manifest.exists(): raise FileExistsError(manifest)
    manifest.write_text(json.dumps({'created_utc': datetime.now(timezone.utc).isoformat(),
        'scope': 'selected evidence; excludes SDK/AVD, Gradle distribution/cache and disposable signing key',
        'files': entries}, indent=2) + '\n')
    files.append(manifest)
    with tarfile.open(args.archive, 'w:gz') as archive:
        for path in files: archive.add(path, arcname=str(path.relative_to(root)), recursive=False)
    expected = {row['path']: (row['bytes'], row['sha256']) for row in entries}
    expected[manifest.name] = (manifest.stat().st_size, sha(manifest))
    seen = set()
    with tarfile.open(args.archive, 'r:gz') as archive:
        for member in archive:
            if not member.isfile() or member.name in seen or member.name not in expected:
                raise ValueError('Unexpected/duplicate archive member')
            data = archive.extractfile(member).read()
            if (len(data), hashlib.sha256(data).hexdigest()) != expected[member.name]:
                raise ValueError('Archive identity mismatch: ' + member.name)
            seen.add(member.name)
    if seen != set(expected): raise ValueError('Missing archive members')
    important = ['freeze.json','generation-freeze.json','runtime-freeze.json','build-results.json',
        'runtime-results.json','model-inspection/inspection.json','model-inspection/metadata.json',
        'model-graph-readback/graph.json',
        'generator-inspection/resolved-artifacts.json','generator-inspection/command.json',
        'stages/agp-generation/command.json','stages/agp-generation/stdout',
        'stages/build-consumers/command.json','boot/readiness.json','stages/stop-device/command.json',
        'executions/wrapper/device/result.json','executions/wrapper/device/raw_output.bin',
        'executions/task/device/result.json','executions/task/device/mask_0_0.bin',
        'validation/readback.json','validation/adversarial-readback.json',
        'project/app/build/generated/ml_source_out/debug/org/example/support770/ml/LiteModelDeeplabv31Metadata2.java']
    receipt = {'root': str(root), 'archive': str(args.archive.resolve()),
        'command': [sys.executable, *sys.argv],
        'archive_bytes': args.archive.stat().st_size, 'archive_sha256': sha(args.archive),
        'verified_members': len(seen), 'manifest': {'path': manifest.name, 'bytes': manifest.stat().st_size, 'sha256': sha(manifest)},
        'selected_records': [row for row in entries if row['path'] in important],
        'scope': 'Verified selected local evidence, not a remote backup or complete offline environment.',
        'human_verification': 'PENDING', 'historical_identity': 'UNKNOWN',
        'created_utc': datetime.now(timezone.utc).isoformat()}
    args.receipt.write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({k: receipt[k] for k in ('archive_bytes','archive_sha256','verified_members')}))


if __name__ == '__main__':
    main()
