# Fresh output / AVD build audit of E1 and E2

Scope: regenerate all 4 E1 and 4 E2 variants from archived original bytes, compile unmodified generated Java, build new APKs and execute actual generated APIs on two previously declared inputs. Existing installed Python/JDK/SDK are reused read-only; this is not a clean SDK installation, independent human reproduction, or a new external sample. All writes are under this rebuild root. Old evidence is sealed.

Two disclosed changes to copied harness/orchestration: before generated newInstance, hash bytes read through AssetManager from the exact same asset name and Context; require E1 fresh primary completion, not an additional same-APK replay, before preparing E2. Patches are saved. No decoder or generated-source change. The asset read proves byte identity at this audit point; generated newInstance's own file-loading implementation is inspected separately rather than intercepted or replaced.

Preservation comparisons: whole original model identity; canonical graph and every nonmetadata buffer; metadata bytes and pre-ZIP prefix; associated filenames/payloads; original/restoration contents; generated source and generated class bytes vs each other and historical evidence; DEX equality within this audit only because harness changes; APK assets/model.tflite vs workspace and runtime AssetManager hash; complete raw tensor bytes and all decoded score bits; top-k indices and labels; generated getter exception and earliest stage. No whole-APK equality criterion. Exception is caught by harness, not application crash.

Planned commands (expanded subprocess argument vectors logged by common.run):

```bash
cd /workspace/metadata-contract-audit-20261004T062010Z/rebuild
python3 setup.py
PYTHONDONTWRITEBYTECODE=1 /workspace/hand-contract-repro/.venv/bin/python scripts/prepare_e1.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/start_emulator.py
PYTHONDONTWRITEBYTECODE=1 /workspace/hand-contract-repro/.venv/bin/python scripts/build_android.py --experiment E1
PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_android.py --experiment E1 --run primary
PYTHONDONTWRITEBYTECODE=1 /workspace/hand-contract-repro/.venv/bin/python scripts/prepare_e2.py
PYTHONDONTWRITEBYTECODE=1 /workspace/hand-contract-repro/.venv/bin/python scripts/build_android.py --experiment E2
PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_android.py --experiment E2 --run primary
sdk/platform-tools/adb -s emulator-5554 emu kill
```

Start emulator and build independent work concurrently after E1 preparation. Do not assume expected outcomes; record build/runtime failure, timeout or missing evidence. No version changes to seek the expected result. Compare observations from fresh artifacts and preserve all failures.
