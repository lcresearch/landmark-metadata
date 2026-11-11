# Current focal experiment

Start with the [runbook](RUNBOOK.md). This is the maintained source path for
E1/E2, the paired Android P2 comparison and the six-reference P3 core. The
[November results](../work/focal-rerun-20261110/RESULTS.md) remain the executed
record; this source-layout revision does not rerun inference or change results.

| Area | Responsibility |
|---|---|
| [inputs](inputs/README.md) | Recover the five pinned model conditions, two RGB inputs and six reference bodies outside Git |
| [run](run/) | Initialize, record environment, collect/resume stages, compare P3 and package evidence |
| [android](android/) | Selected E1/E2 harness, producer, build, collector and independent audits |
| [p2](p2/) | Paired wrapper/Task harnesses, producer, build, collection and normalization |
| [shared](shared/) | One identical subprocess/logging helper staged for both consumers |
| [model](model/) | Shared model parsing/mutation helpers and one code-generation helper |
| [toolchain](toolchain/) | Fixed SDK/JDK/Java prerequisite restore and dependency locks |
| [source-map.json](source-map.json) | Exact source-to-external-run mapping; 27 destinations, 24 distinct source files |

`initialize.py` reads the input/reference pins, stages only the listed producers,
and calls the [Android adapter](../scripts/initialize_android_run.py). The
adapter retains its local-input provenance, functional-readiness and port guards.
Historical producers retain their bytes; external copies receive the same recorded
absolute-path adaptations. Model helper modules remain whole files to preserve
behavior; this is a file-level dependency selection, not a claim that every helper
function is exercised. Run the producers in their staged external layout, not
straight from `experiment/android`, `p2` or `model`.

The previous initializer copied complete Hand/corpus and E1/E2 source suites.
It now stages no Hand campaign, E4/E5 checker, historical report writer or sealing
script. The identical generator and subprocess/logging helper are each stored once and
staged where each consumer needs them. Their runtime paths and bytes stay the same.

P2 evidence readback remains at
[verify_p2_records.py](../work/review-fixes-20261021/verify_p2_records.py).
Other saved-evidence readers and their trusted parser sources are described in
[support](../support/README.md); they are not extra steps of the focal experiment.

Source-copy tests cover the complete staged inventory, local module imports,
producer-byte equality, absent inputs and occupied destinations. SDK installation,
Android builds/inference and full scientific reproducibility were not repeated for
this layout change. Use a fresh external root for any future run. Historical
execution hashes and the manuscript's human PENDING statuses stay unchanged.
