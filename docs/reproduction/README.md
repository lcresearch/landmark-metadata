# Reproduction entry point

This handoff identifies the study's inputs, toolchains, commands and remaining
gaps. **The Git repository contains source and documentation, not a complete
experiment deposit.** Start with the route that matches the materials available
to you; reading saved results and running a new experiment are different tasks.

The original handoff's inspected starting revision was
`052a839cdc64ec43ce362dde0cd3e410926e107d` (after PRs #6 and #7).
The [21 October verifier repairs](../../work/review-fixes-20261021/README.md)
update maintained readback and setup entry points without changing the manuscript,
historical sources or experiment outcomes. Dated validation records below retain
their original scope. All paths below are relative to the repository unless explicitly
absolute. Run command examples from the repository root.

| Route | What you need | Status in this handoff | What it establishes |
|---|---|---|---|
| Check the source checkout | Git checkout, Python 3, Bash | Source checks and regression commands listed in [Commands](COMMANDS.md) | Source integrity, syntax, links and synthetic verifier behavior; no inference |
| Read selected original E1/E2/P2/P3 records | The original external result/input files | Maintained bounded reader executed into a new external directory | Consistency of the selected saved bytes and recorded observations; not a new build, inference or complete preservation audit |
| Read the later reconstructed corpus | Separate `/workspace/repro-*` results and frozen E5 manifest | Required external result roots are missing at their recorded locations; CLI inspection alone is available | Nothing about those missing executions is revalidated by this handoff |
| Rebuild and rerun E1/E2, then P2 | Exact models, generator/runtime dependencies, JDK, Android SDK/image, harness and reviewed output layout | Historical procedures documented; no fresh installation, compilation, emulator or inference in this task | Only a future successful run could establish fresh execution; saved commands do not |
| Recompute the qualified P3 reference | Exact focal/bridge models, publisher cards, label file and provenance | Selected inputs inventoried; full bridge analysis not rerun here | Display-order agreement only at the declared reference scope, not image prediction accuracy |

## Choose an entry

- [Inputs and availability](INPUTS.md), with [machine-readable inventory](inputs.json):
  model identity, synthetic inputs, reference objects, historical evidence and
  acquisition gaps.
- [Toolchain and versions](TOOLCHAIN.md), with [machine-readable inventory](toolchain.json):
  separate original and reconstruction configurations; hashes and where each
  version claim comes from.
- [Commands and expected outcomes](COMMANDS.md): safe source checks, bounded
  readback, prerequisite ordering and historical execution commands.
- [External deposit plan](DEPOSIT_PLAN.md): material required for an independently
  usable handoff, plus the parts that have not been deposited or verified.
- [Verification record](validation.json): exact commands checked in this task,
  script/log digests and the limits of the checks.
- [Maintained P2/parser readers and setup repairs](../../work/review-fixes-20261021/README.md):
  separate coverage, identity and outcome checks, with synthetic negative regressions.

## Minimal checks requiring no model or SDK

```sh
PYTHONDONTWRITEBYTECODE=1 python scripts/check_source_tree.py
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -v
```

The source checker reports historical unavailable locators and unchecked external
archive digests as warnings. These warnings are not silently converted into
verified evidence. The tests use synthetic records; they do not certify the
excluded experimental results.

If you have recovered the original files at the paths in [Inputs](INPUTS.md),
the maintained finite reader can be run without TensorFlow or Android:

```sh
PYTHONDONTWRITEBYTECODE=1 python \
  research/20261004-significance-review/scripts/read_existing_outcomes.py \
  --output-dir /path/outside/repository/new-readback
```

Supply `--e2e-root` and `--p2p3-root` for relocated original packages. The output
directory must not already exist. Inspect the emitted comparison booleans:
zero exit means the report was produced, not that every comparison passed. This
reader covers selected primary records; it does not replace the full maintained
reconstruction reader or independently recompute P3's model/reference bridge.

## How to interpret status and hashes

**Verified in this handoff** means the stated command or byte comparison was
performed now. **Recorded historically** means a source/report documents it but
it was not repeated here. **Inspected only** means its source or CLI was checked.
**Missing** means a specific required local path was checked and absent;
**not checked** is not the same conclusion. Public retrieval endpoints are
documented, but their current responses were not tested in this task.

A locally present file is not a portable download or durable archive. A freshly
computed SHA-256 identifies the bytes read; matching a previously recorded hash
checks identity, not the truth of the experimental conclusion. A manifest-file
hash check does not validate all files named by that manifest. Never derive the
expected frozen manifest digest from the candidate run being validated.

Do not execute historical `commands.sh`, setup, install or seal scripts against
saved evidence. Several commands use fixed absolute paths, have import-time
writes, or assume generated configuration omitted from Git. A fresh execution
needs new external roots and a reviewed path plan before those commands become
safe to run. Do not upgrade dependencies or substitute model bytes merely to
make a run finish.

Keep S, I and D separate, with P as intervention preservation. Preserve failures
and stages not reached. Human verification, a portable external deposit and a
fresh-machine restoration remain separate from this documentation task.
