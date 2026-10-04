#!/usr/bin/env python3
"""Render P3 source provenance and bounded conclusions from archived analysis."""
import hashlib,json,pathlib
R=pathlib.Path(__file__).resolve().parents[1]
x=json.loads((R/'results.json').read_text())
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
ids=['I01-publisher-model','F02-publisher-latest-model','I06-tfhub-lite-model','F07-pinned-lite-card','F10-pinned-parent-card','F11-explicit-class-order','F01-publisher-labels','F15-tpu-labelmap','F17-synset-order','F18-synset-names']
rows=[json.loads((R/'retrieved'/i/'retrieval.json').read_text()) for i in ids]
chain={'claim':'Independent publisher-prescribed output-index to display-label reference, via graph/weights-equivalent official artifact bridge.','semantic_level':'display association; stable class ID lineage abstains','ordered_steps':[{'step':1,'claim':'Official current MediaPipe documentation links a latest float32 model; this and version1 are byte-identical to focal artifact.','records':['I02-publisher-doc','F02-publisher-latest-model','I01-publisher-model']},{'step':2,'claim':'Downloaded official TFHub tensorflow/efficientnet/lite0/fp32/2 has the same complete computational graph, tensor ordering and all165nonmetadata buffers; only metadata buffer165 differs.','records':['I06-tfhub-lite-model'],'analysis':'analysis/artifact-bridge.json'},{'step':3,'claim':'Pinned TFHub catalog card explicitly declares lite0/fp32/2 as deployment of classification/1.','records':['F07-pinned-lite-card'],'lines':[1,2,5]},{'step':4,'claim':'Pinned classification/1 card explicitly maps its1000outputindices to an external file after ignoring firstbackground entry, with index0tench.','records':['F10-pinned-parent-card'],'lines':[77,78,79,80,81,82,83]},{'step':5,'claim':'The prescribed external file has1001lines. Applying documented rule before comparing yields1000/1000original andrestored matches;999/1000permutation mismatches.','records':['F11-explicit-class-order'],'analysis':'analysis/full-display-order-comparison.json'}],'sources':[{k:v for k,v in r.items() if k in ['id','url','status','sha256','bytes','started_utc','body_path']} for r in rows],'limits':x['limitations']}
(R/'analysis/reference-chain.json').write_text(json.dumps(chain,indent=2)+'\n')
extracts=[]
for key,lo,hi in [('F07-pinned-lite-card',1,8),('F10-pinned-parent-card',69,83),('I02-publisher-doc',2845,2856),('I11-tpu-imagenet-source',189,197),('I12-tensorflow-imagenet-mapping-source',67,110)]:
 lines=(R/'retrieved'/key/'body').read_text().splitlines()
 extracts.append(f'## {key}\n\nBody SHA-256 `{h(R/"retrieved"/key/"body")}`. Line numbers refer to archived bytes.\n\n```text\n'+'\n'.join(f'{i}: {lines[i-1]}' for i in range(lo,min(hi,len(lines))+1))+'\n```\n')
