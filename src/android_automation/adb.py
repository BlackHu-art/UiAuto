from __future__ import annotations

import logging
import subprocess
from dataclasses import dataclass

from android_automation.config import AndroidDeviceSettings, AndroidSettings
from android_automation.environment import adb_command, subprocess_environment

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class AdbDevice:
    udid: str
    state: str


def list_adb_devices(settings: AndroidSettings) -> tuple[AdbDevice, ...]:
    """读取当前 adb 可见设备列表。"""
    result = run_adb(settings, "devices")
    if result.returncode != 0:
        LOGGER.warning("Unable to run adb devices: %s", result.stderr.strip())
        return ()

    devices: list[AdbDevice] = []
    for line in result.stdout.splitlines()[1:]:
        parts = line.split()
        if len(parts) >= 2:
            devices.append(AdbDevice(udid=parts[0], state=parts[1]))
    return tuple(devices)


def online_udids(settings: AndroidSettings) -> set[str]:
    """筛出状态为 device 的在线设备。"""
    return {device.udid for device in list_adb_devices(settings) if device.state == "device"}


def wait_for_device(settings: AndroidSettings, device: AndroidDeviceSettings) -> bool:
    """对指定设备执行一次 wait-for-device，减少启动瞬时抖动。"""
    if not device.udid:
        return True

    result = run_adb(settings, "-s", device.udid, "wait-for-device")
    if result.returncode != 0:
        LOGGER.warning("adb wait-for-device failed for %s: %s", device.udid, result.stderr.strip())
        return False
    return True


def describe_device(settings: AndroidSettings, device: AndroidDeviceSettings) -> dict[str, str]:
    """拉取设备型号、品牌和 Android 版本信息，便于诊断。"""
    if not device.udid:
        return {}

    props = {
        "model": "ro.product.model",
        "brand": "ro.product.brand",
        "release": "ro.build.version.release",
        "sdk": "ro.build.version.sdk",
    }
    details: dict[str, str] = {}
    for key, prop in props.items():
        result = run_adb(settings, "-s", device.udid, "shell", "getprop", prop)
        if result.returncode == 0:
            details[key] = result.stdout.strip()
    return details


def run_adb(settings: AndroidSettings, *args: str) -> subprocess.CompletedProcess[str]:
    """统一封装 adb 调用，附带超时和环境变量。"""
    command = [*adb_command(settings), *args]
    try:
        return subprocess.run(
            command,
            text=True,
            capture_output=True,
            env=subprocess_environment(settings),
            timeout=max(5, settings.adb_exec_timeout // 1000),
        )
    except OSError as exc:
        return subprocess.CompletedProcess(command, 1, "", str(exc))
    except subprocess.TimeoutExpired as exc:
        return subprocess.CompletedProcess(command, 1, exc.stdout or "", str(exc))
