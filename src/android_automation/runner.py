from __future__ import annotations

import argparse
import logging
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

from android_automation.adb import list_adb_devices, online_udids, wait_for_device
from android_automation.artifacts import split_allure_results_by_device, write_allure_environment, write_run_metadata
from android_automation.config import AndroidDeviceSettings, ConfigError
from android_automation.logging_config import initialize_log_session, setup_logging, write_combined_log
from android_automation.runtime import ExecutionContext, load_execution_context

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class RunnerOptions:
    appium_config: str
    device_selectors: list[str]
    all_devices: bool
    connected_devices: bool
    skip_offline_devices: bool
    framework_log_level: str
    report_dir: Path
    allure_results_dir: Path | None
    allure_report_dir: Path | None
    no_allure: bool
    no_auto_parallel: bool
    list_devices: bool
    preflight: bool
    pytest_args: list[str]


def main(argv: list[str] | None = None) -> int:
    options = _parse_runner_options(list(argv or []))
    initialize_log_session(options.report_dir / "logs" / "runner.log", reset=True)
    # 主进程日志写入当天目录，避免不同日期运行混在一起。
    setup_logging(options.framework_log_level, options.report_dir / "logs" / "runner.log")

    try:
        execution = load_execution_context(
            config_path=options.appium_config,
            device_selectors=options.device_selectors,
            all_devices=options.all_devices,
            connected_devices=options.connected_devices,
            skip_offline_devices=options.skip_offline_devices,
            validate_app=not options.list_devices,
        )
        execution.apply_environment()
    except ConfigError as exc:
        LOGGER.error("Configuration error: %s", exc)
        return 2

    if options.list_devices:
        _print_devices(execution.devices)
        return 0

    preflight_code = _run_preflight(execution, options)
    if options.preflight or preflight_code != 0:
        combined_log = write_combined_log(options.report_dir)
        if combined_log:
            LOGGER.info("Combined log generated: %s", combined_log)
        return preflight_code

    pytest_args = _build_pytest_args(options, execution.devices)
    _write_metadata(options, execution, pytest_args)

    LOGGER.info("Starting Android UI automation: python -m pytest %s", " ".join(pytest_args))
    import pytest

    exit_code = int(pytest.main(pytest_args))
    LOGGER.info("Android UI automation finished with exit code %s", exit_code)
    combined_log = write_combined_log(options.report_dir)
    if combined_log:
        LOGGER.info("Combined log generated: %s", combined_log)

    _generate_allure_reports(options, execution)
    return exit_code


def _parse_runner_options(args: list[str]) -> RunnerOptions:
    # runner 只解析框架自身参数，其余参数透传给 pytest。
    parser = _create_runner_parser()
    parsed, pytest_args = parser.parse_known_args(args)
    if parsed.connected_devices and (parsed.all_devices or parsed.device):
        parser.error("--connected-devices cannot be combined with --all-devices or --device")

    report_dir = Path(parsed.report_dir)
    no_allure = parsed.no_allure
    allure_results = None if no_allure else Path(
        parsed.allure_results_dir or str(report_dir / "allure-results")
    )
    allure_report = None if no_allure else Path(
        parsed.allure_report_dir or str(report_dir / "allure-report")
    )

    return RunnerOptions(
        appium_config=parsed.appium_config,
        device_selectors=list(parsed.device),
        all_devices=parsed.all_devices,
        connected_devices=parsed.connected_devices,
        skip_offline_devices=parsed.skip_offline_devices,
        framework_log_level=parsed.framework_log_level,
        report_dir=report_dir,
        allure_results_dir=allure_results,
        allure_report_dir=allure_report,
        no_allure=no_allure,
        no_auto_parallel=parsed.no_auto_parallel,
        list_devices=parsed.list_devices,
        preflight=parsed.preflight,
        pytest_args=pytest_args or ["tests"],
    )


def _build_pytest_args(options: RunnerOptions, selected_devices: tuple[AndroidDeviceSettings, ...]) -> list[str]:
    # runner 负责补齐 pytest 所需的公共参数和并行参数。
    args = list(options.pytest_args)
    if not _has_option(args, "--appium-config"):
        args.append(f"--appium-config={options.appium_config}")
    if not _has_option(args, "--report-dir"):
        args.append(f"--report-dir={options.report_dir}")
    if not _has_option(args, "--framework-log-level"):
        args.append(f"--framework-log-level={options.framework_log_level}")
    if _uses_connected_device_discovery(options):
        if "--connected-devices" not in args:
            args.append("--connected-devices")
    elif options.all_devices:
        if "--all-devices" not in args:
            args.append("--all-devices")
    else:
        for selector in options.device_selectors:
            args.extend(["--device", selector])
    if options.skip_offline_devices and "--skip-offline-devices" not in args:
        args.append("--skip-offline-devices")

    if options.allure_results_dir:
        _reset_directory(options.allure_results_dir)
    if options.allure_results_dir and not _has_option(args, "--alluredir"):
        args.append(f"--alluredir={options.allure_results_dir}")

    if len(selected_devices) > 1 and not options.no_auto_parallel:
        if not _has_xdist_workers(args):
            args.extend(["-n", str(len(selected_devices))])
        if not _has_option(args, "--dist"):
            args.append("--dist=loadgroup")

    _validate_parallel_args(args, selected_devices)
    return args


