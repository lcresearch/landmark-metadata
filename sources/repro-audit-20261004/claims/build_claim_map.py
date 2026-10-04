#!/usr/bin/env python3
"""Build a bounded claim ledger; missing historical evidence stays explicit."""
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path('/workspace/repro-claims')
REPO = Path('/workspace/landmark-metadata')
PAPER = REPO / 'sources/metadata-contract-paper-revision-20261004T065132Z/manuscript/paper.tex'
claims = []


def add(id, lines, claim, status, evidence, observation, limit=''):
    records = []
    for name in evidence:
        p = Path(name)
        records.append({'path': str(p), 'exists': p.is_file(),
                        'sha256': hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None})
    claims.append({'id': id, 'manuscript_lines': lines, 'claim': claim, 'status': status,
                   'evidence': records, 'observation': observation, 'limitation': limit})


def main():
    a = '/workspace/repro-android'
    h = '/workspace/repro-hand'
    g = '/workspace/hand-contract-repro'
    t = '/workspace/repro-task'
    e = '/workspace/repro-external'
    o = str(ROOT / 'observation-readback.json')
    s = str(REPO / 'sources/metadata-contract-e2e-20261004T030536Z/scripts')
    add('C01', [43,44], 'S is specifically the Support 0.4.4 MetadataPopulator path, distinct from metadata readability.', 'matched',
        [t+'/baseline-results.json', o], 'All five core files are readable and accepted by population.',
        'A particular validator acceptance is not general artifact validity.')
    add('C02', [46,51,120], 'I requires an artifact-tied external role/class-order reference; EfficientNet semantic abstention.', 'source_supported',
        [s+'/preflight.py', h+'/results/source-component-equivalence.json'],
        'Hand receives a source-to-graph bridge; no independently sourced EfficientNet class-order oracle was supplied.',
        'Absence from this investigation does not prove no reference exists; no accuracy judgment.')
    add('C03', [53,58], 'Selected list-based TensorLabel decoder uses first nonunit axis, label cardinality and final-axis requirement.', 'matched',
        [g+'/results/decoder-results.json', s+'/preflight.py'],
        'Fresh official-library probes reproduce category outcomes; recognized-path shape conditions remain bounded.',
        'Does not verify arbitrary generated processors or every decoder.')
    add('C04', [58], "Checker label counting follows the actual library's line-reading treatment.", 'deviation',
        ['/workspace/repro-audit/independent-audit/label-parser/results.json', '/workspace/repro-audit/independent-audit/probe_label_parser.py'],
        'Python splitlines recognizes vertical-tab and Unicode U+2028; Java BufferedReader.readLine does not. New label-only counterexamples cause both directions of disagreement with actual FileUtil/TensorLabel.',
        'Synthetic fresh probe, not a natural defect; does not change observed outcomes of ordinary historical fixtures.')
    add('C05', [60,61,104,116], 'Interventions preserve computation; associated-resource interventions also preserve metadata/prefix.', 'matched',
        [a+'/E1/static-results.json', a+'/model-preservation-audit.json', h+'/results/variants.json'],
        'Fresh model construction records P checks; source/index and label interventions retain distinct preservation requirements.',
        'Runtime equality and source/class equality must be verified separately; no native-buffer interception.')
    add('C06', [66], 'EfficientNet digest, [1,224,224,3] input, [1,1000] output, 1000 labels and normalization 127/128.', 'matched',
        [a+'/E1/static-results.json', t+'/baseline/original/displayer/metadata.json'],
        'Publisher model was recovered with exact full digest 6c7ab0a6e5dcbf38a8c33b960996a55a3b4300b36a018c4545801de3a3c8bde0; tensor/label/normalization facts agree.')
    add('C07', [68], 'Four E1 variants and deterministic payload restoration; deletion exactly matched an older retained mutant.', 'matched',
        [a+'/E1/static-results.json'], 'Fresh original, description, label deletion and payload restoration were constructed with the historical source.',
        'Historical mutant byte identity cannot be established from narrative alone if the old complete artifact/digest record is unavailable; fresh data are new evidence.')
    add('C08', [70,250], 'Pinned JDK 17.0.12+7, Java8, TFLite 2.13.0, Support 0.4.4, API30 x86_64 and no EfficientNet source repair.', 'matched',
        [a+'/E1/build-results.json', a+'/E1/static-results.json'],
        'Fresh APK build records and source flags agree; official dependency checks were recorded by Android reconstruction.',
        'Historical generated Gradle project is not built unchanged.')
    add('C09', [79,81], 'Actual getter, raw-buffer observation, two specified 224x224 RGB inputs and default preprocessing.', 'matched',
        [s+'/ContractInstrumentation.java', a+'/E1/executions/primary/original/device/result.json', '/workspace/repro-control/android-task-input-comparison.json', o],
        'The complete fresh Android original ran both inputs through the actual getter; raw values and all2000decoded scores were independently reread.',
        'Compilation alone does not establish public-API reachability.')
    add('C10', [25,84,93,94,95,97,100,262], 'E1 original/control/restoration each return 1000 categories; deletion fails at generated getter after inference.', 'pending',
        [a+'/E1/executions/primary/results.json'], 'Android execution is still running at initial ledger generation.',
        'Caught getter exception is not an uncaught application crash.')
    add('C11', [104], 'E1 generated Java/classes/DEX and tested raw bytes equal across all four variants.', 'pending',
        [a+'/E1/static-results.json', a+'/E1/build-results.json', a+'/audit-results.json'],
        'Static generation/build outputs exist; waiting for independent full runtime readback.',
        'Fresh within-run code equality does not establish identity with missing historical classes/DEX.')
    add('C12', [106], 'E1 replay repeats outcomes and outputs.', 'pending',
        [a+'/E1/executions/replay/results.json'], 'Requires completed primary and replay execution records.',
        'Historical replay facts cannot be recovered from a new replay.')
    add('C13', [110,112,114,116], 'E2 cyclic shift, complete multiset preservation, 999 changed positions due to adjacent maillot duplicates at 638/639.', 'pending',
        [a+'/E2/static-results.json', t+'/primary/label_permutation/gray127-decoded.json', o],
        'Linux Task new raw categories independently confirm complete cyclic mapping and 999 changed labels; Android still pending.',
        'A known historical protocol is repeated, not newly blind preregistration.')
    add('C14', [116], 'E2 all stages and getter pass; raw bytes, scores, argmax/top5 and code unchanged; inverse restores lists.', 'pending',
        [a+'/E2/executions/primary/results.json'], 'Requires completed Android E2 output records.',
        'Linux decoded-score agreement is not a substitute for Android raw tensors.')
    add('C15', [118], 'E2 exact score 0.23542051017284393 at904 and 0.001122338930144906 at649, with named label changes.', 'pending',
        [a+'/E1/executions/primary/original/device/result.json', a+'/E2/executions/primary/results.json', o], 'Both exact score values match the fresh Android original; E2 permutation linkage remains pending.',
        'Even if these values match, missing full historical output arrays remain unavailable.')
    add('C16', [122], 'Historical E2 replay transport interruption, missing fourth record, then separate restoration run.', 'not_testable',
        [str(PAPER)], 'Only the historical manuscript/source reports remain; the old transport logs and device records are not in the source-only checkout.',
        'Do not recreate or infer this chronology from new complete runs.')
    add('C17', [126], 'Historical construction audit had eight records/five configurations/16 observations, new key/AVD and pre-load hashes.', 'not_testable',
        [str(REPO/'sources/metadata-contract-audit-20261004T062010Z/rebuild/scripts/audit_results.py')],
        'The audit procedure is present but the historical raw records/APKs are not; new runs can reproduce the mechanism and their own denominators only.',
        'Missing historical output identity is not a failed replication of the underlying behavior.')
    add('C18', [130,132,142,143,144,145], 'Linux Task 0.4.4 original/control/permutation initialize/classify; deletion raises exact cardinality ValueError at init.', 'matched',
        [t+'/task-results.json', t+'/primary/label_deletion/result.json', o],
        'Independent readback covers primary/replay for five variants including restoration: ten Task instances, 16 successful input observations and two init rejections.',
        'The paper used four Task variants; restoration is an explicitly additional fresh control, not historical evidence.')
    add('C19', [130,153], 'Task uses same model bytes and saved inputs; permutation preserves 1000 per-index score bits and changes999 labels; replay equal.', 'matched',
        [t+'/task-results.json', t+'/inputs/manifest.json', o],
        '16,000 decoded categories were independently read; indices exactly0..999, float32 bit fields reserialized, all cyclic mappings and replays checked.',
        'Task public categories are not internal raw tensors; no Android/Linux raw equivalence claim.')
    add('C20', [151], 'Task C++ checks output label cardinality during creation; generated Java checks at TensorLabel getter.', 'source_supported',
        [s+'/task_one.py', a+'/E1/variants/original/generated/src/main/java/org/example/contract/ContractModel.java'],
        'Observed Task diagnostics and generated expression identify the two configured stages.',
        'Source-to-wheel reproducible build is not established; consumer/platform/runtime still confounded.')
    add('C21', [25,155,247], 'E3 only establishes configuration-specific enforcement stages, with platform/runtime differences retained.', 'source_supported',
        [str(PAPER), t+'/primary/label_deletion/result.json'],
        'The manuscript already states this boundary; current work does not isolate a consumer-only treatment.',
        'Same-Android Task-vs-wrapper P2 remains separate planned work.')
    add('C22', [159,161], 'Hand output-role witness exact6acda, source commit4cf89, pin11c272 with 173buffers and only172 differing.', 'matched',
        [h+'/results/source-component-equivalence.json', h+'/results/assets.json', h+'/sources/hand_landmarks_detector_graph.cc', h+'/sources/external_files.bzl'],
        'New source/artifact recovery and byte comparisons reproduce the exact nonmetadata and canonical bridge.',
        'Graph-equivalence bridge is not direct source pinning of the focal complete file; human source interpretation remains pending.')
    add('C23', [163], 'Hand metadata exchange changes four bytes, swaps role agreement; raw Java fails and four separator edits on two lines compile.', 'matched',
        [g+'/results/static-results.json', g+'/results/compile-results.json'],
        'Fresh original/swapped code generation, javac failure, disclosed repair success and javap bindings agree.',
        'The paper describes historical compilation/fresh old audit disassembly; this turn adds new compilation, not retrieval of the old classes.')
    add('C24', [165,167], 'Hand Task0.10.14 IMAGE, one requested hand, thresholds0.5; four bundles, one source-pinned image return1hand21+21 unchanged/replay equal.', 'matched',
        [h+'/scripts/hand_task_one.py', h+'/results/assets.json', h+'/results/variants.json', o],
        'Eight new Task executions and actual decoded JSON independently read; one hand with21+21 coordinates and identical decoded values in every record.',
        'One image; decoded Task outputs, no internal raw tensor/accuracy evidence or old-to-new bit identity.')
    add('C25', [169], 'Hand fixed-index/hardcoded Right/Left Task routing; exchange does not repair generic TensorLabel scalar path.', 'matched',
        [h+'/sources/hand_landmarks_detector_graph.cc', g+'/results/decoder-results.json'],
        'Official integration source and new official-library decoder failures support distinct association and decoder conditions.',
        'No general metadata-insensitivity or repaired Hand Android wrapper execution claim.')
    add('C26', [174], 'Earlier corpus11metadata/10graphs/46variants;11counts rejected;8swaps+5label deletions accepted;35variants/105CPU equal;23JVM.', 'matched',
        ['/workspace/metadata-contract-paper/results/summary.json', '/workspace/repro-control/corpus-verification.json'],
        'Fresh corpus rerun and independent594-check readback verify35accepted,11rejected,105CPU observations,243 output arrays,23decoder probes.',
        'This turn reruns, while the manuscript historical revision only audited prior records; new results do not establish bit identity with missing old arrays.')
    add('C27', [176], 'Historical freeze preceded external metadata inspection.', 'not_testable',
        [e+'/E4/prevalidation-freeze.json', e+'/E4/protocol/REPLAY_CONTEXT.json'],
        'Fresh repeat freeze exists but historical results were already known. It cannot recreate the historical information state.',
        'Do not call the repeat blind validation or third-party preregistration.')
    add('C28', [176,186,187,188], '20externalURLs;16downloads/4HTTP404;18occurrences;exclude1priorcomponent+2priorgraphs;15newgraphs.', 'matched',
        [e+'/E4/results.json', o], 'All exact counts independently recomputed from candidate/component records and15model digests read back.')
    add('C29', [178,189,190,191,192], 'E4 S15/Iabstain15; javac8/7;D4compatible9incompatible2inapplicable;zero runtime.', 'matched',
        [e+'/E4/results.json', o], 'Counts independently recomputed from individual records; E4 is static-only.')
    add('C30', [178], 'Nine E4 incompatibilities split into five existing javac failures and four warned unsupported non-RGB fallbacks.', 'matched',
        [e+'/E4/results.json', o], 'All nine paths inspected; five raw javac failures and four exact unsupported-output warnings reproduced.',
        'Neither nine natural model defects nor any new supported end-to-end natural failure.')
    add('C31', [199,200], 'Preflight identifies EfficientNet getter/output0/axis1/1000vs999 without model inference.', 'matched',
        [e+'/E5/cli-probe-results.json', e+'/E5/results.json'],
        'Real recovered deletion fixture and direct CLI probes expose the expected incompatible D record.',
        'CLI exit0 is not an all-dimensions success contract; consume structured statuses.')
    add('C32', [202], '65distinctfixtures;S52/11/2;D27incompatible8compatible14inapplicable3dynamic2nometa11notreached;I65abstain.', 'matched',
        [e+'/E5/results.json', e+'/E5/replay-summary.json', o],
        'All65actual model hashes, individual check result files and grouped statuses independently reread; exact counts reproduced. Core additions use already-executed Task model files.',
        '65fixtures are not65independent models; generated hardcoded narrative is not supporting raw evidence.')
    add('C33', [204], 'E5 flags actual Android failure, accepts four successful core byte-distinct conditions; dynamicGesture deletion abstains.', 'pending',
        [e+'/E5/results.json', e+'/E5/replay-summary.json'],
        'Dynamic-signature scope is supported by real recovered records; Android linkage awaits actual executions.',
        'Three dynamic abstentions include a concrete-shape isolated failure; no universal failure-detection guarantee.')
    add('C34', [206], 'Limited regex/template matching can miss unknown getter/processor forms; no sound automatic abstention guarantee.', 'matched',
        [s+'/preflight.py', '/workspace/repro-audit/independent-audit/probe-results.json'],
        'Source review and fresh parser probes support the already-disclosed limitation.',
        'New label-line-reading mismatch C04 is an additional limitation beyond this wording.')
    add('C35', [209,211,220,221,222,223,224], 'Five core files readable/populationaccepted;simplebaseline/E5/Taskinit reject deletion only;zero extra E5rejects.', 'matched',
        [t+'/baseline-results.json', e+'/E5/results.json', e+'/E5/core-baseline-comparison.json', o],
        'All20official/simple/Task baseline outcomes independently read and joined by actual model digest to E5, matching fourpasses/onefailure for decoder-related checks.',
        'Static and Linux Task initialization result; no future Android result is inferred and no broad algorithm novelty established.')
    add('C36', [231], 'Separate zero-output-metadata control is readable but rejects at load_metadata_buffer before populate.', 'source_supported',
        ['/workspace/metadata-contract-paper/results/summary.json', str(REPO/'sources/metadata-contract-audit-20261004T062010Z/baseline/audit_one.py')],
        'New corpus confirms count control rejected; exact displayer/load-vs-populate stage requires a dedicated current record.',
        'Historical precise stage report alone is not new raw evidence.')
    add('C37', [234,236,238,240,256], 'Bounded literature methods/positioning: MLGuard vision; DocTer docs constraints; ACETest LLVM/SVF/Z3; DARA architecture metadata.', 'not_testable',
        [str(REPO/'sources/metadata-contract-audit-20261004T062010Z/literature/AUDIT_REPORT.md'), str(PAPER)],
        'Current manuscript references and preserved detailed literature audit were read. They are internally consistent and explicitly bounded.',
        'This turn did not recover/reread all four complete PDFs, verify bibliographic endpoints or rerun prior tools. The old report is secondary evidence, not a fresh full-text/novelty audit.')
    add('C38', [240,255,256], 'Four-paper comparison establishes neither exhaustive novelty nor systematic search; Stalnaker abstract-only.', 'source_supported',
        [str(PAPER), str(REPO/'sources/metadata-contract-audit-20261004T062010Z/literature/AUDIT_REPORT.md')],
        'The manuscript accurately states its claimed literature scope; no new exhaustive novelty check was attempted.')
    add('C39', [250], 'Historical emulator37.2.12build16428233 and API30image archive revision11/internalrevision10.', 'matched',
        [a+'/prerequisites/downloads.json', a+'/prerequisites/android-getprop.command.json', a+'/versions/emulator.command.json'], 'Android agent recovered exact version artifacts with official checksums; current emulator version and runtime properties are preserved.',
        'New toolchain recovery does not prove old unretained machine state.')
    add('C40', [250,253], 'Historical initial rebuild chronology; cumulative logcat attribution; complete sealed local evidence package and companion claim map.', 'not_testable',
        [str(PAPER)], 'Old raw evidence package was not included in the source-only checkout. Newly generated raw evidence is kept under distinct repro paths.',
        'Paths and hashes printed in text do not replace unavailable raw files or authenticate every historical execution.')
    add('C41', [247,253,259], 'No independent human verification, no public standalone evidence deposit; AI-assisted scope.', 'source_supported',
        [str(REPO/'MEMORY.md'), str(REPO/'TODO.md')],
        'No human audit evidence or portable raw-artifact deposit was supplied or created in this delegated audit.',
        'Fresh agent verification must not be relabeled independent human reproduction.')
    readback_path = ROOT/'observation-readback.json'
    readback = json.loads(readback_path.read_text()) if readback_path.is_file() else None
    final = bool(readback and readback['failed'] == 0 and readback['android']['complete'] and
                 readback['android']['completed_execution_records'] == 16)
    if final:
        observations = {
            'C10': 'Both primary and replay completed all four E1 conditions: originals/description/restoration each return1000categories for both inputs; deletion reaches the generated getter after successful inference and throws the exact recorded IllegalArgumentException.',
            'C11': 'Independent direct hashing confirms all eight E1/E2 generated Java files, corresponding three-class sets and DEX sets are identical within the fresh run. Every input output array is4000bytes and equals its fresh original across all variants/phases.',
            'C12': 'All eight E1 primary/replay records were read; all16input observations preserve prescribed input bytes and raw outputs;12category lists succeed and4getter observations fail as expected.',
            'C13': 'All eight E2 primary/replay records complete. The full cyclic mapping changes exactly999labels per input with score preservation; inverse restores original associations. Task and Android use exact matching model artifacts.',
            'C14': 'Independent readback of all16E2input observations confirms raw bytes,1000scorebits, complete cyclic label mapping and restoration. Code equality was separately checked on actual source/classes/DEX files.',
            'C15': 'The fresh Android records exactly reproduce0.23542051017284393at904(window screen to window shade) and0.001122338930144906at649(megalith to microphone) in the permutation and replay. Score fields agree with serialized rawfloat32bits.',
            'C33': 'Exact model digest join connects65E5staticfixtures to the five fresh Android artifact conditions. Only deletion has actual getter failure and E5 INCOMPATIBLE; four other artifact conditions execute successfully. Dynamic Gesture abstention remains unchanged.'}
        for claim in claims:
            if claim['id'] in observations:
                claim['status'] = 'matched'
                claim['observation'] = observations[claim['id']]
                if not any(x['path'] == str(readback_path) for x in claim['evidence']):
                    claim['evidence'].append({'path': str(readback_path), 'exists': True,
                                              'sha256': hashlib.sha256(readback_path.read_bytes()).hexdigest()})
    data = {'manuscript': str(PAPER), 'manuscript_sha256': hashlib.sha256(PAPER.read_bytes()).hexdigest(),
            'fresh_Android_readback_complete': final,
            'status_definitions': {
                'matched': 'The bounded factual result is supported by new observations or fresh artifacts, not necessarily historical raw-byte identity.',
                'deviation': 'A fresh counterexample contradicts the stated general claim.',
                'not_testable': 'Historical event, missing raw evidence or full-text material was not recoverable/reviewed here.',
                'source_supported': 'Supported by inspected code or scope records, not certified by a new end-to-end execution.',
                'pending': 'Required new run or final comparison remains in progress.'},
            'claims': claims, 'status_counts': dict(Counter(c['status'] for c in claims)),
            'global_boundary': 'Never use new raw outputs or repository prose as proof of missing historical output identity. Repeated source/artifact hashes are distinguished from regenerated classes and runtime results.'}
    (ROOT/'claim-map.json').write_text(json.dumps(data, indent=2)+'\n')
    print(json.dumps(data['status_counts']))


if __name__ == '__main__': main()
