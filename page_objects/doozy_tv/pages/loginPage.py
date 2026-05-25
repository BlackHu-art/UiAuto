#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :  
 @time        :    16:26
"""
from common.logger.logTool import logger
from common.yamlTool import YamlTool
from common.appium.remoteControlActions import RemoteControlActions
from page_objects.doozy_tv.elements.loginPageElements import LoginPageElements
from page_objects.doozy_tv.elements.topMenuElements import TopMenuElements
from page_objects.doozy_tv.elements.profilePageElements import ProfilePageElements
from page_objects.doozy_tv.elements.loginMethodPageElements import LoginMethodPageElements


class LoginPage:
    def __init__(self, _appOperator):
        self._appOperator = _appOperator
        self._remoteControl = RemoteControlActions(self._appOperator.getDriver())
        self.loginPageElements = LoginPageElements()
        self.topMenuElements = TopMenuElements()
        self.profilePageElements = ProfilePageElements()
        self.loginMethodPageElements = LoginMethodPageElements()
        self.yamlTool = YamlTool('test_data/doozy_tv/accountInfo.yaml')

    def click_back_btn(self):
        self._remoteControl.press_back()
        logger.warning('press_back')

    def click_profile_btn(self):
        if self._appOperator.is_displayed(self.topMenuElements.top_menu_list_container):
            self._remoteControl.press_up()
            self._remoteControl.press_right()
            self._remoteControl.press_right()
            self._remoteControl.press_right()
            self._remoteControl.press_right()
            self._appOperator.is_selected(self.topMenuElements.profile_menu_container)
            self._appOperator.get_screenshot('profile_menu is Selected')
            self._remoteControl.press_ok()
            logger.warning('profile_menu is clicked')

    def click_login_btn(self):
        if self._appOperator.is_displayed(self.profilePageElements.profile_account_login_btn):
            self._appOperator.move_cursor_to_element(self.profilePageElements.profile_account_login_btn)
            self._appOperator.get_screenshot('login_btn is Selected')
            self._remoteControl.press_ok()
            logger.warning('login_btn is clicked')

    def click_login_with_btn(self):
        if self._appOperator.is_displayed(self.loginMethodPageElements.login_login_with_btn):
            logger.info('login_with_btn is displayed')
            self._appOperator.move_cursor_to_element(self.loginMethodPageElements.login_login_with_btn)
            self._appOperator.get_screenshot('login_login_with_btn is Selected')
            self._remoteControl.press_ok()
            logger.warning('login_login_with_btn is clicked')

    def click_register_btn(self):
        if self._appOperator.is_displayed(self.loginMethodPageElements.login_sign_up_btn):
            logger.info('login_sign_up_btn is displayed')
            self._appOperator.move_cursor_to_element(self.loginMethodPageElements.login_sign_up_btn)
            self._appOperator.get_screenshot('login_sign_up_btn is Selected')
            self._remoteControl.press_ok()
            logger.warning('login_sign_up_btn is clicked')

    def switch_to_login_with_email(self):
        if self._appOperator.is_displayed(self.loginPageElements.login_email_element):
            logger.info('login_with_email_btn is displayed')
            self._appOperator.move_cursor_to_element(self.loginPageElements.login_email_element)
            self._appOperator.get_screenshot('login_email_element is Selected')
            logger.warning('switch_to_login_with_email')

    def input_login_email(self):
        email = self.yamlTool.get_nested_value('USERINFO_PRO', 'ACCOUNT01')
        if self._appOperator.is_displayed(self.loginPageElements.login_email_input_container):
            logger.info('login_email_input_container is displayed')
            self._appOperator.move_cursor_to_element(self.loginPageElements.login_email_input_email_edit)
            self._appOperator.get_screenshot('login_email_input_email_edit is Selected')
            self._appOperator.sendText(self.loginPageElements.login_email_input_email_edit, email)
            self._appOperator.get_screenshot('input_login_email')
            logger.warning('input_login_email')

    def input_login_email_password(self):
        password = self.yamlTool.get_nested_value('USERINFO_PRO', 'APASSWRD01')
        if self._appOperator.is_displayed(self.loginPageElements.login_input_password_edit):
            logger.info('login_input_password_edit is displayed')
            self._appOperator.move_cursor_to_element(self.loginPageElements.login_input_password_edit)
            self._appOperator.get_screenshot('login_input_password_edit is Selected')
            self._appOperator.sendText(self.loginPageElements.login_input_password_edit, password)
            self._appOperator.get_screenshot('input_login_password')
            logger.warning('input_login_email_password')

    def switch_to_login_with_phone(self):
        if self._appOperator.is_displayed(self.loginPageElements.login_phone_element):
            logger.info('login_phone_element is displayed')
            self._appOperator.move_cursor_to_element(self.loginPageElements.login_phone_element)
            self._appOperator.get_screenshot('login_phone_element is Selected')
            logger.warning('switch_to_login_with_phone')

    def input_login_phone(self):
        phone_number = self.yamlTool.get_nested_value('USERINFO_PRO', 'PHONE01')
        if self._appOperator.is_displayed(self.loginPageElements.login_phone_input_phone_edit):
            logger.info('login_phone_input_phone_edit is displayed')
            self._appOperator.move_cursor_to_element(self.loginPageElements.login_phone_input_phone_edit)
            self._appOperator.get_screenshot('login_phone_input_phone_edit is Selected')
            self._appOperator.sendText(self.loginPageElements.login_phone_input_phone_edit, phone_number)
            self._appOperator.get_screenshot('input_login_phone')
            logger.warning('input_login_phone')

    def input_login_phone_password(self):
        password = self.yamlTool.get_nested_value('USERINFO_PRO', 'PPASSWORD01')
        if self._appOperator.is_displayed(self.loginPageElements.login_input_password_edit):
            logger.info('login_input_password_edit is displayed')
            self._appOperator.move_cursor_to_element(self.loginPageElements.login_input_password_edit)
            self._appOperator.get_screenshot('login_input_password_edit is Selected')
            self._appOperator.sendText(self.loginPageElements.login_input_password_edit, password)
            self._appOperator.get_screenshot('input_login_phone_password')
            logger.warning('input_login_phone_password')

    def click_login(self):
        if self._appOperator.is_displayed(self.loginPageElements.login_login_btn):
            logger.info('login_login_btn is displayed')
            self._appOperator.move_cursor_to_element(self.loginPageElements.login_login_btn)
            self._appOperator.get_screenshot('login_login_btn is Selected')
            self._remoteControl.press_ok()
            logger.warning('click_login')

    def check_login_success(self):
        # 需要先进入Profile页面，获取登录账号id确认登录成功
        email = self.yamlTool.get_nested_value('USERINFO_PRO', 'ACCOUNT01')
        if self._appOperator.is_displayed(self.profilePageElements.profile_account_userid):
            if email == self._appOperator.get_element_text_by_id(self.profilePageElements.profile_account_userid):
                self._appOperator.get_screenshot('login_success')
                logger.warning('login success')
                return True
            else:
                logger.error('login fail')
        else:
            return False

    def check_logout_success(self):
        guest = 'Guest Mode'
        if self._appOperator.is_displayed(self.profilePageElements.profile_account_userid):
            if guest == self._appOperator.get_element_text_by_id(self.profilePageElements.profile_account_userid):
                self._appOperator.get_screenshot('logout_success account : ' + guest)
                logger.warning('logout success')
                return True
        else:
            return False


