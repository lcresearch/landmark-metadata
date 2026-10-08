# HA03 agent pre-audit: intervention preservation

Verdict: **SUPPORTED_WITHIN_INSPECTED_SCOPE**. Fresh saved-byte comparisons found no discrepancy in the assigned preservation claims. This is agent pre-audit with a fresh task context on shared infrastructure, not human verification, blinding or forensic independence. Human HA03 remains PENDING.

Target: `/workspace/landmark-agent-preaudit/work/workshop-convergence-20261007/manuscript/paper.tex`, SHA-256 `c79ba7f62a194abd487ec4b8ccedb60428ec4edd1f43e6ee155518ffd8bb416e`; protocol frozen head `24f660cf093c3e52efc0cde0c39e7aea1df48053`. Claims C2/C2R and P were interpreted using the current workshop crosswalk.

## Fresh computation and denominator

The new first-party `audit_ha03.py` read all 21 working model files in the selected package: eight original E1/E2 aliases, eight separate construction-audit aliases and five P2 variants. They represent five distinct model byte conditions of one graph, not 21 independent models. It also read 26 final code builds: eight original, eight rebuild, five P2 wrapper and five P2 Task. Initial `build-before-dependency-closure` and `build-attempt-1` outputs are explicitly excluded. Exact expanded paths, sizes and SHA-256 values are in `findings.json`, including every compared Java/class/DEX input. All 340 applicable comparison checks passed; these are correlated assertions, not reliability statistics.

Every model has 166 buffers. All 165 buffers other than `TFLITE_METADATA` buffer 165 compare byte-for-byte with original. No tensor references buffer 165. All schema-decoded computational fields, including ordered subgraphs/operators/tensors/output definitions and nonmetadata buffer fields, agree after removing only the named TFLITE_METADATA entry and blanking that buffer payload in memory. The one ordered output is tensor 163, `Softmax`, float32 `[1,1000]`, buffer 164. All 164 tensor buffer references per model are retained in the result.

Preservation methods are separate:

- Fresh normalized object serialization tags schema types, byte strings and ndarray dtype/shape/hex data, then produces sorted compact JSON. Its equality digest is `e1f8f725c803d877c57491ff75cc70f8c71c025e2a6be17161bcc3e7b78ea9a2`.
- A local reimplementation of the original `suite_static.canonical` algorithm repacks the metadata-cleared object using FlatBuffers with identifier TFL3. Its equality digest is `73e57df01115600419abb72de4b2c3257200e12eb205d335bcbfc203a589bee8`, also the recorded original static-results digest.
- The prior audit used a differently tagged JSON/base64 serialization and reported `9bf2f59a285519dd62e62941041ad60925376c4bcd2a88433166d25499e818b8`. That value is historical provenance, not the expected digest for the new serialization. No old PASS boolean substitutes for a new byte comparison.

## Metadata, ZIP and labels

Original, deletion, permutation and restoration share embedded-metadata hash `8608ff0e1650d5d7d2d841fb722e91b503730cde0fd7bfa1c2c67acaaa594ecb` and an identical 18,571,560-byte pre-ZIP prefix (SHA-256 `bf0669d6465b48495bb65ff6e6a0590be7a786120adbc65ab7b797ee09998d79`). Description alone changes embedded metadata and prefix: exactly one byte, ASCII P→p, at metadata offset 416 and whole-model offset 1200. The entire description-control model has exactly this one byte difference and unchanged length.

Every ZIP contains the same single label member `labels_without_background.txt`. Deletion has exactly the original first 999 labels; permutation has precisely the declared one-position left cyclic shift, preserves the multiset and changes 999 display strings. Restorations recover the exact 10,473-byte original payload. Labels were read with Java newline delimiters CR/LF/CRLF and the specified String.trim blank-line rule; this focal payload does not depend on broader Python splitlines behavior.

Both restoration aliases and P2 restoration equal each other as complete model files, but differ from the publisher original. They preserve the original pre-ZIP bytes and label payload; the ZIP container is not restored byte-for-byte. No behavioral restoration is newly asserted by HA03; recorded numerics/getter behavior are assigned to HA04–HA06.

