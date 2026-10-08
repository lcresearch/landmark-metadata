#!/usr/bin/env python3
"""Build both manuscript sources in a new external directory; preserve command logs."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
from datetime import datetime, timezone


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--ieeetran", required=True, type=Path)
    args = parser.parse_args()
    source = Path(__file__).resolve().parent
    repository = source.parents[1]
    output = args.output.resolve()
    if output.is_relative_to(repository) or repository.is_relative_to(output):
        raise SystemExit("Build output must be outside and not contain the repository")
    if hashlib.sha256(args.ieeetran.read_bytes()).hexdigest() != (
        "da751920a317ed318b7b5cd7fa585a6cc7d28502d457856382e9be24b10a3bd7"
    ):
        raise SystemExit("IEEEtran V1.8b identity mismatch")
    output.mkdir(parents=True, exist_ok=False)
    tex = output / "tex"
    tex.mkdir()
    shutil.copyfile(args.ieeetran, tex / "IEEEtran.cls")
    shutil.copyfile(__file__, output / "build_documents.py")
    environment = dict(os.environ, TEXINPUTS=str(tex) + ":")
    commands = []

    def run(argv, prefix):
        started = datetime.now(timezone.utc).isoformat()
        result = subprocess.run(argv, cwd=output, env=environment, capture_output=True)
        (output / (prefix + ".stdout")).write_bytes(result.stdout)
        (output / (prefix + ".stderr")).write_bytes(result.stderr)
        commands.append({"argv": argv, "cwd": str(output), "started_utc": started,
                         "returncode": result.returncode, "output_prefix": prefix,
                         "environment_override": {"TEXINPUTS": environment["TEXINPUTS"]}})
        (output / "commands.json").write_text(json.dumps(commands, indent=2) + "\n")
        if result.returncode:
            raise SystemExit(f"Build command failed: {prefix}; see preserved output")

    run(["pdflatex", "--version"], "pdflatex-version")
    run(["pdfinfo", "-v"], "poppler-version")
    for name in ("paper", "paper-full"):
        build = output / name
        build.mkdir()
        shutil.copyfile(source / "manuscript" / (name + ".tex"), build / (name + ".tex"))
        for pass_number in (1, 2):
            run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "-file-line-error",
                 "-output-directory=" + str(build), str(build / (name + ".tex"))],
                f"{name}/pass-{pass_number}")
        pdf = str(build / (name + ".pdf"))
        run(["pdfinfo", pdf], f"{name}/pdfinfo")
        run(["pdftotext", "-layout", pdf, str(build / "paper.txt")], f"{name}/pdftotext")
        run(["pdftoppm", "-scale-to", "1300", "-png", pdf, str(build / "page")],
            f"{name}/render")
    lines = []
    for path in sorted(output.rglob("*")):
        if path.is_file():
            lines.append(hashlib.sha256(path.read_bytes()).hexdigest() + "  " +
                         path.relative_to(output).as_posix())
    (output / "SHA256SUMS").write_text("\n".join(lines) + "\n")
    print(output)


if __name__ == "__main__":
    main()
