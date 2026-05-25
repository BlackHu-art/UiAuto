from __future__ import annotations

from appium import webdriver
from appium.options.android import UiAutomator2Options

from android_automation.config import AndroidDeviceSettings, AndroidSettings


def create_android_driver(settings: AndroidSettings, device: AndroidDeviceSettings):
    """根据全局配置和设备配置组装 Appium capabilities。"""
    options = UiAutomator2Options()
    capabilities = {
        "platformName": settings.platform_name,
        "appium:automationName": settings.automation_name,
        "appium:newCommandTimeout": settings.new_command_timeout,
        "appium:adbExecTimeout": settings.adb_exec_timeout,
        "appium:noReset": settings.no_reset,
        "appium:autoGrantPermissions": settings.auto_grant_permissions,
        "appium:app": str(settings.app_path) if settings.app_path else None,
        "appium:appPackage": settings.app_package,
        "appium:appActivity": settings.app_activity,
        "appium:appWaitActivity": settings.app_wait_activity,
        "appium:deviceName": device.device_name,
        "appium:udid": device.udid,
        "appium:systemPort": device.system_port,
        "appium:chromedriverPort": device.chromedriver_port,
        "appium:mjpegServerPort": device.mjpeg_server_port,
    }
    if settings.adb_path is not None:
        capabilities["appium:adbExec"] = str(settings.adb_path)

    options.load_capabilities(
        {key: value for key, value in capabilities.items() if value not in (None, "")}
    )

    return webdriver.Remote(device.server_url or settings.server_url, options=options)
