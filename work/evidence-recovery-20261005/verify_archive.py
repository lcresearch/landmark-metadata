#!/usr/bin/env python3
"""Read every archive member without extraction; check a separately pinned index."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import re
import tarfile

from stage_evidence import digest, safe_relative


def verify(archive, checksum_pin):
    prefix = 'focal-saved-evidence/'
    observed, checksum_bytes = {}, None
    member_types, required_directories = {}, set()
    # tar iteration stops at its end marker; a separate gzip reader must be
    # consumed through EOF to validate the CRC/length trailer as well.
    with gzip.open(archive, 'rb') as compressed:
        with tarfile.open(fileobj=compressed, mode='r|') as stream:
            for member in stream:
                path = safe_relative(member.name)
                if member.name != prefix[:-1] and not member.name.startswith(prefix):
                    raise ValueError('Unexpected archive root')
                if not member.isdir() and not member.isfile():
                    raise ValueError('Archive includes a link or special object')
                kind = 'directory' if member.isdir() else 'file'
                if member.name in member_types:
                    if kind == member_types[member.name] == 'file':
                        raise ValueError('Duplicate archive file')
                    raise ValueError('Duplicate or conflicting archive member')
                if kind == 'file' and (member.name in required_directories
                                       or member.name == prefix[:-1]):
                    raise ValueError('Archive file conflicts with a directory')
                parents = {str(parent) for parent in path.parents if str(parent) != '.'}
                if any(member_types.get(parent) == 'file' for parent in parents):
                    raise ValueError('Archive file is used as a parent directory')
                member_types[member.name] = kind
                required_directories.update(parents)
                if member.isdir():
                    continue
                name = member.name[len(prefix):]
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
        for _ in iter(lambda: compressed.read(1024 * 1024), b''):
            pass
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
    except (ValueError, OSError, EOFError, tarfile.TarError) as exc:
        parser.exit(1, f'{type(exc).__name__}: {exc}\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
