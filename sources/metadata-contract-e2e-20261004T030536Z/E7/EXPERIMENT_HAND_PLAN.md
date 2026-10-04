# Secondary Hand experiment — E7

E1–E5 are complete before this phase. Recheck the preserved exact Hand component, metadata, graph, syntax-repair audit and compiled binding. Do not rerun the old Hand experiment merely to add invocations. Fresh disassembly of preserved classes is permitted and must be labeled separately from fresh compilation.

Pin official source v0.10.14 to resolved commit `4cf89a70942ca3252e46ace7e4552f53be9bef2e`; preserve its Hand graph and test sources. The graph routes output 0 to landmarks, 1 to presence, 2 to handedness and 3 to world landmarks. It explicitly sets binary handedness classification with hardcoded Right/Left labels and performs coordinate normalization. Verify each statement against source. The release source's relationship to model bytes must be described honestly; do not infer an immutable model hash from a mutable asset URL.

Attempt a task-specific comparison using the official mediapipe==0.10.14 Python HandLandmarker IMAGE API, CPU delegate, num_hands=1, detection/presence/tracking thresholds 0.5. Use a separate environment so the old TFLite Support/protobuf environment is unchanged. Archive wheels and resolved dependencies before execution. The source version and installed runtime version must agree; execution on exact component bytes establishes a tested pairing, not proof of historical publication intent or a reproducible source build of the wheel.

Predeclare one test image now: the release test's `thumb_up.jpg` from `https://storage.googleapis.com/mediapipe-assets/thumb_up.jpg`. Preserve its bytes and digest. Do not search for another image if it fails to exercise the landmark path; record NO_HAND_PATH_EXERCISED. The fixture is a functional-path witness, not a task-accuracy benchmark.

Four task-bundle conditions:

- original: exact preserved official version-1 .task bundle.
- container_control: deterministic ZIP rewrite with every component payload unchanged.
- metadata_exchange: same rewrite, changing only the preserved Hand component's metadata entries 0/2 using the established four-byte intervention; every other component remains identical.
- restoration: put the original component back using the same writer; require equality to container_control.

Compare every bundle member hash and each component's canonical graph/non-metadata buffers. All variant landmark components must retain the original graph and weights. Save complete returned handedness/landmark/world-landmark values and float bit patterns, or exact failures and earliest stage. Call the actual official Task API; no handwritten inference/decoder replacement. Run primary and one separate same-environment replay. Compare decoded Task outputs across conditions; the public Task API does not expose internal raw TFLite tensors, so these outputs must not be mislabeled raw tensors.

Keep the generic generated path separate: original and exchanged Java are expected from recovered records to fail raw javac, and only the disclosed identical separator repair enabled the old bytecode-binding witness. Verify the files and bytecode rather than treating this as an unmodified supported Hand Java path. Association swapping is not a complete repair of scalar handedness decoding or coordinate representation.

Entry commands:

```bash
PYTHONDONTWRITEBYTECODE=1 /workspace/hand-contract-repro/.venv/bin/python scripts/prepare_hand.py
python scripts/setup_hand_task.py
python scripts/run_hand_task.py --run primary
python scripts/run_hand_task.py --run replay
python scripts/summarize_hand.py
```

If required artifacts/dependencies cannot be preserved, the runtime fails, or no hand is detected, stop the corresponding claim and retain the negative result. Do not change the input, thresholds or generated Hand source to obtain the desired observation.
