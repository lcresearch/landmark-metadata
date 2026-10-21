#!/usr/bin/env python3
"""Check the fixed parser probe's saved records; never run Java or a model.

Original labels require either the independently pinned historical manifest or
the fixed-SHA model supplied with --model. Recorded dependency identities and
commands are checked, but this does not authenticate that a process executed.
"""
import argparse
import ast
import base64
import hashlib
import importlib.util
import json
from pathlib import Path, PurePosixPath
import struct
import sys
import zipfile

sys.dont_write_bytecode = True
REPO = Path(__file__).resolve().parents[2]
PRIOR = REPO / 'work/preaudit-followup-20261008/parser'
MODEL_SHA256 = '6c7ab0a6e5dcbf38a8c33b960996a55a3b4300b36a018c4545801de3a3c8bde0'
EXPECTED = {'original': (1000, 1000, 'PASS'),
            'lf_replaced_by_vertical_tab': (1000, 999, 'FAIL'),
            'unicode_separator_inside_first_label': (1001, 1000, 'PASS')}
SOURCE_PATHS = [
    'work/preaudit-followup-20261008/parser/PROTOCOL.md',
    'work/preaudit-followup-20261008/parser/run_probe.py',
    'sources/metadata-contract-paper/scripts/DecoderProbe.java',
    'sources/repro-audit-20261004/maintained/LabelOracle.java',
    'sources/repro-audit-20261004/maintained/java_labels.py',
    'sources/repro-audit-20261004/maintained/test_java_labels.py',
    'sources/repro-audit-20261004/maintained/runtime.py',
    'sources/repro-audit-20261004/probes/probe_label_parser.py',
    'docs/reproduction/toolchain.json',
]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load_contract():
    """Read trusted repository pins, not expected values from candidate records."""
    index = json.loads((PRIOR / 'evidence-index.json').read_text())
    sources = {Path(row['path']).name: row for row in index['executed_source_inputs']}
    if set(sources) != {Path(path).name for path in SOURCE_PATHS}:
        raise ValueError('Trusted source inventory differs from the fixed protocol')
    for relative in SOURCE_PATHS:
        data = (REPO / relative).read_bytes()
        row = sources[Path(relative).name]
        if sha(data) != row['sha256'] or len(data) != row['bytes']:
            raise ValueError('Trusted source changed: ' + relative)
    tree = ast.parse((REPO / SOURCE_PATHS[5]).read_text())
    cases = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            target = node.targets[0]
            if isinstance(target, ast.Name) and target.id in ('CASES', 'MALFORMED'):
                cases[target.id] = eval(compile(ast.Expression(node.value), '<trusted-cases>', 'eval'),
                                        {'__builtins__': {}})
    if (len(cases['CASES']), len(cases['MALFORMED'])) != (22, 3):
        raise ValueError('Trusted parser case inventory changed')
    toolchain = json.loads((REPO / 'docs/reproduction/toolchain.json').read_text())
    pins = {row['jar_filename']: row['jar_sha256']
            for row in toolchain['acquisition_lock']['java_dependencies']
            if row['destination'] == 'hand-deps'}
    dependencies = {Path(row['path']).name: row for row in index['dependency_identities']}
    if len(pins) != 8 or pins != {name: row['sha256'] for name, row in dependencies.items()}:
        raise ValueError('Trusted dependency inventories disagree')
    module_spec = importlib.util.spec_from_file_location('_parser_readback_helper', REPO / SOURCE_PATHS[4])
    helper = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(helper)
    manifest = next(row for row in index['key_raw_identities']
                    if Path(row['path']).name == 'evidence-files.json')
    return {'sources': sources, 'dependencies': dependencies, 'cases': cases['CASES'],
            'malformed': cases['MALFORMED'], 'helper': helper,
            'manifest_sha256': manifest['sha256'], 'model_sha256': MODEL_SHA256}


