from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "config" / "appium.yaml"


class ConfigError(RuntimeError):
    pass


@dataclass(frozen=True)
class AppiumServiceSettings:
    manage_servers: bool
    reuse_existing_servers: bool
    cleanup_stale_servers: bool
    host: str
    base_port: int
    start_timeout_seconds: int
    startup_poll_interval_seconds: int
    stop_timeout_seconds: int
    executable: Path | None


@dataclass(frozen=True)
class DevicePortDefaults:
    appium_port_start: int
    system_port_start: int
    chromedriver_port_start: int
    mjpeg_server_port_start: int


@dataclass(frozen=True)
class AndroidDeviceSettings:
    name: str
    udid: str | None
    device_name: str
    appium_port: int
    system_port: int
    chromedriver_port: int | None
    mjpeg_server_port: int | None
    server_url: str | None = None
    source: str = "configured"


@dataclass(frozen=True)
class AndroidSettings:
    server_url: str
    platform_name: str
    automation_name: str
    app_path: Path | None
    app_package: str | None
    app_activity: str | None
    app_wait_activity: str | None
    no_reset: bool
    auto_grant_permissions: bool
    new_command_timeout: int
    adb_exec_timeout: int
    session_start_retries: int
    session_retry_backoff_seconds: int
    adb_path: Path | None
    android_sdk_root: Path | None
    android_home: Path | None
    smoke_accessibility_id: str | None
    appium_service: AppiumServiceSettings
    device_port_defaults: DevicePortDefaults
    devices: tuple[AndroidDeviceSettings, ...]


def load_settings(config_path: Path | str | None = None, validate_app: bool = True) -> AndroidSettings:
    """加载 YAML 与 .env，并构建框架运行所需的完整设置对象。"""
    _load_dotenv()

    path = _resolve_config_path(config_path)
    data = _load_yaml(path)
    android = data.get("android", {})
    smoke = data.get("smoke", {})
    appium = data.get("appium", {})
    appium_service = _load_appium_service_settings(appium)
    device_port_defaults = _load_device_port_defaults(data, android, appium_service)

    app_value = _env_or_default("ANDROID_APP_PATH", android.get("app", ""))
    settings = AndroidSettings(
        server_url=_env_or_default("APPIUM_SERVER_URL", data.get("server_url", "http://127.0.0.1:4723")),
        platform_name=_env_or_default("ANDROID_PLATFORM_NAME", android.get("platform_name", "Android")),
        automation_name=_env_or_default("ANDROID_AUTOMATION_NAME", android.get("automation_name", "UiAutomator2")),
        app_path=_resolve_optional_path(app_value),
        app_package=_blank_to_none(_env_or_default("ANDROID_APP_PACKAGE", android.get("app_package", ""))),
        app_activity=_blank_to_none(_env_or_default("ANDROID_APP_ACTIVITY", android.get("app_activity", ""))),
        app_wait_activity=_blank_to_none(_env_or_default("ANDROID_APP_WAIT_ACTIVITY", android.get("app_wait_activity", ""))),
        no_reset=_to_bool(_env_or_default("ANDROID_NO_RESET", android.get("no_reset", False))),
        auto_grant_permissions=_to_bool(
            _env_or_default("ANDROID_AUTO_GRANT_PERMISSIONS", android.get("auto_grant_permissions", True))
        ),
        new_command_timeout=_to_int(
            _env_or_default("ANDROID_NEW_COMMAND_TIMEOUT", android.get("new_command_timeout", 120))
        ),
        adb_exec_timeout=_to_int(
            _env_or_default("ANDROID_ADB_EXEC_TIMEOUT", android.get("adb_exec_timeout", 60000))
        ),
        session_start_retries=_to_int(
            _env_or_default("ANDROID_SESSION_START_RETRIES", android.get("session_start_retries", 3))
        ),
        session_retry_backoff_seconds=_to_int(
            _env_or_default(
                "ANDROID_SESSION_RETRY_BACKOFF_SECONDS",
                android.get("session_retry_backoff_seconds", 5),
            )
        ),
        adb_path=_resolve_optional_path(_env_or_default("ANDROID_ADB_PATH", "")),
        android_sdk_root=_resolve_optional_path(_env_or_default("ANDROID_SDK_ROOT", "")),
        android_home=_resolve_optional_path(_env_or_default("ANDROID_HOME", "")),
        smoke_accessibility_id=_blank_to_none(
            _env_or_default("SMOKE_ACCESSIBILITY_ID", smoke.get("accessibility_id", ""))
        ),
        appium_service=appium_service,
        device_port_defaults=device_port_defaults,
        devices=_load_devices(android, appium_service),
    )

    _validate_settings(settings, validate_app=validate_app)
    return settings


