# Hand reference chain

Release source v0.10.14 resolves to commit 4cf89a70942ca3252e46ace7e4552f53be9bef2e. third_party/external_files.bzl pins hand_landmarker.task by SHA-256 32d1eab97e80a9a20edb29231e15301ce65abfd0fa9d41cf1757e0ecc8078a4e and GCS generation 1677051718270846. Both pin and downloaded bytes were verified.

The pinned landmark component is 11c272b891e1a99ab034208e23937a8008388cf11ed2a9d776ed3d01d0ba00e3, not focal 6acda74af3fbf40e68265c20c7394b2bad81a16a481dcd79ad7a081887c3d6b9. Both have 173 buffers; only metadata buffer 172 differs. Their canonical graph hash is fb3baefeb2c67e5c11013ede2408204bc431e99cffc34e81f19df16a7b711793. All 172 non-metadata buffers agree. Output indices/shapes agree. This is a source-pinned graph/weight reference bridge, not exact component identity.

The source graph routes 0→landmarks, 1→presence, 2→handedness, 3→world landmarks. It sets binary handedness conversion and hardcoded Right/Left names, with a TODO to obtain those labels from metadata; it normalizes coordinates in dedicated postprocessing. Output-role associations therefore have a concrete graph-specific official reference independent of the inspected metadata names.

The reference JSONs are research-assistant extractions of that official contract, not independently blinded or human-verified annotations. Their hashes and the model preservation checks make the extraction reviewable; a human must still verify interpretation. The E5 semantic abstention results remain unchanged because this strengthened reference chain was developed later in E7.

The fixed thumb_up.jpg input additionally matches the image hash and GCS generation pinned by the same source revision. No new input or threshold was chosen after observing model results. The runtime wheel is MediaPipe 0.10.14, but no independent source-build equivalence of the wheel is claimed.
