from __future__ import annotations

import logging
from pathlib import Path

import allure
import pytest
from selenium.common.exceptions import WebDriverException

from android_automation.appium_service import start_managed_appium_servers
from android_automation.artifacts import attach_failure_logs, attach_session_metadata, capture_failure_artifacts
from android_automation.config import ConfigError
from android_automation.logging_config import setup_logging
from android_automation.runtime import load_execution_context
from android_automation.session import create_session_with_retries

LOGGER = logging.getLogger(__name__)


def pytest_addoption(parser):
    parser.addoption(
        "--appium-config",
        action="store",
        default="config/appium.yaml",
        help="Path to Appium YAML config.",
    )
    parser.addoption(
        "--device",
        action="append",
        default=[],
        help="Device name or UDID to run against. Can be passed multiple times.",
    )
    parser.addoption(
        "--all-devices",
        action="store_true",
        help="Run each driver test against every configured Android device.",
    )
    parser.addoption(
        "--connected-devices",
        action="store_true",
        help="Run against all currently connected adb devices.",
    )
    parser.addoption(
        "--skip-offline-devices",
        action="store_true",
        help="Skip selected configured devices that are not currently online.",
    )
    parser.addoption(
        "--framework-log-level",
        action="store",
        default="INFO",
        help="Python logging level.",
    )
    parser.addoption(
        "--report-dir",
        action="store",
        default="reports/current",
        help="Framework report/artifact root directory.",
    )


def pytest_configure(config):
    report_dir = Path(config.getoption("--report-dir"))
    if config.getoption("--connected-devices") and (
        config.getoption("--all-devices") or config.getoption("--device")
    ):
        raise pytest.UsageError("--connected-devices cannot be combined with --all-devices or --device")
    # xdist worker 与 runner 使用统一的按日期日志目录。
    setup_logging(config.getoption("--framework-log-level"), report_dir / "logs" / f"{_worker_id(config)}.log")


@pytest.fixture(scope="session")
def execution_context(request):
    try:
        # 执行上下文统一负责配置加载、设备选择和环境变量注入。
        execution = load_execution_context(
            config_path=request.config.getoption("--appium-config"),
            device_selectors=request.config.getoption("--device"),
            all_devices=request.config.getoption("--all-devices"),
            connected_devices=request.config.getoption("--connected-devices"),
            skip_offline_devices=request.config.getoption("--skip-offline-devices"),
        )
        execution.apply_environment()
        LOGGER.info(
            "Loaded Appium config: server=%s app=%s selected_devices=%s",
            execution.settings.server_url,
            execution.settings.app_path,
            ",".join(device.name for device in execution.devices),
        )
        return execution
    except ConfigError as exc:
        pytest.skip(str(exc))


@pytest.fixture(scope="session")
def app_settings(execution_context):
    return execution_context.settings


@pytest.fixture(scope="session")
def device_settings(request, execution_context):
    # 一个 device session 对应同一台设备的整组用例。
    device = request.param
    allure.dynamic.parameter("device", device.name)
    allure.dynamic.parameter("udid", device.udid or "")
    allure.dynamic.parameter("appium_port", device.appium_port)
    allure.dynamic.parameter("system_port", device.system_port)
    allure.dynamic.parameter("appium_server", device.server_url or execution_context.settings.server_url)
    LOGGER.info(
        "Selected device: name=%s udid=%s appium_port=%s system_port=%s chromedriver_port=%s mjpeg_server_port=%s",
        device.name,
        device.udid,
        device.appium_port,
        device.system_port,
        device.chromedriver_port,
        device.mjpeg_server_port,
    )
    return device


@pytest.fixture(scope="session")
def appium_server(request, app_settings, device_settings):
    report_dir = Path(request.config.getoption("--report-dir"))
    server_url = device_settings.server_url or app_settings.server_url
    LOGGER.info(
        "Preparing Appium service for device test session: device=%s server=%s",
        device_settings.name,
        server_url,
    )
    managed_cluster = start_managed_appium_servers(app_settings, (device_settings,), report_dir)
    LOGGER.info(
        "Appium service ready for device test session: device=%s server=%s",
        device_settings.name,
        server_url,
    )
    yield server_url
    LOGGER.info(
        "Stopping Appium service after device test session: device=%s server=%s",
        device_settings.name,
        server_url,
    )
    managed_cluster.stop(app_settings.appium_service.stop_timeout_seconds)


@pytest.fixture
def driver(appium_server, app_settings, device_settings):
    # driver 仍按用例创建，保证测试之间相互隔离。
    driver_instance = create_session_with_retries(app_settings, device_settings)
    yield driver_instance
    LOGGER.info(
        "Quitting Appium driver session: session_id=%s device=%s",
        driver_instance.session_id,
        device_settings.name,
    )
    try:
        driver_instance.quit()
    except WebDriverException:
        LOGGER.warning("Failed to quit Appium session cleanly", exc_info=True)


def pytest_generate_tests(metafunc):
    if "device_settings" not in metafunc.fixturenames:
        return

    try:
        execution = load_execution_context(
            config_path=metafunc.config.getoption("--appium-config"),
            device_selectors=metafunc.config.getoption("--device"),
            all_devices=metafunc.config.getoption("--all-devices"),
            connected_devices=metafunc.config.getoption("--connected-devices"),
            skip_offline_devices=metafunc.config.getoption("--skip-offline-devices"),
            validate_app=False,
        )
    except ConfigError as exc:
        pytest.skip(str(exc))

    params = [
        pytest.param(
            device,
            id=device.name,
            marks=pytest.mark.xdist_group(device.name),
        )
        for device in execution.devices
    ]
    metafunc.parametrize("device_settings", params, scope="session")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not report.failed:
        return

    driver_instance = item.funcargs.get("driver")
    if driver_instance is None:
        return

    device = item.funcargs.get("device_settings")
    device_name = device.name if device else "unknown_device"
    report_dir = Path(item.config.getoption("--report-dir"))
    worker_id = _worker_id(item.config)

    try:
        capture_failure_artifacts(driver_instance, report_dir, device_name, item.nodeid, worker_id)
        attach_session_metadata(driver_instance, device, item.nodeid, worker_id)
        attach_failure_logs(report_dir, device_name, worker_id)
        LOGGER.error("Captured failure artifacts for %s on %s", item.nodeid, device_name)
    except Exception:
        LOGGER.warning("Failed to capture failure artifacts", exc_info=True)


def _worker_id(config) -> str:
    return getattr(config, "workerinput", {}).get("workerid", "local")