def select_devices(settings: AndroidSettings, selectors: list[str] | tuple[str, ...] | None) -> tuple[AndroidDeviceSettings, ...]:
    """根据命令行选择器过滤设备；未传时默认执行全部配置设备。"""
    if not selectors:
        return settings.devices

    selected: list[AndroidDeviceSettings] = []
    missing: list[str] = []

    for selector in selectors:
        device = next(
            (candidate for candidate in settings.devices if selector in {candidate.name, candidate.udid}),
            None,
        )
        if device is None:
            missing.append(selector)
        elif device not in selected:
            selected.append(device)

    if missing:
        available = ", ".join(_device_label(device) for device in settings.devices)
        raise ConfigError(f"Unknown device selector(s): {', '.join(missing)}. Available devices: {available}")

    return tuple(selected)


def _resolve_config_path(config_path: Path | str | None) -> Path:
    if config_path is None:
        return DEFAULT_CONFIG_PATH

    path = Path(config_path)
    if not path.is_absolute():
        path = PROJECT_ROOT / path

    return path.resolve()


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise ConfigError(f"Config file not found: {path}")

    try:
        import yaml
    except ModuleNotFoundError as exc:
        raise ConfigError(
            "Missing dependency PyYAML. Install project dependencies with: python -m pip install -r requirements.txt"
        ) from exc

    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}

    if not isinstance(data, dict):
        raise ConfigError(f"Config file must contain a YAML mapping: {path}")

    return data


def _load_dotenv() -> None:
    try:
        from dotenv import load_dotenv
    except ModuleNotFoundError:
        _load_simple_env(PROJECT_ROOT / ".env")
        return

    load_dotenv(PROJECT_ROOT / ".env")


def _load_simple_env(path: Path) -> None:
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        name, value = line.split("=", 1)
        os.environ.setdefault(name.strip(), value.strip().strip("'\""))


def _load_appium_service_settings(appium: dict[str, Any]) -> AppiumServiceSettings:
    """读取 Appium 服务托管配置。"""
    if not isinstance(appium, dict):
        raise ConfigError("appium must be a mapping")

    return AppiumServiceSettings(
        manage_servers=_to_bool(_env_or_default("APPIUM_MANAGE_SERVERS", appium.get("manage_servers", True))),
        reuse_existing_servers=_to_bool(
            _env_or_default("APPIUM_REUSE_EXISTING_SERVERS", appium.get("reuse_existing_servers", False))
        ),
        cleanup_stale_servers=_to_bool(
            _env_or_default("APPIUM_CLEANUP_STALE_SERVERS", appium.get("cleanup_stale_servers", True))
        ),
        host=_blank_to_none(_env_or_default("APPIUM_HOST", appium.get("host", "127.0.0.1"))) or "127.0.0.1",
        base_port=_to_port(_env_or_default("APPIUM_BASE_PORT", appium.get("base_port", 4723)), "APPIUM_BASE_PORT"),
        start_timeout_seconds=_to_int(
            _env_or_default("APPIUM_START_TIMEOUT_SECONDS", appium.get("start_timeout_seconds", 30))
        ),
        startup_poll_interval_seconds=_to_int(
            _env_or_default(
                "APPIUM_STARTUP_POLL_INTERVAL_SECONDS",
                appium.get("startup_poll_interval_seconds", 1),
            )
        ),
        stop_timeout_seconds=_to_int(
            _env_or_default("APPIUM_STOP_TIMEOUT_SECONDS", appium.get("stop_timeout_seconds", 10))
        ),
        executable=_resolve_optional_path(_env_or_default("APPIUM_EXECUTABLE", appium.get("executable", ""))),
    )


