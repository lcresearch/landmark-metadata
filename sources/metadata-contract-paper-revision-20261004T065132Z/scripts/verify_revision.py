"""Check manuscript evidence mappings without running model experiments."""
import argparse
import datetime
import hashlib
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
EVIDENCE = pathlib.Path('/workspace/metadata-contract-e2e-20261004T030536Z')
ap = argparse.ArgumentParser()
ap.add_argument('--write-map', action='store_true')
ap.add_argument('--record')
args = ap.parse_args()

def load(path):
    return json.loads(pathlib.Path(path).read_text())

def sha(path):
    with pathlib.Path(path).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()

def evidence(path, pointer=None):
    p = EVIDENCE / path
    assert p.is_file(), p
    return {'path': str(p), 'sha256': sha(p), 'json_pointer_or_selector': pointer}

provenance = load(ROOT / 'SOURCE_PROVENANCE.json')
for row in provenance['sources']:
    assert sha(row['path']) == row['sha256'], row['path']

paper = (ROOT / 'manuscript/paper.tex').read_text()
sections = re.findall(r'\\section\{([^}]+)\}', paper)
expected_sections = ['Introduction','Contracts and Preservation','E1: Executed Getter Failure',
 'E2: Successful Decoding With Changed Association','E3: Different Stages of Contract Enforcement',
 'Hand: Reference Agreement and Consumer Reach','Supporting Scope Checks and Pre-flight Limits',
 'Relationship to Existing Work','Validity, Reproduction, and Remaining Work','Conclusion']
assert sections == expected_sections, sections

e1, e2, e3, hand = [load(EVIDENCE / ex / 'results.json') for ex in ['E1','E2','E3','E7']]
for ex, data in [('E1',e1),('E2',e2)]:
    assert data['unit_count'] == 4 and data['primary_inputs_per_unit'] == 2
    for u in data['units']:
        for stage in ['structural_status','generation_status','compile_status','package_status','load_status','input_preparation_status','inference_status']:
            assert u[stage] == 'PASS', (ex,u['variant'],stage)
        p = u['preservation_check']
        assert p['canonical_equal'] and p['nonmetadata_buffers_equal'] and p['generated_source_equal']
        assert p['embedded_metadata_equal'] == (u['variant'] != 'description_control')
        assert u['build']['generated_classes_equal_original'] and u['build']['dex_equal_original']
        c = u['comparisons']
        assert c['replay_same_stage_outcomes'] and c['replay_raw_outputs_equal']
        for inp in c['inputs']:
            assert inp['raw_output_equal_original'] and inp['input_equal_original']
            if u['variant']=='label_deletion':
                assert 'score_bits_equal_original' not in inp
            else:
                assert inp['score_bits_equal_original'] and inp['returned_scores_match_raw_position']
                assert len(inp['changed_label_positions']) == (999 if u['variant']=='label_permutation' else 0)
        expected = 'FAIL' if u['variant']=='label_deletion' else 'PASS'
        assert u['decoder_status']==expected
        if expected=='FAIL':
            assert u['earliest_failing_stage']=='generated_getter'
            assert u['exception_message']=='Label number 999 mismatch the shape on axis 1'

task_delete = next(u for u in e3['units'] if u['variant']=='label_deletion')
assert task_delete['variant_sha256'] == next(u for u in e1['units'] if u['variant']=='label_deletion')['variant_sha256']
o = task_delete['observed']
assert o['initialization_status']=='FAIL' and o['earliest_failing_stage']=='task_initialization'
assert o['inference_status']==o['decoder_status']=='NOT_REACHED'
assert o['exception_message']=='Got 1000 class(es) for output index 0, expected 999 according to the label map.'

bridge = load(EVIDENCE/'E7/source-component-equivalence.json')
assert not bridge['exact_component_equal'] and bridge['canonical_equal']
assert bridge['changed_buffers']==[172] and bridge['source_buffers']==bridge['focal_buffers']==173
for u in hand['units']:
    assert u['decoded_equal_original'] and u['decoded_float_bits_equal_original'] and u['replay_observation_equal']
    assert u['observed']['detected_hands']==1
    assert u['observed']['landmarks_per_hand']==u['observed']['world_landmarks_per_hand']==[21]

