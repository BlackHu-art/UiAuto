from __future__ import annotations

import logging
import os
import shutil
import socket
import subprocess
import time
from dataclasses import dataclass
from io import TextIOWrapper
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

from android_automation.config import AndroidDeviceSettings, AndroidSettings, ConfigError
from android_automation.environment import subprocess_environment
from android_automation.logging_config import resolve_log_session_dir

LOGGER = logging.getLogger(__name__)


@dataclass
class ManagedAppiumServer:
    device: AndroidDeviceSettings
    process: subprocess.Popen[str]
    log_file: Path
    log_handle: TextIOWrapper

    def stop(self, timeout_seconds: int) -> None:
        if self.process.poll() is not None:
            LOGGER.info(
                "Appium 服务进程已退出，无需重复关闭: device=%s log=%s",
                self.device.name,
                self.log_file,
            )
            self.log_handle.close()
            return

        LOGGER.info("开始关闭 Appium 服务: device=%s pid=%s log=%s", self.device.name, self.process.pid, self.log_file)
        self.process.terminate()
        try:
            self.process.wait(timeout=timeout_seconds)
            LOGGER.info("Appium 服务已正常关闭: device=%s pid=%s", self.device.name, self.process.pid)
        except subprocess.TimeoutExpired:
            LOGGER.warning("Appium 服务超时未退出，准备强制结束: device=%s pid=%s", self.device.name, self.process.pid)
            self.process.kill()
            self.process.wait(timeout=timeout_seconds)
            LOGGER.info("Appium 服务已强制关闭: device=%s pid=%s", self.device.name, self.process.pid)
        finally:
            self.log_handle.close()


@dataclass
class ManagedAppiumCluster:
    servers: tuple[ManagedAppiumServer, ...]

    def stop(self, timeout_seconds: int) -> None:
        for server in reversed(self.servers):
            try:
                server.stop(timeout_seconds)
            except Exception:
                LOGGER.warning("Failed to stop Appium server cleanly for %s", server.device.name, exc_info=True)


def start_managed_appium_servers(
    settings: AndroidSettings,
    devices: tuple[AndroidDeviceSettings, ...],
    report_dir: Path,
) -> ManagedAppiumCluster:
    if not settings.appium_service.manage_servers:
        LOGGER.info("当前配置禁用 Appium 托管，跳过服务启动。")
        return ManagedAppiumCluster(())

    executable = _appium_executable(settings)
    servers: list[ManagedAppiumServer] = []
    logs_dir = resolve_log_session_dir(report_dir / "logs" / "runner.log") / "appium"
    logs_dir.mkdir(parents=True, exist_ok=True)

    try:
        for device in devices:
            if not _is_local_server(device.server_url, device.appium_port):
                LOGGER.info("设备使用外部 Appium 服务，跳过托管: device=%s server=%s", device.name, device.server_url)
                continue

            if _server_reachable(device.server_url or ""):
                if settings.appium_service.reuse_existing_servers:
                    LOGGER.info("复用已有 Appium 服务: device=%s server=%s", device.name, device.server_url)
                    continue
                if settings.appium_service.cleanup_stale_servers:
                    _cleanup_existing_local_server(settings, device)
                else:
                    raise ConfigError(
                        f"Appium server already running for {device.name} at {device.server_url}. "
                        "Stop the existing process or set APPIUM_REUSE_EXISTING_SERVERS=true to reuse it intentionally."
                    )

            _ensure_port_available(settings, device)
            server = _start_single_server(settings, device, executable, logs_dir)
            servers.append(server)
            _wait_for_server_ready(settings, server)
        return ManagedAppiumCluster(tuple(servers))
    except Exception:
        ManagedAppiumCluster(tuple(servers)).stop(settings.appium_service.stop_timeout_seconds)
        raise


