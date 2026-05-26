from __future__ import annotations

import ctypes
import logging
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s"
DATE_FORMAT = "%H:%M:%S"
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
    """控制台按级别着色，文件日志保持纯文本。"""

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
    log_file: str | Path = "reports/logs/runner.log",
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


def write_combined_log(report_dir: str | Path) -> Path | None:
    """聚合本次运行的 runner/local/gw 日志，便于多进程执行后按时间查看。"""
    session_dir = resolve_log_session_dir(Path(report_dir) / "logs" / "runner.log")
    if not session_dir.exists():
        return None

    for handler in logging.getLogger().handlers:
        try:
            handler.flush()
        except Exception:
            pass

    records: list[tuple[str, int, int, str]] = []
    for file_index, log_file in enumerate(sorted(session_dir.glob("*.log"))):
        if log_file.name in {"combined.log", "latest-run.log"}:
            continue
        records.extend(_read_log_records(log_file, file_index))

    if not records:
        return None

    records.sort(key=lambda item: (item[0], item[1], item[2]))
    combined_text = "\n".join(record for *_prefix, record in records) + "\n"

    combined_path = session_dir / "combined.log"
    combined_path.write_text(combined_text, encoding="utf-8")

    latest_path = Path(report_dir) / "logs" / "latest-run.log"
    latest_path.parent.mkdir(parents=True, exist_ok=True)
    latest_path.write_text(combined_text, encoding="utf-8")
    return combined_path


def resolve_dated_log_path(log_file: str | Path) -> Path:
    """把日志文件统一放到 logs/YYYY-MM-DD/本次运行时间/ 目录中。"""
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
    """推导日志根目录，兼容传入文件路径或 logs 目录下的子路径。"""
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
    """按日期清理超过保留天数的日志目录。"""
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


def _read_log_records(log_file: Path, file_index: int) -> list[tuple[str, int, int, str]]:
    records: list[tuple[str, int, int, str]] = []
    current_lines: list[str] = []
    current_time = "99:99:99"
    record_index = 0

    for line in log_file.read_text(encoding="utf-8", errors="replace").splitlines():
        if _starts_log_record(line):
            if current_lines:
                records.append((current_time, file_index, record_index, "\n".join(current_lines)))
                record_index += 1
            current_time = line[:8]
            current_lines = [line]
        elif current_lines:
            current_lines.append(line)
        else:
            current_lines = [line]

    if current_lines:
        records.append((current_time, file_index, record_index, "\n".join(current_lines)))

    return records


def _starts_log_record(line: str) -> bool:
    if len(line) < 11:
        return False
    return (
        line[0:2].isdigit()
        and line[2] == ":"
        and line[3:5].isdigit()
        and line[5] == ":"
        and line[6:8].isdigit()
        and line[8:11] == " | "
    )


def _supports_color(stream) -> bool:
    if _env_value("NO_COLOR"):
        return False
    if _truthy_env("ANDROID_AUTOMATION_FORCE_COLOR") or _truthy_env("FORCE_COLOR") or _env_value("PYCHARM_HOSTED"):
        # PyCharm/IDE 控制台通常不是 TTY，但支持 ANSI 颜色。
        return True
    if not hasattr(stream, "isatty") or not stream.isatty():
        return False
    if os.name != "nt":
        return True
    return _enable_windows_ansi(stream)


def _truthy_env(name: str) -> bool:
    value = _env_value(name)
    if value is None:
        return False
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def _env_value(name: str) -> str | None:
    value = os.getenv(name)
    if value is not None:
        return value

    # 日志初始化早于项目配置加载，这里只为颜色开关轻量读取 .env。
    env_path = Path(__file__).resolve().parents[2] / ".env"
    if not env_path.exists():
        return None

    try:
        for raw_line in env_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, raw_value = line.split("=", 1)
            if key.strip() == name:
                return raw_value.strip().strip("'\"")
    except OSError:
        return None

    return None


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
