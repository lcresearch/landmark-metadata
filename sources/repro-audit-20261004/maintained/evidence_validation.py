"""Evidence identity checks; no model execution or optional dependencies."""
import hashlib
import json
import re


def require_exact_identities(actual, expected, label):
    actual, expected = list(actual), list(expected)
    if (len(set(expected)) != len(expected) or len(set(actual)) != len(actual)
            or set(actual) != set(expected)):
        raise ValueError(f'{label}: missing, unexpected or duplicate identities')


def required_fixture_digests(path, expected_sha256):
    """Read a separately frozen manifest, never infer requirements from a run."""
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != expected_sha256:
        raise ValueError('Required-fixture manifest digest mismatch')
    manifest = json.loads(data)
    digests = (manifest['artifact_sha256s'] if 'artifact_sha256s' in manifest
               else [row['model_sha256'] for row in manifest['fixtures']])
    if (len(digests) != 65 or len(set(digests)) != 65
            or any(not isinstance(d, str) or not re.fullmatch(r'[0-9a-f]{64}', d)
                   for d in digests)):
        raise ValueError('Required-fixture manifest must pin 65 distinct SHA-256 identities')
    return digests


def require_fixture_digest(fixture, current=None):
    expected = fixture['model_sha256']
    from pathlib import Path
    actual = hashlib.sha256(Path(fixture['path']).read_bytes()).hexdigest()
    if actual != expected or fixture['report'].get('artifact_sha256') != expected:
        raise ValueError('Fixture bytes, catalog and prior-report digests disagree')
    if current is not None and current.get('artifact_sha256') != expected:
        raise ValueError('Current checker report has a different artifact digest')


def complete_output_positions(outputs, count):
    positions = [row.get('position') for row in outputs]
    return (all(type(p) is int for p in positions)
            and len(positions) == count and set(positions) == set(range(count)))


def require_decoder_records(static, records):
    def identity(component, variant, prediction):
        return component, variant, prediction['field'], prediction['output_position']
    expected = {}
    for component in static:
        for variant in component['variants']:
            for prediction in variant['decoder_checks']:
                key = identity(component['id'], variant['variant'], prediction)
                if key in expected:
                    raise ValueError('Duplicate decoder identity in static suite')
                expected[key] = prediction
    actual = [identity(row['id'], row['variant'], row['prediction']) for row in records]
    require_exact_identities(actual, expected, 'Decoder records')
    if len(expected) != 23:
        raise ValueError('Static suite must declare all 23 decoder probes')
    for key, row in zip(actual, records):
        if row['prediction'] != expected[key]:
            raise ValueError('Decoder prediction differs from static suite')


def generated_sources_identical(records, expected_variants):
    try:
        require_exact_identities((r['variant'] for r in records), expected_variants,
                                 'Generated source conditions')
    except (KeyError, ValueError):
        return False
    digests = [r.get('generated_source_sha256') for r in records]
    return (bool(digests) and all(isinstance(d, str) and re.fullmatch(r'[0-9a-f]{64}', d)
                                  for d in digests)
            and len(set(digests)) == 1)
