from __future__ import annotations

import logging
import time

from selenium.common.exceptions import WebDriverException

from android_automation.config import AndroidDeviceSettings, AndroidSettings
from android_automation.driver_factory import create_android_driver

LOGGER = logging.getLogger(__name__)


def create_session_with_retries(settings: AndroidSettings, device: AndroidDeviceSettings):
    """按配置重试创建 driver session，降低 Appium 启动抖动影响。"""
    start_time = time.monotonic()
    attempts = settings.session_start_retries

    for attempt in range(1, attempts + 1):
        LOGGER.info(
            "Creating Appium driver session: device=%s udid=%s server=%s system_port=%s attempt=%s/%s adb=%s sdk_root=%s",
            device.name,
            device.udid,
            device.server_url or settings.server_url,
            device.system_port,
            attempt,
            attempts,
            settings.adb_path,
            settings.android_sdk_root or settings.android_home,
        )
        try:
            driver_instance = create_android_driver(settings, device)
            LOGGER.info(
                "Appium driver session created in %.2fs: session_id=%s package=%s activity=%s",
                time.monotonic() - start_time,
                driver_instance.session_id,
                driver_instance.current_package,
                driver_instance.current_activity,
            )
            return driver_instance
        except WebDriverException:
            LOGGER.exception(
                "Failed to create Appium driver session for device=%s on attempt %s/%s. "
                "Check the device Appium log under reports/<run>/logs/appium and verify the Appium process is using "
                "the same Android SDK/adb environment as framework preflight.",
                device.name,
                attempt,
                attempts,
            )
            if attempt >= attempts:
                raise
            time.sleep(settings.session_retry_backoff_seconds)

    raise RuntimeError("Appium session creation exhausted without returning a driver")