(R/'SOURCE_EXCERPTS.md').write_text('# P3 archived source statements\n\n'+'\n'.join(extracts))
source_table='\n'.join('| '+r['id']+' | `'+r['sha256']+'` |' for r in rows)
text=f'''# P3 Results: external display-label order established; stable IDs remain unresolved

The bounded inquiry obtained an **external publisher-prescribed output-index → display-label reference** tied to the focal computational graph through an official graph/weights-equivalent TFHub model. It did not establish a complete artifact-specific output-index → stable synset ID provenance chain. These are separate results.

No inference was performed for P3. E1/E2 original, cyclic permutation and restoration model bytes were recovered read-only; network retrievals and comparisons below were fresh. This is automated agent verification, not human verification.

## Observations

| Check | Observation |
|---|---|
| Focal / publisher version1 / documentation-linked latest | Byte-identical SHA-256 `{x['focal_component_sha256']}` |
| TFHub lite0/fp32/2 artifact | Package SHA differs; all165nonmetadata buffers identical out of166; only metadata buffer165 differs |
| Graph and output ordering | All nonbuffer/nonmetadata ModelT fields equal, including operator codes, subgraphs, tensor descriptors, output order and signature definitions; metadata buffer165 is not referenced by any graph tensor |
| Canonical model SHA-256 | `{x['canonical_graph_sha256']}` for both models |
| Exact output | One subgraph output, position0, tensor163, shape[1,1000] |
| Publisher card lineage | Pinned lite0/fp32/2 card explicitly names classification/1 as its parent |
| Parent card rule | The1000outputindices use external ImageNetLabels.txt; ignore its firstbackground entry, so index0means tench |
| Reference object |1001lines, beginning background; SHA-256 `536feacc519de3d418de26b2effb4d75694a8c4c0063e36499a46fa8061e2da9` |
| Original / restoration |1000/1000display labels agree with prescribed external order |
| Cyclic permutation |999/1000display labels disagree; unchanged display atposition638 only |
| Position904 | Reference/original/restoration: window screen; permutation: window shade |
| Stable IDs | ABSTAIN: candidate generic synset order and separately linked checkpoint full names agree at1000positions, but exact artifact-to-synset training lineage was not established |

The background removal follows the explicit parent-card instruction; it was not fitted to maximize agreement. The complete1000-position comparison is saved, not only theposition904witness. There are two duplicate display strings: crane at134/517, maillot at638/639. String equality cannot establish stable class identity; the adjacent maillot pair explains the sole unchanged display under the predetermined one-position cyclic shift.

## Evidence chain

1. MediaPipe's documented latest float32 download and itsversion1download reproduce the focal artifact hash.
2. TFHub's exact logical model `tensorflow/efficientnet/lite0/fp32/2` downloads a distinct package whose computational graph, ordered outputs and every nonmetadata buffer match the focal model. The embedded metadata buffer differs and is not used as a graph tensor buffer. The bridge is independently recomputed without importing the old checker or mutation implementation.
3. The catalog card at repository commit `81fdea8ffa53b5acbd66a012d17fb8f9602c714b` explicitly describes that exact Lite model as deployment of `tensorflow/efficientnet/lite0/classification/1`.
4. That exact parent card, at the same commit, explicitly prescribes `https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt`, its background offset and zero-based output index0. The label object is outside the mutated model package. MediaPipe's own full-label-list URL returns identical reference bytes.
5. The complete original, permutation and restoration associated resources are compared against that independent external reference.

This ties a **display-order specification** to the exact focal graph. It is not a re-executed export or proof of the original undocumented conversion history. The pinned catalog commit preserves the publisher statement retrieved now; we do not assert it was the model's original release-time documentation. The external file URL is unversioned, so the preserved bytes/hash are the reference snapshot.

## Exact publisher statements

Pinned [Lite model card](https://github.com/tensorflow/tfhub.dev/blob/81fdea8ffa53b5acbd66a012d17fb8f9602c714b/assets/docs/tensorflow/models/efficientnet/lite0/fp32/lite/2.md):
> TF Lite deployment of tensorflow/efficientnet/lite0/classification/1.

Pinned [exact parent card](https://github.com/tensorflow/tfhub.dev/blob/81fdea8ffa53b5acbd66a012d17fb8f9602c714b/assets/docs/tensorflow/models/efficientnet/lite0/classification/1.md), lines77–83:
> The indices into logits are the `num_classes` = 1000 classes of the classification from the original training (see above). The mapping from indices to class labels can be found in the file at [download.tensorflow.org/data/ImageNetLabels.txt](https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt) and please ignore the first background class, ie. index 0 corresponds to "tench".

The full protocol question asked for output index → stable class ID → display name. That chain remains incomplete. The completed result is a narrower qualified success for **I_display**; stable-ID I remains **ABSTAIN**. This later reference result does not retroactively change frozen E5 semantic abstentions, nor imply that the existing checker consumed this reference.

## Bounded search and negative outcomes

The frozen plan allowed three official source families,12initial candidates and18follow-ups. Exactly those bounds were reached:25HTTP200responses and5HTTP404responses. The initial legacy TFHub raw paths were404; a pinned repository tree resolved their moved paths. Two assumed Google AutoML README paths were404 and their path-history query was empty. The parent card's TPU tutorial URL now redirects to a general PyTorch TPU guide, not a preserved EfficientNet export recipe. Those outcomes remain in the records.

The official TensorFlow TPU EfficientNet-Lite README separately links checkpoint evaluation names. The candidate official TensorFlow Models synset order yields1000/1000full-name matches against that checkpoint map and1000/1000first-name matches against the display reference. This corroborates a conventional ImageNet ordering but does not independently bind stable synset IDs to the exact downloaded artifact's training lineage. No more sources were sought after the budget. Stable-ID agreement remains ABSTAIN.

## Interpretation and limits

P3 strengthens E2 from a change relative to the embedded baseline to a **violation of an independently supplied publisher display-order specification** for999positions, with restoration agreement. It does not establish prediction accuracy, an incorrect classification of an input image, a natural EfficientNet defect, stable class identities for duplicate labels, or external defect prevalence. The immutable E2 execution evidence supplies successful getter behavior; P3 adds the reference comparison rather than a new runtime execution.

## Tool versions and exact artifact records

Analysis Python: `{x['versions']['python'].splitlines()[0]}`; tflite-support `{x['versions']['tflite_support']}`; FlatBuffers `{x['versions']['flatbuffers']}`; NumPy `{x['versions']['numpy']}`. Requests use Python urllib and retain status, headers, redirects, raw body SHA and UTC retrieval timestamps. Source requests/commands are in the JSON request plans and `commands.sh`.

| Preserved source | SHA-256 |
|---|---|
{source_table}

See `analysis/reference-chain.json`, `analysis/artifact-bridge.json`, `analysis/full-display-order-comparison.json`, `analysis/candidate-synset-comparison.json`, `SOURCE_EXCERPTS.md`, and `results.json`. Raw sources, models and network responses remain outside the source-only GitHub repository.
'''
# Use ordinary spacing in prose; data identifiers and hashes remain exact.
for old,new in [('all165','all 165'),('of166','of 166'),('buffer165','buffer 165'),('the1000','the 1000'),('its1000','its 1000'),('has1001','has 1001'),('yields1000','yields 1000'),('with index0','with index 0'),('index0','index 0'),('at1000','at 1000'),('atposition638','at position 638'),('only theposition904witness','only the position 904 witness'),('position904','position 904'),('position0','position 0'),('tensor163','tensor 163'),('shape[1,1000]','shape [1,1000]'),('background entry','background entry'),('firstbackground','first background'),('1000outputindices','1000 output indices'),('1001lines','1001 lines'),('display labels','display labels'),('1000display','1000 display'),('with the documented rule','with the documented rule'),('12initial','12 initial'),('18follow-ups','18 follow-ups'),('25HTTP200responses','25 HTTP 200 responses'),('5HTTP404responses','5 HTTP 404 responses'),('were404','were 404'),('itsversion1download','its version 1 download'),('for999positions','for 999 positions'),('at134/517','at 134/517'),('at638/639','at 638/639'),('1000full-name','1000 full-name'),('1000first-name','1000 first-name'),('theposition','the position')]:text=text.replace(old,new)
for old,new in [('165nonmetadata','165 nonmetadata'),('The1000','The 1000'),('index 0means','index 0 means'),('Position904','Position 904'),('1000positions','1000 positions'),('complete1000-position','complete 1000-position'),('lines77','lines 77'),('families,12','families, 12'),('and18','and 18'),('reached:25','reached: 25'),('and5','and 5'),('and1000','and 1000'),('version1','version 1'),('|1001','| 1001'),('|1000','| 1000'),('|999','| 999')]:text=text.replace(old,new)
(R/'EXPERIMENT_P3_RESULTS.md').write_text(text)
