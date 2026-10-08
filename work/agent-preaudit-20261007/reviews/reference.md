# HA07 / C5 — agent pre-audit

**Agent disposition: SUPPORTED_WITHIN_INSPECTED_SCOPE. Human status: PENDING.**
Fresh saved-byte computation supports the manuscript's qualified publisher-prescribed
display-order reference. It does not establish stable class IDs, training lineage,
prediction correctness, a release-time documentation chain, or an inference replay.
No historical input/report or human verdict was changed.

Target repository revision is `24f660cf093c3e52efc0cde0c39e7aea1df48053`;
the actually hashed current `work/workshop-convergence-20261007/manuscript/paper.tex`
is `c79ba7f62a194abd487ec4b8ccedb60428ec4edd1f43e6ee155518ffd8bb416e`.
Scope follows HA07 and C5 in the current `CLAIM_EVIDENCE.md`. This is agent task/context
separation on shared infrastructure and inputs, not forensic independence or human review.

## Direct byte and computation checks

Inputs came from `/workspace/evidence-recovery-20261005T170453Z/package-v2/payload/`,
preserving original family paths. `input-identities.json` records exact paths,
sizes and SHA-256 values for 153 selected inputs including the corresponding original
copies. `package-vs-originals.json` records 72/72 selected package files identical to
their currently available `/workspace/<original-family>/...` copies. This is not a
whole-package audit or evidence of independent historical provenance.

Six artifact files were parsed: E1 original; P3 retrieved publisher version 1,
publisher latest, and TFHub fp32/2; E2 permutation and restoration. These represent
one computation, not six independent models. The publisher version-1/latest files
are byte-identical to focal original. TFHub is a different package.

| Artifact | SHA-256 |
|---|---|
| Focal / publisher version 1 / publisher latest | `6c7ab0a6e5dcbf38a8c33b960996a55a3b4300b36a018c4545801de3a3c8bde0` |
| TFHub fp32/2 | `7276a936443685daae8612fc3cb9370247cb1f4966286cd95e02c44e1183f0dd` |
| E2 permutation | `455a04a2c6193ea81bef8fbc47e193aee0449b8cebdc9cc487c7e9e85fe42da7` |
| E2 restoration | `0a605ed10a38fc6f92fc4e266f5560756d2809e2669c45aa3b5a631cd88cea72` |

The new script imports only the archived generated schema, SHA-256
`2359ceb02001d2c611b3f0d571e64992f011ed62cfb06d9d45acf72123537159`.
It recursively compares every known schema object field outside `buffers` and
`metadata`: version, operator codes, subgraphs, description, metadataBuffer and
signatureDefs, including all operator options, tensors and ordered input/output
indices. Numeric arrays preserve dtype, shape and exact bytes. It separately
compares all 166 buffer payloads, other metadata entries and output tensor objects.
There are 62 operators and 164 tensors in the single subgraph. Its sole output is
tensor 163, `Softmax`, float32 `[1,1000]`, buffer 164.

All six parsed artifacts have equal computational fields and ordered outputs,
and all 165 nonmetadata buffers are byte-equal. Buffer 165 is the sole metadata
buffer and is not tensor-referenced. TFHub differs from focal only at buffer 165;
the other selected models preserve all 166 buffer payloads. Appended ZIP bytes
remain outside computational preservation. Full buffer identities and comparisons
are in `fresh-model-bridge.json`; the complete fresh descriptor and ordered output
objects are saved separately. Fresh descriptor SHA-256 is
`78e6672fb306195495adec9b5a1163503becc6448c68a0a2f3515e921e7a62b6` for each artifact.
This serialization differs from the historical FlatBuffer repack, so its digest
is not compared to the recorded `73e57d…` canonical-repack digest.

The reference is the actual body `F11-explicit-class-order`, SHA-256
`536feacc519de3d418de26b2effb4d75694a8c4c0063e36499a46fa8061e2da9`.
The script reads the ZIP member from each actual model and uses the parent-card
instruction to omit the first of 1,001 external lines (`background`) before any
comparison. All resources contain 1,000 plain-LF labels; the script does not rely
on Python `splitlines()` as a substitute for general Java label parsing.

| Full-position comparison against external reference | Matches | Mismatches |
|---|---:|---:|
| Original | 1,000 | 0 |
| Permutation | 1 | 999 |
| Restoration | 1,000 | 0 |

Publisher version 1/latest and TFHub also match all 1,000 labels. The permutation
is the exact one-position left rotation. Index 638 is unchanged because indices
638 and 639 both display `maillot`; `crane` also occurs twice, at 134 and 517.
At index 904, original/reference/restoration say `window screen`; permutation says
`window shade`. No score or inference was inspected in this HA07 subreview.
`fresh-label-rows.json` contains every derived row. Only after deriving it was the
stored comparison opened: all 1,000 stored rows match these fresh results.

