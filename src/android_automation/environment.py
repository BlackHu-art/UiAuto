from __future__ import annotations

import os
from pathlib import Path

from android_automation.config import AndroidSettings


def android_environment(settings: AndroidSettings) -> dict[str, str]:
    """生成 Android 相关环境变量，供当前进程和子进程共享。"""
    env_updates: dict[str, str] = {}

    if settings.adb_path is not None:
        env_updates["PATH"] = _prepend_path(settings.adb_path.parent)

    if settings.android_sdk_root is not None:
        env_updates["ANDROID_SDK_ROOT"] = str(settings.android_sdk_root)
    if settings.android_home is not None:
        env_updates["ANDROID_HOME"] = str(settings.android_home)

    return env_updates


def subprocess_environment(settings: AndroidSettings) -> dict[str, str]:
    """子进程环境基于当前环境复制后再叠加 Android 配置。"""
    env = os.environ.copy()
    env.update(android_environment(settings))
    return env


def adb_command(settings: AndroidSettings) -> list[str]:
    """优先使用显式配置的 adb 路径，否则退回系统 PATH 中的 adb。"""
    return [str(settings.adb_path)] if settings.adb_path else ["adb"]


def _prepend_path(path: Path) -> str:
    existing = os.environ.get("PATH", "")
    parts = [str(path), existing] if existing else [str(path)]
    return os.pathsep.join(parts)
