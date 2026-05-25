#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :  
 @time        :    11:00
"""
from base.app_ui.android_Project_client import Android_Project_Client
from page_objects.doozy_tv.pages.loadingPage import LoadingPage
from common.logger.logTool import logger
import pytest


class TestLoadingPage:
    def setup_class(self):
        """复用 Android_Project_Client 实例，只初始化一次"""
        self.demoProjectClient = Android_Project_Client()  # 此处不会重新初始化
        self.loadingPage = LoadingPage(self.demoProjectClient.appOperator)

    @pytest.fixture
    def fixture_test(self):
        logger.info('\n......start......')
        yield self.fixture_test
        logger.info('\n...... end ......')

    @pytest.mark.run(order=3)
    @pytest.mark.skipif(reason='跳过此用例')
    def test_start_up_loading_page(self, fixture_test):
        self.demoProjectClient.appOperator.start_app()
        self.loadingPage.test_start_up_loading_page()

    def teardown_class(self):
        logger.info('TestLoadingPage测试用例执行结束，保留应用状态')
        # self.demoProjectClient.appOperator.close_app()
        pass  # 如果不需要关闭应用或销毁 session，则保留应用状态