def _load_device_port_defaults(
    data: dict[str, Any],
    android: dict[str, Any],
    appium_service: AppiumServiceSettings,
) -> DevicePortDefaults:
    """读取动态发现设备的端口池起点；未配置时沿用当前项目默认端口。"""
    raw_defaults = data.get("device_defaults") or android.get("device_defaults") or {}
    if not isinstance(raw_defaults, dict):
        raise ConfigError("device_defaults must be a mapping")

    return DevicePortDefaults(
        appium_port_start=_to_port(
            _env_or_default(
                "ANDROID_APPIUM_PORT_START",
                raw_defaults.get("appium_port_start", appium_service.base_port),
            ),
            "ANDROID_APPIUM_PORT_START",
        ),
        system_port_start=_to_port(
            _env_or_default("ANDROID_SYSTEM_PORT_START", raw_defaults.get("system_port_start", 8200)),
            "ANDROID_SYSTEM_PORT_START",
        ),
        chromedriver_port_start=_to_port(
            _env_or_default(
                "ANDROID_CHROMEDRIVER_PORT_START",
                raw_defaults.get("chromedriver_port_start", 9515),
            ),
            "ANDROID_CHROMEDRIVER_PORT_START",
        ),
        mjpeg_server_port_start=_to_port(
            _env_or_default(
                "ANDROID_MJPEG_SERVER_PORT_START",
                raw_defaults.get("mjpeg_server_port_start", 7810),
            ),
            "ANDROID_MJPEG_SERVER_PORT_START",
        ),
    )


def _load_devices(
    android: dict[str, Any],
    appium_service: AppiumServiceSettings,
) -> tuple[AndroidDeviceSettings, ...]:
    """构建设备矩阵，支持单设备环境变量覆盖和多设备 YAML 配置。"""
    env_udid = _blank_to_none(os.getenv("ANDROID_UDID"))
    env_device_name = _blank_to_none(os.getenv("ANDROID_DEVICE_NAME"))
    env_appium_port = _blank_to_none(os.getenv("ANDROID_APPIUM_PORT") or os.getenv("APPIUM_PORT"))
    env_system_port = _blank_to_none(os.getenv("ANDROID_SYSTEM_PORT"))
    env_chromedriver_port = _blank_to_none(os.getenv("ANDROID_CHROMEDRIVER_PORT"))
    env_mjpeg_server_port = _blank_to_none(os.getenv("ANDROID_MJPEG_SERVER_PORT"))

    if any([env_udid, env_device_name, env_appium_port, env_system_port, env_chromedriver_port, env_mjpeg_server_port]):
        return (
            AndroidDeviceSettings(
                name=_safe_device_name(env_udid or env_device_name or "android"),
                udid=env_udid,
                device_name=env_device_name or android.get("device_name", "Android"),
                appium_port=_to_port(
                    env_appium_port or android.get("appium_port") or appium_service.base_port,
                    "ANDROID_APPIUM_PORT",
                ),
                system_port=_to_port(env_system_port or android.get("system_port") or 8200, "ANDROID_SYSTEM_PORT"),
                chromedriver_port=_optional_port(
                    env_chromedriver_port or android.get("chromedriver_port") or 9515,
                    "ANDROID_CHROMEDRIVER_PORT",
                ),
                mjpeg_server_port=_optional_port(
                    env_mjpeg_server_port or android.get("mjpeg_server_port") or 7810,
                    "ANDROID_MJPEG_SERVER_PORT",
                ),
                server_url=_blank_to_none(android.get("server_url")),
            ),
        )

    raw_devices = android.get("devices") or []
    if not raw_devices:
        raw_devices = [
            {
                "name": android.get("name") or _safe_device_name(android.get("udid") or android.get("device_name") or "android"),
                "udid": android.get("udid", ""),
                "device_name": android.get("device_name", "Android"),
                "appium_port": android.get("appium_port"),
                "system_port": android.get("system_port"),
                "chromedriver_port": android.get("chromedriver_port"),
                "mjpeg_server_port": android.get("mjpeg_server_port"),
                "server_url": android.get("server_url"),
            }
        ]

    if not isinstance(raw_devices, list):
        raise ConfigError("android.devices must be a list")

    devices: list[AndroidDeviceSettings] = []
    for index, raw_device in enumerate(raw_devices):
        if not isinstance(raw_device, dict):
            raise ConfigError("Each android.devices entry must be a mapping")

        name = _blank_to_none(raw_device.get("name")) or _safe_device_name(
            raw_device.get("udid") or raw_device.get("device_name") or f"android_{index + 1}"
        )
        device = AndroidDeviceSettings(
            name=name,
            udid=_blank_to_none(raw_device.get("udid")),
            device_name=_blank_to_none(raw_device.get("device_name")) or "Android",
            appium_port=_to_port(
                raw_device.get("appium_port") or appium_service.base_port + index,
                f"{name}.appium_port",
            ),
            system_port=_to_port(raw_device.get("system_port") or 8200 + index, f"{name}.system_port"),
            chromedriver_port=_optional_port(
                raw_device.get("chromedriver_port") or 9515 + index,
                f"{name}.chromedriver_port",
            ),
            mjpeg_server_port=_optional_port(
                raw_device.get("mjpeg_server_port") or 7810 + index,
                f"{name}.mjpeg_server_port",
            ),
            server_url=_blank_to_none(raw_device.get("server_url")),
        )
        devices.append(device)

    return tuple(devices)


