#!/usr/bin/env python3
"""Bounded ordinary public retrieval; keep third-party bytes outside Git.

Each invocation makes exactly one public request (normal redirects allowed).
The caller must inspect denial/error records before any further source request.
This does not retry or bypass policy. Existing evidence is never overwritten.
"""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("url")
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    body_path = args.output_dir / (args.name + ".body")
    record_path = args.output_dir / (args.name + ".json")
    if body_path.exists() or record_path.exists():
        raise SystemExit("Refusing to overwrite preserved retrieval")
    record = {
        "url": args.url,
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "body_path": str(body_path),
        "request_count": 1,
    }
    try:
        with urlopen(Request(args.url, headers={"User-Agent": "ResearchSourceAudit/1.0"}), timeout=45) as response:
            body = response.read()
            record.update(status=response.status, final_url=response.url, headers=dict(response.headers))
    except HTTPError as exc:
        body = exc.read()
        record.update(status=exc.code, final_url=exc.url, headers=dict(exc.headers), error=str(exc))
    except (URLError, TimeoutError) as exc:
        body = b""
        record.update(status=None, error=str(exc))
    with body_path.open("xb") as handle:
        handle.write(body)
    record.update(size_bytes=len(body), sha256=hashlib.sha256(body).hexdigest())
    with record_path.open("x", encoding="utf-8") as handle:
        json.dump(record, handle, indent=2)
        handle.write("\n")
    print(json.dumps({key: record.get(key) for key in ("url", "status", "final_url", "size_bytes", "sha256", "error")}))


if __name__ == "__main__":
    main()
