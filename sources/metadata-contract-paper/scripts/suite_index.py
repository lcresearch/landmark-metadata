from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]

def main():
    contracts=json.loads((ROOT/'contracts.json').read_text())['contracts'];results=[]
    for component in json.loads((ROOT/'results/static-suite.json').read_text()):
        matches=[contract for prefix,contract in contracts.items() if component['sha256'].startswith(prefix)]
        assert len(matches)<=1
        for variant in component['variants']:
            record={'id':component['id'],'sha256':component['sha256'],'variant':variant['variant']}
            if not variant['structural_validation']['accepted']:
                record.update(status='NOT_EVALUATED_STRUCTURAL_REJECTION');results.append(record);continue
            if not matches:
                record.update(status='ABSTAIN_NO_SEMANTIC_REFERENCE');results.append(record);continue
            contract=matches[0];record['source']=contract['source']
            metadata=variant['inspection']['metadata']['subgraph_metadata'][0]['output_tensor_metadata']
            issues=[];unknown=[]
            for i,expected in enumerate(contract['expected_roles']):
                name=metadata[i].get('name');actual=contract['name_to_role'].get(name)
                if actual is None:unknown.append(i)
                elif actual!=expected:issues.append({'position':i,'metadata_name':name,'mapped_role':actual,'expected_role':expected})
            record.update(status='FAIL' if issues else ('ABSTAIN_UNKNOWN_NAME' if unknown else 'PASS'),issues=issues,unknown_positions=unknown)
            results.append(record)
    (ROOT/'results/index-suite.json').write_text(json.dumps(results,indent=2))
    for record in results:
        if record['status'] in ['PASS','FAIL']:print(record['id'],record['variant'],record['status'],record['issues'])

if __name__=='__main__':main()
