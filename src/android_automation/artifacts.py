from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any

from android_automation.config import AndroidDeviceSettings, AndroidSettings


def safe_path(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value).strip("_") or "item"


def write_run_metadata(
    report_dir: Path,
    settings: AndroidSettings,
    devices: tuple[AndroidDeviceSettings, ...],
    pytest_args: list[str],
) -> None:
    """记录本次运行的参数与设备清单，便于复盘。"""
    metadata_dir = report_dir / "metadata"
    metadata_dir.mkdir(parents=True, exist_ok=True)
    (metadata_dir / "pytest_args.txt").write_text(" ".join(pytest_args), encoding="utf-8")
    (metadata_dir / "devices.json").write_text(
        json.dumps(_device_metadata(settings, devices), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def write_allure_environment(
    allure_results_dir: Path,
    settings: AndroidSettings,
    devices: tuple[AndroidDeviceSettings, ...],
) -> None:
    """为 Allure 写入环境信息。"""
    allure_results_dir.mkdir(parents=True, exist_ok=True)
    (allure_results_dir / "environment.properties").write_text(
        "\n".join(
            [
                "platform=Android",
                f"appPackage={settings.app_package or ''}",
                f"appActivity={settings.app_activity or ''}",
                f"appiumServer={settings.server_url}",
                f"selectedDevices={','.join(device.name for device in devices)}",
                f"python={sys.version.split()[0]}",
            ]
        ),
        encoding="utf-8",
    )


def split_allure_results_by_device(
    allure_results_dir: Path,
    settings: AndroidSettings,
    devices: tuple[AndroidDeviceSettings, ...],
) -> dict[str, Path]:
    """把混合的 Allure 原始结果按设备拆分，生成独立报告输入目录。"""
    if not allure_results_dir.exists():
        return {}

    device_result_dirs: dict[str, Path] = {}
    uuid_to_device: dict[str, str] = {}
    copied_files: dict[str, set[str]] = {device.name: set() for device in devices}

    for device in devices:
        device_dir = allure_results_dir.parent / f"allure-results-{safe_path(device.name)}"
        if device_dir.exists():
            shutil.rmtree(device_dir)
        device_dir.mkdir(parents=True, exist_ok=True)
        device_result_dirs[device.name] = device_dir

    result_files = sorted(allure_results_dir.glob("*-result.json"))
    for result_file in result_files:
        # result 文件里携带设备参数，可以直接作为拆分依据。
        data = _read_json(result_file)
        device_name = _device_name_from_result(data)
        if not device_name or device_name not in device_result_dirs:
            continue

        _copy_once(result_file, device_result_dirs[device_name], copied_files[device_name])
        if result_uuid := data.get("uuid"):
            uuid_to_device[str(result_uuid)] = device_name

        for attachment in data.get("attachments", []):
            source = attachment.get("source")
            if isinstance(source, str):
                _copy_named_file(allure_results_dir, source, device_result_dirs[device_name], copied_files[device_name])

    for container_file in sorted(allure_results_dir.glob("*-container.json")):
        # container 通过 children -> result uuid 关联到具体设备。
        data = _read_json(container_file)
        device_name = _device_name_from_container(data, uuid_to_device)
        if not device_name or device_name not in device_result_dirs:
            continue

        _copy_once(container_file, device_result_dirs[device_name], copied_files[device_name])
        for attachment_name in _container_attachment_sources(data):
            _copy_named_file(allure_results_dir, attachment_name, device_result_dirs[device_name], copied_files[device_name])

    for device in devices:
        write_allure_environment(device_result_dirs[device.name], settings, (device,))

    return device_result_dirs


def capture_failure_artifacts(driver_instance, report_dir: Path, device_name: str, nodeid: str, worker_id: str) -> None:
    """失败时同时保留截图和页面源码。"""
    safe_nodeid = safe_path(nodeid)
    safe_device = safe_path(device_name)
    _capture_screenshot(driver_instance, report_dir, safe_device, safe_nodeid, worker_id)
    _capture_page_source(driver_instance, report_dir, safe_device, safe_nodeid, worker_id)


def attach_session_metadata(driver_instance, device: AndroidDeviceSettings | None, nodeid: str, worker_id: str) -> None:
    """把 session 元数据挂到 Allure，便于问题回溯。"""
    import allure

    metadata: dict[str, Any] = {
        "nodeid": nodeid,
        "worker_id": worker_id,
        "device": getattr(device, "name", None),
        "udid": getattr(device, "udid", None),
        "session_id": driver_instance.session_id,
        "current_package": driver_instance.current_package,
        "current_activity": driver_instance.current_activity,
        "capabilities": driver_instance.capabilities,
    }
    allure.attach(
        json.dumps(metadata, ensure_ascii=False, indent=2, default=str),
        name="session_metadata",
        attachment_type=allure.attachment_type.JSON,
    )


def _capture_screenshot(driver_instance, report_dir: Path, safe_device: str, safe_nodeid: str, worker_id: str) -> None:
    import allure

    screenshot = driver_instance.get_screenshot_as_png()
    screenshots_dir = report_dir / "screenshots" / safe_device / worker_id
    screenshots_dir.mkdir(parents=True, exist_ok=True)
    screenshot_path = screenshots_dir / f"{safe_nodeid}.png"
    screenshot_path.write_bytes(screenshot)
    allure.attach(screenshot, name="failure_screenshot", attachment_type=allure.attachment_type.PNG)


def _capture_page_source(driver_instance, report_dir: Path, safe_device: str, safe_nodeid: str, worker_id: str) -> None:
    import allure

    page_source = driver_instance.page_source
    page_sources_dir = report_dir / "page_sources" / safe_device / worker_id
    page_sources_dir.mkdir(parents=True, exist_ok=True)
    page_source_path = page_sources_dir / f"{safe_nodeid}.xml"
    page_source_path.write_text(page_source, encoding="utf-8")
    allure.attach(page_source, name="page_source", attachment_type=allure.attachment_type.XML)


def _device_metadata(settings: AndroidSettings, devices: tuple[AndroidDeviceSettings, ...]) -> list[dict[str, Any]]:
    return [
        {
            "name": device.name,
            "udid": device.udid,
            "device_name": device.device_name,
            "server_url": device.server_url or settings.server_url,
            "appium_port": device.appium_port,
            "system_port": device.system_port,
            "chromedriver_port": device.chromedriver_port,
            "mjpeg_server_port": device.mjpeg_server_port,
        }
        for device in devices
    ]


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _device_name_from_result(data: dict[str, Any]) -> str | None:
    for parameter in data.get("parameters", []):
        if parameter.get("name") != "device_settings":
            continue
        value = parameter.get("value")
        if not isinstance(value, str):
            return None
        match = re.search(r"name='([^']+)'", value)
        if match:
            return match.group(1)
    test_name = data.get("name")
    if isinstance(test_name, str):
        match = re.search(r"\[([^\]]+)\]$", test_name)
        if match:
            return match.group(1)
    return None


def _device_name_from_container(data: dict[str, Any], uuid_to_device: dict[str, str]) -> str | None:
    for child in data.get("children", []):
        device_name = uuid_to_device.get(str(child))
        if device_name:
            return device_name
    return None


def _container_attachment_sources(data: dict[str, Any]) -> list[str]:
    sources: list[str] = []
    for fixture_section in ("befores", "afters"):
        for item in data.get(fixture_section, []):
            for attachment in item.get("attachments", []):
                source = attachment.get("source")
                if isinstance(source, str):
                    sources.append(source)
    return sources


def _copy_named_file(source_dir: Path, file_name: str, target_dir: Path, copied_files: set[str]) -> None:
    source_path = source_dir / file_name
    if source_path.exists():
        _copy_once(source_path, target_dir, copied_files)


def _copy_once(source_path: Path, target_dir: Path, copied_files: set[str]) -> None:
    if source_path.name in copied_files:
        return
    shutil.copy2(source_path, target_dir / source_path.name)
    copied_files.add(source_path.name)
