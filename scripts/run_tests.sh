#!/usr/bin/env bash
set -euo pipefail

PYTHONPATH="${PYTHONPATH:-src}" python -m android_automation.runner "$@"
