# Toolchain and dependency inventory

This handoff records the toolchain needed for EfficientNet E1/E2, the same-Android
P2 comparison, and P3 reference analysis/readback. It does not install or execute
that toolchain. [toolchain.json](toolchain.json) separates **recorded versions**,
**fresh local file hash comparisons**, **existence-only checks**, and **unknowns**.
Every underlying version log/lock is identified there by path and SHA-256. Binary
inputs and tools remain outside Git. Public acquisition URLs were not tested again
in this handoff.

## Exact versions and supported scope

| Item | Recorded value | Source and qualification |
|---|---|---|
| Python used by original audit and P2/P3 | CPython 3.11.16; P2/P3 full string `3.11.16 (main, Sep 24 2026, 17:56:40) [Clang 22.1.3 ]` | Historical `rebuild/versions/python.stdout` and P2/P3 version fields; interpreter was not launched now |
| Recorded host | Linux 6.18.44, x86_64, glibc 2.41 | P2/P3 logs; this is a recorded environment, not a claim that every future host must have this kernel |
| Metadata reader / model code generator | Python `tflite-support==0.4.4` | Original 11-package source lock and P2 package log |
| Schema reconstruction dependencies | `numpy==1.26.4`, `flatbuffers==25.12.19`, `protobuf==3.20.3` | Lock; P2 log directly reports NumPy/FlatBuffers. Full lock linked below |
| Host CPU interpreter | `tflite-runtime==2.14.0` | Python lock; separate from Android wrapper runtime |
| Generated Android wrapper libraries | Support/API/metadata 0.4.4; TFLite Java API and native JNI 2.13.0 | Explicit classpath and JNI hashes in P2 `resolved-lock.json`; E1/E2 build sources |
| Android Task API | `tensorflow-lite-task-vision:0.4.4`, `tensorflow-lite-task-base:0.4.4` | Maven acquisition and extracted Java/native digests |
| Task's embedded native interpreter | **UNKNOWN** | The pinned Task `.so` does not establish equality with standalone TFLite 2.13.0 |
| JDK / Java target | Temurin 17.0.12+7; `javac --release 8` | Logs plus both build scripts |
| Android platform / manifest | API 30, platform r3; min SDK 23 / target SDK 30; x86_64 ABI | SDK archive metadata and build sources |
| Android build tools | 35.0.0; aapt2 `2.19-11948202`; D8 `8.6.2-dev`, build `abaab469b5ebd4dd2bb91ba0ed6f45277faae4ca` | P2 version log |
| ADB / platform tools | ADB 1.0.41, platform-tools 37.0.1-15733141 | P2 version log |
| Emulator | 37.2.12.0, build 16428233 | P2 and original version logs |
| System image | API-30 default x86_64, download `x86_64-30_r11.zip`; internal `Pkg.Revision=10` | The r11/r10 packaging discrepancy is documented; original download and reconstruction lock record the same archive digest |

E1/E2 and the generated-wrapper side of P2 compile the EfficientNet generated
`ContractModel.java` without source repair. The separate Hand separator repair
is not a prerequisite for this focal route. Android Studio/Gradle is not part of
these recorded builds: Java compilation, D8, aapt2, zipalign and apksigner are
called directly. P2 used two APK consumers; this is not a claim of one shared
native runtime or an Android Studio build reproduction.

## Acquisition and byte identities

The [Android prerequisite lock](../../sources/repro-audit-20261004/android/android-prerequisites.lock.json)
contains official URLs and SHA-256 for **five SDK archives, one JDK archive and
11 Java archives**, plus extracted Java-class digests. The
[restorer](../../sources/repro-audit-20261004/android/restore_prerequisites.py)
checks these expected bytes; it does not recover models or Python. Do not run its
restore or `--verify-cache` mode against preserved evidence: even verify mode
writes an integrity report.

The following are the main archive identities; the linked lock and JSON contain
all dependency identities rather than truncating hashes in commands.

| Archive | SHA-256 |
|---|---|
| Temurin `OpenJDK17U-jdk_x64_linux_hotspot_17.0.12_7.tar.gz` | `9d4dd339bf7e6a9dcba8347661603b74c61ab2a5083ae67bf76da6285da8a778` |
| Android API-30 `platform-30_r03.zip` | `f3f5b75744dbf6ee6ed3e8174a71e513bfee502d0bc3463ea97e517bff68d84e` |
| `build-tools_r35_linux.zip` | `bd3a4966912eb8b30ed0d00b0cda6b6543b949d5ffe00bea54c04c81e1561d88` |
| `platform-tools_r37.0.1-linux.zip` | `d230f13842f60f782a8645f9c813f8f845bf36089ea7289f28c48f17979313f1` |
| `emulator-linux_x64-16428233.zip` | `b08fc43d8608d2955f607f1b287beb525041e730086bdca3af152accac3af9c1` |
| `x86_64-30_r11.zip` | `8d591034a4244a920d7a3ec274bb1734dd6474a3d8c11d0fce902010db3a13aa` |
| Task Vision 0.4.4 AAR | `5b7a55269d0a21febab9aa5f41746269d938ff91924173330460c2d251d5b9ce` |
| Task Base 0.4.4 AAR | `8b1599db15d3fa7a58f687cee38600f8cce175b86896dcbc0042d31eeb145e5f` |

