#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :  
 @time        :    10:56
"""
import time

from common.logger.logTool import logger
from common.appium.remoteControlActions import RemoteControlActions
from page_objects.doozy_tv.elements.topMenuElements import TopMenuElements


class StartPage:
    def __init__(self, _appOperator):
        self._appOperator = _appOperator
        self._remoteControl = RemoteControlActions(self._appOperator.getDriver())
        self._topMenuElements = TopMenuElements()

    def Locate_button_home(self):
        """
        @Description：光标定位到home lab
        """
        if self._appOperator.is_displayed(self._topMenuElements.home_menu_container):
            logger.info('top_menu_list_container show')
            while not self._appOperator.is_displayed(self._topMenuElements.home_menu_container):
                self._remoteControl.press_back()
                time.sleep(1)  # 等待1秒，防止频繁点击
            logger.info(f'Element is displayed')
