from __future__ import annotations

import re
from dataclasses import dataclass
from dataclasses import replace

from android_automation.adb import AdbDevice, list_adb_devices, run_adb
from android_automation.config import AndroidDeviceSettings, AndroidSettings, ConfigError, select_devices
from android_automation.port_allocator import PortAllocator, PortStarts, configured_ports


@dataclass(frozen=True)
class SkippedDevice:
    name: str
    udid: str | None
    reason: str
    state: str | None = None


@dataclass(frozen=True)
class DeviceResolution:
    devices: tuple[AndroidDeviceSettings, ...]
    skipped_devices: tuple[SkippedDevice, ...]
    adb_devices: tuple[AdbDevice, ...]


def resolve_device_selection(
    settings: AndroidSettings,
    device_selectors: tuple[str, ...] | list[str] | None = None,
    *,
    all_devices: bool = False,
    connected_devices: bool = False,
    skip_offline_devices: bool = False,
) -> DeviceResolution:
    """统一解析本次运行的有效设备矩阵，确保 runner 和 pytest 使用同一套规则。"""
    if connected_devices:
        if all_devices or device_selectors:
            raise ConfigError("--connected-devices cannot be combined with --all-devices or --device")
        return _resolve_connected_devices(settings)

    selected = settings.devices if all_devices else select_devices(settings, tuple(device_selectors or ()))
    if skip_offline_devices:
        return _filter_online_configured_devices(settings, selected)

    return DeviceResolution(devices=selected, skipped_devices=(), adb_devices=())


def _resolve_connected_devices(settings: AndroidSettings) -> DeviceResolution:
    """以 adb 当前在线设备为准生成运行设备；YAML 中已知设备优先复用固定参数。"""
    adb_devices = list_adb_devices(settings)
    online_udids = tuple(sorted(device.udid for device in adb_devices if device.state == "device"))
    skipped = tuple(
        SkippedDevice(
            name=_device_name_from_udid(device.udid),
            udid=device.udid,
            reason="adb device is not ready",
            state=device.state,
        )
        for device in adb_devices
        if device.state != "device"
    )

    if not online_udids:
        visible = ", ".join(f"{device.udid}:{device.state}" for device in adb_devices) or "none"
        raise ConfigError(f"No connected Android devices are online. adb devices: {visible}")

    configured_by_udid = {
        device.udid: device
        for device in settings.devices
        if device.udid
    }
    configured_online = [
        replace(configured_by_udid[udid], source="configured")
        for udid in online_udids
        if udid in configured_by_udid
    ]

    allocator = PortAllocator(
        host=settings.appium_service.host,
        starts=PortStarts(
            appium_port=settings.device_port_defaults.appium_port_start,
            system_port=settings.device_port_defaults.system_port_start,
            chromedriver_port=settings.device_port_defaults.chromedriver_port_start,
            mjpeg_server_port=settings.device_port_defaults.mjpeg_server_port_start,
        ),
        reserved_ports=configured_ports(configured_online),
    )

    resolved: list[AndroidDeviceSettings] = []
    for udid in online_udids:
        configured_device = configured_by_udid.get(udid)
        if configured_device is not None:
            resolved.append(replace(configured_device, source="configured"))
            continue

        ports = allocator.allocate()
        resolved.append(
            AndroidDeviceSettings(
                name=_device_name_from_udid(udid),
                udid=udid,
                device_name=_device_model(settings, udid),
                appium_port=ports.appium_port,
                system_port=ports.system_port,
                chromedriver_port=ports.chromedriver_port,
                mjpeg_server_port=ports.mjpeg_server_port,
                source="discovered",
            )
        )

    return DeviceResolution(devices=tuple(resolved), skipped_devices=skipped, adb_devices=adb_devices)


def _filter_online_configured_devices(
    settings: AndroidSettings,
    selected: tuple[AndroidDeviceSettings, ...],
) -> DeviceResolution:
    """在配置设备范围内跳过离线设备，用于“配置内尽量跑在线设备”的容错模式。"""
    adb_devices = list_adb_devices(settings)
    states_by_udid = {device.udid: device.state for device in adb_devices}

    resolved: list[AndroidDeviceSettings] = []
    skipped: list[SkippedDevice] = []
    for device in selected:
        if not device.udid:
            # 未配置 UDID 的设备无法用 adb 判断在线状态，保守保留给 Appium 自行匹配。
            resolved.append(device)
            continue

        state = states_by_udid.get(device.udid)
        if state == "device":
            resolved.append(device)
            continue

        skipped.append(
            SkippedDevice(
                name=device.name,
                udid=device.udid,
                reason="configured device is not online",
                state=state or "missing",
            )
        )

    if not resolved:
        visible = ", ".join(f"{device.udid}:{device.state}" for device in adb_devices) or "none"
        raise ConfigError(f"No selected Android devices are online. adb devices: {visible}")

    return DeviceResolution(devices=tuple(resolved), skipped_devices=tuple(skipped), adb_devices=adb_devices)


def _device_model(settings: AndroidSettings, udid: str) -> str:
    result = run_adb(settings, "-s", udid, "shell", "getprop", "ro.product.model")
    model = result.stdout.strip() if result.returncode == 0 else ""
    return model or "Android"


def _device_name_from_udid(udid: str) -> str:
    if udid.startswith("emulator-"):
        return udid.replace("-", "_")

    safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", udid).strip("_")
    return f"device_{safe}" if safe else "device"
