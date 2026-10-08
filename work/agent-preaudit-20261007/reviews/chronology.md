# HA05 chronology and deterministic resource subcheck

Agent pre-audit only; human HA05 remains PENDING. Verdict: **PARTIAL** for historical predeclaration chronology; **SUPPORTED_WITHIN_INSPECTED_SCOPE** for saved plan identity, deterministic source and full resource permutation/inverse. No evidence or repository edits, builds, model generation, or inference were performed.

Primary inspected root E: `/workspace/evidence-recovery-20261005T170453Z/package-v2/payload/metadata-contract-e2e-20261004T030536Z/`. Secondary original root O: `/workspace/metadata-contract-e2e-20261004T030536Z/`. Read HA05 at `/workspace/landmark-agent-preaudit/docs/human-audit/CHECKLIST.md:142` and the current C4 crosswalk.

Method: read JSON/source/plan and `commands-executed.sh`; fresh Python stdlib `hashlib.sha256` and `zipfile.ZipFile` reads of E2 model bytes; split and compare all 1,000 lines; direct `diff -u` of runner versions. No prior PASS report substituted for these checks.

## Chronology scope

- `E/phase0/pre-E2-freeze.json` has precisely the plan hash plus `frozen_before_E1_Android_predictions: true`; **it contains no timestamp**. Its SHA-256 is `ddb0b20a9670daaa524a59cba497feeb03895b96a7cc9a6c7cdd3afbd8b2de40`.
- Fresh hash of both `E/EXPERIMENT_E2_PLAN.md` and `E/E2/EXPERIMENT_E2_PLAN.md` is `4a9693fd929173d4c1efcb4204e0ced32148e159e8713c79d0922a38d196bae0`, exactly matching the freeze and `E/E2/implementation-identities.json` (`af5ad481398265cc4903266e28c94a24291685188e2bb84f60bc44b2fbc1200f`). The plan explicitly declares the fixed left rotation before inspecting E1 Android predictions, forbids selection from predictions, and gates E2 on working E1.
- Secondary original freeze mtime from `stat -c '%y %n'`: **2026-10-04 03:20:56.253070753 +0000**. Filesystem mtime is mutable local supporting metadata, not independent timestamp proof. The recovered package's copy-time metadata cannot supply the original freeze time.
- Preserved `E/E2/commands-executed.sh` (`53af91dc903eafb47b4197fc60e75a0c1d6651a64d79d6f5a4f5b90f99749702`) includes E1 as well as E2 commands. First recorded E1 original instrumentation **started** at `2026-10-04T03:22:46.484280+00:00`; final E1 replay/restoration instrumentation started `03:32:47.255734+00:00`; first E2 code generation started `03:34:50.517016+00:00`; first E2 original instrumentation started `03:35:14.677817+00:00`; primary permutation started `03:37:21.702459+00:00`; recovery restoration started `03:46:42.068681+00:00`.
- Timestamp interpretation is verified from `E/scripts/common.py` (`b2e7bdd6bcf94beb94584df24dcd3d8634a4b4ec1f1865e1c163d44d77f0d5d7`): `started_utc` is taken before `subprocess.run` and then copied into command-log comments. These are recorded start times, not predictions/completion times. No logged freeze-writing command or independently attested freeze timestamp was found in inspected records.
- These local artifacts are consistent with pre-E1 freeze and later E2 execution. They do **not independently prove historical predeclaration**. Deterministic present-day code is separate evidence from historical order. The E4 `PREVALIDATION_PROTOCOL.md` explicitly calls E1–E3 already observed development evidence; its later freeze cannot establish E2 predeclaration.

## Full resource transformation check (3 saved E2 variants × 1 resource)

Resource name remains `labels_without_background.txt`; all three contain 1,000 lines. The mutant list equals original `[1:] + [:1]` across every position, and inverse-restored list equals original across every position. This exact cyclic equality also establishes preserved multiplicities. There are **999/1,000 changed strings**; only position **638** is unchanged (`maillot`, from adjacent duplicate entries at 638/639). This says nothing by itself about distinct stable class IDs or semantic truth.

| Variant | Full model SHA-256 | Resource SHA-256 |
| --- | --- | --- |
| original | `6c7ab0a6e5dcbf38a8c33b960996a55a3b4300b36a018c4545801de3a3c8bde0` | `e697a491aa735cc6c2aaf982f8e86e8fc7b0a1ea7750a2cc6a2bdfc1e109012f` |
| label_permutation | `455a04a2c6193ea81bef8fbc47e193aee0449b8cebdc9cc487c7e9e85fe42da7` | `334152d1cce3445fc73c27c32001b5a6e8b7e548a37cc0e050ea363ebde18d3a` |
| permutation_restoration | `0a605ed10a38fc6f92fc4e266f5560756d2809e2669c45aa3b5a631cd88cea72` | `e697a491aa735cc6c2aaf982f8e86e8fc7b0a1ea7750a2cc6a2bdfc1e109012f` |

Each model path is `E/E2/variants/<variant>/model.tflite`. Resource equality is not whole-file equality: restored model and original model have different SHA-256, as disclosed above. Graph/ZIP-envelope preservation belongs to HA03 and was not rechecked here.

`E/scripts/prepare_e2.py` and `E/E2/implementation-snapshot/prepare_e2.py` both hash `01a5b1d08d80f324896ae10aa526b69c111787f81a2f7b24ab889ff61c38bb73`. Source asserts E1 primary/replay four rows, load/inference PASS and baseline decoder PASS, fixes 1,000 labels, performs `lines[1:]+lines[:1]`, checks `Counter`, and reverses with `shifted[-1:]+shifted[:-1]`; it never examines prediction values to choose a permutation.

## Replay history

`E/E2/implementation-history/run_android-before-recovery.py` hashes `70325ae97b4fa01e3984226da04b495358fc989c07de4a9de1b7d6483cd36c2d`, matching the runner identity listed in `implementation-identities.json`. The later `E/E2/implementation-snapshot/run_android.py` hashes `64add6c3dd8e60e58c0d56faf64fe8e71f44d0acd0c5cc24705c481e43ca73a5`; direct diff shows only addition of `--variants` and filtering rows by it. This is a disclosed recovery-controller change, not unexplained identity equality.

`E/E2/deviations.json` hashes `4f54bcf403247b553416fd478b59520f57a3aa3eb21f0deca458a68471ccb931`; it records original replay restoration as `INCOMPLETE_TRANSPORT`, says no complete instrumentation log/result was recovered, and identifies restoration-only `replay-recovery-20261004T034600Z`. The separate recovery must not convert the original interrupted attempt into success. Raw primary/replay output and returned score/list comparisons are assigned to the parent reviewer and not claimed by this subcheck.

Next human action: examine the freeze assertion and recorded command starts together, assess whether mutable same-session metadata is sufficient for intended chronology wording, and retain a limitation if no independent contemporaneous timestamp is available. Complete HA05 raw input/output/full decoded-list checks separately; use HA07 for reference-backed interpretation. No evidence discrepancy was found in the transformation; independent proof of chronology remains unavailable within inspected scope.
