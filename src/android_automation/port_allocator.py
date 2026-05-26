from __future__ import annotations

import socket
from dataclasses import dataclass
from typing import Iterable

from android_automation.config import ConfigError


@dataclass(frozen=True)
class PortSet:
    appium_port: int
    system_port: int
    chromedriver_port: int
    mjpeg_server_port: int


@dataclass(frozen=True)
class PortStarts:
    appium_port: int
    system_port: int = 8200
    chromedriver_port: int = 9515
    mjpeg_server_port: int = 7810


class PortAllocator:
    """为运行时发现的新设备分配端口，避免和本次运行内的设备互相冲突。"""

    def __init__(self, host: str, starts: PortStarts, reserved_ports: Iterable[int | None] = ()):
        self.host = host
        self.starts = starts
        self._reserved = {port for port in reserved_ports if port is not None}

    def allocate(self) -> PortSet:
        """从各自端口池里挑选当前可用端口，返回一组 Appium 能力所需端口。"""
        return PortSet(
            appium_port=self._next_available(self.starts.appium_port),
            system_port=self._next_available(self.starts.system_port),
            chromedriver_port=self._next_available(self.starts.chromedriver_port),
            mjpeg_server_port=self._next_available(self.starts.mjpeg_server_port),
        )

    def _next_available(self, start: int) -> int:
        port = start
        while port <= 65535:
            if port not in self._reserved and not _port_open(self.host, port):
                self._reserved.add(port)
                return port
            port += 1

        raise ConfigError(f"No available local port found from {start}")


def configured_ports(devices) -> set[int]:
    """收集已纳入本次运行设备的端口，供动态设备避让。"""
    ports: set[int] = set()
    for device in devices:
        ports.update(
            port
            for port in (
                device.appium_port,
                device.system_port,
                device.chromedriver_port,
                device.mjpeg_server_port,
            )
            if port is not None
        )
    return ports


def _port_open(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)
        return sock.connect_ex((host, port)) == 0
