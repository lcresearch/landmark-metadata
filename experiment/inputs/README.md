# Pinned focal inputs

Use a new directory outside the source checkout. Obtain the original publisher
model identified in [inputs.json](../../docs/reproduction/inputs.json), recording
its acquisition separately, then run:

```sh
python3 experiment/inputs/recover_inputs.py \
  --original-file /path/to/efficientnet_lite0.tflite \
  --output-dir /path/outside/repository/new-inputs
python3 experiment/inputs/retrieve_references.py \
  --original-file /path/to/efficientnet_lite0.tflite \
  --output-dir /path/outside/repository/new-references
```

The first command verifies/reconstructs the five model conditions and two RGB
inputs. The second retrieves six pinned reference bodies. Both reject existing
outputs; matching inputs do not recover the old execution logs or authenticate
old results. The [November acquisition record](../../work/input-recovery-20261110/README.md)
is historical provenance. Continue with the [current runbook](../RUNBOOK.md).
