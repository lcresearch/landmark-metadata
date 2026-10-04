#!/usr/bin/env python3
"""Extract the six saved guide bodies with lxml; verify existing text, never replace it."""
import argparse
import hashlib
import json
from pathlib import Path
import re

from lxml import etree, html


def digest(path):
    data = path.read_bytes()
    return {"path": str(path), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, required=True)
    parser.add_argument("--index", type=Path, required=True)
    args = parser.parse_args()
    if args.index.exists():
        raise FileExistsError(args.index)
    records = []
    for number in range(1, 7):
        ident = f"WF{number:02d}"
        source = args.directory / f"{ident}.html"
        record_path = args.directory / f"{ident}.record.json"
        record = json.loads(record_path.read_text())
        if record["http_status"] != 200 or record["curl_exit_code"] != 0:
            records.append({"id": ident, "inspection": "unavailable", "retrieval": record})
            continue
        tree = html.fromstring(source.read_bytes())
        bodies = tree.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," devsite-article-body ")]')
        if not bodies:
            bodies = tree.xpath("//main")
        if not bodies:
            raise ValueError(f"No article body for {ident}")
        text = "\n".join(body.text_content() for body in bodies)
        text = "\n".join(line.rstrip() for line in text.splitlines() if line.strip()) + "\n"
        target = source.with_suffix(".txt")
        encoded = text.encode("utf-8")
        if target.exists():
            if target.read_bytes() != encoded:
                raise ValueError(f"Existing extraction differs for {ident}")
        else:
            with target.open("xb") as output:
                output.write(encoded)
        dates = sorted(set(re.findall(r"Last updated (\d{4}-\d{2}-\d{2}) UTC", source.read_text())))
        records.append({"id": ident, "inspection": "selected_sections", "retrieval": record,
                        "title": tree.xpath("//title/text()"), "displayed_last_updated_dates": dates,
                        "extracted_text": digest(target), "line_count": len(text.splitlines())})
    result = {"lxml_version": etree.LXML_VERSION, "documents": records}
    with args.index.open("x") as output:
        json.dump(result, output, indent=2)
        output.write("\n")
    print(f"Indexed {len(records)} guides in {args.index}")


if __name__ == "__main__":
    main()
