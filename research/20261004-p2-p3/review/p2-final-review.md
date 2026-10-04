# P2 final agent review

**Outcome: PASS within the checks below; no material wording or mechanism issue
found in the reviewed final P2 report.** This is a separate agent review of saved
records and source relationships, not independent human verification or another
Android execution. No P2 or sealed mechanism artifact was modified.

## Reviewed versions

All paths are relative to `/workspace/metadata-contract-p2p3-20261004T073824Z`.

| Reviewed input | SHA-256 |
|---|---|
| `P2/results.json` | `8828d53f32d0eb6a8a5276092e5f2834f548389d780fde1d3726cde0b263d45d` |
| `P2/EXPERIMENT_P2_RESULTS.md` | `38dbe80a4b9e106376f57c1f3f89b0afa8e2ad586db9f09900952a42819667f9` |
| `P2/MANUSCRIPT_IMPACT.md` | `0408d83c62260ff69362eda63fea31c1ab9e504aa1298fe49f50794a8ae15348` |
| `verification/runtime-record-review.json` | `5d307a205ce17df113e235a6a8650f39d7c68d80721c91f7bde5bc65c9d8bfd6` |
| `P2/scripts/TaskInstrumentation.java` | `f955fe6e43f004420b90ab80f69ac12ed622aaadd9864c841ee1dbb972b1527e` |
| `P2/scripts/ContractInstrumentation.java` | `6a7aaddfb8009f12d3df1df658f24dbbdc7a132573f4cd24a0a6ba7991f2d346` |
| `review/mechanism/SHA256SUMS` | `6c841bdc38f0a959d5ce8579143d8da8f1e036dfdd795ff23ca2fb9b8b32c545` |

Also read the frozen P2 plan, analysis script, root verification script and both
deletion device records. Rechecked all 34 entries in the sealed mechanism
manifest: unchanged. The root raw-record verification reports 152 checks, all
PASS; its runtime and human-verification flags correctly remain false.

## Stage and exception checks

- **PASS — generated route.** Both deletion observations record successful
  constructor/input preparation/`process`, a saved 4,000-byte raw output, and a
  caught `IllegalArgumentException` at the actual generated category getter.
  The stack includes `ContractModel$Outputs.getProbabilityAsCategoryList:47`
  and both `TensorLabel` constructor overloads. The reported message exactly
  matches the device record. Harness status assignment follows the public API
  return; later serialization/IO is a separate observation stage.
- **PASS — Task route.** The deletion constructor throws before any input
  observation. Final stage records keep later input preparation, inference and
  classify/decoding `NOT_REACHED`. The preserved public outer exception is
  `IllegalStateException: Error getting native address of native library:
  task_vision_jni`. Its cause is the recorded `IllegalArgumentException` with
  `Got 1000 class(es) for output index 0, expected 999 according to the label
  map.` This is a wrapped label-cardinality rejection, not evidence that the
  native library was missing.
- **PASS — public granularity.** Successful Task records mark the public
  `classify` call successful while marking internal inference/decoder stages
  `NOT_SEPARATELY_OBSERVED`. The report discloses normalization of the collector's
  atomic-stage marker and preserves the original execution records. It does not
  convert a granularity marker into evidence that deletion inference ran.
- **PASS — initialization scope.** Task creation is described as combined
  loading/initialization. Pre-load asset hashing is explicitly bounded; no
  separately successful native loading stage is asserted for the rejected
  artifact.

## Alignment, denominators and numerical wording

- **PASS — index alignment.** The harness records Task `Category.getIndex()`;
  the analysis uses that field to align Task categories to wrapper list/output
  positions. Task ranked-list position is not treated as tensor position.
- **PASS — public scores versus raw tensors.** Each of the eight successful
  cross-consumer condition/input comparisons covers 1,000 indices, with 1,000
  equal score bit patterns and labels, and zero maximum absolute score
  difference. The report calls these returned/public scores. It does not claim
  that native Task raw tensors were captured or compared. Wrapper raw equality
  is reported separately.
- **PASS — permutation/restoration interpretation.** Within each consumer,
  permutation changes 999 displayed labels while scores at the aligned indices
  remain equal; restoration recovers the observed original association. P2
  supplies no independent class-order oracle, so the report retains
  original-relative association wording.
- **PASS — denominators.** One graph, five byte conditions and two consumer
  configurations yield ten primary units. The actual observations are ten
  wrapper inputs plus eight Task inputs, with sixteen decoded lists. The two
  planned Task deletion inputs are explicitly unreached and excluded from the
  eighteen observed-input count. Mutation conditions and inputs are not called
  independent models.

## Mechanism and remaining configuration differences

The device stack and reported cause are consistent with the sealed Java-bytecode
and pinned-source review. The precise Android source route is:

`ImageClassifier.createFromFileAndOptions`
→ `TaskJniUtils.createHandleFromFdAndOptions/createHandleFromLibrary`
→ `initJniWithModelFdAndOptions`
→ `vision::ImageClassifier::CreateFromOptions`
→ `Init`
→ `CheckAndSetOutputs`.

The count branch is in pinned `cc/task/vision/image_classifier.cc:253`, commit
`133228616ca14e1b64c03f6a0ea8610f41a60783`. It is not the separate
`ClassificationPostprocessor::Init` route. The report points to the mechanism
review and does not make that incorrect attribution. Native symbols and matching
diagnostic strings support consistency, not a proof of complete native
binary–source equivalence or of the packaged interpreter's exact version.

The report correctly limits the comparison to two official configurations in
the same API 30 x86_64 AVD. It preserves separate Task and standalone Lite JNI
integrations, avoids claiming identical native implementations, and avoids
isolating interpreter-version causality. Shared Support API jar identity does
not eliminate these differences.

No follow-up correction is required by this review. Human verification,
independent rebuild by a separate researcher, class-order reference validation
and any deployment-impact claim remain outside this review's completed scope.
