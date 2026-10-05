#!/usr/bin/env python3
"""Read every archive member without extraction; check a separately pinned index."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import tarfile

from stage_evidence import digest, safe_relative


def verify(archive, checksum_pin):
    prefix = 'focal-saved-evidence/'
    observed, checksum_bytes = {}, None
    with tarfile.open(archive, 'r|gz') as stream:
        for member in stream:
            safe_relative(member.name)
            if member.name != prefix[:-1] and not member.name.startswith(prefix):
                raise ValueError('Unexpected archive root')
            if member.isdir():
                continue
            if not member.isfile():
                raise ValueError('Archive includes a link or special object')
            name = member.name[len(prefix):]
            if name in observed:
                raise ValueError('Duplicate archive file')
            h = hashlib.sha256()
            size = 0
            is_checksums = name == 'SHA256SUMS'
            chunks = []
            if is_checksums and member.size > 8 * 1024 * 1024:
                raise ValueError('Unexpectedly large checksum file')
            with stream.extractfile(member) as source:
                for chunk in iter(lambda: source.read(1024 * 1024), b''):
                    h.update(chunk)
                    size += len(chunk)
                    if is_checksums:
                        chunks.append(chunk)
            if size != member.size:
                raise ValueError('Truncated archive member')
            observed[name] = {'sha256':h.hexdigest(), 'bytes':size}
            if is_checksums:
                checksum_bytes = b''.join(chunks)
    if checksum_bytes is None or hashlib.sha256(checksum_bytes).hexdigest() != checksum_pin:
        raise ValueError('Archive checksum file does not match independent pin')
    expected = {}
    for line in checksum_bytes.decode().splitlines():
        match = re.fullmatch(r'([0-9a-f]{64}) [ *](.+)', line)
        if not match:
            raise ValueError('Malformed checksum row')
        name = str(safe_relative(match[2]))
        if name in expected:
            raise ValueError('Duplicate checksum row')
        expected[name] = match[1]
    if set(observed) != set(expected) | {'SHA256SUMS'}:
        raise ValueError('Archive file inventory differs from pinned checksum list')
    for name, sha in expected.items():
        if observed[name]['sha256'] != sha:
            raise ValueError(f'Archive member digest mismatch: {name}')
    return {'archive_integrity':'PASS', 'archive_path':str(archive),
            'archive_bytes':archive.stat().st_size, 'archive_sha256':digest(archive),
            'checksum_file_sha256':checksum_pin, 'verified_files':len(observed),
            'payload_files':sum(n.startswith('payload/') for n in observed),
            'uncompressed_file_bytes':sum(r['bytes'] for r in observed.values()),
            'extracted':False, 'model_experiments_run':False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', type=Path, required=True)
    parser.add_argument('--checksums-sha256', required=True)
    args = parser.parse_args()
    try:
        result = verify(args.archive, args.checksums_sha256)
    except (ValueError, OSError, tarfile.TarError) as exc:
        parser.exit(1, f'{type(exc).__name__}: {exc}\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
