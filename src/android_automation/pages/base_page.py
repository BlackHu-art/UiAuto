from __future__ import annotations

import allure

from android_automation.waits import is_visible, wait_for_clickable, wait_for_present, wait_for_visible


class BasePage:
    """页面对象基类，封装最常用的查找、点击、输入和回退动作。"""

    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.timeout = timeout

    def find(self, locator: tuple[str, str]):
        return wait_for_visible(self.driver, locator, self.timeout)

    def tap(self, locator: tuple[str, str]) -> None:
        with allure.step(f"Tap element: {locator}"):
            wait_for_clickable(self.driver, locator, self.timeout).click()

    def text(self, locator: tuple[str, str]) -> str:
        return self.find(locator).text

    def type_text(self, locator: tuple[str, str], value: str) -> None:
        with allure.step(f"Type text into element: {locator}"):
            element = self.find(locator)
            element.clear()
            element.send_keys(value)

    def is_visible(self, locator: tuple[str, str]) -> bool:
        return is_visible(self.driver, locator, self.timeout)

    def exists(self, locator: tuple[str, str]) -> bool:
        try:
            wait_for_present(self.driver, locator, self.timeout)
            return True
        except Exception:
            return False

    def back(self) -> None:
        with allure.step("Navigate back"):
            self.driver.back()

    def screenshot(self) -> bytes:
        return self.driver.get_screenshot_as_png()
