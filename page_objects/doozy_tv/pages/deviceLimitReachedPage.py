#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :  
 @time        :    10:04
"""
from common.appium.remoteControlActions import RemoteControlActions
from common.logger.logTool import logger
from page_objects.doozy_tv.elements.deviceLimitReachedPageElements import DeviceLimitReachedPageElements


class LoadingPage:
    def __init__(self, appOperator):
        self._appOperator = appOperator
        self._remoteControl = RemoteControlActions(self._appOperator.getDriver())
        self._loadingPageElements = DeviceLimitReachedPageElements()

    def found_reached_container(self):
        return self._loadingPageElements.device_limit_reached_container.is_displayed()

    def found_button_container(self):
        return self._loadingPageElements.device_limit_reached_button_container.is_displayed()

    def click_login_btn(self):
        if self.found_reached_container():
            if self.found_button_container():
                self._appOperator.get_screenshot('login_btn')
                self._loadingPageElements.device_limit_reached_button_login.click()
                logger.info('click_login_btn')

    def click_exit_btn(self):
        if self.found_reached_container():
            if self.found_button_container():
                self._appOperator.get_screenshot('exit_btn')
                self._loadingPageElements.device_limit_reached_button_exit.click()
                logger.info('click_exit_btn')

    def getElements(self):
        return self._loadingPageElements
