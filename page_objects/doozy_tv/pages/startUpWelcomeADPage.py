#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :  
 @time        :    13:39
"""
import time

from common.logger.logTool import logger
from common.appium.remoteControlActions import RemoteControlActions
from page_objects.doozy_tv.elements.startUpWelcomeADPageElements import StartUpWelcomeADPageElements


class StartUpWelcomeADPage:
    def __init__(self, appOperator):
        self._appOperator = appOperator
        self._remoteControl = RemoteControlActions(self._appOperator.getDriver())
        self._startUpWelcomeADPageElements = StartUpWelcomeADPageElements()

    def start_up_welcome_ad_container(self):
        if self._appOperator.launch_app():
            logger.info('StartUpWelcomeADPage app is launched !')
        if self._appOperator.is_displayed(self._startUpWelcomeADPageElements.start_up_welcome_ad_skip_button):
            logger.info('start_up_welcome_ad_container is displayed !')
            self._remoteControl.press_button(self._remoteControl.press_right())
            logger.info('press_right')
            self._appOperator.get_screenshot('start_up_welcome_ad_container')
            logger.info('get_screenshot start_up_welcome_ad_container')
        else:
            logger.warning('loading AD container is not displayed !')
            assert False

    def getElements(self):
        return self._startUpWelcomeADPageElements
