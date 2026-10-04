#!/usr/bin/env bash
set -eu
cd /workspace/metadata-contract-p2p3-20261004T073824Z/review/mechanism
python collect_sources.py
python inspect_binaries.py
python summarize_mechanism.py
