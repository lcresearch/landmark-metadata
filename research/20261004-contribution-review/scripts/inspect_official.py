#!/usr/bin/env python3
"""Retrieve or verify this review's fixed official source set outside Git.

This checks source identity, not experimental outcomes or source/binary identity.
It uses the normal configured urllib proxy and does not search alternate hosts.
Existing files are verified, never overwritten. HTTP/JSON provenance responses
are digest-pinned as retrieved; an upstream serialization change fails explicitly.
"""

import argparse
import hashlib
import json
from pathlib import Path
import urllib.request


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", required=True, type=Path)
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    manifest = json.loads(
        (Path(__file__).resolve().parents[1] / "official-sources.json").read_text()
    )
    directory = args.directory.resolve()
    repository = Path(__file__).resolve().parents[3]
    if directory == repository or repository in directory.parents:
        parser.error("Downloaded third-party source must remain outside the repository")
    directory.mkdir(parents=True, exist_ok=True)
    checked = []
    for source in manifest["sources"]:
        destination = directory / source["repository_path"]
        if not destination.exists():
            if args.verify_only:
                raise FileNotFoundError(destination)
            with urllib.request.urlopen(source["url"], timeout=30) as response:
                data = response.read()
            if hashlib.sha256(data).hexdigest() != source["sha256"]:
                raise ValueError(f"Retrieved digest mismatch: {source['source_id']}")
            destination.parent.mkdir(parents=True, exist_ok=True)
            with destination.open("xb") as output:
                output.write(data)
        data = destination.read_bytes()
        if hashlib.sha256(data).hexdigest() != source["sha256"]:
            raise ValueError(f"Stored digest mismatch: {source['source_id']}")
        if "git_blob_sha1" in source:
            blob = b"blob " + str(len(data)).encode() + b"\0" + data
            if hashlib.sha1(blob).hexdigest() != source["git_blob_sha1"]:
                raise ValueError(f"Git blob mismatch: {source['source_id']}")
        checked.append(source["source_id"])
    tag = json.loads((directory / "tag.json").read_text())
    tree = json.loads((directory / "tree.json").read_text())
    if tag["sha"] != manifest["resolved_commit"]:
        raise ValueError("Tag does not resolve to pinned commit")
    if tree["sha"] != manifest["resolved_commit"] or tree["truncated"]:
        raise ValueError("Pinned tree is incomplete or identifies another commit")
    entries = {entry["path"]: entry for entry in tree["tree"]}
    for source in manifest["sources"]:
        if "git_blob_sha1" in source:
            if entries[source["repository_path"]]["sha"] != source["git_blob_sha1"]:
                raise ValueError(f"Tree membership mismatch: {source['source_id']}")
    print(json.dumps({"status": "PASS", "checked_sources": checked,
                      "commit": manifest["resolved_commit"],
                      "scope": "source identity only"}, indent=2))


if __name__ == "__main__":
    main()
