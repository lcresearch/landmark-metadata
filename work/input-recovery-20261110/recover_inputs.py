#!/usr/bin/env python3
"""Reconstruct pinned focal inputs into a new external directory; no inference.

Matching historical input hashes does not recover old execution evidence. This
tool reads a caller-supplied model; it does not claim to have retrieved that file.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import zipfile


REPOSITORY = Path(__file__).resolve().parents[2]
INDEX = REPOSITORY / 'docs/reproduction/inputs.json'
INDEX_SHA256 = 'b297d7b0756a8f10f8488f2b2bbe8b15a51239e9de354983ca17d264127069cf'
LABEL_MEMBER = 'labels_without_background.txt'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def inventory():
    data = INDEX.read_bytes()
    if sha(data) != INDEX_SHA256:
        raise ValueError('Historical input index differs from the pinned source')
    return json.loads(data)


def entries(data):
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        names = archive.namelist()
        if names != [LABEL_MEMBER]:
            raise ValueError('Unexpected associated-file inventory')
        return {name: archive.read(name) for name in names}


def repack(data, payloads):
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        start = min(member.header_offset for member in archive.infolist())
    output = io.BytesIO(data[:start])
    with zipfile.ZipFile(output, 'a', compression=zipfile.ZIP_STORED) as archive:
        for name, payload in payloads.items():
            info = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_STORED
            archive.writestr(info, payload)
    return output.getvalue()


def reconstruct(original_file, output_dir):
    original_file, output_dir = Path(original_file), Path(output_dir)
    if output_dir.exists() or output_dir.is_symlink():
        raise FileExistsError('Choose a new output directory; existing material is preserved')
    if output_dir.resolve().is_relative_to(REPOSITORY):
        raise ValueError('Input artifacts must stay outside the source-only repository')
    if any(parent.is_symlink() for parent in output_dir.parents):
        raise ValueError('Output directory must not traverse symlinks')
    index = inventory()
    models = {row['id']: row for row in index['model_conditions']}
    if original_file.stat().st_size != models['original']['primary_model']['bytes']:
        raise ValueError('Original model size mismatch')
    original = original_file.read_bytes()
    if sha(original) != models['original']['primary_model']['expected_sha256']:
        raise ValueError('Original model digest mismatch')

    associated = entries(original)
    labels = associated[LABEL_MEMBER].decode('utf-8').splitlines()
    if len(labels) != 1000:
        raise ValueError('Expected exactly 1000 original label lines')
    description = b'Probabilities of the 1000 labels respectively.'
    if original.count(description) != 1:
        raise ValueError('Description edit does not have a unique anchor')
    changed = bytearray(original)
    changed[original.index(description)] ^= 32
    deletion = dict(associated)
    deletion[LABEL_MEMBER] = ('\n'.join(labels[:-1]) + '\n').encode()
    permutation = dict(associated)
    ending = '\n' if associated[LABEL_MEMBER].endswith(b'\n') else ''
    permutation[LABEL_MEMBER] = ('\n'.join(labels[1:] + labels[:1]) + ending).encode()
    dropped = repack(original, deletion)
    variants = {'original': original, 'description_control': bytes(changed),
                'label_deletion': dropped, 'label_permutation': repack(original, permutation),
                'restoration': repack(dropped, associated)}
    payloads, records = {}, []
    for name, data in variants.items():
        expected = models[name]
        label_bytes = entries(data)[LABEL_MEMBER]
        if (sha(data) != expected['primary_model']['expected_sha256'] or
                len(data) != expected['primary_model']['bytes'] or
                sha(label_bytes) != expected['associated_file']['expected_sha256']):
            raise ValueError('Reconstructed model/resource does not match historical pin: ' + name)
        path = 'models/' + name + '.tflite'
        payloads[path] = data
        records.append({'path': path, 'sha256': sha(data), 'bytes': len(data),
                        'label_sha256': sha(label_bytes), 'matches_historical_pin': True})
    count = 224 * 224 * 3
    rgb = {'gray127': bytes([127]) * count,
           'rgb_pattern': bytes((37 * i + 17) % 256 for i in range(count))}
    for expected in index['rgb_inputs']:
        name = expected['id']
        data = rgb[name]
        if sha(data) != expected['expected_sha256'] or len(data) != expected['bytes']:
            raise ValueError('Reconstructed RGB input does not match historical pin: ' + name)
        path = 'inputs/' + name + '-input.rgb'
        payloads[path] = data
        records.append({'path': path, 'sha256': sha(data), 'bytes': len(data),
                        'matches_historical_pin': True})
    report = {'status': 'RECONSTRUCTED_INPUT_BYTES_MATCH_HISTORICAL_PINS',
              'created_at_utc': datetime.now(timezone.utc).isoformat(),
              'original_file': str(original_file.resolve()), 'input_index_sha256': INDEX_SHA256,
              'reconstruction_script_sha256': sha(Path(__file__).read_bytes()),
              'acquisition': 'Caller-supplied local bytes; retrieval provenance must be recorded separately.',
              'files': records, 'model_experiments_run': False,
              'old_execution_evidence_recovered': False, 'human_verification': False}
    # All identity checks finish before writing. An I/O interruption can leave
    # an incomplete new directory; the success report is written last.
    output_dir.mkdir(parents=True, exist_ok=False)
    for relative, data in payloads.items():
        path = output_dir / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('xb') as stream:
            stream.write(data)
    with (output_dir / 'input-recovery.json').open('x') as stream:
        json.dump(report, stream, indent=2)
        stream.write('\n')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--original-file', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    try:
        report = reconstruct(args.original_file, args.output_dir)
    except (OSError, ValueError, zipfile.BadZipFile) as error:
        parser.exit(1, f'{type(error).__name__}: {error}\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
