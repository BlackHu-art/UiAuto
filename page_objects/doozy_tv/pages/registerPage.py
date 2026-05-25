#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :  
 @time        :    13:45
"""
import threading
import time

from common.logger.logTool import logger
from common.yamlTool import YamlTool
from common.mail.tempEmailService import EmailService
from common.appium.remoteControlActions import RemoteControlActions
from page_objects.doozy_tv.elements.registerPageElements import RegisterPageElements
from page_objects.doozy_tv.elements.topMenuElements import TopMenuElements
from page_objects.doozy_tv.elements.profilePageElements import ProfilePageElements
from page_objects.doozy_tv.elements.loginMethodPageElements import LoginMethodPageElements


class RegisterPage:
    def __init__(self, _appOperator):
        self._appOperator = _appOperator
        self._remoteControl = RemoteControlActions(self._appOperator.getDriver())
        self.registerPageElements = RegisterPageElements()
        self.topMenuElements = TopMenuElements()
        self.profilePageElements = ProfilePageElements()
        self.loginMethodPageElements = LoginMethodPageElements()
        self.emailService = EmailService()

    def click_back_btn(self):
        self._remoteControl.press_back()
        logger.warning('Click back button')

    def move_to_register_email_element(self):
        if self._appOperator.is_displayed(self.registerPageElements.register_email_element):
            self._appOperator.move_cursor_to_element(self.registerPageElements.register_email_element)
            # if self._appOperator.is_selected(self.registerPageElements.register_email_element):
            logger.info('Move to register email element')
            self._appOperator.get_screenshot('Move to register email element')
            self._remoteControl.press_ok()
            logger.warning('Register email element is selected')

    def move_to_email_input_element(self):
        if self._appOperator.is_displayed(self.registerPageElements.register_email_input_text):
            self._appOperator.move_cursor_to_element(self.registerPageElements.register_email_input_text)
            logger.info('Move to email input element')
            self._appOperator.get_screenshot('Move to email input element')
            # if self._appOperator.is_selected(self.registerPageElements.register_email_input_text):
            logger.warning('Email input element is selected')

    def input_register_email_and_verify_code(self):
        # 创建一个新线程来执行 start_with_new_account
        thread = threading.Thread(target=self.emailService.fetch_and_process_email)
        thread.start()
        time.sleep(3)
        # 此处为一个请求循环监听器，用于获取邮箱验证码
        if self._appOperator.is_displayed(self.registerPageElements.register_email_input_text):
            self._appOperator.move_cursor_to_element(self.registerPageElements.register_email_input_text)
            logger.info('Email input element is selected')
            email = YamlTool("common/mail/mail.yaml").get_nested_value('userRegisterInfoPro', 'account')
            self._appOperator.sendText(self.registerPageElements.register_email_input_text, email)
            self._appOperator.get_screenshot('Input register email')
            logger.info('Input register email success')
        self._appOperator.is_displayed(self.registerPageElements.register_email_verify_code_btn)
        self._appOperator.move_cursor_to_element(self.registerPageElements.register_email_verify_code_btn)
        self._remoteControl.press_ok()
        time.sleep(2)
        self._appOperator.get_screenshot('Click register email verify code button')
        # 等待线程完成
        thread.join()
        # verification_code = self.emailService.get_email_detail()
        verification_code = YamlTool("common/mail/mail.yaml").get_nested_value('userRegisterInfoPro', 'verifyCode')
        # logger.warning(f"获取到的验证码: {verification_code}")
        self._appOperator.move_cursor_to_element(self.registerPageElements.register_input_verify_code_edit)
        self._appOperator.sendText(self.registerPageElements.register_input_verify_code_edit, verification_code)
        self._appOperator.get_screenshot('Input register email verify code')
        logger.warning('Input register email verify code success')

    def input_register_email_password(self):
        password = YamlTool("common/mail/mail.yaml").get_nested_value('userRegisterInfoPro', 'password')
        self._appOperator.move_cursor_to_element(self.registerPageElements.register_input_password_edit)
        self._appOperator.sendText(self.registerPageElements.register_input_password_edit, password)
        self._appOperator.get_screenshot('Input register email password')
        logger.warning('Input register email password success')

    def move_to_register_phone_element(self):
        if self._appOperator.is_displayed(self.registerPageElements.register_phone_element):
            self._appOperator.move_cursor_to_element(self.registerPageElements.register_phone_element)
            logger.info('Move to register phone element')
            self._appOperator.get_screenshot('Move to register phone element')
            logger.warning('Register phone element is selected')

    def click_register_submit_btn(self):
        self._appOperator.move_cursor_to_element(self.registerPageElements.register_submit_btn)
        self._appOperator.is_selected(self.registerPageElements.register_submit_btn)
        self._appOperator.get_screenshot('Click register submit button')
        self._remoteControl.press_ok()
        logger.warning('Click register submit button')

    def check_register_success(self):
        uid = self._appOperator.get_element_text_by_id(self.profilePageElements.profile_account_userid)
        if uid == YamlTool("common/mail/mail.yaml").get_nested_value('userRegisterInfoPro', 'account'):
            logger.warning('Register success')
            return True
        else:
            logger.error('Register failed')
            return False