def _run_preflight(execution: ExecutionContext, options: RunnerOptions) -> int:
    # preflight 只做轻量检查，尽量在真正跑用例前把环境问题暴露出来。
    settings = execution.settings
    devices = execution.devices
    ok = True
    LOGGER.info("Preflight: app=%s package=%s activity=%s", settings.app_path, settings.app_package, settings.app_activity)
    LOGGER.info(
        "Preflight Android tooling: adb=%s sdk_root=%s android_home=%s retries=%s adb_exec_timeout=%sms",
        settings.adb_path,
        settings.android_sdk_root,
        settings.android_home,
        settings.session_start_retries,
        settings.adb_exec_timeout,
    )
    for skipped in execution.skipped_devices:
        LOGGER.warning(
            "Skipped device before preflight: device=%s udid=%s state=%s reason=%s",
            skipped.name,
            skipped.udid,
            skipped.state,
            skipped.reason,
        )

    if settings.app_path and not settings.app_path.exists():
        LOGGER.error("Preflight failed: APK not found: %s", settings.app_path)
        ok = False

    if settings.adb_path and not settings.adb_path.exists():
        LOGGER.error("Preflight failed: configured adb does not exist: %s", settings.adb_path)
        ok = False

    adb_devices = list_adb_devices(settings)
    if adb_devices:
        LOGGER.info("Preflight adb devices: %s", ", ".join(f"{d.udid}:{d.state}" for d in adb_devices))

    online_devices = online_udids(settings)
    for device in devices:
        if device.udid and device.udid not in online_devices:
            LOGGER.warning("Device not online in initial adb list, waiting once: device=%s udid=%s", device.name, device.udid)
            if wait_for_device(settings, device):
                online_devices = online_udids(settings)

        if device.udid and device.udid not in online_devices:
            LOGGER.error("Preflight failed: device offline or missing: device=%s udid=%s", device.name, device.udid)
            ok = False
        else:
            LOGGER.info("Preflight device OK: device=%s udid=%s", device.name, device.udid)

    for device in devices:
        server_url = device.server_url or settings.server_url
        if settings.appium_service.manage_servers and _is_managed_server(execution, server_url):
            LOGGER.info("Preflight Appium server will be managed by the runner: device=%s server=%s", device.name, server_url)
            continue
        if not _server_reachable(server_url):
            LOGGER.error("Preflight failed: Appium server is not reachable: device=%s server=%s", device.name, server_url)
            ok = False
        else:
            LOGGER.info("Preflight Appium server OK: device=%s server=%s", device.name, server_url)

    if options.allure_results_dir and _allure_executable() is None:
        LOGGER.warning("Allure CLI not found. Raw results will be kept, but HTML report generation will be skipped.")
    elif options.allure_results_dir:
        LOGGER.info("Preflight Allure CLI OK")

    return 0 if ok else 2


def _generate_allure_reports(options: RunnerOptions, execution: ExecutionContext) -> None:
    # 单设备生成默认报告；多设备只生成分设备独立报告，避免混合结果干扰查看。
    if not options.allure_results_dir or not options.allure_report_dir:
        return

    allure_executable = _allure_executable()
    if allure_executable is None:
        LOGGER.warning("Allure CLI not found. Install it to generate HTML reports. Raw results: %s", options.allure_results_dir)
        return

    if len(execution.devices) == 1:
        _generate_single_allure_report(
            allure_executable=allure_executable,
            results_dir=options.allure_results_dir,
            report_dir=options.allure_report_dir,
            label=f"device={execution.devices[0].name}",
        )
        return

    if options.allure_report_dir.exists():
        shutil.rmtree(options.allure_report_dir)
        LOGGER.info("Removed mixed Allure report directory for multi-device run: %s", options.allure_report_dir)

    device_results = split_allure_results_by_device(
        options.allure_results_dir,
        execution.settings,
        execution.devices,
    )
    for device in execution.devices:
        results_dir = device_results.get(device.name)
        if results_dir is None:
            LOGGER.warning("No device-specific Allure results found for %s", device.name)
            continue
        report_dir = options.report_dir / f"allure-report-{_safe_report_name(device.name)}"
        _generate_single_allure_report(
            allure_executable=allure_executable,
            results_dir=results_dir,
            report_dir=report_dir,
            label=f"device={device.name}",
        )


def _generate_single_allure_report(
    *,
    allure_executable: str,
    results_dir: Path,
    report_dir: Path,
    label: str,
) -> None:
    _reset_directory(report_dir)

    command = [
        allure_executable,
        "generate",
        str(results_dir),
        "-o",
        str(report_dir),
        "--clean",
    ]
    LOGGER.info("Generating Allure report (%s): %s", label, " ".join(command))
    result = subprocess.run(command, text=True, capture_output=True)
    if result.returncode != 0:
        LOGGER.warning(
            "Allure report generation failed (%s): %s",
            label,
            result.stderr.strip() or result.stdout.strip(),
        )
        return

    LOGGER.info("Allure report generated (%s): %s", label, report_dir)


