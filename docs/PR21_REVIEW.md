# PR #21 follow-up review

The first published head (`3c3a7758537a7d2a97cc50534439b6deddb82459`) was not ready
to integrate with the newly published paper PR. Review reproduced these issues:

1. The documented `python3 scripts/check_source_tree.py` command imported the
   archive helper before suppressing bytecode. On a clean checkout it created
   `archive/__pycache__/catalog.cpython-313.pyc` and then rejected its own output.
   Tests had used `PYTHONDONTWRITEBYTECODE=1`, hiding this entry-point regression.
2. PR #22's `recheck_core.py` still read the old Android audit/P3 paths, and its
   `index_evidence.py` assumed the old packaging script and all ledger sources
   were present as physical files. The source cleanup removed those paths.
3. Navigation checking skipped missing local links when the target had an
   archived blob. Byte preservation does not make a local hyperlink usable.

The checker now disables bytecode before local imports, fails on dead current
links, and reports archived historical locators with their fixed Git URLs.
A missing memory-bound import yields a structured failure rather than a traceback.
Regressions cover the ordinary CLI twice with no bytecode environment override,
dead current links to archived paths, and the missing memory source.

PR #21 is stacked on paper PR #22 at
`481f62dff5b0d947621330dfd85866e50cd7d802`. Only the feature branch receives a
content-preserving integration plus these compatibility fixes; neither PR is
merged into main. Integrate #22 before #21, checking the then-current reviewed
heads. No force push or default-branch write is used.

The paper readback now uses the promoted, still byte-pinned audit sources and
current P3 path. Indexing resolves removed source bytes from the verified Git
archive, records `archived_git_object` rather than `working_tree`, and retains
exact older-Git fallback for changed historical documents. The committed paper,
claim map, handoff, evidence index and all 13 current/historical artifact pins are
unchanged from #22. The original executed versions of the two adapted drivers
remain available at the fixed #22 head above; no old source pin is refreshed.

## Validation and limits

- The complete regression suite passes, including ordinary-command, archive,
  staging, parser/P2, and paper-index tests. All 193 tests pass.
- The ordinary source checker passes and validates 354 imports, 280 archived
  source paths and 13 manuscript/evidence pins. It reports the original twelve
  warnings plus six explicitly archived historical source locators in a clean
  clone (five files and one now-empty directory). The old working directory
  retained that empty directory; it is absent from Git checkouts. Archived file
  targets were silently skipped by the earlier version.
- Actual saved-byte core readback passes for Android/model preservation, all
  348 P2 checks and the six-input P3 core. All ten receipt-pinned original records
  still match after readback. No Android inference, build or JVM probe is run.
- Rebuilding a new external evidence index reads the same 1,036 selected members.
  Every member's path/size/hash/group matches the original committed index.
  The 48 historical sources resolve as 36 working-tree files, eight archived Git
  blobs and four exact earlier Git versions; these are storage classifications,
  not new model observations or human verification.

New local review outputs are `/tmp/pr21-review-core-readback/`,
`/tmp/pr21-review-evidence-index.json` and `/tmp/pr21-review-tests.log`.
Existing raw evidence, the committed index and the paper branch remain unchanged.
The 3.32 GB evidence archive was not re-read during this follow-up; its previously
verified, receipt-pinned manifest was reused for selected live-file checks.
