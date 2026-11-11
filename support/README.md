# Auxiliary evidence support

These files support retained evidence readers and regression tests. They are not
part of the [current focal execution](../experiment/README.md).

- `reproduction/maintained/evidence_validation.py` supplies the strict observation
  reader's identity checks.
- `parser/DecoderProbe.java`, `reproduction/maintained/{LabelOracle.java,java_labels.py,
  test_java_labels.py,runtime.py}` and `reproduction/probes/probe_label_parser.py`
  retain byte-exact source inputs checked by the maintained parser reader.
- The small `hand/scripts/fetch_assets.py` and `reproduction/retrieve_literature.py`
  modules retain the failure-preservation regressions in `test_reproduction_review.py`.

The historical runtime/probe helpers retain original layout assumptions. Readback
checks their bytes; it does not execute a new probe. To run a historical workflow,
restore the complete [archived tree](../archive/README.md) into a separate folder.
The [maintained readers](../work/review-fixes-20261021/README.md), observation reader
and evidence-recovery tools keep their existing entry points and regression tests.