def _write_metadata(options: RunnerOptions, execution: ExecutionContext, pytest_args: list[str]) -> None:
    write_run_metadata(
        options.report_dir,
        execution.settings,
        execution.devices,
        pytest_args,
        skipped_devices=execution.skipped_devices,
    )
    if options.allure_results_dir:
        write_allure_environment(options.allure_results_dir, execution.settings, execution.devices)


def _print_devices(devices: tuple[AndroidDeviceSettings, ...]) -> None:
    for device in devices:
        print(
            f"{device.name}\tudid={device.udid or '-'}\tappium_port={device.appium_port}\tsystem_port={device.system_port}\t"
            f"chromedriver_port={device.chromedriver_port or '-'}\tmjpeg_server_port={device.mjpeg_server_port or '-'}\t"
            f"source={device.source}"
        )


def _validate_parallel_args(args: list[str], devices: tuple[AndroidDeviceSettings, ...]) -> None:
    if len(devices) <= 1:
        return

    dist = _option_value(args, "--dist")
    if dist and dist != "loadgroup":
        raise SystemExit("Multi-device execution requires --dist=loadgroup")

    workers = _xdist_worker_count(args)
    if workers is not None and workers < len(devices):
        LOGGER.warning("Selected %s devices but only %s xdist workers configured.", len(devices), workers)
    elif workers is not None and workers > len(devices):
        LOGGER.info("Selected %s devices with %s xdist workers; extra workers may be idle.", len(devices), workers)


def _uses_connected_device_discovery(options: RunnerOptions) -> bool:
    # 无参数本地运行默认发现当前在线设备；显式 --all-devices 才严格跑配置内全部设备。
    return options.connected_devices or (
        not options.all_devices
        and not options.skip_offline_devices
        and not options.device_selectors
    )


def _allure_executable() -> str | None:
    return shutil.which("allure") or shutil.which("allure.cmd") or shutil.which("allure.CMD")


def _server_reachable(url: str) -> bool:
    try:
        with urlopen(f"{url.rstrip('/')}/status", timeout=3) as response:
            return 200 <= response.status < 500
    except (OSError, URLError):
        return False


def _is_managed_server(execution: ExecutionContext, server_url: str) -> bool:
    managed_urls = {device.server_url for device in execution.devices if device.server_url}
    return server_url in managed_urls


def _create_runner_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
    parser.add_argument("--appium-config", default="config/appium.yaml")
    parser.add_argument("--device", action="append", default=[])
    parser.add_argument("--all-devices", action="store_true")
    parser.add_argument("--connected-devices", action="store_true")
    parser.add_argument("--skip-offline-devices", action="store_true")
    parser.add_argument("--framework-log-level", default="INFO")
    parser.add_argument("--report-dir", default="reports/latest")
    parser.add_argument("--allure-results-dir")
    parser.add_argument("--allure-report-dir")
    parser.add_argument("--no-allure", action="store_true")
    parser.add_argument("--no-auto-parallel", action="store_true")
    parser.add_argument("--list-devices", action="store_true")
    parser.add_argument("--preflight", action="store_true")
    return parser


def _has_option(args: list[str], name: str) -> bool:
    return any(value == name or value.startswith(f"{name}=") for value in args)


def _option_value(args: list[str], name: str) -> str | None:
    for index, value in enumerate(args):
        if value == name and index + 1 < len(args):
            return args[index + 1]
        if value.startswith(f"{name}="):
            return value.split("=", 1)[1]
    return None


def _has_xdist_workers(args: list[str]) -> bool:
    return "-n" in args or "--numprocesses" in args or any(
        value.startswith("-n=") or value.startswith("--numprocesses=") for value in args
    )


def _xdist_worker_count(args: list[str]) -> int | None:
    for index, value in enumerate(args):
        if value in {"-n", "--numprocesses"} and index + 1 < len(args):
            return _parse_worker_count(args[index + 1])
        if value.startswith("-n=") or value.startswith("--numprocesses="):
            return _parse_worker_count(value.split("=", 1)[1])
    return None


def _reset_directory(path: Path) -> None:
    resolved = path.resolve()
    if str(resolved) == resolved.anchor:
        raise SystemExit(f"Refusing to reset filesystem root: {resolved}")
    if resolved.exists():
        shutil.rmtree(resolved)
    resolved.mkdir(parents=True, exist_ok=True)


def _parse_worker_count(value: str) -> int | None:
    try:
        return int(value)
    except ValueError:
        return None


def _safe_report_name(value: str) -> str:
    return "".join(char if char.isalnum() or char in {"-", "_"} else "_" for char in value).strip("_") or "device"


if __name__ == "__main__":
    raise SystemExit(main())
