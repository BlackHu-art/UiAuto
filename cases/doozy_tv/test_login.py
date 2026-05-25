#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :  
 @time        :    10:45
"""
from base.app_ui.android_Project_client import Android_Project_Client
from page_objects.doozy_tv.pages.loginPage import LoginPage
from common.logger.logTool import logger
import pytest


class TestLogin:
    def setup_class(self):
        """复用 Android_Project_Client 实例，只初始化一次"""
        self._demoProjectClient = Android_Project_Client()  # 此处不会重新初始化
        self._loginPage = LoginPage(self._demoProjectClient.appOperator)
        self._appOperator = self._demoProjectClient.appOperator

    @pytest.fixture
    def fixture_test(self):
        logger.info('\n......start......')
        yield self.fixture_test
        logger.info('\n...... end ......')

    @pytest.mark.run(order=7)
    # @pytest.mark.skipif(reason='跳过此用例')
    def test_login_email(self, fixture_test):
        self._appOperator.restart_app()
        self._loginPage.click_profile_btn()
        self._loginPage.click_login_btn()
        self._loginPage.click_login_with_btn()
        self._loginPage.switch_to_login_with_email()
        self._loginPage.input_login_email()
        self._loginPage.input_login_email_password()
        self._loginPage.click_login()
        self._loginPage.click_profile_btn()
        self._loginPage.check_login_success()

    @pytest.mark.run(order=8)
    # @pytest.mark.skipif(reason='跳过此用例')
    def test_logout_email(self, fixture_test):
        self._appOperator.restart_app()
        self._loginPage.click_profile_btn()
        self._loginPage.click_login_btn()
        self._loginPage.click_profile_btn()
        self._loginPage.check_logout_success()


    def teardown_class(self):
        logger.info('TestStartUpADPage 用例执行结束，保留应用状态')
        pass  # 如果不需要关闭应用或销毁 session，则保留应用状态