external = load(EVIDENCE/'E4/summary.json')
assert (external['candidate_urls'],external['downloaded'],len(external['unavailable']),external['new_canonical_graphs'])==(20,16,4,15)
assert external['structural_counts']=={'PASS':15} and external['compile_counts']=={'PASS':8,'FAIL':7}
assert external['fresh_runtime_invocations']==0
assert (external['decoder_category_pass_components'],external['decoder_category_incompatible_components'],external['decoder_inapplicable_components'])==(4,9,2)
pre = load(EVIDENCE/'E5/summary.json')
assert pre['distinct_artifact_fixtures']==65 and pre['semantic_counts']=={'ABSTAIN':65}
assert pre['known_successfully_executed_Android_artifact_conditions']==4 and pre['incorrect_rejections_of_those_conditions']==0
assert pre['known_getter_failure_flagged']

claims = [
 {'id':'C1','section':'3 / E1','claim':'Associated-label deletion preserves computation, embedded metadata and generated code but fails at the actual generated Android getter; description and restoration succeed.',
  'artifacts':[evidence('E1/results.json','units; comparison_checks'),evidence('E1/static-results.json'),evidence('E1/build-results.json'),evidence('scripts/ContractInstrumentation.java'),evidence('E1/executions/primary/label_deletion/device/result.json'),evidence('E1/executions/replay/label_deletion/device/result.json')],
  'boundary':'Caught injected error in a pinned minimal Android consumer, not a natural EfficientNet defect or uncaught production crash; description control changes embedded metadata.'},
 {'id':'C2','section':'4 / E2','claim':'Predeclared cyclic label permutation preserves scores and raw positions but changes 999 label strings; inverse restores the baseline.',
  'artifacts':[evidence('phase0/pre-E2-freeze.json'),evidence('EXPERIMENT_E2_PLAN.md'),evidence('E2/results.json','units; comparison_checks'),evidence('E2/deviations.json'),evidence('E2/executions/primary/label_permutation/device/rgb_pattern-decoded.json')],
  'boundary':'No independently established class order; returned-list position is used because Category.getIndex() is unset. Interrupted replay recovery is disclosed.'},
 {'id':'C3','section':'5 / E3','claim':'The identical deletion artifact fails at Task initialization rather than the Android getter; Task permutation also succeeds with changed labels.',
  'artifacts':[evidence('E3/results.json','stage_matrix; comparisons'),evidence('E3/compatibility.json'),evidence('E3/implementation.json'),evidence('E3/executions/primary/label_deletion/outputs/result.json'),evidence('E3/sources/image_classifier.cc'),evidence('E3/sources/_pywrap_image_classifier.cc')],
  'boundary':'Consumer and platform/toolchain both differ. Task returned categories are not raw interpreter tensors; no cross-platform raw equality.'},
 {'id':'C4','section':'6 / Hand reference','claim':'Source-backed roles disagree with focal metadata; a source-pinned different component is linked by graph/weight equivalence.',
  'artifacts':[evidence('E7/REFERENCE_CHAIN.md'),evidence('E7/source-component-equivalence.json'),evidence('E7/source-pinned-assets.json'),evidence('E7/sources/immutable-commit-source-verification.json'),evidence('E7/original-role-reference.json'),evidence('E7/metadata_exchange-role-reference.json')],
  'boundary':'Source does not directly pin focal 6acda7... bytes. Assistant-extracted reference remains subject to human audit.'},
 {'id':'C5','section':'6 / Hand consumers','claim':'Preserved repaired generic bindings reverse after metadata exchange, but official Hand Task decoded values are unchanged on the fixed image.',
  'artifacts':[evidence('E7/binding-audit.json'),evidence('E7/results.json'),evidence('E7/executions/primary/original/outputs/result.json'),evidence('E7/executions/primary/metadata_exchange/outputs/result.json')],
  'boundary':'Generic javac results are recovered; fresh disassembly and Task execution are distinct. No complete repair, raw Task tensors, all-metadata-insensitivity or task-accuracy claim.'},
 {'id':'C6','section':'7.1 / external scope','claim':'Fixed candidate set yields 15 new graph groups with full semantic abstention and no external runtime execution; static incompatibilities retain official failure/warning context.',
  'artifacts':[evidence('E4/prevalidation-freeze.json'),evidence('PREVALIDATION_PROTOCOL.md'),evidence('E4/results.json'),evidence('E4/summary.json')],
  'boundary':'Purposive local freeze, not independent preregistration, prevalence or an established new supported natural end-to-end failure.'},
 {'id':'C7','section':'7.2–7.3 / pre-flight','claim':'Scoped pre-flight flags the actual EfficientNet failure, preserves tested good conditions, and explicitly abstains on dynamic Gesture and unsupported semantic inference.',
  'artifacts':[evidence('E5/results.json'),evidence('E5/summary.json'),evidence('E5/preflight.py')],
  'boundary':'65 byte-distinct fixtures, not independent models; known dynamic Gesture failure remains outside scope; template regex extraction does not guarantee safe abstention for every unknown syntax. Official consumers already enforce the selected condition.'},
 {'id':'C8','section':'7.1 / recovered development','claim':'Historical 11 metadata-bearing components/10 graph groups, 46 variants, 105 CPU calls and 23 isolated probes are separately identified recovered evidence.',
  'artifacts':[evidence('phase0/results.json'),evidence('phase0/all-preservation-and-array-audit.json')],
  'boundary':'Fresh byte/array audit does not turn historical execution into new runs; these counts are not pooled with E1/E2.'},
]
AUDIT = pathlib.Path('/workspace/metadata-contract-audit-20261004T062010Z')
fresh = load(AUDIT/'verification/fresh-runtime-crosscheck.json')
assert fresh['status']=='PASS'
assert (fresh['phase_variant_execution_records'],fresh['unique_artifact_consumer_configurations'],fresh['input_observations'])==(8,5,16)
assert fresh['successful_category_lists']==14 and fresh['recorded_getter_exceptions']==2
assert fresh['all_generated_sources_and_generated_classes_equal_historical']
assert fresh['all_fresh_DEX_equal'] and fresh['all_inputs_and_raw_outputs_equal_historical']
baseline=load(AUDIT/'baseline/results.json')
assert len(baseline['models'])==5
for row in baseline['models']:
    c=row['checks']
    assert c['displayer']['status']=='READABLE' and c['populator']['status']=='ACCEPTED'
    expected='INCOMPATIBLE' if row['condition']=='label_deletion' else 'COMPATIBLE_PRECONDITIONS'
    assert c['simple_baseline']['status']==c['e5']['DECODER_COMPATIBILITY']['status']==expected
    assert c['task_init']['status']==('FAIL' if row['condition']=='label_deletion' else 'PASS')