def _start_single_server(
    settings: AndroidSettings,
    device: AndroidDeviceSettings,
    executable: str,
    logs_dir: Path,
) -> ManagedAppiumServer:
    log_file = logs_dir / f"{device.name}.log"
    log_handle = log_file.open("w", encoding="utf-8")
    command = [
        executable,
        "--address",
        settings.appium_service.host,
        "--port",
        str(device.appium_port),
        "--base-path",
        "/",
        "--log-timestamp",
    ]
    LOGGER.info(
        "启动 Appium 服务: device=%s port=%s log=%s command=%s",
        device.name,
        device.appium_port,
        log_file,
        " ".join(command),
    )
    process = subprocess.Popen(
        command,
        stdout=log_handle,
        stderr=subprocess.STDOUT,
        text=True,
        env=subprocess_environment(settings),
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    return ManagedAppiumServer(device=device, process=process, log_file=log_file, log_handle=log_handle)


def _wait_for_server_ready(settings: AndroidSettings, server: ManagedAppiumServer) -> None:
    deadline = time.monotonic() + settings.appium_service.start_timeout_seconds
    poll_interval = settings.appium_service.startup_poll_interval_seconds
    server_url = server.device.server_url or ""

    while time.monotonic() < deadline:
        if server.process.poll() is not None:
            raise ConfigError(
                f"Appium server exited early for {server.device.name}. Check log: {server.log_file}"
            )
        if _server_reachable(server_url):
            LOGGER.info("Appium 服务已就绪: device=%s server=%s pid=%s", server.device.name, server_url, server.process.pid)
            return
        time.sleep(poll_interval)

    raise ConfigError(
        f"Timed out waiting for Appium server for {server.device.name}: {server_url}. Check log: {server.log_file}"
    )


def _ensure_port_available(settings: AndroidSettings, device: AndroidDeviceSettings) -> None:
    if _port_open(settings.appium_service.host, device.appium_port):
        raise ConfigError(
            f"Appium port already in use for {device.name}: {settings.appium_service.host}:{device.appium_port}"
        )


def _port_open(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        return sock.connect_ex((host, port)) == 0


def _appium_executable(settings: AndroidSettings) -> str:
    if settings.appium_service.executable is not None:
        if not settings.appium_service.executable.exists():
            raise ConfigError(f"Configured Appium executable not found: {settings.appium_service.executable}")
        return str(settings.appium_service.executable)

    executable = shutil.which("appium") or shutil.which("appium.cmd") or shutil.which("appium.CMD")
    if executable is None:
        raise ConfigError(
            "Appium executable not found in PATH. Install Appium 2 or set APPIUM_EXECUTABLE."
        )
    return executable


def _is_local_server(server_url: str | None, port: int) -> bool:
    if not server_url:
        return True
    normalized = server_url.lower()
    return normalized in {
        f"http://127.0.0.1:{port}",
        f"http://localhost:{port}",
    }


def _server_reachable(url: str) -> bool:
    if not url:
        return False
    try:
        with urlopen(f"{url.rstrip('/')}/status", timeout=2) as response:
            return 200 <= response.status < 500
    except (OSError, URLError):
        return False


def _cleanup_existing_local_server(settings: AndroidSettings, device: AndroidDeviceSettings) -> None:
    pid = _listening_pid(device.appium_port)
    if pid is None:
        return

    if not _is_appium_process(pid):
        raise ConfigError(
            f"Port {device.appium_port} for {device.name} is occupied by a non-Appium process (pid={pid}). "
            "Change appium_port or stop that process manually."
        )

    LOGGER.warning(
        "启动前发现残留 Appium 服务，准备清理: device=%s pid=%s port=%s",
        device.name,
        pid,
        device.appium_port,
    )
    _terminate_process(pid, settings.appium_service.stop_timeout_seconds)

    deadline = time.monotonic() + settings.appium_service.stop_timeout_seconds
    while time.monotonic() < deadline:
        if not _port_open(settings.appium_service.host, device.appium_port):
            return
        time.sleep(0.5)

    raise ConfigError(
        f"Timed out waiting for stale Appium server to release port {device.appium_port} for {device.name}."
    )


def _listening_pid(port: int) -> int | None:
    command = ["netstat", "-ano", "-p", "tcp"]
    result = subprocess.run(command, text=True, capture_output=True, timeout=10)
    if result.returncode != 0:
        return None

    for line in result.stdout.splitlines():
        if f":{port}" not in line or "LISTENING" not in line.upper():
            continue
        parts = line.split()
        if len(parts) >= 5:
            try:
                return int(parts[-1])
            except ValueError:
                return None
    return None


def _is_appium_process(pid: int) -> bool:
    command = [
        "powershell",
        "-NoProfile",
        "-Command",
        f"(Get-CimInstance Win32_Process -Filter \"ProcessId = {pid}\").CommandLine",
    ]
    result = subprocess.run(command, text=True, capture_output=True, timeout=10)
    if result.returncode != 0:
        return False

    command_line = (result.stdout or "").strip().lower()
    return "appium" in command_line


def _terminate_process(pid: int, timeout_seconds: int) -> None:
    if os.name == "nt":
        result = subprocess.run(
            ["taskkill", "/PID", str(pid), "/F"],
            text=True,
            capture_output=True,
            timeout=max(5, timeout_seconds),
        )
        if result.returncode != 0:
            raise ConfigError(f"Failed to stop stale Appium process {pid}: {result.stderr.strip() or result.stdout.strip()}")
        return

    try:
        os.kill(pid, 15)
    except OSError as exc:
        raise ConfigError(f"Failed to stop stale Appium process {pid}: {exc}") from exc
