#!/usr/bin/env python3
"""Collect the fixed, bounded GitHub issue sample; keep all API bytes outside Git.

Run search before manual title/body triage. Then run inspect with a JSON list of
eligible issue URLs in the deduplicated search order. This script neither runs
issue code nor downloads models. GitHub authentication/proxy are inherited by gh.
Output files are exclusively created: use a new directory for a new inquiry.
"""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
from urllib.parse import urlparse


QUERIES = [
    'repo:tensorflow/tflite-support is:issue "Label number"',
    'repo:tensorflow/tensorflow is:issue "Label number"',
    'repo:google-ai-edge/mediapipe is:issue "label map"',
    'repo:tensorflow/tflite-support is:issue "label map"',
    'repo:tensorflow/tensorflow is:issue metadata label order',
    'repo:tensorflow/tflite-support is:issue label order',
    'repo:google-ai-edge/mediapipe is:issue metadata output',
    'repo:tensorflow/tflite-support is:issue metadata output',
]
CUTOFF = '2026-10-04'


def write(path, data):
    with path.open('xb') as stream:
        stream.write(data)


def record_json(path, value):
    write(path, (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode())


def request(root, stem, endpoint, fields=()):
    command = ['gh', 'api', '--method', 'GET', endpoint]
    for key, value in fields:
        command.extend(['-f', f'{key}={value}'])
    started = datetime.now(timezone.utc).isoformat()
    result = subprocess.run(command, capture_output=True, check=False)
    response = root / f'{stem}.json'
    stderr = root / f'{stem}.stderr'
    write(response, result.stdout)
    write(stderr, result.stderr)
    record = {
        'command': command, 'retrieved_utc': started,
        'exit_code': result.returncode, 'response_path': str(response),
        'response_sha256': hashlib.sha256(result.stdout).hexdigest(),
        'response_bytes': len(result.stdout), 'stderr_path': str(stderr),
        'stderr_sha256': hashlib.sha256(result.stderr).hexdigest(),
    }
    try:
        payload = json.loads(result.stdout) if result.returncode == 0 else None
    except json.JSONDecodeError:
        payload = None
    record['status'] = 'FETCHED' if payload is not None else 'UNAVAILABLE'
    record_json(root / f'{stem}.request.json', record)
    return record, payload


def search(root):
    searches = []
    unique = {}
    for number, base in enumerate(QUERIES, 1):
        query = f'{base} created:<={CUTOFF}'
        record, payload = request(root, f'query-{number:02d}', 'search/issues', [
            ('q', query), ('sort', 'created'), ('order', 'asc'), ('per_page', 5), ('page', 1),
        ])
        record.update({'query_id': number, 'query': query})
        if payload is not None:
            items = payload['items']
            record.update({
                'total_count': payload['total_count'],
                'incomplete_results': payload['incomplete_results'],
                'returned_count': len(items),
                'returned_urls': [item['html_url'] for item in items],
                'returned_ids': [item['id'] for item in items],
            })
            for rank, item in enumerate(items, 1):
                url = item['html_url']
                if url not in unique:
                    unique[url] = {
                        'url': url, 'id': item['id'], 'number': item['number'],
                        'title': item['title'], 'created_at': item['created_at'],
                        'first_query': number, 'first_rank': rank, 'occurrences': [],
                    }
                unique[url]['occurrences'].append({'query': number, 'rank': rank})
        searches.append(record)
    output = {'searches': searches, 'unique_issues': list(unique.values())}
    record_json(root / 'search-index.json', output)
    print(json.dumps(output, indent=2, ensure_ascii=False))


def inspect(root, eligible_file):
    eligible = json.loads(eligible_file.read_text())
    index = json.loads((root / 'search-index.json').read_text())
    order = [item['url'] for item in index['unique_issues']]
    if len(set(eligible)) != len(eligible) or eligible != [url for url in order if url in eligible]:
        raise ValueError('Eligible URLs must be unique and follow the fixed search order')
    reports = []
    for number, url in enumerate(eligible[:8], 1):
        parts = urlparse(url).path.strip('/').split('/')
        owner, repo, kind, issue = parts
        if kind != 'issues':
            raise ValueError(f'Not an issue URL: {url}')
        endpoint = f'repos/{owner}/{repo}/issues/{issue}'
        record, payload = request(root, f'issue-{number:02d}', endpoint)
        comments_record, comments = request(root, f'issue-{number:02d}-comments',
                                           endpoint + '/comments', [('per_page', 100), ('page', 1)])
        record.update({
            'url': url, 'comments_request': comments_record,
            'reported_comment_count': payload.get('comments') if payload else None,
            'returned_comments': len(comments) if isinstance(comments, list) else None,
        })
        if payload is not None and isinstance(comments, list):
            record['omitted_comments'] = max(0, payload['comments'] - len(comments))
        reports.append(record)
    record_json(root / 'inspection-index.json', reports)
    print(json.dumps(reports, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['search', 'inspect'])
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--eligible', type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    if args.mode == 'search':
        search(args.output)
    elif args.eligible is None:
        parser.error('inspect requires --eligible')
    else:
        inspect(args.output, args.eligible)


if __name__ == '__main__':
    main()
