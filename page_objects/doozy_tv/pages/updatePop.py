#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :  
 @time        :    17:04
"""
from common.logger.logTool import logger
from common.appium.remoteControlActions import RemoteControlActions
from page_objects.doozy_tv.elements.updatePopElements import UpdateElements


class UpdatePop:
    def __init__(self, _appOperator):
        self._appOperator = _appOperator
        self._remoteControl = RemoteControlActions(self._appOperator.getDriver())
        self._updateElements = UpdateElements()
