#!/usr/bin/env python3
"""Retrieve six declared official guides; keep third-party bytes outside Git.

Requires curl. This does not execute models or expand the source set. Existing
files are never overwritten. HTTP bodies, redirect headers and curl diagnostics
are retained even when the document is unavailable.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess


GUIDES = [
    ("WF01", "Metadata code generation", "https://www.tensorflow.org/lite/inference_with_metadata/codegen"),
    ("WF02", "Android Studio ML Model Binding", "https://developer.android.com/studio/releases/past-releases/as-4-1-0-release-notes#tensorflow-lite-models"),
    ("WF03", "Support library labeling", "https://www.tensorflow.org/lite/inference_with_metadata/lite_support"),
    ("WF04", "Task ImageClassifier", "https://www.tensorflow.org/lite/inference_with_metadata/task_library/image_classifier"),
    ("WF05", "Metadata and associated files", "https://www.tensorflow.org/lite/models/convert/metadata"),
    ("WF06", "Metadata writer tutorial", "https://www.tensorflow.org/lite/models/convert/metadata_writer_tutorial"),
]


def fetch(item, directory):
    ident, title, url = item
    paths = {suffix: directory / (ident + suffix) for suffix in
             (".html", ".headers", ".curl.json", ".stderr", ".record.json")}
    if any(path.exists() for path in paths.values()):
        raise FileExistsError(f"Refusing to replace evidence for {ident}")
    timestamp = datetime.now(timezone.utc).isoformat()
    command = ["curl", "--location", "--max-time", "60", "--silent", "--show-error",
               "--dump-header", str(paths[".headers"]), "--output", str(paths[".html"]),
               "--write-out", "%{json}", url]
    completed = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    paths[".curl.json"].write_bytes(completed.stdout)
    paths[".stderr"].write_bytes(completed.stderr)
    try:
        info = json.loads(completed.stdout)
    except (json.JSONDecodeError, UnicodeDecodeError):
        info = {}
    record = {"id": ident, "title": title, "requested_url": url,
              "retrieved_at_utc": timestamp, "command": command,
              "curl_exit_code": completed.returncode,
              "http_status": info.get("http_code"), "effective_url": info.get("url_effective"),
              "num_redirects": info.get("num_redirects"), "files": {}}
    for suffix, path in paths.items():
        if suffix == ".record.json" or not path.exists():
            continue
        data = path.read_bytes()
        record["files"][suffix] = {"path": str(path), "bytes": len(data),
                                  "sha256": hashlib.sha256(data).hexdigest()}
    with paths[".record.json"].open("x") as output:
        json.dump(record, output, indent=2)
        output.write("\n")
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, required=True)
    args = parser.parse_args()
    args.directory.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=6) as executor:
        records = list(executor.map(lambda item: fetch(item, args.directory), GUIDES))
    with (args.directory / "retrieval-index.json").open("x") as output:
        json.dump(records, output, indent=2)
        output.write("\n")
    for record in records:
        print(record["id"], record["http_status"], record["effective_url"])


if __name__ == "__main__":
    main()