| Condition | Complete model SHA-256 | Labels |
|---|---|---:|
| original | `6c7ab0a6e5dcbf38a8c33b960996a55a3b4300b36a018c4545801de3a3c8bde0` | 1000 |
| description_control | `ed16d9573d8fe3e489c27637036a4e5c8476d15f013b7116f89864d55432f51d` | 1000 |
| label_deletion | `739f08462e831806db6a9bce7ed5b70a037fce593003028e5d6911dbd284fd83` | 999 |
| label_permutation | `455a04a2c6193ea81bef8fbc47e193aee0449b8cebdc9cc487c7e9e85fe42da7` | 1000 |
| label_restoration | `0a605ed10a38fc6f92fc4e266f5560756d2809e2669c45aa3b5a631cd88cea72` | 1000 |

## Exact Java, classes and DEX scopes

All 21 generated `ContractModel.java` files are byte-identical, SHA-256 `60c1fb6022891cc2bd41b5bacdd2194361eb0ca40e37da2eddf6cba963279670`. All three generated ContractModel class files are likewise identical across original, rebuild and P2 wrapper. Within each of original eight builds, rebuild eight builds, P2 wrapper five builds and P2 Task five builds, every class file including that family’s harness and the full DEX are byte-identical.

Across original versus rebuild/P2 wrapper, the generated model classes still agree; harness class and full DEX differ. Thus whole-class-set or DEX identity must not be carried across these build families. P2 Task has its own harness and no generated ContractModel.

| Final build family | Full DEX SHA-256 |
|---|---|
| original/E1/original | `82ae7e4dafaeba6a1dcc4be479693cd1eb9cfc02ff04f661e801ac0466c5ee99` |
| rebuild/E1/original | `b5ce8404d0d7b197c1532003e934d7cb32d381aed47c7af2201044e89a50c821` |
| P2/wrapper/original | `4b8c5a96fcdb8c4f61c1007bf35f267fb629e9d21b8f2a41734d5de3b75467d3` |
| P2/task/original | `f46fd408e94d6b85eb3ba38c0fefcb01195312e38f88ad2caddf954fc3f58782` |

## Dependencies, provenance and limits

The preserved shared schema parser is `/workspace/evidence-recovery-20261005T170453Z/package-v2/payload/SUPPLEMENTARY_SOURCE/schema_py_generated.py`, SHA-256 `2359ceb02001d2c611b3f0d571e64992f011ed62cfb06d9d45acf72123537159`; metadata schema SHA-256 `bcd857b0f5af7d74ec948e882d4d8e31f4bdd41dece562110d1ffcbd8453bf50`. They were imported read-only with `-B` and `PYTHONDONTWRITEBYTECODE=1`. Existing `/workspace/hand-contract-repro/.venv/bin/python` supplied Python 3.11, flatbuffers 25.12.19, numpy 1.26.4. No inspection dependencies were installed. The default environment lacked flatbuffers. The schema is shared, not an independently implemented FlatBuffer parser; exact pre-ZIP equality and the single-byte description difference give a separate mutation-surface check.

No generator, APK build, emulator, inference, whole-APK attribution, structural MetadataPopulator run or new execution occurred. No missing binary prerequisite blocked this assigned HA03 scope. Matching saved bytes do not authenticate run chronology, provenance, source authority or numerical invariance on untested inputs. Historical report/source records were read for scope and algorithms and distinguished from the new computed comparisons. Package-wide inventory authentication and APK attribution belong to other assigned checks. No repository/evidence files or human verdict fields were edited.

## Next human action

Review the frozen manuscript and HA03 checklist, inspect `audit_ha03.py` and the expanded input inventory, and independently repeat the comparisons or inspect the preserved buffers, prefixes, ZIP payloads and final code artifacts. Record original, rebuilt and P2 scopes separately. Specifically verify metadata buffer 165 is unreferenced, retain description-control metadata inequality, restoration container inequality, and original/rebuild full-DEX inequality. Record a named human observation and conclusion in the human template; this agent report supplies no human signature.

Artifacts: `REPORT.md`, `findings.json`, `audit_ha03.py`, `COMMANDS.txt`, `audit.stdout`, `audit.stderr`. The command record distinguishes reproducible substantive commands from reconnaissance and does not claim to be a complete terminal transcript.

## Fail-closed script refinement

After the initial report, the coordinator requested explicit nonzero exit on failed comparisons. The current `audit_ha03.py` now returns exit 1 on a false comparison, accepts an explicit output directory and refuses to overwrite an existing `findings.json`. A final run to `strict-rerun/` exited 0. Its 340 checks, model observations, code observations and denominators exactly equal the initial run; original outputs remain preserved. `strict-rerun/findings.json` inventories the current script digest. For another run, supply a new output directory using the final command in `COMMANDS.txt`.
