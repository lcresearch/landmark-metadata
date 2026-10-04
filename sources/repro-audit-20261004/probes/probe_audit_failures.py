#!/usr/bin/env python3
"""Synthetic regression probes of preserved audit logic, without model execution.

Historical files remain unchanged. AST extraction/rebinding changes only external
paths or chooses a self-contained logic block; provenance is recorded in JSON.
Fixtures are explicitly synthetic and cannot support historical model claims.
"""
import argparse
import ast
import collections
import contextlib
import hashlib
import io
import json
import pathlib
import subprocess
import sys
import tempfile
import types
import zipfile

REPO = pathlib.Path(__file__).resolve().parents[3]
BASE = pathlib.Path('/workspace/repro-audit/independent-audit')
AUDIT = REPO / 'sources/metadata-contract-audit-20261004T062010Z'
E2E = REPO / 'sources/metadata-contract-e2e-20261004T030536Z'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2))


def run_ast(tree, path, namespace):
    stream = io.StringIO()
    exit_code = 0
    with contextlib.redirect_stdout(stream):
        try:
            exec(compile(ast.fix_missing_locations(tree), str(path), 'exec'), namespace)
        except SystemExit as exc:
            exit_code = exc.code
    return exit_code, stream.getvalue()


def probe_missing_raw(root):
    fresh, old = root / 'fresh', root / 'old'
    source_bytes = b'// synthetic generated source placeholder\n'
    class_bytes = b'synthetic class bytes (not executable)'
    dex_bytes = b'synthetic dex bytes (not executable)'
    variants = {
        'E1': ['original', 'description_control', 'label_deletion', 'label_restoration'],
        'E2': ['original', 'description_control', 'label_permutation', 'permutation_restoration'],
    }
    for phase, names in variants.items():
        rows = []
        for variant in names:
            model_bytes = b'synthetic model bytes (not executable) ' + variant.encode()
            folder = fresh / phase / 'variants' / variant
            for place in (folder, old / phase / 'variants' / variant):
                source = place / 'generated/src/main/java/org/example/contract/ContractModel.java'
                source.parent.mkdir(parents=True, exist_ok=True)
                source.write_bytes(source_bytes)
                classes = place / 'build/classes/org/example/contract/ContractModel.class'
                classes.parent.mkdir(parents=True, exist_ok=True)
                classes.write_bytes(class_bytes)
            (folder / 'model.tflite').write_bytes(model_bytes)
            dex = folder / 'build/dex/classes.dex'
            dex.parent.mkdir(parents=True)
            dex.write_bytes(dex_bytes)
            with zipfile.ZipFile(folder / 'build/consumer.apk', 'w') as archive:
                archive.writestr('assets/model.tflite', model_bytes)
            rows.append({
                'variant': variant,
                'artifact_paths': {'execution': f'{phase}/executions/primary/{variant}'},
                'observed': {'loaded_asset_sha256': sha(model_bytes), 'observations': [], 'platform': 'synthetic'},
                'build': {'generated_class_hashes': {'org/example/contract/ContractModel.class': sha(class_bytes)},
                          'dex_hashes': {'classes.dex': sha(dex_bytes)}, 'apk_sha256': 'synthetic'},
                'source_sha256': sha(source_bytes),
                'preservation_check': {k: True for k in ['canonical_equal', 'nonmetadata_buffers_equal', 'embedded_metadata_equal', 'flatbuffer_prefix_equal']},
                'component_name': 'synthetic', 'canonical_graph_sha256': 'synthetic',
                'metadata_sha256': 'synthetic', 'associated_file_sha256': {}, 'raw_output_hashes': {},
                **{k: 'PASS' for k in ['structural_status', 'generation_status', 'compile_status', 'package_status', 'load_status', 'inference_status', 'decoder_status']},
                **{k: 'synthetic' for k in ['consumer', 'runtime_version', 'generator_version', 'compiler_version']},
            })
        save(fresh / phase / 'executions/primary/results.json', rows)
        save(old / phase / 'executions/primary/results.json', rows)
    path = AUDIT / 'rebuild/scripts/audit_results.py'
    tree = ast.parse(path.read_text())
    tree.body = [node for node in tree.body if not (isinstance(node, ast.ImportFrom) and node.module == 'common')
                 and not (isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'OLD' for t in node.targets))]
    ns = {'__file__': str(path), 'ROOT': fresh, 'OLD': old, 'save': save, 'sha': sha}
    code, stdout = run_ast(tree, path, ns)
    report = json.loads((fresh / 'results.json').read_text())
    return {'script': str(path), 'script_sha256': sha(path.read_bytes()), 'method': 'Full script AST; only common import and OLD path rebound to synthetic fixture roots.',
            'exit_code': code, 'summary': report['summary'], 'denominators': report['denominators'],
            'narrative_claims_reproduced': 'The fresh E1 deletion reproduces' in (fresh / 'AUDIT_REPORT.md').read_text(),
            'stdout': stdout}