def verify(evidence, model=None):
    root = Path(evidence).resolve()
    checks = []
    anchor = None

    def check(name, passed):
        checks.append({'check': name, 'passed': bool(passed)})

    def data(relative):
        path = root / relative
        if not path.resolve().is_relative_to(root) or path.is_symlink():
            raise ValueError('Evidence path escapes root or is a symlink: ' + str(relative))
        return path.read_bytes()

    def read(relative):
        return json.loads(data(relative))

    def exact(rows, field, names, label, transform=lambda value: value):
        keys = [transform(row[field]) for row in rows]
        check(label, len(keys) == len(set(keys)) and set(keys) == set(names))
        if len(keys) != len(set(keys)) or set(keys) != set(names):
            raise ValueError('Incorrect identity set: ' + label)
        return dict(zip(keys, rows))

    try:
        contract = load_contract()
        result = read('results.json')
        environment = read('environment.json')
        recorded_root = PurePosixPath(result['scores']['path']).parent
        if not recorded_root.is_absolute() or '..' in recorded_root.parts:
            raise ValueError('Invalid recorded evidence root')

        def relative_record(path):
            path = PurePosixPath(path)
            if '..' in path.parts or not path.is_absolute():
                raise ValueError('Invalid recorded path')
            return path.relative_to(recorded_root).as_posix()

        def identity(row, relative):
            payload = data(relative)
            check('recorded identity: ' + relative,
                  relative_record(row['path']) == relative and row['sha256'] == sha(payload)
                  and row['bytes'] == len(payload))
            return payload

        entries = read('evidence-files.json')
        actual = set()
        for path in root.rglob('*'):
            if path.is_symlink():
                raise ValueError('Symlink in evidence tree')
            if path.is_file() and path != root / 'evidence-files.json':
                actual.add(path.relative_to(root).as_posix())
        manifest = exact(entries, 'path', actual, 'exact nonempty manifest inventory', relative_record)
        check('nonempty manifest', bool(manifest))
        for relative, row in manifest.items():
            identity(row, relative)

        original = data('decoder/original/labels.txt')
        if model is None:
            anchored = sha(data('evidence-files.json')) == contract['manifest_sha256']
            check('independent historical manifest pin', anchored)
            if anchored:
                anchor = 'preserved historical evidence-files.json SHA-256'
        else:
            model_bytes = Path(model).read_bytes()
            model_matches = sha(model_bytes) == contract['model_sha256']
            check('independent source model pin', model_matches)
            with zipfile.ZipFile(model) as archive:
                labels_match = original == archive.read('labels_without_background.txt')
                check('original labels extracted from supplied model', labels_match)
            if model_matches and labels_match:
                anchor = 'fixed-SHA model and exact associated label bytes'
        check('recorded fixed model identity', environment['model']['sha256'] == contract['model_sha256'])

        sources = exact(environment['sources'], 'path', contract['sources'],
                        'exact source identities', lambda path: Path(path).name)
        for name, expected in contract['sources'].items():
            payload = data('sources/' + name)
            row = sources[name]
            check('trusted source pin: ' + name,
                  sha(payload) == row['sha256'] == expected['sha256']
                  and len(payload) == row['bytes'] == expected['bytes'])
        dependencies = exact(environment['dependencies'], 'path', contract['dependencies'],
                             'exact dependency identities', lambda path: Path(path).name)
        for name, expected in contract['dependencies'].items():
            row = dependencies[name]
            check('trusted dependency pin: ' + name,
                  row['sha256'] == row['expected_sha256'] == expected['sha256']
                  and row['bytes'] == expected['bytes'] and row['matches_pin'] is True)

        decoder = exact(result['decoder_conditions'], 'condition', EXPECTED, 'exact decoder conditions')
        valid = exact(result['valid_utf8_cases'], 'case', contract['cases'], 'exact 22 valid cases')
        malformed = exact(result['malformed_cases'], 'case', contract['malformed'], 'exact 3 malformed cases')
        commands = {'java-version', 'javac-version', 'python-version', 'javac'}
        commands |= {name + suffix for name in EXPECTED for suffix in ('-decoder', '-oracle')}
        commands |= {'valid-' + name for name in valid}
        commands |= {'malformed-' + name for name in malformed}
        actual_commands = {path.name.removesuffix('.command.json')
                           for path in (root / 'commands').glob('*.command.json')}
        check('exact 35 command identities', len(commands) == 35 and actual_commands == commands)
        command_records = {}
        for name in sorted(commands):
            row = read('commands/' + name + '.command.json')
            command_records[name] = row
            check('successful recorded command: ' + name,
                  row['exit_code'] == 0 and PurePosixPath(row['cwd']) == recorded_root)
            data('commands/' + name + '.stdout')
            data('commands/' + name + '.stderr')

        java_path = environment['java_executable']['path']
        javac_path = environment['javac_executable']['path']
        classpath = ':'.join([str(recorded_root / 'classes'),
                              *sorted(row['path'] for row in dependencies.values())])
        java_command = [java_path, '-cp', classpath]
        version_commands = {'java-version': [java_path, '-version'],
                            'javac-version': [javac_path, '-version'],
                            'python-version': [read('invocation.json')['command'][0], '--version']}
        for name, expected_command in version_commands.items():
            check('version command identity: ' + name, command_records[name]['command'] == expected_command)
            check('version stdout/stderr record: ' + name,
                  environment['versions'][name] == {
                      stream: data('commands/' + name + '.' + stream).decode()
                      for stream in ('stdout', 'stderr')})
        check('fixed JDK version', '17.0.12' in environment['versions']['java-version']['stderr'])
        check('compiler command identity', command_records['javac']['command'] == [
            javac_path, '--release', '8', '-cp',
            ':'.join(sorted(row['path'] for row in dependencies.values())),
            '-d', str(recorded_root / 'classes'),
            str(recorded_root / 'sources/DecoderProbe.java'),
            str(recorded_root / 'sources/LabelOracle.java')])

        def oracle(name, payload):
            lines = data('commands/' + name + '.stdout').decode('ascii').splitlines()
            labels = [base64.b64decode(line, validate=True).decode('utf8') for line in lines[1:]]
            check('oracle transport: ' + name, int(lines[0]) == len(labels))
            command = command_records[name]['command']
            check('oracle command payload: ' + name,
                  command == java_command + ['LabelOracle', base64.b64encode(payload).decode('ascii')])
            return labels

        scores = identity(result['scores'], 'scores.f32')
        check('fixed synthetic scores', scores == struct.pack('<1000f', *[i / 1000 for i in range(1000)]))
        variants = {'original': original,
                    'lf_replaced_by_vertical_tab': original.replace(b'\n', b'\v', 1),
                    'unicode_separator_inside_first_label': original.replace(b'\n', '\u2028suffix\n'.encode(), 1)}
        helper = contract['helper']
        for name, expected_payload in variants.items():
            row = decoder[name]
            relative = 'decoder/' + name + '/labels.txt'
            payload = identity(row['label_input'], relative)
            check('exact decoder transformation: ' + name, payload == expected_payload)
            labels = oracle(name + '-oracle', payload)
            check('actual/helper decoder labels: ' + name, helper.load_java_utf8_labels(payload) == labels
                  and row['maintained_equals_actual_labels'] is True)
            actual = read('commands/' + name + '-decoder.stdout')
            check('decoder stdout record: ' + name, actual == row['actual_library'])
            command = command_records[name + '-decoder']['command']
            check('decoder command inputs: ' + name,
                  command == java_command + ['DecoderProbe', '1,1000', str(recorded_root / 'scores.f32'),
                                              str(recorded_root / relative)])
            python_count = len([line for line in payload.decode().splitlines()
                                if line.strip(''.join(chr(i) for i in range(33)))])
            check('declared decoder comparison: ' + name,
                  (python_count, len(labels), actual['status']) == EXPECTED[name]
                  and row['python_splitlines_count'] == python_count and actual['labels'] == len(labels)
                  and row['passed_declared_comparison'] is True)
            if name == 'lf_replaced_by_vertical_tab':
                check('exact VT exception', actual.get('exception') == 'java.lang.IllegalArgumentException'
                      and actual.get('message') == 'Label number 999 mismatch the shape on axis 1')
            else:
                check('1000 returned categories: ' + name, actual.get('categories') == 1000)
        for name, expected_payload in contract['cases'].items():
            row = valid[name]
            payload = identity(row['input'], 'differential/' + name + '.bin')
            check('fixed valid payload: ' + name, payload == expected_payload)
            labels = oracle('valid-' + name, payload)
            check('valid exact strings: ' + name, labels == row['oracle_labels'] == row['helper_labels']
                  == helper.load_java_utf8_labels(payload) and row['equal_strings'] is True)
        for name, expected_payload in contract['malformed'].items():
            row = malformed[name]
            payload = identity(row['input'], 'malformed/' + name + '.bin')
            check('fixed malformed payload: ' + name, payload == expected_payload)
            labels = oracle('malformed-' + name, payload)
            try:
                helper.load_java_utf8_labels(payload)
            except helper.LabelEncodingUnsupported:
                abstained = True
            else:
                abstained = False
            check('malformed abstention: ' + name, labels == row['oracle_labels'] and abstained
                  and row['helper_abstained'] is True
                  and row['python_replace_text'] == payload.decode('utf8', errors='replace'))
        check('aggregate completion', result['status'] == 'PASS' and result['passed_comparisons'] == 28
              and result['failed_comparisons'] == 0 and read('completion.json')['exit_code'] == 0)
    except (OSError, ValueError, KeyError, TypeError, IndexError, AttributeError,
            zipfile.BadZipFile) as error:
        checks.append({'check': 'required evidence and schema', 'passed': False,
                       'detail': type(error).__name__ + ': ' + str(error)})
    failed = sum(not row['passed'] for row in checks)
    return {'status': 'FAIL' if failed else 'PASS', 'evidence': str(root),
            'original_label_anchor': anchor, 'passed': len(checks) - failed, 'failed': failed,
            'checks': checks, 'scope': 'Fixed saved-record consistency and independent identity checks only',
            'limits': ['No Java/model execution or human verification',
                       'Recorded dependency hashes are compared with trusted pins; JAR bytes are not read',
                       'Command records and stdout do not authenticate historical process execution'],
            'new_library_execution': False, 'human_verification': False}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--evidence', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--model', type=Path, help='Fixed-SHA model required for a new capture without the historical manifest pin')
    args = parser.parse_args(argv)
    if args.report.is_symlink():
        parser.error('Report must not be a symlink')
    output = args.report.resolve()
    if output.is_relative_to(REPO) or output.is_relative_to(args.evidence.resolve()):
        parser.error('Report must stay outside the source checkout and evidence directory')
    if output.exists():
        parser.error('Report already exists; choose a new path')
    result = verify(args.evidence, args.model)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('x') as stream:
        stream.write(json.dumps(result, indent=2) + '\n')
    print(json.dumps({key: result[key] for key in ('status', 'passed', 'failed', 'original_label_anchor')}))
    return int(result['failed'] != 0)


if __name__ == '__main__':
    raise SystemExit(main())
