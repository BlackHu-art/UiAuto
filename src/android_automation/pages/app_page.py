from __future__ import annotations

from android_automation.base.base_page import BasePage


class AppPage(BasePage):
    def current_package(self) -> str:
        return self.driver.current_package

    def current_activity(self) -> str:
        return self.driver.current_activity
