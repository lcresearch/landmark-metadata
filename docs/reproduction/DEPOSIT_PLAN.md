# Plan for an independently usable external evidence deposit

This is a plan, not an existing deposit or an upload instruction. The repository
continues to exclude models, SDKs, dependencies, generated code, APK/classes/DEX,
raw tensors, logs and archives. No destination has been selected and no such
material is published by this handoff. A local path, an official mutable URL and
a checksum each serve different purposes; none alone supplies a usable archive.

## Minimum packages and acceptance conditions

| Package | Material needed outside Git | Acceptance condition before claiming availability |
|---|---|---|
| Focal inputs | Exact original EfficientNet file; all tested resource/control variants; associated-file payloads; synthetic input bytes or their exact generator/specification | Match recorded file identities and explicit condition aliases. Preserve graph/weights, embedded metadata and associated ZIP/resources as distinct comparisons; do not infer full-model identity from only the graph hash |
| Source and execution configuration | Source checkout at an identified commit; generated configuration such as original `INPUTS.json`; exact command order, paths, environment flags, harness and generated source relationships | A recipient can identify every input and output root and recreate missing configuration from a documented recipe; no unexplained manual patch or overwrite of original evidence |
| Toolchain | Pinned Python packages and dependency locks, generator, runtime AAR/JAR/native dependencies, JDK, Android platform/build tools/system image and emulator configuration | Acquisition endpoints plus expected archive hashes where established, or a permitted cache; verify installed contents/versions. Do not equate an API level or archive filename with exact binary identity |
| Original observations | Stage records, caught exceptions/stacks, input/raw/decoded bytes, generated source and class comparisons, APK asset identity records and build logs | All required units/inputs present; immutable manifest with a separately trusted digest; strict readback and manual inspection agree on the stated scope |
| P2 consumer comparison | Both consumers' dependency/configuration identities, same tested model/input bytes, device records and cause chains | Preserve Task construction versus atomic classify boundaries and unknown embedded interpreter version; do not invent separately observed native raw tensors |
| P3 qualified reference | Exact bridge model, publisher cards/revisions, external display labels, retrieval/provenance and full mapping comparison | Verify artifact linkage and complete display order; retain stable-class-ID and task-accuracy limits. Recovering just a generic ImageNet list is insufficient |
| Secondary claims, if included in the paper | Hand source/reference/model/binding evidence, E4 declared candidates and dispositions, E5 frozen 65-artifact catalog and matching payloads, actual-library parser probes | Provide each claim's own prerequisites or explicitly mark it unreproduced. Do not replace the separately pinned E5 manifest with a catalog generated from the run being tested |

## Keep the two experiment histories separate

The original E1/E2 and P2/P3 packages and the later `/workspace/repro-*`
reconstruction are distinct evidence sets. [Inputs](INPUTS.md) records which
selected files are currently visible. Do not move a file from one run into the
other merely to satisfy a missing pathname. A newly reconstructed model or
report receives its own provenance; matching numerical behavior does not
authenticate an unavailable original archive.

The minimal first release can prioritize E1/E2 plus P2/P3, but it must state that
the full maintained reconstruction reader also expects Linux Task, Hand and E4/E5
inputs. A focal package is not sufficient for that whole-reader command. Broad
checker regression is blocked until the independently pinned original fixture
set is recoverable; a later self-consistent set is not an equivalent trust anchor.

## Release procedure still to complete

1. Choose a durable destination, access terms and retention policy. Confirm which
   third-party dependencies/models/reference documents may be redistributed;
   where bytes cannot be deposited, document the acquisition route and identity
   checks and explicitly retain the availability dependency.
2. Collect material into a new staging directory without altering saved packages.
   Resolve missing generated configuration and path assumptions. Record absent
   objects rather than filling them from guessed versions.
3. Produce a complete manifest of relative paths, sizes and SHA-256 values.
   Publish the manifest identity separately from the data it checks. Include a
   source commit, run/unit identifiers and a machine-readable acquisition table.
4. Verify the staged input identities and readback completeness. Then have a
   fresh workspace recover/install the stated dependencies and perform the
   chosen minimal build/run. Preserve all failures and deviations; matching old
   reports is not a replacement for new execution records.
5. Record exactly what was reproduced, by whom, when and with what environment.
   Separate author checking, agent automation and independent human work.

Until those steps finish, describe the repository as a **documented source
handoff with scoped local checks**, not a one-command clean-machine reproduction
or a complete preserved evidence release. The current task can complete the
inventory and command documentation while these delivery and execution steps
remain open.
