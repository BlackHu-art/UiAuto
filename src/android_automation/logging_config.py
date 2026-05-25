from __future__ import annotations

import logging
import os
import shutil
import sys
import ctypes
from datetime import datetime
from pathlib import Path

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
DEFAULT_LOG_RETENTION_DAYS = 7

LEVEL_COLORS = {
    logging.DEBUG: "\033[36m",
    logging.INFO: "\033[32m",
    logging.WARNING: "\033[33m",
    logging.ERROR: "\033[31m",
    logging.CRITICAL: "\033[35m",
}
RESET_COLOR = "\033[0m"
LOG_SESSION_DIR_ENV = "ANDROID_AUTOMATION_LOG_SESSION_DIR"
_WINDOWS_ANSI_ENABLED: bool | None = None


class ColorFormatter(logging.Formatter):
    """控制台输出使用彩色日志级别，便于快速定位异常。"""

    def format(self, record: logging.LogRecord) -> str:
        original_levelname = record.levelname
        color = LEVEL_COLORS.get(record.levelno, "")
        if color and _supports_color(sys.stdout):
            record.levelname = f"{color}{record.levelname}{RESET_COLOR}"
        try:
            return super().format(record)
        finally:
            record.levelname = original_levelname


def setup_logging(
    level: str = "INFO",
    log_file: str | Path = "reports/logs/master.log",
    retention_days: int = DEFAULT_LOG_RETENTION_DAYS,
) -> None:
    """初始化控制台与文件日志，并按日期整理日志目录。"""
    root = logging.getLogger()
    root.setLevel(level.upper())

    console_formatter = ColorFormatter(LOG_FORMAT, DATE_FORMAT)
    file_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)

    stream_handler_exists = False
    for handler in root.handlers:
        if isinstance(handler, logging.StreamHandler) and handler.stream is sys.stdout:
            handler.setFormatter(console_formatter)
            stream_handler_exists = True
    if not stream_handler_exists:
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(console_formatter)
        root.addHandler(stream_handler)

    retention_days = _retention_days_from_env(retention_days)
    dated_log_path = resolve_dated_log_path(log_file)
    dated_log_path.parent.mkdir(parents=True, exist_ok=True)
    cleanup_old_log_directories(log_root_for(log_file), retention_days)

    resolved_log_path = dated_log_path.resolve()
    existing_file_handler = None
    for handler in root.handlers:
        if not isinstance(handler, logging.FileHandler):
            continue
        handler_path = Path(handler.baseFilename).resolve()
        if handler_path == resolved_log_path:
            existing_file_handler = handler
            continue
        root.removeHandler(handler)
        handler.close()

    if existing_file_handler is not None:
        existing_file_handler.setFormatter(file_formatter)
        return

    file_handler = logging.FileHandler(dated_log_path, encoding="utf-8")
    file_handler.setFormatter(file_formatter)
    root.addHandler(file_handler)


def resolve_dated_log_path(log_file: str | Path) -> Path:
    """把日志文件统一放到 logs/YYYY-MM-DD/本次运行时间/ 目录下。"""
    path = Path(log_file)
    return resolve_log_session_dir(path) / path.name


def initialize_log_session(log_file: str | Path, reset: bool = False) -> Path:
    """初始化一次运行的日志目录，供 runner、pytest 和 Appium 子进程共用。"""
    return resolve_log_session_dir(log_file, reset=reset)


def resolve_log_session_dir(log_file: str | Path, reset: bool = False) -> Path:
    logs_root = log_root_for(log_file)
    existing = os.getenv(LOG_SESSION_DIR_ENV)
    if existing and not reset:
        session_dir = Path(existing)
        session_dir.mkdir(parents=True, exist_ok=True)
        return session_dir

    date_dir = logs_root / current_log_date()
    date_dir.mkdir(parents=True, exist_ok=True)

    stamp = datetime.now().strftime("%H%M%S")
    session_dir = date_dir / stamp
    index = 1
    while session_dir.exists():
        session_dir = date_dir / f"{stamp}_{index:02d}"
        index += 1

    session_dir.mkdir(parents=True, exist_ok=True)
    os.environ[LOG_SESSION_DIR_ENV] = str(session_dir)
    return session_dir


def log_root_for(log_file: str | Path) -> Path:
    """推导日志根目录，兼容传入文件路径或 logs 目录下的任意子路径。"""
    path = Path(log_file)
    if path.parent.name == "logs":
        return path.parent
    if "logs" in path.parts:
        parts = path.parts
        logs_index = parts.index("logs")
        return Path(*parts[: logs_index + 1])
    return path.parent / "logs"


def current_log_date() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def cleanup_old_log_directories(logs_root: Path, retention_days: int) -> None:
    """按日期清理超出保留天数的日志目录。"""
    if retention_days < 1 or not logs_root.exists():
        return

    cutoff = datetime.now().date()
    for child in logs_root.iterdir():
        if not child.is_dir():
            continue
        try:
            log_date = datetime.strptime(child.name, "%Y-%m-%d").date()
        except ValueError:
            continue
        if (cutoff - log_date).days >= retention_days:
            shutil.rmtree(child, ignore_errors=True)


def _supports_color(stream) -> bool:
    if not hasattr(stream, "isatty") or not stream.isatty():
        return False
    if os.name != "nt":
        return True
    return _enable_windows_ansi(stream)


def _retention_days_from_env(default_value: int) -> int:
    raw_value = os.getenv("ANDROID_AUTOMATION_LOG_RETENTION_DAYS")
    if raw_value is None:
        return default_value
    try:
        return max(1, int(raw_value))
    except ValueError:
        return default_value


def _enable_windows_ansi(stream) -> bool:
    global _WINDOWS_ANSI_ENABLED
    if _WINDOWS_ANSI_ENABLED is not None:
        return _WINDOWS_ANSI_ENABLED

    try:
        std_handle = -11 if stream is sys.stdout else -12
        handle = ctypes.windll.kernel32.GetStdHandle(std_handle)
        if handle in (0, -1):
            _WINDOWS_ANSI_ENABLED = False
            return False

        mode = ctypes.c_uint()
        if not ctypes.windll.kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            _WINDOWS_ANSI_ENABLED = False
            return False

        enable_virtual_terminal_processing = 0x0004
        if mode.value & enable_virtual_terminal_processing:
            _WINDOWS_ANSI_ENABLED = True
            return True

        success = ctypes.windll.kernel32.SetConsoleMode(
            handle,
            mode.value | enable_virtual_terminal_processing,
        )
        _WINDOWS_ANSI_ENABLED = bool(success)
        return _WINDOWS_ANSI_ENABLED
    except Exception:
        _WINDOWS_ANSI_ENABLED = False
        return False
