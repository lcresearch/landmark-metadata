"""Create a compact claim/evidence index and seal this completed local round.

No experiments are executed. Refuses to overwrite the final manifest. Historical
subpackages are read-only; P2 SDK/AVD and unmanifested operational state are excluded.
"""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def write_json(name, data):
    path = ROOT / name
    if path.exists():
        raise SystemExit('Refusing to overwrite ' + str(path))
    path.write_text(json.dumps(data, indent=2) + '\n')


def pointer(path):
    p = ROOT / path
    return {'path': str(p), 'sha256': sha(p)}


def main():
    if (ROOT / 'SHA256SUMS').exists():
        raise SystemExit('Round already sealed')
    runtime = json.loads((ROOT / 'verification/runtime-record-review.json').read_text())
    reference = json.loads((ROOT / 'review/reference-audit/results.json').read_text())
    protected = json.loads((ROOT / 'verification/protected-evidence-review.json').read_text())
    assert runtime['status'] == protected['status'] == 'PASS'
    assert reference['status'] == 'PASS_DISPLAY_REFERENCE_ONLY'
    assert (runtime['unit_count'], runtime['completed_input_observations'],
            runtime['decoded_lists'], runtime['wrapper_raw_tensors']) == (10, 18, 16, 10)

    evidence = {name: pointer(name) for name in [
        'P2/SHA256SUMS', 'P2/results.json', 'P2/versions/versions.json',
        'P2/dependencies/resolved-lock.json', 'P3/SHA256SUMS', 'P3/results.json',
        'review/mechanism/SHA256SUMS', 'review/reference-audit/audit-output-manifest.json',
        'verification/runtime-record-review.json', 'verification/protected-evidence-review.json',
        'review/manuscript-p2-review.md', 'review/manuscript-reference-review.md',
        'manuscript/paper.tex', 'manuscript/paper.pdf']}
    write_json('EVIDENCE_INDEX.json', {
        'local_root': str(ROOT), 'evidence': evidence,
        'source_only_repository': 'https://github.com/lcresearch/landmark-metadata',
        'repository_contains_full_evidence': False, 'human_audit': 'PENDING'})

    claims = [
        {'id': 'P2-stage', 'claim': 'Same-Android Task construction rejects deletion; wrapper process returns and actual getter rejects.',
         'sources': ['P2/results.json', 'review/p2-final-review.md', 'review/mechanism/MECHANISM_REVIEW.md'],
         'boundary': 'Different native integrations remain; classify internals not separately observed; exceptions caught.'},
        {'id': 'P2-preservation', 'claim': 'Five variants preserve graph; generated source/classes/DEX equal within consumer; raw wrapper bytes equal per input.',
         'sources': ['P2/static-results.json', 'P2/build-results.json', 'verification/runtime-record-review.json'],
         'boundary': 'Task raw tensors not directly captured; returned scores align by category index, not list rank.'},
        {'id': 'P3-display', 'claim': 'External publisher-prescribed display order is linked to the exact computation; original/restoration1000matches, permutation999disagreements.',
         'sources': ['P3/results.json', 'P3/analysis/reference-chain.json', 'review/reference-audit/AUDIT_REPORT.md'],
         'boundary': 'Stable-ID lineage remains ABSTAIN; no prediction correctness or natural defect claim; old E5 outputs unchanged.'},
        {'id': 'integrity', 'claim': 'All3207 prior manifest entries and five pinned inputs remain unchanged.',
         'sources': ['verification/protected-evidence-review.json'],
         'boundary': 'Byte integrity does not replace human validation or a portable reproduction deposit.'},
    ]
    for claim in claims:
        claim['sources'] = [pointer(p) for p in claim['sources']]
    old_map = Path('/workspace/metadata-contract-paper-revision-20261004T065132Z/CLAIM_EVIDENCE.json')
    write_json('CLAIM_EVIDENCE_FOLLOWUP.json', {
        'scope': 'New or strengthened P2/P3 claims; prior claims retain their historical source map.',
        'prior_claim_map': {'path': str(old_map), 'sha256': sha(old_map)}, 'claims': claims})
    write_json('results.json', {
        'status': 'COMPLETE_WITH_QUALIFIED_DISPLAY_REFERENCE',
        'P2': {'units': 10, 'canonical_graphs': 1, 'variants': 5, 'consumers': 2,
               'input_observations': 18, 'decoded_lists': 16, 'wrapper_raw_tensors': 10,
               'earliest_deletion_rejection': {'wrapper': 'generated_getter', 'task': 'model_initialization'}},
        'P3': {'candidate_requests': 30, 'http200': 25, 'http404': 5,
               'original_display_matches': 1000, 'permutation_display_disagreements': 999,
               'restored_display_matches': 1000, 'stable_class_id_chain': 'ABSTAIN', 'inference_runs': 0},
        'manuscript_pages_generic_template': 9, 'human_audit': 'PENDING',
        'natural_case_search_performed': False, 'evidence_index': 'EVIDENCE_INDEX.json'})

    sealed_subdirs = ['P2', 'P3', 'review/mechanism']
    entries = {}
    for directory in sealed_subdirs:
        base = ROOT / directory
        manifest = base / 'SHA256SUMS'
        for line in manifest.read_text().splitlines():
            if not line.strip():
                continue
            expected, rel = line.split(maxsplit=1)
            path = base / rel.lstrip('*')
            assert path.is_file() and sha(path) == expected, str(path)
            entries[str(path.relative_to(ROOT))] = expected
        entries[str(manifest.relative_to(ROOT))] = sha(manifest)
    for path in sorted(ROOT.rglob('*')):
        rel = path.relative_to(ROOT)
        if any(rel == Path(d) or Path(d) in rel.parents for d in sealed_subdirs):
            continue
        if path.is_symlink() or '__pycache__' in rel.parts or not path.is_file():
            continue
        entries[str(rel)] = sha(path)
    (ROOT / 'SHA256SUMS').write_text(''.join(f'{digest}  {name}\n' for name, digest in sorted(entries.items())))
    print(json.dumps({'entries': len(entries), 'manifest_sha256': sha(ROOT / 'SHA256SUMS'),
                      'excluded': 'P2 operational SDK/AVD and files excluded by its submanifest; symlinks and Python caches.'}, indent=2))


if __name__ == '__main__':
    main()
