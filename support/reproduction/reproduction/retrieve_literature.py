#!/usr/bin/env python3
"""Bounded retrieval of the manuscript's four method papers and cited identities.

Retains normal proxy and CA verification. No alternate-host fallback after a
policy denial. Outputs belong outside Git; this script may be committed.
"""
import argparse
import concurrent.futures
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import urllib.error
import urllib.request

VERSIONS = {"mlguard": "2309.01379v1", "docter": "2109.01002v4", "acetest": "2305.17914v2"}
DOIS = {
    "mlguard": "10.1145/3617574.3617859",
    "docter": "10.1145/3533767.3534220",
    "acetest": "10.1145/3597926.3598088",
    "meyer": "10.1109/2.161279",
    "stalnaker": "10.1145/3776739",
    "dara": "10.1007/s10664-025-10711-4",
}


def fetch(job, root):
    name, url = job
    row = {"name": name, "url": url, "retrieved_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    path = root / name
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "LiteratureAudit/1.0 (bounded reproducibility review)"})
        with urllib.request.urlopen(request, timeout=45) as response:
            payload = response.read()
            row.update(http_status=response.status, final_url=response.geturl(), content_type=response.headers.get("Content-Type"))
        path.write_bytes(payload)
        row.update(status="DOWNLOADED", path=str(path), bytes=len(payload), sha256=hashlib.sha256(payload).hexdigest())
        if path.suffix == ".pdf":
            if not payload.startswith(b"%PDF"):
                row["status"] = "NOT_A_PDF"
            else:
                command = ["pdftotext", "-layout", str(path), str(path.with_suffix(".txt"))]
                row['text_command'] = command
                try:
                    process = subprocess.run(command, capture_output=True, text=True, timeout=45)
                    row.update(text_status='PASS' if process.returncode == 0 else 'FAIL',
                               text_exit=process.returncode, text_error=process.stderr)
                except subprocess.TimeoutExpired:
                    row.update(text_status='TIMEOUT', text_timeout_seconds=45)
                except OSError as error:
                    row.update(text_status='UNAVAILABLE', text_error=str(error))
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        row.update(status="UNAVAILABLE", error_type=type(error).__name__, error=str(error))
        if isinstance(error, urllib.error.HTTPError):
            row["http_status"] = error.code
    return row


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=False)
    jobs = [(name + "-crossref.json", "https://api.crossref.org/works/" + doi) for name, doi in DOIS.items()]
    for name, version in VERSIONS.items():
        jobs.extend([(name + ".pdf", "https://arxiv.org/pdf/" + version), (name + "-abstract.html", "https://arxiv.org/abs/" + version)])
    jobs.extend([
        ("dara.pdf", "https://link.springer.com/content/pdf/10.1007/s10664-025-10711-4.pdf"),
        ("aibom-abstract.html", "https://arxiv.org/abs/2607.17242v1"),
    ])
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(lambda job: fetch(job, args.output_dir), jobs))
    (args.output_dir / "retrieval.json").write_text(json.dumps(results, indent=2))
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