The Android reconstruction lock **does not include Task Vision/Base**. P2's
[fetch source](../../research/20261004-p2-p3/P2/scripts/fetch_dependencies.py)
and [explicit dependency selection](../../research/20261004-p2-p3/P2/dependencies/resolved-lock.json)
identify these additions. `toolchain.json` adds their exact acquisition URLs,
AAR/POM digests, extracted `classes.jar` and x86_64 native-library hashes from the
available old download records. The original fetcher records newly downloaded
hashes but does not compare them to an independently supplied expected lock;
validate against the recorded expected identities before interpreting a replay.
It is not a general Maven resolver. AndroidX annotation 1.3.0 was selected although
an upstream provided declaration names 1.1.0; the selected classpath is the tested
configuration.

The [Python lock](../../sources/hand-contract-repro/requirements.lock) has 11
exact version pins. The existing original wheel index supplies filenames and
SHA-256 for all 11 wheels, now indexed in `toolchain.json`. Exact historical wheel
download URLs and the CPython distribution archive digest are not established by
that index. Resolve those versions through the configured package source, verify
the selected wheel identities, and retain retrieval provenance in a new external
run. Version equality alone does not prove wheel equality. The original audit's
`python -m pip freeze` capture failed with `No module named pip`; the lock,
recorded package observations and wheel index are distinct evidence, not a
successful pip-freeze record. The helper uses `uv` to install the source lock;
this inventory does not establish an exact `uv` binary version/hash.

## Original records versus fresh reconstruction

- The original E1/E2 audit and P2 used an already installed pinned JDK/SDK/Python
  setup, with new build/run directories and AVDs. Those historical records are
  not a toolchain-from-archive installation.
- The later [cloud reconstruction report](../../sources/repro-audit-20261004/REPORT.md)
  reports fresh public-prerequisite recovery and actual E1/E2 runs under
  `/workspace/repro-*`. Those reconstruction roots are absent at the locations
  checked in this handoff; this turn does not authenticate those excluded raw
  outputs or rerun installation.
- Original historical tool/archive directories are present on this host. Their
  selected archive/dependency bytes were compared with recorded hashes for this
  inventory. This does not certify every installed SDK member, live process,
  complete evidence package, or ability to run another build. All checks retain
  their exact scope in the JSON.

## Host and path prerequisites

The recorded emulator uses software execution (`-accel off`), SwiftShader, two
virtual cores and 2 GiB guest RAM, with a 2 GiB guest data partition. This is a
configuration, not a measured minimum host-memory/disk requirement. The active
host needs adequate additional space for expanded SDKs, model variants, builds
and logs; the project has not measured a portable minimum. The recorded readiness
deadline is 900 seconds. Require functional package/activity services, not only
`sys.boot_completed`. Check for port 5554 conflicts and a writable Android user
configuration directory before creating task-owned processes. Do not change
`HOME` or overwrite an existing `~/.android`.

The imported scripts intentionally retain paths and imports:

- `common.py`: `/workspace/hand-contract-repro/.venv/bin/python` and
  `/workspace/hand-contract-repro/toolchains/jdk-17.0.12+7`.
- E1/E2 preparation: `/workspace/metadata-contract-paper/scripts` and its
  previously constructed `runs/6c7ab0a6e5dc/` models.
- P2 preparation/build: `INPUTS.json` model paths, that same corpus import,
  `/workspace/hand-contract-repro/deps`, and original E1/E2 extra jars/native files.
- P3 analysis: original E1/E2 model paths and its archived retrieval bodies;
  `flatbuffers`, NumPy and the Support schema package are required for full graph
  reconstruction. The limited stored-result readback is a different operation.

Use source copies in fresh external roots for any future execution. Do not run
historical `commands.sh` or builders in `sources/`, `research/`, or sealed old
roots: they write outputs relative to their script directories. The
[base preparation instructions](../../sources/repro-audit-20261004/base/REPRODUCE.md)
and [Android instructions](../../sources/repro-audit-20261004/android/REPRODUCE.md)
describe historical prerequisites and adapters. `--copy-only` validates copying,
not Python installation or model execution. These scripts have not been made
universally relocatable by this inventory.