## Source authority from actual saved bodies

The saved MediaPipe documentation body directly links the latest model URL and
the separate labels URL. Latest/version-1 retrieved bodies equal the focal file.
The TFHub retrieval record starts at the versioned official fp32/2 address,
records its redirect through Kaggle to Google storage, and records storage metadata
`x-goog-meta-kaggle-remoteurl` naming the same fp32/2 `.tflite` resource. Its saved
generation is `1673541759037639`. The bridge above supplies ordered computation
identity across the two different packages; the redirect record is retained
historical evidence, not a newly authenticated live retrieval.

The actual Lite card body declares `tensorflow/efficientnet/lite0/fp32/2` and
explicitly names `tensorflow/efficientnet/lite0/classification/1` as its parent.
The actual classification/1 card states 1,000 classes, links the exact F11 URL,
and explicitly says to ignore its first background entry, with index 0 = `tench`.
Their body hashes are respectively
`77300c8c37140316900b5712ad4c73f9dd2e87d0701c5804cdccf185b2b8bfae` and
`2b94894d016a0b9a6edcb09d19d3e4b9a3d22ab5393c1af85c70d34a75511f58`.
F11's retrieval-parent bookkeeping names F08 (classification/2), but the exact
classification/1 body independently prescribes the identical URL and background
rule. Thus the qualified chain does not substitute classification/2 for the
explicitly declared parent.

The retained TFHub commit response identifies commit
`81fdea8ffa53b5acbd66a012d17fb8f9602c714b`, dated 2024-03-18, and root tree
`1dade93cc8973a65e45373a0fdbc2cc2d99088f7`. From the complete 6,267-entry recursive
tree response, the new script reconstructs all 3,411 tree object hashes. Every
tree matches, including that root. The two card bytes produce the corresponding
Git blob IDs in their exact paths. Reconstructing the signed commit object from
the saved verification payload and signature also yields its declared commit ID.
GitHub's saved response says the signature is verified; this review does **not**
cryptographically validate the signature or authenticate the historical network
transaction. The saved recursive-tree header echoes the commit ID, not root-tree
ID; tree object reconstruction resolves that distinction.

All 30 retained request bodies match their recorded hashes and sizes. This is
full identity checking of those bodies, not substantive source analysis of every
candidate. Direct authority analysis covers the actual documentation, exact cards,
commit/tree, reference labels and relevant artifact retrieval records above.
The first historical audit attempt remains preserved as FAIL on its tree-header
assumption; its preservation note explains the later object reconstruction. The
current script also initially trimmed the commit signature's trailing newline;
that serialization attempt did not match. Its stdout is retained separately.
Preserving the complete signature yields the exact commit ID; input bytes were
never changed to obtain the match.

## Boundaries, recorded findings and human handoff

The catalog is a later retrieved snapshot, not demonstrated original-release-time
documentation. The external label URL remains unversioned; its archived bytes and
saved generation `1542242075395516` identify the inspected snapshot, not lifetime
immutability. Saved retrievals date to 2026-10-04. Hash/tree consistency supplies
strong internal source linkage while sharing the preserved evidence's provenance.

The ancillary saved synset/name bodies yield 1,000 unique candidate synsets,
1,000 matching checkpoint names and 1,000 matching first display synonyms. This
is independently recomputed name correspondence, **not** artifact-linked stable
IDs or verified training lineage. Duplicate display strings demonstrate why that
promotion is unjustified. The reference-backed result concerns display labels.

No substantive discrepancy with C5 or its current qualified wording was found.
Current wording already retains different-package, date, unversioned-label and
stable-ID limits. The manuscript's statement that *recovery* did not rederive
reference authority remains true of that historical activity; this new pre-audit
can be documented separately without rewriting it as human verification.

**Next human action:** record the current manuscript hash, open the saved Lite
card and exact classification/1 parent, assess their publisher authority and date
limits, rerun `commands.sh` and inspect its full label/bridge outputs. Then couple
the display-map conclusion to the separately attributed HA05 execution evidence.
Do not mark training lineage, stable-ID semantic correctness or prediction accuracy
verified. All human checklist items remain PENDING; the only agent conclusion
here is HA07/C5 within the scope above.

`commands.sh` and `audit_reference.py` are new first-party source. Existing Python
3.11.16, flatbuffers 25.12.19 and numpy 1.26.4 were reused; no install, network query,
model generation, Android build, emulator or inference was performed. Bytecode
writes were disabled during schema imports. The command exits nonzero if any
required computed comparison disagrees; the final run completed successfully.
