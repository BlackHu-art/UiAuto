# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## Repository purpose

This repository is a Python Appium Android UI automation framework for testing an existing APK across one or more Android devices. It uses pytest for execution, pytest-xdist for device-level parallelism, pytest-order for ordered lifecycle tests, Appium 2 + UiAutomator2 for Android automation, and Allure as the primary report system.

## Common commands

Install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Install Appium 2 Android driver:

```bash
npm install -g appium@2
bash scripts/install_uiautomator2.sh
```

Start Appium server:

```bash
bash scripts/start_appium.sh
```

Run default ordered flow on the first configured device:

```bash
python run_tests.py
```

Run one selected device:

```bash
python run_tests.py --device emulator_5554
```

Run all configured devices concurrently; runner auto-adds `-n <device_count> --dist=loadgroup`:

```bash
python run_tests.py --all-devices
```

List configured devices:

```bash
python run_tests.py --list-devices
```

Run preflight only:

```bash
python run_tests.py --preflight --all-devices
```

Check Android/Appium tooling:

```bash
python --version
node --version
java -version
adb version
appium -v
adb devices
```

## Configuration

- Put the APK under `apps/`, and configure `android.app` in `config/appium.yaml`.
- `config/appium.yaml` contains shared app settings and the multi-device list.
- Each configured device needs unique `name`, `udid`, `system_port`, `chromedriver_port`, and `mjpeg_server_port`.
- If Appium cannot infer launch details from the APK, configure `app_package`, `app_activity`, and `app_wait_activity`.
- `.env` may override app/single-device values for local debugging.
- Current verified local combo: Appium `2.19.0` with UiAutomator2 driver `4.2.9`.

## Architecture

- `run_tests.py` is the root startup file for PyCharm and shell usage.
- `src/android_automation/runner.py` parses framework options, derives selected devices, auto-adds xdist options for multi-device runs, writes metadata, runs pytest, and generates Allure reports.
- `src/android_automation/config.py` loads YAML and `.env`, resolves APK paths, validates shared app settings, and builds the selected Android device matrix.
- `src/android_automation/driver_factory.py` builds `UiAutomator2Options` from shared app settings plus per-device Appium ports.
- `src/android_automation/logging_config.py` configures console and file logging.
- `tests/conftest.py` owns pytest CLI options, device parameterization, logging setup, driver lifecycle, xdist grouping, failure screenshots, page source capture, and Allure attachments.
- `tests/test_app_lifecycle.py` contains ordered install/uninstall tests.
- `tests/test_smoke.py` contains an ordered launch smoke test and an optional locator-based sample test.

## Reports and artifacts

Each framework run writes to `reports/latest` by default:

```text
reports/latest/
  logs/
  screenshots/
  page_sources/
  metadata/
  allure-results/
  allure-report/
```

Use `--report-dir reports/<name>` only when a separate report directory is intentional. Allure raw results are produced automatically through `allure-pytest`; the globally installed Allure CLI generates `allure-report` after pytest finishes.

## Multi-device execution notes

- Use `--device <name-or-udid>` one or more times to select devices.
- Use `--all-devices` to run against every configured device.
- For more than one selected device, `runner.py` auto-adds `-n <device_count> --dist=loadgroup` unless `--no-auto-parallel` is passed.
- `--dist=loadgroup` keeps each device's ordered tests serialized while different devices run concurrently.

## Existing workspace files

- `.mcp.json` configures project MCP servers.
- `.Codex/` contains Codex settings.
- `.remember/` contains session continuity notes and hook logs.
