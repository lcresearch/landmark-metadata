# Phase-0 audit addendum

After the initial read-only audit, every one of the 46 previously preserved variants was checked against its original from raw bytes: canonical graph and all non-metadata buffers agree. Every structurally accepted variant's saved numerical arrays match its original arrays byte-for-byte. This is a fresh verification of saved arrays, not new inference.

Machine record: `phase0/all-preservation-and-array-audit.json`.

The existing generated Gradle file was inspected: it targets an old Android Gradle plugin and experimental/nightly library coordinates. E1 instead uses the disclosed, pinned Android build harness. This does not establish that the original generated Gradle project itself builds.
