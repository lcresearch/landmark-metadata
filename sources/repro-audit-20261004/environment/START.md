Use the existing checkout at `/workspace/landmark-metadata`; do not create a Git
worktree unless explicitly requested. Read AGENTS.md, MEMORY.md, TODO.md,
docs/DECISIONS.md and README.md, then the fresh report at
`sources/repro-audit-20261004/REPORT.md`. The fresh source is on
`audit/fresh-reproduction-20261004` / PR #1 until merged. Do not reset the branch
or overwrite historical imported snapshots.

Run `python scripts/check_source_tree.py` from the repository. Python 3, Bash,
rg, Git, uv, pdflatex, pdftotext, pdftoppm and pdfinfo are installed and tested.
This check validates source integrity/syntax, not model results.

The saved install script refreshes retained dependencies and verifies pinned
archive caches. It was executed successfully in this machine; it is not a
claim that an empty machine or future snapshot has been restored. Retained
CPython is `/workspace/repro-control/python/cpython-3.11.16-linux-x86_64-gnu/bin/python3.11`.
Use `/workspace/hand-contract-repro/.venv/bin/python` for Support 0.4.4 / runtime
2.14.0 and `/workspace/repro-hand/.venv/bin/python` for MediaPipe 0.10.14 Hand
Task. Keep the venv executable path; resolving its symlink bypasses the venv.
The two environments have different protobuf versions and must remain separate.
The exact JDK is `/workspace/hand-contract-repro/toolchains/jdk-17.0.12+7`;
Android SDK is `/workspace/repro-android/sdk`. Do not upgrade these versions to
make a result pass. Source locks and checks are under the fresh `base/`,
`android/` and `hand/` areas.

Standard startup does not rerun model experiments or require a service. Build
the current paper outside Git: create a fresh directory with
`mktemp -d /workspace/landmark-paper.XXXXXX`, create its `manuscript/` directory,
copy the current revision's `manuscript/paper.tex` there and its `build.sh` to
the directory root, then run that build script. Check exit status and
`paper-pdfinfo.txt`. The audited unchanged draft has eight pages; it still needs
the label-count limitation correction documented in TODO.md.

Run expensive experiments only when requested. Start from the source area's
REPRODUCE.md instructions; use new external evidence roots and explicit output
paths. Existing results under `/workspace/repro-*`, `/workspace/metadata-contract-paper`
and `/workspace/hand-contract-repro` are retained evidence, not scratch output.
Never run sealing/finalization scripts against them. Missing prerequisites must
fail explicitly rather than becoming a skipped success. Keep Python assertions
enabled when running preserved scripts. Inspect S/I/D, completeness, raw files
and strict-check results rather than relying on exit zero or old fixed prose.

Processes do not survive environment snapshots. Before Android work, check for
existing task-owned emulator processes and avoid port conflicts; do not assume
the prior AVD is running. The tested path uses API 30 x86_64, software emulation
without KVM, one active emulator and a readiness deadline of 900 seconds. Boot
can take about nine minutes. Use the fresh initialize/start helpers and
`check_android_ready.py` to require boot completion, real package/activity
services and repeated stable system_server observations. The second concurrent
AVD failed before model loading; do not count its install failures as model
failures. ADB 37 needs a writable `~/.android`; this snapshot has the scoped
symlink to `/workspace/repro-android/android-user`. Do not overwrite an existing
user directory or change HOME. Stop only emulator processes created by this
workflow, using the recorded PID after verifying its command.

Required custom network domains have been saved in the draft. Official model,
GitHub and dependency downloads were tested. Fresh arXiv/Crossref/publisher
full-text retrieval still received proxy CONNECT 403; a saved domain does not
establish applied network access. Preserve that limitation and do not disable
TLS verification or bypass the proxy.

Keep models, SDKs, dependencies, generated wrappers/APKs, raw tensors/results,
logs, keys and rendered papers outside Git. End with source checks and
`git status --short`; preserve negative/partial attempts. Automated reruns do
not complete independent human review. Review/save/publish the environment
configuration separately; saved draft instructions alone do not publish it.
