#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :  
 @time        :    13:49
"""
from base.app_ui.android_Project_client import Android_Project_Client
from page_objects.doozy_tv.pages.startUpWelcomeADPage import StartUpWelcomeADPage
from common.logger.logTool import logger
import pytest


class TestStartUpADPage:
    def setup_class(self):
        """复用 Android_Project_Client 实例，只初始化一次"""
        self._demoProjectClient = Android_Project_Client()  # 此处不会重新初始化
        self._startUpWelcomeADPage = StartUpWelcomeADPage(self._demoProjectClient.appOperator)
        logger.info('TestStartUpADPage setup_class')

    @pytest.fixture
    def fixture_test(self):
        logger.info('\n......start......')
        yield self.fixture_test
        logger.info('\n...... end ......')

    @pytest.mark.run(order=4)
    @pytest.mark.skipif(reason='跳过此用例')
    def test_start_up_welcome_ad_page(self, fixture_test):
        self._startUpWelcomeADPage.start_up_welcome_ad_container()

    def teardown_class(self):
        logger.info('TestStartUpADPage 用例执行结束，保留应用状态')
        pass  # 如果不需要关闭应用或销毁 session，则保留应用状态
