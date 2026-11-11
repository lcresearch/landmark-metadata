# Historical source archive

The complete pre-cleanup tree is retained at immutable commit
[`e9da459f6043684cdecba913c9c711433371909d`](https://github.com/lcresearch/landmark-metadata/tree/e9da459f6043684cdecba913c9c711433371909d).
It is an ancestor of this cleanup, not an unpushed branch, generated ZIP, Release
or LFS object. Original source bytes, paths, negative results and older manuscript
versions remain accessible there. Git history was not rewritten.

[manifest.json](manifest.json) lists every removed path, its original SHA-256 and
size, and its current replacement where applicable. The archive checker reads the
actual blobs from that fixed tree, checks all recorded bytes and rejects omitted
removals. A replacement is a maintained working source, not a claim that subsequent
edits change the historical execution. Unchanged focal producers are also compared
byte-for-byte against the old tree by regression tests.

```sh
# Verify all archived source bytes; requires the fixed commit in local Git history.
python3 archive/catalog.py
# Restore the COMPLETE old source layout to an absent external directory.
python3 archive/catalog.py --restore /tmp/landmark-historical-source
```

Use a full clone. A shallow clone or downloaded working-tree ZIP may omit the
historical objects; verification fails explicitly rather than claiming success.
If needed, obtain the commit using `git fetch origin e9da459f6043684cdecba913c9c711433371909d`.
Restoration does not run any historical script. Its original absolute `/workspace`
paths and unavailable external prerequisites still require separate handling.

Current source is under [experiment](../experiment/README.md). Historical reports,
input inventories, import indexes and manuscript lineage stay as text references
at their existing paths to preserve their pinned identities. Read their original
complete directory context in the archived tree. Three older source files linked
directly by the pinned October manuscript handoff/crosswalk remain locally present;
they are reference dependencies, not additional current experiment entry points.

This is a **source archive only**. No models, raw outputs, SDKs, emulator state or
evidence archives were moved, uploaded or deleted. Git source restoration does not
recover the missing October execution evidence or back up the new external run.
