# Current-manuscript claim audit

Target: `sources/metadata-contract-paper-revision-20261004T065132Z/manuscript/paper.tex`, SHA-256 `390445a494c24cf9e9069ca3d5ab62e4d0174587f631856b764846d54908782d`.

`claim-map.json` maps 41 grouped factual claims to exact manuscript lines, new evidence paths/digests, observations and limits: **29 matched, 6 source-supported, 1 contradicted generalization, 5 not testable from available historical/full-text evidence, and zero pending**. Definitions, methodological scope and historical events are distinguished from new empirical results. Abstract/conclusion repetitions map to their underlying experiment rows. A matched fresh result does not establish identity with unavailable old raw files.

## Independently verified in this sub-audit

`verify_observations.py` directly rereads new execution/category records, code files and E4/E5 records rather than trusting report prose. Its final `observation-readback.json` has **677 passed checks, zero failed checks, all 16 required Android execution records, and no missing records**. These are software audit checks, not 677 independent experiments. The script exits nonzero for failed checks or incomplete required Android records.

- Linux Task: ten initialized-or-rejected instances across five variants and primary/replay; sixteen successful observations across the two fixed inputs, containing 16,000 category entries. All class indices, float32 bit encodings, controls, complete cyclic permutation and replay results were checked. Deletion rejects at initialization with the exact reported `ValueError`; each permutation changes 999 labels and preserves every score bit.
- Five-condition baseline: all twenty displayer/populator/simple-baseline/Task-initialization records agree with the claimed distinction. Joining exact model digests to the new E5 records confirms zero additional rejections over either comparator.
- Hand Task: all eight actual decoded records contain one hand, 21 landmarks and 21 world landmarks; all decoded values and serialized float-bit files equal the primary original. Other new Hand evidence confirms the pinned source-component bridge, four-byte exchange, fresh raw compilation failures/disclosed repair and isolated decoder boundary.
- E4: all twenty URLs, eighteen occurrences and fifteen model digests were checked. The 16/4 HTTP split, 15 structural acceptances/semantic abstentions, 8/7 raw compilation split, 4/9/2 D split, and five-uncompilable/four-warned decomposition agree.
- E5: all 65 distinct model files were hashed and each combined report compared with its individual check JSON; S 52/11/2 and D 27/8/14/3/2/11 counts match the manuscript. The five actual Android artifact digests were joined to these records; only the deletion is D-incompatible and has an executed getter failure.
- Android: 16 completed phase/variant records across E1/E2 primary/replay cover five byte-distinct artifacts, one graph and 32 input observations. Every prescribed RGB input and every 4,000-byte raw tensor was read back. The 28 successful category lists preserve all 1,000 score bits; the four deletion observations reach the actual generated getter and raise the precise cardinality exception. Permutation changes exactly 999 labels, and restoration returns the baseline. Both exact paper score examples match. The unset category index field is preserved and never substituted for list position.
- Code: all eight fresh E1/E2 generated Java files, their three generated-class files and their complete DEX sets were hashed directly from disk and match across variants. This is within-current-run equality; historical binaries are unavailable.

The second attempted AVD produced four package-installation setup failures before any model execution. Those records remain outside the 16 completed model records and are neither getter failures nor failed inference observations. The completed replay used the stable primary AVD. It is therefore a same-environment replay, not a successful independent second-AVD execution.

The parent audit additionally reran and independently checked the earlier corpus: 35 accepted variants, 11 rejected count controls, 105 CPU observations, 243 output arrays and 23 isolated decoder probes. Those are new observations, not retrieved historical numerical arrays.

## Correction supported by new evidence

Current manuscript line 58 presents label counting as following the library. The actual E5 implementation uses Python `splitlines()`, while Java `FileUtil` uses `BufferedReader.readLine()` and trimming. Their recognized line separators differ. The independently generated real label-only probes demonstrate both directions:

| Label intervention | E5 | Actual pinned FileUtil/TensorLabel |
|---|---|---|
| Replace one LF with vertical tab | 1000 labels, compatible | 999 labels, cardinality exception |
| Insert U+2028 inside first label | 1001 labels, incompatible | 1000 labels, success |

Evidence: `/workspace/repro-audit/independent-audit/label-parser/results.json`. These are synthetic isolated Java-consumer probes; they are not natural defects or Android wrapper executions. They add a real checker limitation beyond the regex/processor limitations already disclosed at line 206. They do not retroactively overturn the ordinary-label results in the original 65-fixture evaluation.

## Historical facts that a new run cannot establish

- The exact E2 transport interruption and separate completion chronology at line 122.
- The historical eight-record/five-configuration/16-observation construction audit, old classes/DEX identities and prior AssetManager records at line 126.
- The information state and timing of the original freeze at line 176. A new freeze repeats a known protocol and is not newly blind validation.
- Historical raw-array equality across separate sessions, complete archive/toolchain identity, initial APK rebuild chronology and historical cumulative-logcat attribution at lines 250–253.

The source-only checkout contains descriptions and scripts, but not those historical raw files. New model bytes can be tied to recorded publisher digests, and new generated code/output arrays can be compared within the current run. Neither operation authenticates missing old outputs. Missing historical evidence is an auditability limitation, not evidence that the underlying behavioral claims are false.

## Literature scope

This turn read the entire current manuscript and bibliography, the preserved `literature/AUDIT_REPORT.md`, the prior claim audit and revision positioning proposal. The manuscript accurately carries forward the reported bounds: MLGuard as a vision, DocTer as documentation-guided constraint testing, ACETest as implementation-derived constraint testing with LLVM/SVF/Z3, DARA as model-derived architecture assessment, Stalnaker abstract-based, and no exhaustive novelty claim.

This sub-audit did **not** newly recover and reread all four full PDFs, verify all publication endpoints, or run the prior tools. The parent task's attempted PDF retrieval remained blocked by proxy CONNECT 403. The preserved literature report is secondary evidence of an earlier inspection. It must not be described as a new full-text literature replication or a proof of novelty.

## Reusable source and remaining limits

`source-export/` contains the two audit scripts, this report, the claim map and a compact verification summary with evidence identities. It excludes model files, arrays, generated Java/classes/DEX, logs, PDFs and dependency binaries. The raw `observation-readback.json` remains in this workspace. Re-running `verify_observations.py` requires the recorded external evidence paths; this source export is not a standalone evidence archive.

The earlier broad corpus was rerun and checked by the parent task, while historical raw identities and claimed historical events remain unverified. Independent human audit, an artifact-tied EfficientNet class-order reference, a fresh full-text literature review and a portable public evidence deposit remain open. None is supplied by the 677 automated checks.

No repository file was changed by this sub-audit. New helper source and reports are outside the checkout for parent review/import under the source-only policy.