def probe_companion_fail(root):
    path = AUDIT / 'preservation/audit_preservation.py'
    tree = ast.parse(path.read_text())
    tree.body = [node for node in tree.body if node.lineno >= 335]
    out = root / 'companion'
    save(out / 'bytecode/results.json', {'status': 'FAIL', 'review_findings': {'synthetic_failure': True}})
    ns = {'OUT': out, 'digest': sha, 'json': json, 'sys': sys,
          'result': {'status': 'PASS'}, 'status_counts': collections.Counter({'PASS': 1}),
          'model_rows': [], 'execution_rows': [], 'observations': [], 'incomplete': [], 'checks': []}
    code, stdout = run_ast(tree, path, ns)
    return {'script': str(path), 'script_sha256': sha(path.read_bytes()), 'method': 'Execute unchanged lines 335-354 with prior local checks PASS and companion bytecode FAIL.',
            'exit_code': code, 'result': json.loads((out / 'results.json').read_text()), 'stdout': stdout}


def probe_empty_e5(root):
    path = E2E / 'scripts/summarize_e5.py'
    tree = ast.parse(path.read_text())
    tree.body = [node for node in tree.body if not (isinstance(node, ast.ImportFrom) and node.module == 'common')]
    out = root / 'empty-e5'
    save(out / 'E5/results.json', {'fixtures': []})
    code, stdout = run_ast(tree, path, {'ROOT': out, 'save': save})
    summary = json.loads((out / 'E5/summary.json').read_text())
    prose = (out / 'EXPERIMENT_E5_RESULTS.md').read_text()
    return {'script': str(path), 'script_sha256': sha(path.read_bytes()), 'method': 'Full script with empty input fixture list and common path rebound.',
            'exit_code': code, 'summary': summary,
            'prose_says_65_semantic_abstentions': 'All 65 semantic judgments abstain' in prose,
            'prose_says_27_paths_flagged': 'D flags 27 selected category paths' in prose}


def probe_optimized_claim_assertions():
    path = AUDIT / 'claims/recompute.py'
    tree = ast.parse(path.read_text())
    count = sum(isinstance(n, ast.Assert) for n in ast.walk(tree))
    node = next(n for n in ast.walk(tree) if isinstance(n, ast.Assert) and n.lineno == 76)
    selected = ast.Module(body=[node], type_ignores=[])
    ns = {'s': collections.Counter()}
    observations = {}
    for level in (0, 1):
        try:
            exec(compile(selected, str(path), 'exec', optimize=level), dict(ns))
            observations[str(level)] = 'accepted empty structural counts'
        except AssertionError:
            observations[str(level)] = 'AssertionError'
    return {'script': str(path), 'script_sha256': sha(path.read_bytes()), 'assert_nodes': count,
            'method': 'Execute unchanged line 76 assertion with empty observed counts, compile optimize=0 and 1.',
            'optimization_results': observations}


def probe_line_reader(root):
    java = root / 'ReadLines.java'
    java.write_text('''import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
public class ReadLines {
  public static void main(String[] args) throws Exception {
    try (BufferedReader r = Files.newBufferedReader(Path.of(args[0]), StandardCharsets.UTF_8)) {
      int count = 0; String line;
      while ((line = r.readLine()) != null) if (line.trim().length() > 0) count++;
      System.out.println(count);
    }
  }
}
''')
    path = E2E / 'scripts/preflight.py'
    tree = ast.parse(path.read_text())
    assignment = next(n for n in ast.walk(tree) if isinstance(n, ast.Assign) and n.lineno == 93)
    report = []
    for name, payload in [('lf', b'cat\ndog\n'), ('vertical_tab', b'cat\vdog\n'), ('unicode_line_separator', 'cat\u2028dog\n'.encode())]:
        sample = root / (name + '.txt')
        sample.write_bytes(payload)
        ns = {'files': {'labels': payload}, 'filename': 'labels'}
        exec(compile(ast.Module(body=[assignment], type_ignores=[]), str(path), 'exec'), ns)
        process = subprocess.run(['java', '-XX:-UsePerfData', str(java), str(sample)], text=True, capture_output=True)
        if process.returncode:
            raise RuntimeError(process.stderr)
        report.append({'fixture': name, 'hex': payload.hex(), 'python_preflight_labels': ns['labels'],
                       'python_count': len(ns['labels']), 'java_buffered_reader_count': int(process.stdout)})
    return {'script': str(path), 'script_sha256': sha(path.read_bytes()),
            'method': 'Unchanged line 93 labels expression vs actual Java BufferedReader.readLine + trim. Not yet an actual Support jar call.', 'fixtures': report}


def main():
    global BASE
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', required=True, type=pathlib.Path)
    BASE = parser.parse_args().output_dir.resolve()
    if BASE.is_relative_to(REPO):
        raise ValueError('Synthetic evidence must stay outside the source repository')
    BASE.mkdir(parents=True, exist_ok=False)
    root = pathlib.Path(tempfile.mkdtemp(prefix='audit-probes-', dir=BASE))
    result = {'scope': 'Synthetic auditor regressions; no model experiment or historical evidence re-executed.',
              'fixture_root': str(root),
              'rebuild_missing_raw': probe_missing_raw(root),
              'preservation_companion_failure': probe_companion_fail(root),
              'empty_e5_summary': probe_empty_e5(root),
              'optimized_claims': probe_optimized_claim_assertions(),
              'label_line_reader': probe_line_reader(root)}
    save(BASE / 'probe-results.json', result)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
