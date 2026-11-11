#!/usr/bin/env python3
"""Differential regression tests using the real Support 0.4.4 FileUtil API.

No downloaded assets or model inference. Requires the recovered JDK/JARs and
writes only into a new external output directory. Missing prerequisites fail.
"""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
sys.dont_write_bytecode = True

from java_labels import LabelEncodingUnsupported, load_java_utf8_labels
from runtime import require_external

SUPPORT_API_SHA256 = "15d59ab34528d75908306432715e522a278f781ba6f4802d6b41917a5838a59d"
CASES = {
    "empty": b"",
    "single_no_final_newline": b"cat",
    "lf": b"cat\ndog\n",
    "cr": b"cat\rdog\r",
    "crlf": b"cat\r\ndog\r\n",
    "mixed_crlf": b"\ncat\r\n\rdog\n\rfox\r",
    "blank_lines": b"\r\n\r\r\n\n",
    "java_trim_blank": b" \t\x00\x1f\r\n\x0b\x0c\n",
    "retain_label_whitespace": b" \tcat\t \n dog \n",
    "vt_within_label": b"cat\vdog\n",
    "ff_within_label": b"cat\fdog\n",
    "record_separators_within_label": b"cat\x1c\x1d\x1edog\n",
    "nel_within_label": "cat\u0085dog\n".encode(),
    "line_separator_within_label": "cat\u2028dog\n".encode(),
    "paragraph_separator_within_label": "cat\u2029dog\n".encode(),
    "unicode_separator_only_lines": "\u0085\n\u2028\n\u2029\n".encode(),
    "unicode_whitespace_retained": "\u00a0\n\u2003\n\u3000\n".encode(),
    "utf8_bom_retained": b"\xef\xbb\xbfcat\n",
    "non_ascii": "猫\n犬😀\n".encode(),
    "embedded_null_retained": b"cat\0dog\n",
    "efficientnet_lf_to_vt_regression": b"cat\vdog\n" + b"label\n" * 998,
    "efficientnet_unicode_separator_regression": "cat\u2028suffix\n".encode() + b"label\n" * 999,
}
MALFORMED = {
    "surrogate_encoding": b"cat\xed\xa0\x80dog\n",
    "truncated_multibyte": b"cat\xe2\x82\n",
    "lone_continuation": b"cat\x80dog\n",
}


def checked_run(command):
    result = subprocess.run(list(map(str, command)), capture_output=True, text=True, timeout=60)
    if result.returncode:
        raise RuntimeError(f"Command failed ({result.returncode}): {command!r}\n{result.stderr}")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--java-home", type=Path, default=Path("/workspace/hand-contract-repro/toolchains/jdk-17.0.12+7"))
    parser.add_argument("--deps", type=Path, default=Path("/workspace/hand-contract-repro/deps"))
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    out = require_external(args.output_dir) if args.output_dir else Path(tempfile.mkdtemp(prefix="java-label-regression-", dir="/tmp"))
    if args.output_dir:
        out.mkdir(parents=True, exist_ok=False)
    jars = sorted(args.deps.glob("*.jar"))
    support_api = args.deps / "tensorflow-lite-support-api-0.4.4.jar"
    if hashlib.sha256(support_api.read_bytes()).hexdigest() != SUPPORT_API_SHA256:
        raise RuntimeError("The FileUtil oracle JAR does not match the pinned artifact digest")
    classpath = ":".join(map(str, jars))
    source = Path(__file__).resolve().with_name("LabelOracle.java")
    compile_command = [args.java_home / "bin/javac", "--release", "8", "-cp", classpath, "-d", out, source]
    checked_run(compile_command)
    java = [args.java_home / "bin/java", "-cp", str(out) + ":" + classpath, "LabelOracle"]

    def oracle(payload):
        lines = checked_run(java + [base64.b64encode(payload).decode()]).stdout.splitlines()
        labels = [base64.b64decode(line).decode("utf-8") for line in lines[1:]]
        if int(lines[0]) != len(labels):
            raise RuntimeError("Oracle transport count mismatch")
        return labels

    rows = []
    for name, payload in CASES.items():
        actual = load_java_utf8_labels(payload)
        expected = oracle(payload)
        rows.append({"case": name, "payload_sha256": hashlib.sha256(payload).hexdigest(),
                     "helper_count": len(actual), "oracle_count": len(expected), "equal_strings": actual == expected})
        if actual != expected:
            raise AssertionError(f"{name}: helper {actual!r} != Java {expected!r}")
    malformed = []
    for name, payload in MALFORMED.items():
        expected = oracle(payload)
        try:
            load_java_utf8_labels(payload)
        except LabelEncodingUnsupported:
            pass
        else:
            raise AssertionError(f"{name}: malformed bytes must require abstention")
        malformed.append({"case": name, "helper": "ABSTAIN_REQUIRED", "java_labels": expected,
                          "python_replace_text": payload.decode("utf-8", errors="replace"),
                          "reason": "Replacement-decoder equivalence intentionally not assumed."})
    if len(CASES) == 0 or len(MALFORMED) == 0:
        raise RuntimeError("Empty regression suite")
    result = {"status": "PASS", "valid_utf8_cases": rows, "malformed_cases": malformed,
              "valid_utf8_count": len(rows), "abstention_count": len(malformed),
              "oracle_support_api_sha256": SUPPORT_API_SHA256,
              "java_version": checked_run([args.java_home / "bin/java", "-version"]).stderr,
              "compile_command": list(map(str, compile_command))}
    (out / "result.json").write_text(json.dumps(result, indent=2))
    print(json.dumps({"status": "PASS", "valid_utf8_cases": len(rows), "malformed_abstentions": len(malformed), "evidence": str(out / "result.json")}, indent=2))


if __name__ == "__main__":
    main()
