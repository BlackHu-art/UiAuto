from __future__ import annotations

from typing import Callable

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

DEFAULT_TIMEOUT = 10
DEFAULT_POLL_FREQUENCY = 0.5


def wait_for_visible(driver, locator: tuple[str, str], timeout: int = DEFAULT_TIMEOUT):
    """等待元素可见。"""
    return _wait(driver, timeout).until(
        EC.visibility_of_element_located(locator),
        message=f"Element not visible within {timeout}s: {locator}",
    )


def wait_for_clickable(driver, locator: tuple[str, str], timeout: int = DEFAULT_TIMEOUT):
    """等待元素可点击。"""
    return _wait(driver, timeout).until(
        EC.element_to_be_clickable(locator),
        message=f"Element not clickable within {timeout}s: {locator}",
    )


def wait_for_present(driver, locator: tuple[str, str], timeout: int = DEFAULT_TIMEOUT):
    """等待元素出现在 DOM/页面结构中。"""
    return _wait(driver, timeout).until(
        EC.presence_of_element_located(locator),
        message=f"Element not present within {timeout}s: {locator}",
    )


def wait_until(driver, condition: Callable, timeout: int = DEFAULT_TIMEOUT, message: str = ""):
    return _wait(driver, timeout).until(condition, message=message)


def is_visible(driver, locator: tuple[str, str], timeout: int = DEFAULT_TIMEOUT) -> bool:
    try:
        return wait_for_visible(driver, locator, timeout).is_displayed()
    except TimeoutException:
        return False


def _wait(driver, timeout: int):
    return WebDriverWait(driver, timeout, poll_frequency=DEFAULT_POLL_FREQUENCY)
