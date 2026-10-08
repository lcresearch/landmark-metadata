#!/usr/bin/env python3
"""Fresh, bounded actual-library parser probe; raw evidence stays outside Git."""
import argparse
import base64
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import shutil
import struct
import subprocess
import sys
import traceback
import zipfile

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
MODEL_SHA256 = "6c7ab0a6e5dcbf38a8c33b960996a55a3b4300b36a018c4545801de3a3c8bde0"
CATALOG_SHA256 = "bf49a475696eec4b38fb17587f6541a8393da14297e5dca1d433a051ba166e79"
MISSING = [
    "/workspace/repro-audit/independent-audit/label-parser/results.json",
    "/workspace/repro-audit/independent-audit/label-parser/baseline-task-comparison.json",
    "/workspace/repro-external/E5/results.json",
    "/workspace/repro-external/E5/evaluation-fixtures-before-run.json",
]


def utc():
    return datetime.now(timezone.utc).isoformat()


def identity(path):
    path = Path(path)
    data = path.read_bytes()
    return {"path": str(path), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")


def run(out, name, command):
    command = list(map(str, command))
    log = out / "commands" / name
    log.parent.mkdir(parents=True, exist_ok=True)
    record = {"command": command, "cwd": str(out), "started_utc": utc(),
              "environment_overrides": {"PYTHONDONTWRITEBYTECODE": "1"}}
    try:
        result = subprocess.run(command, cwd=out, capture_output=True, timeout=120,
                                env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
        record.update(exit_code=result.returncode, finished_utc=utc())
        stdout, stderr = result.stdout, result.stderr
    except subprocess.TimeoutExpired as error:
        stdout, stderr = error.stdout or b"", error.stderr or b""
        record.update(timeout_seconds=120, finished_utc=utc())
        result = None
    log.with_suffix(".stdout").write_bytes(stdout)
    log.with_suffix(".stderr").write_bytes(stderr)
    save(log.with_suffix(".command.json"), record)
    if result is None or result.returncode:
        raise RuntimeError(f"Command failed or timed out: {name}; see retained logs")
    return result


def recovery(out):
    """Read only exact locators, saved indexes and top-level ZIP directories."""
    rows = [{"path": name, "exists": Path(name).is_file(),
             **(identity(name) if Path(name).is_file() else {})} for name in MISSING]
    search = Path("/workspace/evidence-recovery-20261005T170453Z/search")
    targets = ("label-parser/", "baseline-task-comparison.json", "repro-external/E5/",
               "repro-audit/independent-audit")
    indexes = []
    for path in sorted(search.glob("archive-*-entries.txt")) + [search / "scanned-file-paths.txt"]:
        if not path.is_file():
            indexes.append({"path": str(path), "exists": False})
            continue
        text = path.read_text()
        indexes.append({**identity(path), "lines": len(text.splitlines()),
                        "target_matches": [line for line in text.splitlines()
                                           if any(term in line for term in targets)]})
    archives = []
    for path in sorted(Path("/workspace").glob("*.zip")):
        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()
        archives.append({**identity(path), "members": len(names),
                         "target_matches": [name for name in names
                                            if any(term in name for term in targets)]})
    candidates = []
    historical = Path("/workspace/metadata-contract-e2e-20261004T030536Z/E5")
    for name in ("results.json", "evaluation-fixtures-before-run.json"):
        path = historical / name
        if path.is_file():
            item = identity(path)
            item["matches_required_later_catalog"] = item["sha256"] == CATALOG_SHA256
            candidates.append(item)
    report = {"checked_utc": utc(), "exact_paths": rows, "indexes": indexes,
              "top_level_zip_archives": archives, "historical_candidates": candidates,
              "required_later_catalog_sha256": CATALOG_SHA256,
              "scope": "Exact paths, existing saved indexes, top-level ZIP namelists; no extraction or model search"}
    save(out / "recovery.json", report)
    return report


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def execute(args, out):
    recovery_report = recovery(out)
    maintained = REPO / "sources/repro-audit-20261004/maintained"
    sys.path.insert(0, str(maintained))
    cases = load_module("historical_cases", maintained / "test_java_labels.py")
    from java_labels import LabelEncodingUnsupported, load_java_utf8_labels

    sources = [HERE / "PROTOCOL.md", HERE / "run_probe.py",
               REPO / "sources/metadata-contract-paper/scripts/DecoderProbe.java",
               maintained / "LabelOracle.java", maintained / "java_labels.py",
               maintained / "test_java_labels.py", maintained / "runtime.py",
               REPO / "sources/repro-audit-20261004/probes/probe_label_parser.py",
               REPO / "docs/reproduction/toolchain.json"]
    source_dir = out / "sources"
    source_dir.mkdir()
    for path in sources:
        shutil.copyfile(path, source_dir / path.name)
    toolchain = json.loads((REPO / "docs/reproduction/toolchain.json").read_text())
    jars = sorted(args.deps.glob("*.jar"))
    pins = {row["jar_filename"]: row["jar_sha256"]
            for row in toolchain["acquisition_lock"]["java_dependencies"]
            if row["destination"] == "hand-deps"}
    if set(pins) != {path.name for path in jars} or len(pins) != 8:
        raise RuntimeError("Expected exact historical eight-JAR classpath")
    dependencies = []
    for path in jars:
        item = identity(path)
        item["expected_sha256"] = pins[path.name]
        item["matches_pin"] = item["sha256"] == pins[path.name]
        dependencies.append(item)
    if not all(row["matches_pin"] for row in dependencies):
        save(out / "dependencies.json", dependencies)
        raise RuntimeError("Dependency pin mismatch")
    if pins["tensorflow-lite-support-api-0.4.4.jar"] != cases.SUPPORT_API_SHA256:
        raise RuntimeError("Support oracle pin mismatch")
    model_identity = identity(args.model)
    if model_identity["sha256"] != MODEL_SHA256:
        raise RuntimeError("Source classifier pin mismatch")
    with zipfile.ZipFile(args.model) as archive:
        labels = archive.read("labels_without_background.txt")
    versions = {}
    for name, command in [("java-version", [args.java_home / "bin/java", "-version"]),
                          ("javac-version", [args.java_home / "bin/javac", "-version"]),
                          ("python-version", [sys.executable, "--version"])]:
        result = run(out, name, command)
        versions[name] = {"stdout": result.stdout.decode(), "stderr": result.stderr.decode()}
    if "17.0.12" not in versions["java-version"]["stderr"]:
        raise RuntimeError("Unexpected installed JDK version")
    environment = {"captured_utc": utc(), "python": sys.version, "platform": platform.platform(),
                   "machine": platform.machine(), "versions": versions,
                   "java_executable": identity(args.java_home / "bin/java"),
                   "javac_executable": identity(args.java_home / "bin/javac"),
                   "jdk_release": identity(args.java_home / "release"),
                   "sources": [identity(path) for path in sources],
                   "dependencies": dependencies, "model": model_identity}
    save(out / "environment.json", environment)
    shutil.copyfile(args.java_home / "release", out / "jdk-release.txt")
    classes = out / "classes"
    classes.mkdir()
    cp = ":".join(map(str, jars))
    run(out, "javac", [args.java_home / "bin/javac", "--release", "8", "-cp", cp,
                        "-d", classes, source_dir / "DecoderProbe.java", source_dir / "LabelOracle.java"])
    java = [args.java_home / "bin/java", "-cp", str(classes) + ":" + cp]
    scores = out / "scores.f32"
    scores.write_bytes(struct.pack("<1000f", *[i / 1000 for i in range(1000)]))
    variants = {
        "original": labels,
        "lf_replaced_by_vertical_tab": labels.replace(b"\n", b"\v", 1),
        "unicode_separator_inside_first_label": labels.replace(b"\n", "\u2028suffix\n".encode(), 1),
    }
    expected = {"original": (1000, 1000, "PASS"),
                "lf_replaced_by_vertical_tab": (1000, 999, "FAIL"),
                "unicode_separator_inside_first_label": (1001, 1000, "PASS")}

    def oracle(name, payload):
        result = run(out, name, java + ["LabelOracle", base64.b64encode(payload).decode()])
        lines = result.stdout.decode("ascii").splitlines()
        decoded = [base64.b64decode(line, validate=True).decode("utf8") for line in lines[1:]]
        if not lines or int(lines[0]) != len(decoded):
            raise RuntimeError("Oracle transport mismatch")
        return decoded

    checks = []
    records = []
    for name, payload in variants.items():
        folder = out / "decoder" / name
        folder.mkdir(parents=True)
        path = folder / "labels.txt"
        path.write_bytes(payload)
        actual = json.loads(run(out, name + "-decoder",
                                java + ["DecoderProbe", "1,1000", scores, path]).stdout)
        oracle_labels = oracle(name + "-oracle", payload)
        helper_labels = load_java_utf8_labels(payload)
        python_count = len([line for line in payload.decode().splitlines()
                            if line.strip("".join(chr(i) for i in range(33)))])
        python_expected, java_expected, status_expected = expected[name]
        passed = (python_count == python_expected and actual["labels"] == java_expected
                  and actual["status"] == status_expected and len(oracle_labels) == java_expected
                  and helper_labels == oracle_labels)
        if status_expected == "FAIL":
            passed = passed and actual.get("exception") == "java.lang.IllegalArgumentException"
            passed = passed and actual.get("message") == "Label number 999 mismatch the shape on axis 1"
        else:
            passed = passed and actual.get("categories") == 1000
        records.append({"condition": name, "label_input": identity(path),
                        "python_splitlines_count": python_count, "actual_library": actual,
                        "maintained_equals_actual_labels": helper_labels == oracle_labels,
                        "passed_declared_comparison": passed})
        checks.append(passed)
    differential = []
    for name, payload in cases.CASES.items():
        path = out / "differential" / (name + ".bin")
        path.parent.mkdir(exist_ok=True)
        path.write_bytes(payload)
        actual = oracle("valid-" + name, payload)
        helper = load_java_utf8_labels(payload)
        passed = actual == helper
        differential.append({"case": name, "input": identity(path), "oracle_labels": actual,
                             "helper_labels": helper, "equal_strings": passed})
        checks.append(passed)
    malformed = []
    for name, payload in cases.MALFORMED.items():
        path = out / "malformed" / (name + ".bin")
        path.parent.mkdir(exist_ok=True)
        path.write_bytes(payload)
        actual = oracle("malformed-" + name, payload)
        try:
            helper = load_java_utf8_labels(payload)
        except LabelEncodingUnsupported as error:
            abstain = True
            detail = str(error)
        else:
            abstain, detail = False, repr(helper)
        malformed.append({"case": name, "input": identity(path), "oracle_labels": actual,
                          "helper_abstained": abstain, "helper_detail": detail,
                          "python_replace_text": payload.decode("utf8", errors="replace")})
        checks.append(abstain)
    if (len(records), len(differential), len(malformed)) != (3, 22, 3):
        raise RuntimeError("Unexpected comparison denominator")
    report = {"status": "PASS" if all(checks) else "FAIL", "finished_utc": utc(),
              "scope": "Fresh isolated FileUtil/TensorLabel and maintained helper probes; no model inference, Task or 65-fixture regression",
              "historical_exact_paths_still_absent": all(not row["exists"] for row in recovery_report["exact_paths"]),
              "decoder_conditions": records, "valid_utf8_cases": differential,
              "malformed_cases": malformed, "scores": identity(scores),
              "passed_comparisons": sum(checks), "failed_comparisons": len(checks) - sum(checks)}
    save(out / "results.json", report)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--java-home", type=Path, default=Path("/workspace/hand-contract-repro/toolchains/jdk-17.0.12+7"))
    parser.add_argument("--deps", type=Path, default=Path("/workspace/hand-contract-repro/deps"))
    parser.add_argument("--model", type=Path, default=Path("/workspace/metadata-contract-paper/models/components") / (MODEL_SHA256 + ".tflite"))
    args = parser.parse_args()
    out = args.output_dir.resolve()
    if out.is_relative_to(REPO):
        parser.error("Raw evidence must remain outside the source checkout")
    out.mkdir(parents=True, exist_ok=False)
    save(out / "invocation.json", {"command": [sys.executable, *sys.argv], "started_utc": utc(),
                                   "cwd": str(Path.cwd()), "runner": identity(__file__),
                                   "protocol": identity(HERE / "PROTOCOL.md")})
    exit_code = 1
    try:
        report = execute(args, out)
        exit_code = 0 if report["status"] == "PASS" else 1
        print(json.dumps({"status": report["status"], "passed_comparisons": report["passed_comparisons"],
                          "failed_comparisons": report["failed_comparisons"], "output": str(out)}))
    except Exception as error:
        save(out / "controller-error.json", {"type": type(error).__name__, "message": str(error),
                                             "traceback": traceback.format_exc()})
        traceback.print_exc()
    finally:
        save(out / "completion.json", {"finished_utc": utc(), "exit_code": exit_code})
        entries = [identity(path) for path in sorted(out.rglob("*")) if path.is_file()]
        save(out / "evidence-files.json", entries)
    raise SystemExit(exit_code)


if __name__ == "__main__":
    main()