negative=baseline['separate_structural_negative_control']['checks']
assert negative['displayer']['status']=='READABLE' and negative['populator']['status']=='FAIL'
assert 'load_metadata_buffer' in negative['populator']['stack_trace']
literature=load(AUDIT/'literature/results.json')
assert literature['full_text_checks_completed']==4 and not literature['novelty_established']
assert all(x['full_text_review']=='PASS' for x in literature['papers'])
assert 'no guarantee that every unknown form' in paper
assert 'adds zero rejected conditions' in paper
assert 'five byte-distinct artifact--consumer configurations' in paper
assert 'no further model experiments' in paper
assert 'Dynamic signatures and unrecognized processing require abstention' not in paper
assert 'checkregenerated' not in paper
for key in ['mlguard','docter','acetest']:
    assert r'\bibitem{'+key+'}' in paper and r'\cite{'+key+'}' in paper
def audit_evidence(name):
    p=AUDIT/name
    return {'path':str(p),'sha256':sha(p)}
claims.extend([
 {'id':'C9','section':'4.1 / construction audit','claim':'Fresh generation/build/new AVD reproduce E1/E2 outcomes in 8 phase execution records, 5 distinct artifact configurations and 16 input observations; source and generated class bytes match historical files.',
  'artifacts':[audit_evidence('rebuild/results.json'),audit_evidence('verification/fresh-runtime-crosscheck.json'),audit_evidence('rebuild/ContractInstrumentation.java.patch')],
  'boundary':'Reuses installed toolchain. Pre-load AssetManager hash is not native-buffer interception; full DEX equality is within fresh builds only. No independent human reproduction.'},
 {'id':'C10','section':'7.3 / baseline','claim':'Five conditions yield identical rejection vectors for the scoped simple baseline, E5 and Task initialization; metadata reader/populator accept all five. Entry-count control is distinct.',
  'artifacts':[audit_evidence('baseline/results.json'),audit_evidence('baseline/RESULTS.md'),audit_evidence('baseline/tensorlabel-binary-audit.json')],
  'boundary':'Five byte-distinct variants of one graph; no accuracy/prevalence estimate, no Task classification or Android execution in this baseline comparison.'},
 {'id':'C11','section':'2 / 7.2 / scope correction','claim':'E5 uses template regex associations and does not guarantee safe abstention for every unrecognized getter or processor syntax.',
  'artifacts':[audit_evidence('claims/claim-audit.json'),audit_evidence('baseline/RESULTS.md'),evidence('E5/preflight.py')],
  'boundary':'Parser limitation, not an established wrong result on a newly executed natural fixture.'},
 {'id':'C12','section':'8 / 9 / literature','claim':'Bounded full-text comparison positions MLGuard as vision, DocTer/ACETest as implemented constraint extraction/testing, and DARA as model architecture/metadata assessment.',
  'artifacts':[audit_evidence('literature/results.json'),audit_evidence('literature/AUDIT_REPORT.md')],
  'boundary':'Pinned author versions and preserved DARA journal version; no tool reruns or exhaustive novelty proof.'},
])

