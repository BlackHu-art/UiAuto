#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :
 @time        :  2024/10/16 13:45
"""
from base.app_ui.android_Project_client import Android_Project_Client
from page_objects.doozy_tv.pages.startPage import StartPage
from common.logger.logTool import logger
import pytest


class TestPermission:
    def setup_class(self):
        """在测试类级别初始化Android_Project_Client，只运行一次"""
        self.demoProjectClient = Android_Project_Client()
        self.startPage = StartPage(self.demoProjectClient.appOperator)
        self.appOperator = self.demoProjectClient.appOperator


    """该函数为一个Pytest fixture，自动用于每个测试用例"""

    # @pytest.fixture(autouse=True)
    # def record_test_case_video(self):
    #     self.demoProjectClient.appOperator.start_recording_screen()
    #     yield self.record_test_case_video
    #     self.demoProjectClient.appOperator.stop_recording_screen()

    # @pytest.mark.run(order=1)
    # pytest顺序执行器

    @pytest.fixture
    def fixture_test(self):
        """
        该函数是一个PyTest测试夹具（fixture），名为fixture_test_silde：
            执行测试前打印“start......”；
            使用yield提供fixture对象给测试函数使用；
            测试完成后，打印“end......”。
        """
        logger.info('\n......start......')
        yield self.fixture_test
        logger.info('\n...... end ......')

    @pytest.mark.run(order=2)
    def test_click_allow_btn(self, fixture_test):
        self.appOperator.reset_app()
        self.startPage.click_allow_btn()

    @pytest.mark.run(order=1)
    def test_click_deny_btn(self, fixture_test):
        self.appOperator.reset_app()
        self.startPage.click_deny_btn()

    def teardown_class(self):
        """在测试类结束时执行的清理工作"""
        logger.info('TestStartPage 用例执行结束，不关闭应用以保留状态')
        pass  # 如果你不需要关闭应用，保持应用的状态
