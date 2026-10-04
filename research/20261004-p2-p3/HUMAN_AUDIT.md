# Human audit for P2/P3 — pending

No checkbox in this file is completed by an agent check.

- [ ] Verify the five input identities against the original E1/E2 artifacts and
  verify those same identities in both newly packaged and loaded Android assets.
- [ ] Inspect generated-wrapper use: byte-unmodified generated source, actual
  public process/getter calls, and non-mutating output observation.
- [ ] Inspect the official Task Java calls, options and resolved dependencies;
  confirm no handwritten replacement decoder is being tested.
- [ ] Check the same emulator/API/ABI and exact pixel inputs for both paths;
  retain differences in native libraries and runtime integration.
- [ ] Inspect attributed per-execution records, stack traces, and earliest
  externally observable failures. Treat Task classify as atomic where no finer
  instrumentation exists; do not invent separate inference/decoder outcomes.
- [ ] Check preservation, score/index alignment, controls and restoration from
  raw records, including unsuccessful attempts and stages not reached.
- [ ] Check the JNI/source interpretation against the actually used library;
  distinguish matching version/source evidence from proven binary correspondence.
- [ ] Inspect P3's frozen scope, all retrieval outcomes, artifact provenance
  links and full mapping comparisons. A matching generic label list alone is not
  an independent class-order oracle for the exact model.
- [ ] Verify TFHub fp32/2 -> classification/1 -> external ImageNetLabels and
  explicit background omission, together with the full computational-field and
  165-buffer equality bridge. Check all 1,000 positions, not just position 904.
- [ ] Confirm that display-order agreement is distinct from the still-unproven
  stable class-ID lineage, especially the duplicate crane/maillot strings.
- [ ] Inspect the preserved initial reference-audit assumption failure and its
  resolution through reconstructed Git tree/blob identities.
- [ ] Confirm manuscript changes stay within the measured evidence and that
  human, agent, author and independent-reproducer roles are correctly stated.

When completed by a human, record name or appropriate identifier, date, method,
artifacts inspected and per-item conclusions. Author verification and independent
human reproduction must be identified separately.
