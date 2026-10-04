"""Summarize retained observations without rewriting any per-check raw record."""
import datetime
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OLD = Path('/workspace/metadata-contract-e2e-20261004T030536Z')
def sha(data): return hashlib.sha256(data).hexdigest()
def save(path, obj): path.write_text(json.dumps(obj, indent=2) + '\n')

anchors = [
    ('metadata_population_entry_count', 'sources/installed-metadata.py', 610, 644,
     'Output/input tensor metadata entry count, independent of associated label-string count.'),
    ('metadata_load_validation', 'sources/installed-metadata.py', 292, 306,
     'load_metadata_buffer invokes _validate_metadata before population.'),
    ('metadata_display', 'sources/installed-metadata.py', 749, 776,
     'Associated payload retrieval and JSON display are not the population check.'),
    ('e5_source_extraction', 'sources/preflight.py', 65, 83,
     'Generator invocation and regular-expression extraction/joins.'),
    ('e5_processor_and_dynamic_scope', 'sources/preflight.py', 84, 90,
     'Modeled processor regex and dynamic/nonpositive abstention.'),
    ('e5_axis_rule_and_status', 'sources/preflight.py', 91, 104,
     'Selected payload, first nonunit axis, cardinality, exact final axis and unmatched-getter outcome.'),
    ('tensorlabel_constructor', 'sources/TensorLabel.java', 74, 105,
     'List overload selects first nonunit axis; constructor enforces label cardinality.'),
    ('tensorlabel_category', 'sources/TensorLabel.java', 175, 214,
     'Exact final-axis and flattened-cardinality checks; first-nonunit selector.'),
    ('tensorlabel_actual_binary', 'logs/source_audit--tensorlabel_javap.stdout', 297, 391,
     'Fresh disassembly of actual Android-build Support API jar confirms category guards and axis selector.'),
    ('python_task_factory', 'sources/installed-image_classifier.py', 77, 95,
     'Installed Python wrapper invokes native create_from_options.'),
    ('task_pybind_factory', 'sources/_pywrap_image_classifier.cc', 39, 68,
     'Pybind routes to ImageClassifier::CreateFromOptions.'),
    ('task_factory_init', 'sources/image_classifier.cc', 52, 81,
     'Factory calls Init.'),
    ('task_initialization_outputs', 'sources/image_classifier.cc', 121, 139,
     'Init calls CheckAndSetOutputs.'),
    ('task_output_cardinality', 'sources/image_classifier.cc', 242, 260,
     'Class count versus label-map item count check in selected ImageClassifier implementation.'),
]
records = []
for identifier, relative, start, end, qualification in anchors:
    path = ROOT / relative
    lines = path.read_text().splitlines()
    records.append({'id': identifier, 'path': relative, 'sha256': sha(path.read_bytes()),
                    'start_line': start, 'end_line': end, 'qualification': qualification,
                    'excerpt': '\n'.join('%d: %s' % (i + 1, lines[i]) for i in range(start - 1, min(end, len(lines))))})
save(ROOT / 'source-anchors.json', records)

results = json.loads((ROOT / 'results.json').read_text())
comparisons = []
for model in results['models']:
    c = model['checks']; b = c['simple_baseline']; e = c['e5']
    findings = e['DECODER_COMPATIBILITY']['findings']
    baseline_binding = b['selected_binding']; actual = findings[0]
    binding_equal = len(findings) == 1 and all([
        baseline_binding['output_position'] == actual['output_position'],
        baseline_binding['metadata_position'] == actual['metadata_position_for_labels'],
        baseline_binding['associated_file_position'] == actual['associated_file_position'],
        baseline_binding['label_file'] == actual['label_file'],
        baseline_binding['label_payload_sha256'] == actual['label_sha256'],
        baseline_binding['label_count'] == actual['label_count'],
    ])
    comparisons.append({'condition': model['condition'], 'sha256': model['sha256'],
        'displayer_readable': c['displayer']['status'] == 'READABLE',
        'population_accepted': c['populator']['status'] == 'ACCEPTED',
        'baseline_rejected': b['status'] == 'INCOMPATIBLE',
        'e5_rejected': e['DECODER_COMPATIBILITY']['status'] == 'INCOMPATIBLE',
        'task_initialization_rejected': c['task_init']['status'] == 'FAIL',
        'selected_binding_agrees_baseline_e5': binding_equal,
        'metadata_entry_count': c['displayer']['facts']['output_metadata_entry_count'],
        'graph_output_count': c['displayer']['facts']['graph_output_count'],
        'label_count': baseline_binding['label_count']})
