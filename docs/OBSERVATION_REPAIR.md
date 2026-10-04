# Observation-reader and manuscript correction

The review of main commit `1edadb1ae0d49df63fdc941cbe315db9f5facff9`
confirmed two remaining completeness gaps with synthetic evidence. A 65-fixture
E5 catalog could replace a non-core artifact while retaining the aggregate
outcomes and self-consistent reports. Task results with empty or contradictory
input observations could still be counted as successful if decoded files remained.
These were reader counterexamples, not a finding that historical model results
were incorrect.

## Maintained reader

The [maintained entry point](../work/observation-review-20261004/verify_observations.py)
now requires a digest-pinned original E5 manifest before accepting the observed
fixture set. The default digest comes from the preserved claim C32 catalog;
an alternate manifest must be supplied with its independently established digest.
The expected set must not be generated from the run being checked. The existing
fixture-validation helper provides the identity checks without model execution.

Task validation uses the fields written by the actual preserved worker and
runner. Successful configurations require `gray127` and `rgb_pattern` exactly
once, successful input preparation and public `classify` return, matching category
counts, and the prescribed RGB bytes with matching recorded hashes. Output
score, index, label and replay comparisons remain in place. `classify` is still
one observed public call; this does not introduce separately instrumented Task
inference or decoding stages.

Missing requirements or contradictory observations prevent successful readback.
Reports continue to use a new output directory and never replace existing reports.
The exported original reader, source hashes and historical 677-check result stay
unchanged; the new regressions do not retroactively certify that old execution.

## Manuscript

The [current working draft](../work/review-followup-20261004/manuscript/paper.tex)
removes the overbroad library-equivalent label-count claim. It discloses the
vertical-tab and U+2028 counterexamples and separates the corrected valid-UTF-8
reader and malformed-input abstention from the historical 65-fixture evaluation.
The counterexamples exercise pinned FileUtil/TensorLabel on synthetic scores
and Task initialization; they are not new Android wrapper inference results.

P2's same-Android comparison and P3's qualified display-order reference remain
intact. The preserved parent manuscript and all imported evidence sources are
unchanged. The current-source digest is refreshed in the manuscript index.

## Validation scope

Run the source check and repository regressions with:

```sh
PYTHONDONTWRITEBYTECODE=1 python scripts/check_source_tree.py
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -v
```

New cases exercise the original false-pass conditions, missing and duplicate
identities, hash/status/count disagreement, and complete reordered evidence.
They use temporary synthetic files and do not execute models. The source check
also verifies preserved import bytes and current/parent manuscript hashes.
The paper is built in a separate directory; build products remain outside Git.

Validation completed for this repair: all 40 repository tests pass, including
the 11 new readback regressions. Source/navigation checks pass; all 354 imported
files and five historical claim-export hashes remain unchanged. Two LaTeX passes
produce a ten-page generic reading draft without overfull boxes or undefined
references; the changed pages were visually checked by an agent. This is not a
venue-specific page-fit or human-review result.

The new reconstruction's raw `/workspace/repro-*` evidence is unavailable in
this checkout. No complete fresh model readback or human audit is claimed by
this repair, and the historical 65-fixture outcomes are not recomputed here.
