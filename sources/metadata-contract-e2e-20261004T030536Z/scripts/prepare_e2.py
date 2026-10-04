import collections, json
from common import ROOT
from prepare_e1 import prepare, rewrite_associated, associated

def main():
    # Gate execution on complete E1 primary and replay, including all four variants.
    for run in ['primary','replay']:
        rows=json.loads((ROOT/'E1/executions'/run/'results.json').read_text());assert len(rows)==4
        for r in rows:
            assert r['load_status']=='PASS' and r['inference_status']=='PASS'
            assert r['decoder_status'] in ['PASS','FAIL']
            if r['variant'] in ['original','description_control']:assert r['decoder_status']=='PASS'
    original=(ROOT/'E1/variants/original/model.tflite').read_bytes();entries=associated(original)
    name='labels_without_background.txt';lines=entries[name].decode('utf-8').splitlines();assert len(lines)==1000
    shifted=lines[1:]+lines[:1];assert collections.Counter(shifted)==collections.Counter(lines)
    ending='\n' if entries[name].endswith(b'\n') else ''
    changed=dict(entries);changed[name]=('\n'.join(shifted)+ending).encode()
    mutant=rewrite_associated(original,changed)
    restored_lines=shifted[-1:]+shifted[:-1];restored=dict(changed);restored[name]=('\n'.join(restored_lines)+ending).encode()
    assert restored==entries
    variants=dict(original=original,description_control=(ROOT/'E1/variants/description_control/model.tflite').read_bytes(),label_permutation=mutant,permutation_restoration=rewrite_associated(mutant,restored))
    prepare('E2',variants,original,'Same exact EfficientNet version-1 bytes as E1; see CURRENT_STATE.md')
if __name__=='__main__':main()