summary = {'conditions': comparisons,
           'all_baseline_and_e5_bindings_agree': all(x['selected_binding_agrees_baseline_e5'] for x in comparisons),
           'baseline_e5_rejection_vector_equal': all(x['baseline_rejected'] == x['e5_rejected'] for x in comparisons),
           'task_init_e5_rejection_vector_equal': all(x['task_initialization_rejected'] == x['e5_rejected'] for x in comparisons),
           'e5_additional_rejections_over_baseline': sum(x['e5_rejected'] and not x['baseline_rejected'] for x in comparisons),
           'e5_additional_rejections_over_task_init': sum(x['e5_rejected'] and not x['task_initialization_rejected'] for x in comparisons),
           'e5_rejections_population_accepts': sum(x['e5_rejected'] and x['population_accepted'] for x in comparisons)}
results['comparison'] = summary
results['separate_structural_negative_control']['precise_population_substage'] = {
    'failed': 'MetadataPopulator.load_metadata_buffer -> _validate_metadata',
    'populate_reached': False, 'basis': 'Preserved exception stack in raw result',
    'graph_output_count': 1, 'output_metadata_entry_count': 0,
    'retained_label_payload_count': 1000,
    'not_pooled_with_label_resource_conditions': True}
results['task_execution_scope'] = 'Only create_from_options requested; no classify call, emulator, or independently instrumented initialization internals.'
results['versions_path'] = 'versions.json'
results['source_anchors_path'] = 'source-anchors.json'
results['binary_audit_path'] = 'tensorlabel-binary-audit.json'
results['source_review_limits'] = {
    'analysis_kind': 'Fixed-template regex extraction, not general Java dataflow analysis',
    'unmatched_getter_risk': 'May be reported INAPPLICABLE_NO_SELECTED_GETTER rather than unknown syntax',
    'processor_pattern_risk': 'Only .add(new Word( operation forms are enumerated; cannot guarantee abstention for arbitrary syntax',
    'full_buffer_and_processor_binding_verified': False,
    'dynamic_policy': 'ABSTAIN on any shape/signature dimension <= 0',
    'defer_runtime_obligations_implemented': False,
    'semantic_reference_supplied': False,
    'independent_human_audit': False}
before = json.loads((ROOT / 'protected-before.json').read_text())
final = {name: {'sha256': sha(Path(name).read_bytes()), 'bytes': Path(name).stat().st_size} for name in before}
seal = {'checked_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'all_protected_files_unchanged': final == before,
        'old_commands_log': str(OLD / 'commands-executed.sh'),
        'old_commands_log_before': before[str(OLD / 'commands-executed.sh')],
        'old_commands_log_after': final[str(OLD / 'commands-executed.sh')],
        'files': final}
save(ROOT / 'protected-final.json', seal)
results['final_preservation_check'] = 'protected-final.json'
results['final_protected_files_unchanged'] = final == before
prior_task = json.loads((OLD / 'E3/implementation.json').read_text())
versions = json.loads((ROOT / 'versions.json').read_text())
installed = {p['path']: p for p in versions['files']}
results['task_implementation_identity'] = {
    'python_matches_preserved_E3': installed[prior_task['python_source']]['sha256'] == prior_task['python_source_sha256'],
    'native_matches_preserved_E3': installed[prior_task['native_library']]['sha256'] == prior_task['native_library_sha256'],
    'source_build_equivalence': 'NOT_ESTABLISHED'}
all_commands = []
for path in sorted(ROOT.rglob('*.command.json')):
    all_commands.append({'record_path': str(path.relative_to(ROOT)), **json.loads(path.read_text())})
save(ROOT / 'all-command-records.json', all_commands)
results['all_command_records_path'] = 'all-command-records.json'
save(ROOT / 'results.json', results)
manifest = []
for path in sorted(ROOT.rglob('*')):
    if path.is_file() and path.name != 'SHA256SUMS':
        manifest.append(sha(path.read_bytes()) + '  ' + str(path.relative_to(ROOT)))
(ROOT / 'SHA256SUMS').write_text('\n'.join(manifest) + '\n')
print(json.dumps({'summary': summary, 'protected_unchanged': final == before, 'manifest_files': len(manifest)}, indent=2))
