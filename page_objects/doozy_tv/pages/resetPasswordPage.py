#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :  
 @time        :    11:29
"""
import threading
import time

from common.logger.logTool import logger
from common.yamlTool import YamlTool
from common.mail.registerMailAccount import WebSocketClient
from common.appium.remoteControlActions import RemoteControlActions
from page_objects.doozy_tv.elements.topMenuElements import TopMenuElements
from page_objects.doozy_tv.elements.loginPageElements import LoginPageElements
from page_objects.doozy_tv.elements.profilePageElements import ProfilePageElements
from page_objects.doozy_tv.elements.resetPasswordPageElements import ResetPasswordPageElements
from page_objects.doozy_tv.elements.loginMethodPageElements import LoginMethodPageElements


class RegisterPage:
    def __init__(self, _appOperator):
        self._appOperator = _appOperator
        self._remoteControl = RemoteControlActions(self._appOperator.getDriver())
        self.topMenuElements = TopMenuElements()
        self.loginPageElements = LoginPageElements()
        self.profilePageElements = ProfilePageElements()
        self.loginMethodPageElements = LoginMethodPageElements()
        self.restPasswordPageElements = ResetPasswordPageElements()
        self.client = WebSocketClient()

    def click_back_btn(self):
        self._remoteControl.press_back()
        logger.warning('Click back button')

    def click_reset_password_btn(self):
        self._appOperator.is_displayed(self.loginPageElements.login_forget_password_btn)
        self._appOperator.move_cursor_to_element(self.loginPageElements.login_forget_password_btn)
        self._remoteControl.press_ok()
        logger.warning('Click reset password button')

