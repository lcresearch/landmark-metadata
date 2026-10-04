from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]

def main():
    summary=json.loads((ROOT/'results/summary.json').read_text())
    rows=[]
    names={'natural':'Original','negative_control':'Description control','structural_positive_control':'Count reduction','seeded_association_exchange':'Index exchange','associated_label_mutation':'Label deletion'}
    for item in summary['interventions']:
        rows.append(f"{names[item['kind']]} & {item['variants']} & {item['structural_accept']} & {item['cpu_invocations']} & {item['raw_javac_success']} & {item['decoder_pass']}/{item['decoder_fail']} " + chr(92)*2)
    header=r'\begin{tabular}{@{}lrrrrr@{}}'+'\n'+r'\toprule'+'\n'+r'Variant & $N$ & S & CPU & J & D $+/-$\\'+'\n'+r'\midrule'+'\n'
    footer='\n'+r'\bottomrule'+'\n'+r'\end{tabular}'+'\n'
    (ROOT/'manuscript/interventions.tex').write_text(header+'\n'.join(rows)+footer)
    selected=[('945f713bc235','Palm detector (2 binaries)','[1,2016,1]'),('6acda74af3fb','Hand landmarks','[1,63]'),('62a87ded76da','Gesture classifier','[1,8]'),('6c7ab0a6e5dc','EfficientNet classifier','[1,1000]'),('40338edf5ec7','EfficientDet detector','[1,19206,90]'),('ff36e24d4054','DeepLab segmenter','[1,257,257,21]')]
    baseline={x['id']:x for x in summary['baseline']};rows=[]
    for cid,label,shape in selected:
        item=baseline[cid];check=item['decoder_checks'][0]
        obs=item['decoder_observed']['status'].lower()
        comp='yes' if item['raw_javac_exit_code']==0 else 'no'
        if cid=='ff36e24d4054':label+='\\textsuperscript{*}'
        rows.append(f'{label} & \\texttt{{{shape}}} & {check["label_count"]} & {obs} & {comp} \\\\')
    header=r'\begin{tabular}{@{}llrll@{}}'+'\n'+r'\toprule'+'\n'+r'Original generated category path & Output shape & Labels & JVM probe & Raw Java compiles\\'+'\n'+r'\midrule'+'\n'
    (ROOT/'manuscript/baselines.tex').write_text(header+'\n'.join(rows)+footer)

if __name__=='__main__':main()
