#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :
 @time        :  2024/10/10 11:11
"""
from common.logger.logTool import logger
from common.appium.remoteControlActions import RemoteControlActions
from page_objects.doozy_tv.elements.startPageElements import StartPageElements


class StartPage:
    def __init__(self, _appOperator):
        self._appOperator = _appOperator
        self._remoteControl = RemoteControlActions(self._appOperator.getDriver())
        self._startPageElements = StartPageElements()

    def is_allow_container_displayed(self):
        if self._appOperator.is_displayed(self._startPageElements.permission_container):
            self._appOperator.get_screenshot('dialog_container')
            logger.info('permission_container is displayed')
        else:
            logger.info('permission_container is not displayed')
            return False

    def click_allow_btn(self):
        self.is_allow_container_displayed()
        # self._remoteControl.press_down()
        # self._remoteControl.press_right()
        if self._appOperator.is_displayed(self._startPageElements.permission_allow_button):
            self._appOperator.move_cursor_to_element(self._startPageElements.permission_allow_button)
            logger.info('move_cursor_to_element permission_allow_button')
            # if self._appOperator.selected(self._startPageElements.permission_allow_button):
            self._appOperator.touch_tap(self._startPageElements.permission_allow_button)
            logger.info('touch_tap permission_allow_button')
            self._appOperator.get_screenshot('after_click_allow_btn')

    def click_deny_btn(self):
        self.is_allow_container_displayed()
        # self._remoteControl.press_down()
        if self._appOperator.is_displayed(self._startPageElements.permission_deny_button):
            self._appOperator.move_cursor_to_element(self._startPageElements.permission_deny_button)
            self._appOperator.touch_tap(self._startPageElements.permission_deny_button)
            logger.info('touch_tap permission_deny_button')
            self._appOperator.get_screenshot('after_click_deny_btn')

    def getElements(self):
        return self._startPageElements
