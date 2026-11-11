#!/usr/bin/env python3
"""Retrieve the six pinned P3 input bodies as new acquisitions, not old logs."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess

from recover_inputs import INDEX_SHA256, REPOSITORY, inventory, sha


def retrieve(original_file, output_dir):
    rows = inventory()['p3_reference_prerequisites']
    original_file, output_dir = Path(original_file), Path(output_dir)
    if output_dir.exists() or output_dir.is_symlink():
        raise FileExistsError('Choose a new reference acquisition directory')
    if output_dir.resolve().is_relative_to(REPOSITORY):
        raise ValueError('Acquisition artifacts must stay outside the source repository')
    if any(p.is_symlink() for p in output_dir.parents):
        raise ValueError('Output directory must not traverse symlinks')
    focal = next(row for row in rows if row['id'] == 'I01-publisher-model')
    original = original_file.read_bytes()
    if sha(original) != focal['body']['expected_sha256']:
        raise ValueError('Supplied focal model differs from historical pin')
    # Check curl availability before creating the external acquisition directory.
    version = subprocess.run(['curl', '--version'], capture_output=True, text=True, check=True)
    output_dir.mkdir(parents=True, exist_ok=False)
    records = []
    for row in rows:
        folder = output_dir / row['id']
        folder.mkdir()
        body = folder / 'body'
        record = {'id': row['id'], 'requested_url': row['acquisition_url'],
                  'started_at_utc': datetime.now(timezone.utc).isoformat(),
                  'expected_sha256': row['body']['expected_sha256'],
                  'expected_bytes': row['body']['bytes']}
        if row['id'] == 'I01-publisher-model':
            body.write_bytes(original)
            record.update(acquisition='REUSED_NEW_LOCAL_ACQUISITION', source_path=str(original_file.resolve()))
            transport_ok = True
        else:
            command = ['curl', '--silent', '--show-error', '--fail-with-body', '--location',
                       '--proto', '=https', '--proto-redir', '=https', '--connect-timeout', '15',
                       '--max-time', '60', '--max-filesize', '30000000',
                       '--dump-header', str(folder / 'headers.txt'), '--output', str(body),
                       '--write-out', '%{json}', row['acquisition_url']]
            process = subprocess.run(command, capture_output=True, timeout=75)
            (folder / 'curl-transfer.json').write_bytes(process.stdout)
            (folder / 'curl.stderr').write_bytes(process.stderr)
            record.update(acquisition='NEW_HTTPS_RETRIEVAL', command=command, exit_code=process.returncode)
            transport_ok = process.returncode == 0
        if body.is_file():
            data = body.read_bytes()
            record.update(actual_sha256=sha(data), actual_bytes=len(data))
        record['matches_historical_pin'] = (transport_ok and
            record.get('actual_sha256') == record['expected_sha256'] and
            record.get('actual_bytes') == record['expected_bytes'])
        records.append(record)
        (folder / 'acquisition.json').write_text(json.dumps(record, indent=2) + '\n')
        print(row['id'], 'MATCH' if record['matches_historical_pin'] else 'MISSING_OR_MISMATCH', flush=True)
    report = {'status': 'REFERENCE_INPUT_BYTES_MATCH_HISTORICAL_PINS' if
              all(row['matches_historical_pin'] for row in records) else 'PARTIAL_REFERENCE_RECOVERY',
              'input_index_sha256': INDEX_SHA256,
              'retrieval_script_sha256': sha(Path(__file__).read_bytes()),
              'curl_version': version.stdout.splitlines()[0], 'records': records,
              'old_retrieval_records_recovered': False, 'graph_bridge_recomputed': False,
              'model_experiments_run': False, 'human_verification': False}
    (output_dir / 'reference-recovery.json').write_text(json.dumps(report, indent=2) + '\n')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--original-file', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    try:
        result = retrieve(args.original_file, args.output_dir)
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        parser.exit(1, f'{type(error).__name__}: {error}\n')
    return int(result['status'] == 'PARTIAL_REFERENCE_RECOVERY')


if __name__ == '__main__':
    raise SystemExit(main())
