#!/usr/bin/env bash
set -euo pipefail

appium driver install uiautomator2@4.2.9
appium driver list --installed
