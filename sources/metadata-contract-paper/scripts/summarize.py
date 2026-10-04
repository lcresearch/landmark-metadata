from pathlib import Path
import collections
import json

ROOT=Path(__file__).resolve().parents[1]

def main():
    s=json.loads((ROOT/'results/static-suite.json').read_text());r=json.loads((ROOT/'results/runtime-suite.json').read_text())
    c=json.loads((ROOT/'results/compile-suite.json').read_text());d=json.loads((ROOT/'results/decoder-suite.json').read_text())
    variants=[v for component in s for v in component['variants']]
    runtime={(x['id'],v['variant']):v for x in r for v in x['variants']}
    compilation={(x['id'],v['variant']):v for x in c for v in x['variants']}
    decoder={(x['id'],x['variant']):x for x in d}
    baseline=[]
    for component in s:
        row={'id':component['id'],'sha256':component['sha256'],'occurrences':component['occurrences'],'canonical_sha256':component['canonical_sha256'],'status':component['status']}
        if component['variants']:
            original=component['variants'][0];key=(component['id'],'original')
            row.update(outputs=[o['shape'] for o in original['inspection']['output_tensors']],decoder_checks=original['decoder_checks'],
              raw_javac_exit_code=compilation[key]['exit_code'],generator_diagnostics=original['generation']['diagnostics'])
            if key in decoder:row['decoder_observed']=decoder[key]['observed']
        baseline.append(row)
    counts=[]
    for kind in ['natural','negative_control','structural_positive_control','seeded_association_exchange','associated_label_mutation']:
        selected=[(component,v) for component in s for v in component['variants'] if v['intervention']['kind']==kind]
        probes=[decoder[(component['id'],v['variant'])] for component,v in selected if (component['id'],v['variant']) in decoder]
        counts.append({'kind':kind,'variants':len(selected),'structural_accept':sum(v['structural_validation']['accepted'] for _,v in selected),
          'cpu_invocations':sum(runtime[(component['id'],v['variant'])].get('invocations',0) for component,v in selected),
          'raw_javac_success':sum(compilation[(component['id'],v['variant'])].get('exit_code')==0 for component,v in selected),
          'decoder_pass':sum(x['observed']['status']=='PASS' for x in probes),'decoder_fail':sum(x['observed']['status']=='FAIL' for x in probes)})
    controls=[]
    for component in s:
        if not component['variants']:continue
        original=component['variants'][0]
        for variant in component['variants']:
            if variant['intervention']['kind'] in ['negative_control','associated_label_mutation']:
                equal=original['generation']['source_sha256']==variant['generation']['source_sha256'];assert equal
                item={'id':component['id'],'variant':variant['variant'],'generated_java_equal':equal}
                baseline_class=compilation[(component['id'],'original')]
                mutated_class=compilation[(component['id'],variant['variant'])]
                if baseline_class.get('exit_code')==0 and mutated_class.get('exit_code')==0:
                    item['compiled_classes_equal']=baseline_class['class_hashes']==mutated_class['class_hashes'];assert item['compiled_classes_equal']
                controls.append(item)
    doc={'component_occurrences':sum(len(x['occurrences']) for x in s),'byte_unique_components':len(s),
      'canonical_graph_groups':len({x['canonical_sha256'] for x in s}),
      'metadata_components':sum(bool(x['variants']) for x in s),'metadata_graph_groups':len({x['canonical_sha256'] for x in s if x['variants']}),
      'variants':len(variants),'cpu_invocations':sum(x['cpu_invocations'] for x in counts),'decoder_probes':len(d),
      'all_runtime_outputs_equal':all(v.get('bitwise_equal_original',True) for x in r for v in x['variants']),
      'all_decoder_predictions_match':all(x.get('prediction_matches',False) for x in d),
      'baseline':baseline,'interventions':counts,'controls':controls,
      'interpretation':'Purposive descriptive counts. Mutations, duplicated graphs, repeated invocations, and oracle-aligned API checks do not estimate prevalence, detector accuracy, or independent replication.'}
    assert doc['byte_unique_components']==13 and doc['canonical_graph_groups']==12
    assert doc['metadata_components']==11 and doc['metadata_graph_groups']==10
    assert doc['variants']==46 and doc['cpu_invocations']==105 and doc['decoder_probes']==23
    assert doc['all_runtime_outputs_equal'] and doc['all_decoder_predictions_match']
    (ROOT/'results/summary.json').write_text(json.dumps(doc,indent=2))
    print(json.dumps({k:v for k,v in doc.items() if k not in ['baseline','controls']},indent=2))

if __name__=='__main__':main()
