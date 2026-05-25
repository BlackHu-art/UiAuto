from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy

from android_automation.base.base_page import BasePage


class HomePage(BasePage):
    def __init__(self, driver, timeout: int = 10, smoke_accessibility_id: str | None = None):
        super().__init__(driver, timeout)
        self._smoke_accessibility_id = smoke_accessibility_id

    def is_smoke_element_visible(self) -> bool:
        if not self._smoke_accessibility_id:
            raise ValueError("smoke_accessibility_id is required to validate the home page smoke element")
        locator = (AppiumBy.ACCESSIBILITY_ID, self._smoke_accessibility_id)
        return self.is_visible(locator)
