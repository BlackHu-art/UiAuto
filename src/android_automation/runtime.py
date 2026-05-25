from __future__ import annotations

import os
from dataclasses import replace
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from android_automation.config import AndroidDeviceSettings, AndroidSettings, load_settings, select_devices
from android_automation.environment import android_environment


@dataclass(frozen=True)
class ExecutionContext:
    settings: AndroidSettings
    devices: tuple[AndroidDeviceSettings, ...]
    env_updates: dict[str, str]

    def apply_environment(self) -> None:
        """把解析后的 Android 环境变量注入到当前进程。"""
        os.environ.update(self.env_updates)


def load_execution_context(
    config_path: str | Path | None = None,
    device_selectors: Iterable[str] | None = None,
    *,
    all_devices: bool = False,
    validate_app: bool = True,
) -> ExecutionContext:
    """构建一次测试执行所需的统一上下文。"""
    settings = load_settings(config_path, validate_app=validate_app)
    selected_devices = settings.devices if all_devices else select_devices(settings, tuple(device_selectors or ()))
    devices = tuple(_resolve_device_server(settings, device) for device in selected_devices)
    return ExecutionContext(
        settings=settings,
        devices=devices,
        env_updates=android_environment(settings),
    )


def _resolve_device_server(settings: AndroidSettings, device: AndroidDeviceSettings) -> AndroidDeviceSettings:
    """为每台设备补齐最终使用的 Appium server 地址。"""
    if device.server_url:
        return device

    if settings.appium_service.manage_servers:
        server_url = f"http://{settings.appium_service.host}:{device.appium_port}"
        return replace(device, server_url=server_url)

    return replace(device, server_url=settings.server_url)