def _env_or_default(name: str, default: Any) -> Any:
    value = os.getenv(name)
    return default if value is None else value


def _blank_to_none(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _resolve_optional_path(value: Any) -> Path | None:
    text = _blank_to_none(value)
    if text is None:
        return None

    path = Path(text)
    if not path.is_absolute():
        path = PROJECT_ROOT / path

    return path.resolve()


def _to_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value

    text = str(value).strip().lower()
    if text in {"1", "true", "yes", "y", "on"}:
        return True
    if text in {"0", "false", "no", "n", "off"}:
        return False

    raise ConfigError(f"Invalid boolean value: {value!r}")


def _to_int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise ConfigError(f"Invalid integer value: {value!r}") from exc


def _to_port(value: Any, name: str) -> int:
    port = _to_int(value)
    if not 1 <= port <= 65535:
        raise ConfigError(f"{name} must be between 1 and 65535: {port}")
    return port


def _optional_port(value: Any, name: str) -> int | None:
    if _blank_to_none(value) is None:
        return None
    return _to_port(value, name)


def _safe_device_name(value: Any) -> str:
    text = _blank_to_none(value) or "android"
    return "".join(char if char.isalnum() else "_" for char in text).strip("_") or "android"


def _validate_settings(settings: AndroidSettings, validate_app: bool = True) -> None:
    """启动前统一校验配置完整性，尽早暴露问题。"""
    if validate_app:
        if settings.app_path:
            if not settings.app_path.exists():
                raise ConfigError(
                    f"APK not found: {settings.app_path}. Put your APK there or set ANDROID_APP_PATH in .env."
                )
        elif not (settings.app_package and settings.app_activity):
            raise ConfigError(
                "Set ANDROID_APP_PATH for an APK, or set both ANDROID_APP_PACKAGE and ANDROID_APP_ACTIVITY for an installed app."
            )

    if not settings.devices:
        raise ConfigError("Configure at least one Android device in config/appium.yaml")

    if settings.session_start_retries < 1:
        raise ConfigError("ANDROID_SESSION_START_RETRIES must be at least 1")
    if settings.session_retry_backoff_seconds < 0:
        raise ConfigError("ANDROID_SESSION_RETRY_BACKOFF_SECONDS must be 0 or greater")
    if settings.appium_service.start_timeout_seconds < 1:
        raise ConfigError("APPIUM_START_TIMEOUT_SECONDS must be at least 1")
    if settings.appium_service.startup_poll_interval_seconds < 1:
        raise ConfigError("APPIUM_STARTUP_POLL_INTERVAL_SECONDS must be at least 1")
    if settings.appium_service.stop_timeout_seconds < 1:
        raise ConfigError("APPIUM_STOP_TIMEOUT_SECONDS must be at least 1")

    _validate_unique("device name", [device.name for device in settings.devices])
    _validate_unique("device udid", [device.udid for device in settings.devices if device.udid])
    _validate_unique("appium_port", [str(device.appium_port) for device in settings.devices])
    _validate_unique("system_port", [str(device.system_port) for device in settings.devices])
    _validate_unique(
        "chromedriver_port",
        [str(device.chromedriver_port) for device in settings.devices if device.chromedriver_port],
    )
    _validate_unique(
        "mjpeg_server_port",
        [str(device.mjpeg_server_port) for device in settings.devices if device.mjpeg_server_port],
    )


def _validate_unique(label: str, values: list[str]) -> None:
    duplicates = sorted({value for value in values if values.count(value) > 1})
    if duplicates:
        raise ConfigError(f"Duplicate {label}: {', '.join(duplicates)}")


def _device_label(device: AndroidDeviceSettings) -> str:
    return f"{device.name}" + (f" ({device.udid})" if device.udid else "")
