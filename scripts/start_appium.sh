#!/usr/bin/env bash
set -euo pipefail

appium --address "${APPIUM_HOST:-127.0.0.1}" --port "${APPIUM_PORT:-4723}"
