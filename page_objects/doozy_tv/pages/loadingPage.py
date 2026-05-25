#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :  
 @time        :    11:00
"""
import time
from common.logger.logTool import logger
from common.appium.remoteControlActions import RemoteControlActions
from page_objects.doozy_tv.elements.loadingPageElements import LoadingPageElements


class LoadingPage:
    def __init__(self, appOperator):
        self._appOperator = appOperator
        self._remoteControl = RemoteControlActions(self._appOperator.getDriver())
        self._loadingPageElements = LoadingPageElements()

    def test_start_up_loading_page(self):
        if self._appOperator.is_displayed(self._loadingPageElements.loading_container):
            logger.info('loading_container is displayed !')
            self._appOperator.get_screenshot('loading_container')
        else:
            logger.warning('loading AD container is not displayed !')

    def getElements(self):
        return self._loadingPageElements
