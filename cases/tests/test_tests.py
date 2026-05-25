#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :  
 @time        :    14:59
"""
from base.app_ui.android_Project_client import Android_Project_Client
from page_objects.doozy_tv.pages.loginPage import LoginPage
from page_objects.doozy_tv.pages.registerPage import RegisterPage
from common.logger.logTool import logger
import pytest


class TestRegister:
    def setup_class(self):
        """复用 Android_Project_Client 实例，只初始化一次"""
        self._demoProjectClient = Android_Project_Client()  # 此处不会重新初始化
        self._loginPage = LoginPage(self._demoProjectClient.appOperator)
        self._registerPage = RegisterPage(self._demoProjectClient.appOperator)
        self._appOperator = self._demoProjectClient.appOperator

    @pytest.fixture
    def fixture_test(self):
        logger.info('\n......start......')
        yield self.fixture_test
        logger.info('\n...... end ......')

    @pytest.mark.run(order=9)
    # @pytest.mark.skipif(reason='跳过此用例')
    def test_reset_email_password(self, fixture_test):
        self._appOperator.restart_app()
        self._loginPage.click_profile_btn()
        self._loginPage.click_login_btn()
        self._loginPage.click_profile_btn()
        self._loginPage.check_logout_success()

    def teardown_class(self):
        logger.info('TestStartUpADPage 用例执行结束，保留应用状态')
        pass  # 如果不需要关闭应用或销毁 session，则保留应用状态