model_identities = {}
for ex, data in [('E1',e1),('E2',e2)]:
    model_identities[ex] = [{k:u[k] for k in ['variant','component_sha256','variant_sha256','canonical_graph_sha256','metadata_sha256','associated_file_sha256','source_sha256']} for u in data['units']]
model_identities['Hand_reference_bridge'] = {k:bridge[k] for k in ['source_component_sha256','focal_component_sha256','source_canonical_sha256','focal_canonical_sha256']}
claim_map = {'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'manuscript_sha256':sha(ROOT/'manuscript/paper.tex'),
 'activity':'Editorial revision incorporating completed agent audit and fresh construction evidence; no new model experiments in this editing task','claims':claims,'model_identities':model_identities,
 'human_verification':'PENDING; AI agent reviews are not human verification'}
if args.write_map:
    with (ROOT/'CLAIM_EVIDENCE.json').open('x') as f:json.dump(claim_map,f,indent=2)
elif (ROOT/'CLAIM_EVIDENCE.json').exists():
    assert load(ROOT/'CLAIM_EVIDENCE.json')['manuscript_sha256']==sha(ROOT/'manuscript/paper.tex')

log = (ROOT/'manuscript/paper.log').read_text(errors='replace')
assert not re.search(r'Overfull|undefined references|undefined on input',log)
pages = int(re.search(r'Output written on paper.pdf \((\d+) pages',log).group(1))
text = re.sub(r'\s+', ' ', (ROOT/'manuscript/paper-reading.txt').read_text())
# Two-column extraction can separate a phrase that crosses a column break.
# Check the exact witness wording in source and its tokens in extracted PDF text;
# rendered pages are also visually inspected and recorded separately.
assert 'window shade' in paper
assert all(token in text for token in ['999', 'window', 'shade', 'not reached'])
record = {'status':'PASS','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'manuscript_sha256':sha(ROOT/'manuscript/paper.tex'),'pdf_sha256':sha(ROOT/'manuscript/paper.pdf'),
 'pages_in_generic_reading_layout':pages,'source_provenance_entries_unchanged':len(provenance['sources']),
 'checks':['requested section order','E1/E2 preservation and stage records','E3 identical artifact and earliest stage','Hand reference bridge and decoded values','E4/E5 denominators and abstentions','fresh reconstruction counts and source/class/raw comparisons','five-condition official and simple baseline comparison','E5 syntax-coverage limitation disclosed','four pinned full-text literature comparisons','references resolved and no overfull boxes','PDF witness tokens and exact source phrase'],
 'model_experiments_rerun':False,'human_audit_complete':False,'venue_fit_claimed':False}
if args.record:
    with (ROOT/args.record).open('x') as f:json.dump(record,f,indent=2)
print(json.dumps(record,indent=2))
