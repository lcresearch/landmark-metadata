# E4/E5 reproduction and audit notes

The source-only repository was treated as read-only. All new models, Java classes,
check outputs and failure-injection data are under `/workspace/repro-external`.
The original E4 and E5 checker sources are byte-preserved; `source-provenance.json`
records their hashes.

## E4 repeated experiment

A new local freeze (`f92b2ffb32d48197b2c155d829f2acff79a67724`) was created before
this repeat's E4 downloads. The historical published results were already known;
this is a repeat, not a fresh blind validation or a recreated historical
preregistration. `E4/protocol/REPLAY_CONTEXT.json` records this distinction.
`run_e4.py` changes only download concurrency from four to at most two; frozen
checker logic is unchanged.

All 20 original candidate URLs were attempted without substitution. Sixteen
returned 200, four returned 404. The 18 component occurrences yielded 15 checked
canonical groups, one excluded prior component and two excluded prior graphs.
All 15 passed official structural population; Java compiled for eight and failed
for seven. Decoder checks reported four compatible paths, nine incompatible
paths and two inapplicable paths. All 15 semantic checks abstained. The included
candidate digest prefixes match every row of the historical published table;
the prior-exclusion full digest and canonical-graph sets match the freshly
recovered 13-component base suite. All frozen source hashes remained unchanged.
See `E4/results.json`, `E4/summary.json` and `E4/replay-comparison.json`.

These are static original-only observations. The five incompatible detector
wrappers fail Java compilation; four incompatible segmentation wrappers compile
with an explicit unsupported non-RGB fallback warning. No supported external
end-to-end natural failure or independent semantic error is established.

## Confirmed audit issue: reports can invent outcomes from absent evidence

The unchanged `scripts/summarize_e4.py` was given 20 synthetic failed download
records and zero model components. It exited 0 and still said that one prior
component and two prior graphs were excluded, five detector wrappers failed
compilation and four segmentation wrappers compiled. Its generated JSON counters
correctly said zero downloads/components, contradicting its Markdown report.
Relevant original lines: `summarize_e4.py:17`, `:21`, `:23`.

The unchanged `scripts/summarize_e5.py` was given an empty fixture list. It exited
0, wrote `known_getter_failure_flagged: true`, and claimed 52 accepted fixtures,
65 semantic abstentions and detection of the actual EfficientNet getter failure.
The true flag comes from `all([])`; the narrative counts and conclusions are
literal strings. Relevant original lines: `summarize_e5.py:19`, `:25`.

Both probes are synthetic controller tests, not experimental model evidence.
Inputs, unchanged scripts, outputs and assertions are retained in
`failure-injection/`; `failure-injection/audit-result.json` is the compact record.
The required fix in a separate coding task is to derive every report claim from
validated records, represent missing evidence explicitly, reject incomplete
required datasets, and require a nonempty failure set before claiming all known
failures were detected. Historical snapshots must remain preserved.

## E5 execution method

`run_e5_incremental.py` uses the unchanged historical `preflight.check()` on real
recovered files. It catalogs and deduplicates artifact bytes from the base suite,
E4 and freshly reconstructed core Task conditions. It reuses completed outputs only after verifying
their model digest; it adds actual Android outcomes only from new run records.
Its summary uses observed counts and leaves failure-detection unknown when no
actual failing Android outcome has been supplied. This new orchestration is
explicitly distinct from the original monolithic fixture controller.

The completed E5 run executed 65 real byte-distinct fixtures (48 prior/control,
15 external and two additional core conditions): S accepted 52, rejected 11,
and abstained on two without metadata; D reported 27 incompatible, eight
compatible, 14 inapplicable, three dynamic abstentions, two no-metadata
abstentions, and 11 not reached. There were zero controller errors and all 65
semantic judgments abstained. Every aggregate matches the historical report.
The E4-to-E5 comparison agrees on all 15 included external groups.

The two additional core conditions use actual reconstructed model files from
`/workspace/repro-task/models`, generated with the original mutation rules and
already executed through Linux Task. Aliases explicitly identify this source.
All formally prepared E1/E2 model files match the corresponding core model
hashes. The five core conditions reproduce zero additional E5 rejections over
the simple baseline and Task initialization: all three reject only label
deletion. See `E5/core-baseline-comparison.json`. The separately completed Android E1/E2 primary and replay summaries now link
five exact artifact conditions: four successful getters and one failing getter.
E5 flags the actual failing condition and incorrectly rejects none of the four
successful conditions. `E5/android-linkage-validation.json` verifies that all
65 existing static reports and all 481 static evidence files were preserved
byte-for-byte during this association refresh.

Four separate real-fixture CLI invocations confirmed exit 2 for structural or
decoder rejection, and exit 0 for compatible-with-semantic-abstention and
missing-metadata-abstention cases. Thus exit 0 does not establish all-dimension
acceptance. See `E5/cli-probe-results.json`.

The shared support environment matches all 11 packages in the frozen lockfile.
Python is 3.11.16; the Java compiler/runtime is Temurin 17.0.12+7, with `--release
8` used by the original controller. See `runtime-environment.json`.

A second synthetic E5 summarizer probe exercises the protocol's dynamic-output
abstention branch: `frozen_D=ABSTAIN_DYNAMIC_OUTPUT` and new `D=ABSTAIN`. Line 13
maps every non-list frozen outcome to `INAPPLICABLE_NO_SELECTED_GETTER`, so the
summary incorrectly calls this a disagreement. The retained evidence is
`failure-injection-dynamic/audit-result.json`. This branch was not encountered
in the current 15 external groups and does not alter their observed agreement.

## Reuse the Android association refresh

The completed association refresh added actual E1/E2 observations and formal
aliases without rerunning the 65 static checks. For another unsealed working
replay with finalized Android results, the command is:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 \
/workspace/hand-contract-repro/.venv/bin/python \
/workspace/repro-external/run_e5_incremental.py --include-core \
--core-models /workspace/repro-task/models
```

This command requires formal E1 and E2 variant directories. If the model bytes
differ, it retains them as additional distinct fixtures instead of silently
merging them. Actual Android outcomes are read only from the new results files.
