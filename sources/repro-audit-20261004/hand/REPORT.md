# Hand / E7 fresh reproduction and audit

Executed on 2026-10-04 UTC in a new cloud machine. Historical repository snapshots were not modified. This is a fresh agent reconstruction from official sources, not independent human verification and not a comparison with the unavailable sealed historical raw outputs.

## Observed result

The Hand results reproduced. The exact focal component has metadata roles inconsistent with the source-backed output order. A controlled exchange changes generated binding but preserves the graph and tested raw computation. The official MediaPipe Task succeeds on the fixed image and returns identical decoded outputs for every condition. The metadata exchange does not repair the generic scalar category decoder.

| Actual check | Result |
| --- | --- |
| Official focal and source-pinned bundle recovery | PASS; exact expected component and source-pinned bundle hashes |
| Fixed `thumb_up.jpg` recovery | PASS; source-pinned image digest |
| Source-to-artifact bridge | PASS; 173 buffers, only metadata buffer 172 differs, all 172 nonmetadata buffers and canonical graph equal |
| Generic static/model-generation stages | PASS for original, swapped, description control, swap-back |
| Unmodified generated Java compilation | Expected failure for all four conditions |
| Identical separator repair and compilation | PASS for all four; exactly lines 71 and 315 changed |
| Fresh javap binding | Original handedness→0 / landmarks→2; swapped handedness→2 / landmarks→0 |
| CPU raw computation | 4 conditions × 12 synthetic inputs = 48 invocations; 192 output arrays bitwise equal to original |
| Host-JVM TensorLabel, original `[1,63]` | Expected `Label number 2 mismatch the shape on axis 1` |
| Host-JVM TensorLabel, swapped `[1,1]` | Expected `Cannot find an axis to label` |
| Explicit two-score decoder positive control | PASS; two categories |
| Official MediaPipe Task | 4 conditions × primary/replay = 8 successful calls; each returns 1 hand, 21 landmarks and 21 world landmarks |
| Task comparisons | All decoded JSON hashes, float-bit hashes and replay observations equal |

Fresh CPU NPZ files were independently read back and all 192 arrays compared, rather than accepting the script's summary flags. Task decoded files, float-bit files and counts were independently read back too. The four generic conditions and four Task conditions are interventions on one graph; they are not independent models.

## Exact identities

| Artifact | SHA-256 |
| --- | --- |
| Official version-1 task bundle | `fbc2a30080c3c557093b5ddfc334698132eb341044ccee322ccf8bcf3607cde1` |
| Focal Hand component | `6acda74af3fbf40e68265c20c7394b2bad81a16a481dcd79ad7a081887c3d6b9` |
| Controlled swapped component | `5c4a32919676d6645c082b4b2912ae4881862af967b5aa5b40e0ef6d616a3025` |
| Source-pinned task bundle | `32d1eab97e80a9a20edb29231e15301ce65abfd0fa9d41cf1757e0ecc8078a4e` |
| Source-pinned component | `11c272b891e1a99ab034208e23937a8008388cf11ed2a9d776ed3d01d0ba00e3` |
| Canonical graph/weights | `fb3baefeb2c67e5c11013ede2408204bc431e99cffc34e81f19df16a7b711793` |
| Fixed thumb-up image | `5d673c081ab13b8a1812269ff57047066f9c33c07db5f4178089e8cb3fdc0291` |
| Every Task decoded result | `3979eb57fec51e574cabbdb15f34957e6e2d5988c6ca10240b79a2bc9efdfe2c` |
| Every Task decoded float-bit stream | `227d1830be3ee8b0122fe79acdbd106c26288fa8e7bf438464ca78d99637d0ae` |

`git ls-remote` confirms MediaPipe `v0.10.14` resolves to `4cf89a70942ca3252e46ace7e4552f53be9bef2e`. Fresh immutable-source recovery confirms:

- `third_party/external_files.bzl:524` pins the task bundle above with GCS generation `1677051718270846`; lines 1394–1396 pin the image with generation `1662650667349746`.
- `hand_landmarks_detector_graph.cc:280` routes output 0 to landmarks, 1 to presence, 2 to handedness, 3 to world landmarks.
- Lines 129–141 explicitly select binary classification and hardcode `Right`/`Left`, with a TODO to use model metadata.
- Lines 285–302 perform landmark normalization; metadata text is insufficient to treat the raw 63 values as already normalized coordinates.

