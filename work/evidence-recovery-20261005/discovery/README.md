# Discovery command snapshots

These two first-party scripts preserve the code used for the bounded search and
independent scope inventory in this task. They read saved inputs and write new
reports under a fixed external recovery root. **Do not run these snapshots in
place:** they use fixed output names and can overwrite this task's reports.

- `search_local.py`: bounded filename/hash/archive-member search. Subsequent
  text-search and summarized findings are recorded in external JSON reports.
- `build_scope_inventory.py`: independent proposed focal selection, exclusions
  and historical-manifest path coverage; this alone does not hash every entry.

To repeat discovery, review the code, copy it to a new task directory and change
its output root before execution; preserve the old reports. Use the maintained
stager/verification commands in the parent entry for package operations. Neither
snapshot executes models or establishes independent human verification.
