# Authorized squash integration of PRs 10–14

The user explicitly authorized **“ok. squash and merge”** after the scoped
[stack review](../pr10-14-review-20261008/README.md). This continuation record
supersedes that review's then-current authorization/open-state notes without
rewriting its frozen identities or conclusions.

## Verified predecessor merges

| PR | Reviewed original head | Verified squash commit |
|---|---|---|
| #10 | `72ff55041be97ba04e377fa9c4a18b948b8dc106` | `dec99facec2122350bc4022aac70fab4f872467b` |
| #11 | `e23d62e3af56376eb0f1946dd30eb7cba870fa04` | `6e3185068eb8c0b43ae3402f229f09f1bfc69404` |
| #12 | `24f660cf093c3e52efc0cde0c39e7aea1df48053` | `10450f9102d29586f8fd4315ddb283867dc2d233` |
| #13 | `57ff5585039e7f63de54a67981d5d98cb9ba84e8` | `52e6eafcf239ff608605bcd8db3032a68c655a1f` |

Every result has exactly one parent, forming a chain from original main
`ba1b5c5a0e5df44c28e7232b044bc6741d29bb47`. Every complete merged tree equals
the corresponding reviewed original tree. #11–#13 received content-preserving
feature-branch base-sync commits and were retargeted to main. No force push,
direct main push or branch deletion was performed.

## Terminal PR and self-contained completion rule

[PR #14](https://github.com/lcresearch/landmark-metadata/pull/14) is the final
gate and carries this record. Its **MERGED** state completes the five-PR stack;
OPEN means the final operation is still in progress. Its final merge SHA is
GitHub's `merge_commit_sha`, rather than a self-referential SHA written inside
the commit before it exists.

The final operation pins the reviewed candidate head, requires main to equal
the #13 result above, and verifies one parent plus exact candidate-tree equality
after squash. The scientific payload at reviewed #14 delivery head
`caa00fc1550f7c6c64d8d851ff207e7129aeb0e6` is unchanged. The only subsequent
content changes are integration TODO/continuation/navigation/pointer records.
An independent agent reviews this narrow delta before the final operation and
checks the resulting PR/commit chain afterward.

Current manuscript SHA-256 remains
`aac0903bc50d41dc1066232f6be13f9596b3241bff8168eac625c0da58ab67b4`;
the full companion remains
`a2b2ffe54cae5b62286c94729b725e4117ecff34f6b1cf81b61a8b8205463d19`.
All human statuses stay PENDING. Merge approval is not a human research signature,
a durable evidence deposit, recovery of missing history or paper submission.

## Operation records

Exact Git/API requests and responses are outside Git at
`/workspace/pr10-14-merge-20261008T070219Z/`. Each `pr-N/result.json` records the
original/synchronized head, main before merge, squash result, parents and trees.
The accompanying [index](integration-index.json) pins the already completed
predecessor records and external guarded driver. The final #14 record is produced
after its merge. The driver uses normal feature pushes and the GitHub PR merge
API with `merge_method: squash`; it never writes the default branch directly.

The completed source review and 83 repository tests remain the baseline.
Only the narrow integration-document delta requires new source/navigation and
identity checks; no model, Java probe or document rendering is rerun here.
