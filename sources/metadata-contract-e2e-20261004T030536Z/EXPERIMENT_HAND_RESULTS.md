# E7 Hand results

| Task condition | Initialize | Detect | Hands | Landmarks / world landmarks | Decoded float bits equal original | Replay equal |
|---|---|---|---:|---|---|---|
| original | PASS | PASS | 1 | [21] / [21] | True | True |
| container_control | PASS | PASS | 1 | [21] / [21] | True | True |
| metadata_exchange | PASS | PASS | 1 | [21] / [21] | True | True |
| restoration | PASS | PASS | 1 | [21] / [21] | True | True |

All four official MediaPipe 0.10.14 CPU Task conditions return one hand, 21 landmarks, 21 world landmarks and identical handedness/coordinate values on the single predeclared thumb_up.jpg fixture. The fixture matches the image pinned by the release’s external_files.bzl. Primary and same-environment replay agree. These are decoded Task outputs, not internal raw model tensors or an accuracy benchmark.

## Exact reference bridge

The v0.10.14 tag resolves to commit `4cf89a70942ca3252e46ace7e4552f53be9bef2e`; immutable-commit source reads match the preserved files. That revision pins task bundle `32d1eab97e80a9a20edb29231e15301ce65abfd0fa9d41cf1757e0ecc8078a4e` and GCS generation `1677051718270846`. Its landmark component is `11c272b891e1a99ab034208e23937a8008388cf11ed2a9d776ed3d01d0ba00e3`, while the focal component remains `6acda74af3fbf40e68265c20c7394b2bad81a16a481dcd79ad7a081887c3d6b9`.

These component files are not identical. Both contain 173 buffers, and only metadata buffer 172 differs. All 172 non-metadata buffers and canonical graph `fb3baefeb2c67e5c11013ede2408204bc431e99cffc34e81f19df16a7b711793` agree. Thus the output-role reference is transferred through a verified graph/weight bridge to the source-pinned test artifact; it is not a claim that the source directly pins the focal file hash. See REFERENCE_CHAIN.md and source-component-equivalence.json.

## Four distinct concerns

- Output-index association: the source routes 0→landmarks, 1→presence, 2→handedness, 3→world landmarks. Focal metadata says handedness at 0 [1,63] and landmarks at 2 [1,1]. The provided source-backed role reference disagrees with original and agrees after the controlled 0/2 exchange. The extraction was made with knowledge of the case, not by blinded human annotators.
- Handedness representation: the Task graph explicitly sets binary classification with hardcoded Right/Left labels and a TODO to obtain labels from metadata. This is a specific scalar conversion, not a two-element raw category tensor.
- Category decoder suitability: the generated TensorLabel path is incompatible both before exchange ([1,63], two labels) and afterward ([1,1], no nonunit axis). A role-association exchange is not a complete repair.
- Coordinate normalization: the Task graph normalizes landmark coordinates in dedicated postprocessing. The embedded text does not establish that the raw 63-value output is already normalized.

## Generic binding and Task boundaries

The old raw Hand Java compile failures (1/1) and separator-repaired successes (0/0) remain recovered execution results. Fresh byte/hash checks and in-memory reapplication of the same four separator rules match the preserved repaired sources; both alter lines 71 and 315. Fresh javap of preserved classes recovers handedness→0 / landmarks→2 before exchange and handedness→2 / landmarks→0 afterward. No new Hand compiler run or repaired Android wrapper execution is claimed.

The official Task comparison actually exercises its landmark path, and the tested output-metadata association exchange does not change its decoded result. Its fixed index wiring and hardcoded handedness conversion explain this boundary. This does not show that all metadata is ignored: input preprocessing still obtains model/image tensor specifications. No official Task failure, user harm or task-accuracy conclusion follows.

The installed runtime is the archived MediaPipe 0.10.14 wheel; native-library hashes match that wheel. Its separate embedded TFLite version was not exposed/established, and no independent source-build equivalence of the wheel is claimed. A human must still audit the source interpretation and preservation bridge.
