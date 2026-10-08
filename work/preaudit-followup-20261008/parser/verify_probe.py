#!/usr/bin/env python3
"""Read back saved fresh parser bytes and actual-library stdout without rerunning."""
import argparse
import base64
import hashlib
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()
    root = args.evidence.resolve()
    report_path = args.report.resolve()
    repo = Path(__file__).resolve().parents[3]
    if report_path.is_relative_to(repo) or report_path.is_relative_to(root):
        parser.error("Readback output must stay outside Git and the frozen probe directory")
    if report_path.exists():
        parser.error("Readback report already exists; choose a new path")
    checks = []

    def check(name, passed):
        checks.append({"check": name, "passed": bool(passed)})

    def read(name):
        return json.loads((root / name).read_text())

    entries = read("evidence-files.json")
    paths = [Path(row["path"]).resolve() for row in entries]
    actual_files = {path.resolve() for path in root.rglob("*") if path.is_file()
                    and path != root / "evidence-files.json"}
    check("manifest exact nonempty file set without self", bool(paths)
          and len(paths) == len(set(paths)) and set(paths) == actual_files)
    for row, path in zip(entries, paths):
        check("manifest path inside evidence: " + path.name, path.is_relative_to(root))
        data = path.read_bytes()
        check("manifest bytes and SHA-256: " + str(path.relative_to(root)),
              len(data) == row["bytes"] and hashlib.sha256(data).hexdigest() == row["sha256"])
    result = read("results.json")
    environment = read("environment.json")
    expected = {"original": (1000, 1000, "PASS"),
                "lf_replaced_by_vertical_tab": (1000, 999, "FAIL"),
                "unicode_separator_inside_first_label": (1001, 1000, "PASS")}
    check("exact decoder condition names", len(result["decoder_conditions"]) == 3
          and {row["condition"] for row in result["decoder_conditions"]} == set(expected))
    commands = sorted((root / "commands").glob("*.command.json"))
    check("35 retained successful process calls", len(commands) == 35
          and all(json.loads(path.read_text())["exit_code"] == 0 for path in commands))

    def oracle(name):
        lines = (root / "commands" / (name + ".stdout")).read_text().splitlines()
        labels = [base64.b64decode(line, validate=True).decode("utf8") for line in lines[1:]]
        check("oracle transport " + name, int(lines[0]) == len(labels))
        return labels

    for row in result["decoder_conditions"]:
        name = row["condition"]
        actual = read("commands/" + name + "-decoder.stdout")
        check("actual decoder stdout " + name, actual == row["actual_library"])
        labels = oracle(name + "-oracle")
        payload = (root / "decoder" / name / "labels.txt").read_bytes()
        python_count = len([line for line in payload.decode().splitlines()
                            if line.strip("".join(chr(i) for i in range(33)))])
        check("declared counts/status " + name,
              (python_count, len(labels), actual["status"]) == expected[name]
              and actual["labels"] == len(labels) and row["python_splitlines_count"] == python_count)
        if name == "lf_replaced_by_vertical_tab":
            check("VT exact exception", actual.get("exception") == "java.lang.IllegalArgumentException"
                  and actual.get("message") == "Label number 999 mismatch the shape on axis 1")
        else:
            check("1000 returned categories " + name, actual.get("categories") == 1000)
    check("22 valid and 3 malformed cases", len(result["valid_utf8_cases"]) == 22
          and len(result["malformed_cases"]) == 3)
    for row in result["valid_utf8_cases"]:
        labels = oracle("valid-" + row["case"])
        check("valid exact strings " + row["case"], labels == row["oracle_labels"]
              and labels == row["helper_labels"] and row["equal_strings"])
    for row in result["malformed_cases"]:
        labels = oracle("malformed-" + row["case"])
        check("malformed abstention " + row["case"], labels == row["oracle_labels"]
              and row["helper_abstained"])
    check("all dependency identities match prior pins", len(environment["dependencies"]) == 8
          and all(row["sha256"] == row["expected_sha256"] and row["matches_pin"]
                  for row in environment["dependencies"]))
    for row in environment["sources"]:
        copied = root / "sources" / Path(row["path"]).name
        check("copied source identity " + copied.name,
              hashlib.sha256(copied.read_bytes()).hexdigest() == row["sha256"])
    check("fresh aggregate result", result["status"] == "PASS"
          and result["passed_comparisons"] == 28 and result["failed_comparisons"] == 0
          and read("completion.json")["exit_code"] == 0)
    output = {"scope": "Saved-byte and actual stdout readback; no new library execution or human review",
              "evidence": str(root), "manifest_entries": len(entries),
              "passed": sum(row["passed"] for row in checks),
              "failed": sum(not row["passed"] for row in checks), "checks": checks}
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({key: value for key, value in output.items() if key != "checks"}))
    raise SystemExit(1 if output["failed"] else 0)


if __name__ == "__main__":
    main()