The reference and focal components are different files; the bridge is graph/weight equality, not a direct source pin to the focal component's file hash. Both recovered components contain the same mislabeled output-role names. The case-informed source interpretation remains unaudited by a human.

## Freshly confirmed repository defects

1. `sources/metadata-contract-e2e-20261004T030536Z/E7/hand_task_one.py:24` catches Task failures and then exits zero after writing its JSON. An actual invalid-bundle negative control produced `RuntimeError: Unable to open zip archive.` at initialization with exit code 0. A caller must inspect the result fields. The new external runner does so.
2. `sources/metadata-contract-e2e-20261004T030536Z/E7/summarize_hand.py:17` unconditionally writes prose claiming all four Task conditions succeeded. A separately labeled synthetic harness fixture containing four copies of the actual invalid-bundle failure produced that all-pass sentence, even though its table said `NOT_REACHED` and its computed equality flags were false. This is a reporting defect; it does not invalidate the eight successful Task calls observed here.
3. The generic Hand Java generator produces malformed separators in all four tested conditions. Fresh raw javac failures and the disclosed minimal repair reproduced this existing boundary. The repaired wrapper's binding is a compile/disassembly witness; no repaired Android Hand-wrapper inference was run.

Evidence for the reporting tests is separate from experiment evidence under `audit/`. The synthetic summary fixture is explicitly labeled and is not included in the experimental counts.

## Evidence locations

- Generic pipeline and four step exit statuses: `/workspace/hand-contract-repro/results/run-manifest.json`
- Static preservation and generated interfaces: `/workspace/hand-contract-repro/results/static-results.json`
- Fresh Java compilation/disassembly: `/workspace/hand-contract-repro/results/compile-results.json`
- CPU raw results: `/workspace/hand-contract-repro/results/inference-results.json`, with NPZ/float files under `results/runtime-arrays/`
- Official host-JVM decoder: `/workspace/hand-contract-repro/results/decoder-results.json`
- Independent CPU readback: `/workspace/repro-hand/results/independent-array-readback.json`
- Exact assets and URLs: `/workspace/repro-hand/results/assets.json`
- Reference bridge: `/workspace/repro-hand/results/source-component-equivalence.json`
- Four Task variants: `/workspace/repro-hand/results/variants.json`
- Task primary: `/workspace/repro-hand/executions/primary/results.json`
- Task replay: `/workspace/repro-hand/executions/replay/results.json`
- Independently checked Task summary: `/workspace/repro-hand/results/task-summary.json`
- Executed historical scripts' byte equality: `/workspace/repro-hand/results/executed-source-provenance.json`
- Worker exit-status negative control: `/workspace/repro-hand/audit/worker-exit-status.json`
- Synthetic summary negative control: `/workspace/repro-hand/audit/synthetic-summary-negative-control/audit-result.json`

## Runtime and limits

Generic work used the reconstructed shared Python 3.11.16 / TFLite Support 0.4.4 / TFLite runtime 2.14.0 environment and the restored JDK 17.0.12+7 / Java dependency set. Task work used a separate Python 3.11.16 virtualenv and all 26 exact lines from archived E7 `requirements.lock`, including MediaPipe 0.10.14 and NumPy 1.26.4. `pip check` passed and observed freeze exactly matched the lock. Wheels were freshly downloaded and hashed; all three installed MediaPipe native libraries equal the freshly downloaded wheel's members. Original archived wheels were unavailable, so byte equality to that archive is not established.

Official asset access initially failed through the proxy (403 for `storage.googleapis.com`), then succeeded following a reported network configuration change. TLS/proxy verification remained enabled.

The fixed-image results are decoded public Task outputs, not internal raw Task tensors or an accuracy benchmark. The Task's embedded TFLite version is not established separately, and wheel/source-build equivalence is not proved. Human verification and comparisons to the original sealed evidence remain outstanding.
