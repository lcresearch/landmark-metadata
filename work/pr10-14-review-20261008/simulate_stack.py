#!/usr/bin/env python3
"""Simulate stacked squash merges using local Git objects only; never update refs."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--freeze', required=True, type=Path)
    ap.add_argument('--output', required=True, type=Path)
    args = ap.parse_args()
    repo = Path(subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], text=True).strip())
    out = args.output.resolve()
    if out.is_relative_to(repo):
        ap.error('Raw simulation records must remain outside Git')
    out.mkdir(parents=True, exist_ok=False)
    f = json.loads(args.freeze.read_text())
    prs = sorted(f['prs'], key=lambda row: row['number'])
    if [p['number'] for p in prs] != [10, 11, 12, 13, 14]:
        ap.error('Expected exact PR set 10 through 14')
    commands = []

    def git(*argv, stdin=None, checked=True):
        result = subprocess.run(['git', *argv], input=stdin, text=True, capture_output=True)
        commands.append({'argv': ['git', *argv], 'stdin': stdin, 'exit': result.returncode,
                         'stdout': result.stdout, 'stderr': result.stderr})
        (out/'commands.json').write_text(json.dumps(commands, indent=2)+'\n')
        if checked and result.returncode:
            raise RuntimeError('Local git command failed; see commands.json')
        return result

    def tree(commit):
        return git('rev-parse', commit+'^{tree}').stdout.strip()

    previous_original = previous_squash = f['main']
    rows = []
    for p in prs:
        head = p['headRefOid']
        if git('merge-base', '--is-ancestor', previous_original, head, checked=False).returncode:
            raise RuntimeError('Original PR stack is not an ancestor chain')
        if tree(previous_squash) != tree(previous_original):
            raise RuntimeError('Main content differs from exact reviewed predecessor; stop, do not discard changes')
        original_tree = tree(head)
        direct = git('merge-tree', '--write-tree', previous_squash, head, checked=False)
        if direct.returncode not in (0, 1):
            raise RuntimeError('Unexpected merge-tree failure')
        direct_tree = direct.stdout.splitlines()[0]
        chosen_head = head
        refreshed = False
        if direct.returncode or direct_tree != original_tree:
            # Predecessor-tree equality above proves main adds no unreviewed content.
            # A two-parent synchronization commit preserves the complete child tree.
            chosen_head = git('commit-tree', original_tree, '-p', head, '-p', previous_squash,
                              stdin=f'LOCAL-ONLY content-preserving base synchronization for PR #{p["number"]}\n').stdout.strip()
            refreshed = True
        merged = git('merge-tree', '--write-tree', previous_squash, chosen_head)
        if merged.stdout.splitlines()[0] != original_tree:
            raise RuntimeError('Final merged tree differs from reviewed PR tree')
        squash = git('commit-tree', original_tree, '-p', previous_squash,
                     stdin=f'LOCAL-ONLY squash simulation of PR #{p["number"]}\n').stdout.strip()
        rows.append({'pr': p['number'], 'reviewed_original_head': head, 'reviewed_tree': original_tree,
                     'synthetic_main_before': previous_squash, 'direct_merge_exit': direct.returncode,
                     'base_sync_required': refreshed, 'synthetic_synced_head': chosen_head,
                     'synthetic_squash': squash, 'final_tree_matches_reviewed': tree(squash) == original_tree})
        previous_original, previous_squash = head, squash
    record = {'status': 'PASS', 'finished_utc': datetime.now(timezone.utc).isoformat(),
              'scope': 'Local Git objects only; no branch, remote, pull request or default-branch ref changed',
              'main': f['main'], 'rows': rows,
              'requires_fresh_identity_and_main_tree_checks_before_real_merge': True}
    (out/'result.json').write_text(json.dumps(record, indent=2)+'\n')
    print(json.dumps({'status': record['status'], 'prs': len(rows),
                      'base_sync_required': [r['pr'] for r in rows if r['base_sync_required']],
                      'no_refs_updated': True}))


if __name__ == '__main__':
    main()
