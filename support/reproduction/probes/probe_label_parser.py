#!/usr/bin/env python3
"""Real pinned E5 and Support Java comparison on declared label-only mutants.

This is a new fault-injection experiment, not a natural defect or historical
fixture reproduction. The Java probe calls FileUtil and TensorLabel on fixed
synthetic score bytes; it does not execute the Android generated wrapper.
"""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import struct
import subprocess
import sys
import zipfile

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'maintained'))
from evidence_validation import generated_sources_identical
BASE = Path('/workspace/repro-audit/independent-audit')
ROOT = BASE / 'label-parser'
HAND = Path('/workspace/hand-contract-repro')
PYTHON = HAND / '.venv/bin/python'
JDK = HAND / 'toolchains/jdk-17.0.12+7'
E2E = REPO / 'sources/metadata-contract-e2e-20261004T030536Z'
PAPER = REPO / 'sources/metadata-contract-paper'
MODEL = Path('/workspace/metadata-contract-paper/models/components/6c7ab0a6e5dcbf38a8c33b960996a55a3b4300b36a018c4545801de3a3c8bde0.tflite')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def run(command, name):
    result = subprocess.run(list(map(str, command)), capture_output=True, timeout=120,
                            env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
    (ROOT / (name + '.stdout')).write_bytes(result.stdout)
    (ROOT / (name + '.stderr')).write_bytes(result.stderr)
    (ROOT / (name + '.command.json')).write_text(json.dumps({'command': list(map(str, command)), 'exit_code': result.returncode}, indent=2))
    return result


def main():
    global ROOT, BASE, MODEL
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, required=True, help='New isolated directory outside the source checkout.')
    parser.add_argument('--model', type=Path, default=MODEL)
    args = parser.parse_args()
    BASE = args.output_dir.resolve()
    if BASE.is_relative_to(REPO):
        raise ValueError('Synthetic evidence must stay outside the source repository')
    BASE.mkdir(parents=True, exist_ok=False)
    ROOT = BASE / 'label-parser'
    MODEL = args.model.resolve()
    ROOT.mkdir(parents=True, exist_ok=False)
    scripts = ROOT / 'scripts'
    scripts.mkdir()
    for name in ('preflight.py', 'common.py', 'codegen_one.py'):
        shutil.copyfile(E2E / 'scripts' / name, scripts / name)
    imports = BASE / 'metadata-contract-paper/scripts'
    imports.mkdir(parents=True, exist_ok=False)
    for name in ('suite_static.py', 'inspect_suite.py'):
        shutil.copyfile(PAPER / 'scripts' / name, imports / name)
    java = ROOT / 'DecoderProbe.java'
    shutil.copyfile(PAPER / 'scripts/DecoderProbe.java', java)
    classes = ROOT / 'classes'
    classes.mkdir()
    cp = ':'.join(map(str, sorted((HAND / 'deps').glob('*.jar'))))
    compile_result = run([JDK / 'bin/javac', '--release', '8', '-cp', cp, '-d', classes, java], 'javac')
    if compile_result.returncode:
        raise RuntimeError(compile_result.stderr.decode())
    original = MODEL.read_bytes()
    if digest(original) != MODEL.stem:
        raise RuntimeError('Publisher artifact digest mismatch')
    with zipfile.ZipFile(io.BytesIO(original)) as archive:
        entries = {name: archive.read(name) for name in archive.namelist()}
        prefix_size = min(item.header_offset for item in archive.infolist())
    name = 'labels_without_background.txt'
    labels = entries[name]
    variants = {
        'original': labels,
        'lf_replaced_by_vertical_tab': labels.replace(b'\n', b'\v', 1),
        'unicode_separator_inside_first_label': labels.replace(b'\n', '\u2028suffix\n'.encode(), 1),
    }
    scores = ROOT / 'scores.f32'
    scores.write_bytes(struct.pack('<1000f', *[i / 1000 for i in range(1000)]))
    records = []
    for variant, payload in variants.items():
        folder = ROOT / variant
        folder.mkdir()
        label_file = folder / 'labels.txt'
        label_file.write_bytes(payload)
        if variant == 'original':
            data = original
        else:
            output = io.BytesIO(original[:prefix_size])
            with zipfile.ZipFile(output, 'a', compression=zipfile.ZIP_STORED) as archive:
                for entry_name, content in entries.items():
                    archive.writestr(zipfile.ZipInfo(entry_name, (1980, 1, 1, 0, 0, 0)), payload if entry_name == name else content)
            data = output.getvalue()
        model = folder / 'model.tflite'
        model.write_bytes(data)
        command = [PYTHON, scripts / 'preflight.py', model, '--evidence-dir', folder / 'evidence', '--baseline', MODEL]
        static = run(command, variant + '-preflight')
        report = json.loads((folder / 'evidence/result.json').read_text())
        runtime = run([JDK / 'bin/java', '-cp', str(classes) + ':' + cp, 'DecoderProbe', '1,1000', scores, label_file], variant + '-java')
        if runtime.returncode:
            raise RuntimeError(runtime.stderr.decode())
        decoded = json.loads(runtime.stdout)
        additional = {}
        for mode in ('simple_baseline', 'task_init'):
            dest = folder / mode
            process = run([PYTHON, REPO / 'sources/metadata-contract-audit-20261004T062010Z/baseline/audit_one.py', mode, model, dest], variant + '-' + mode)
            additional[mode] = {'exit_code': process.returncode, 'report': json.loads((dest / 'result.json').read_text())}
        records.append({'variant': variant, 'artifact_sha256': digest(data), 'label_sha256': digest(payload),
                        'prefix_preserved': data[:prefix_size] == original[:prefix_size],
                        'preflight_exit': static.returncode, 'S': report['STRUCTURAL'],
                        'D': report['DECODER_COMPATIBILITY'], 'P': report['PRESERVATION'],
                        'generated_source_sha256': report.get('generated_source_sha256'),
                        'actual_java_FileUtil_TensorLabel': decoded, 'additional_checks': additional,
                        'python_splitlines_count': len([x for x in payload.decode().splitlines() if x.strip(''.join(chr(i) for i in range(33)))])})
    result = {'scope': __doc__, 'model_source': str(MODEL), 'model_sha256': digest(original),
              'java_probe_source': str(java), 'java_probe_sha256': digest(java.read_bytes()),
              'pinned_library_hashes': {p.name: digest(p.read_bytes()) for p in sorted((HAND / 'deps').glob('*.jar'))},
              'copied_historical_source_hashes': {str(p): digest(p.read_bytes()) for p in sorted(scripts.glob('*.py'))},
              'all_generated_source_hashes_identical': generated_sources_identical(records, variants),
              'records': records}
    (ROOT / 'results.json').write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
