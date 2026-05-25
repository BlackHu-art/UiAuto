from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy

from android_automation.base.base_page import BasePage


class LoginPage(BasePage):
    USERNAME_INPUT = (AppiumBy.ACCESSIBILITY_ID, "login_username")
    PASSWORD_INPUT = (AppiumBy.ACCESSIBILITY_ID, "login_password")
    LOGIN_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "login_submit")

    def enter_username(self, username: str) -> None:
        self.type_text(self.USERNAME_INPUT, username)

    def enter_password(self, password: str) -> None:
        self.type_text(self.PASSWORD_INPUT, password)

    def submit(self) -> None:
        self.tap(self.LOGIN_BUTTON)

    def login(self, username: str, password: str) -> None:
        self.enter_username(username)
        self.enter_password(password)
        self.submit()
