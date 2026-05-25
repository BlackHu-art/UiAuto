#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :  
 @time        :    11:32
"""
from page_objects.createElement import CreateElement
from page_objects.doozy_tv.wait_type import Wait_Type as Wait_By
from page_objects.doozy_tv.locator_type import Locator_Type


class ResetPasswordPageElements:
    def __init__(self):

        # back btn
        self.reset_password_back_btn = CreateElement.create(Locator_Type.ID,
                                                   'com.mm.droid.livetv.stb31023418:id/resetpwd_tv_return',
                                                   wait_type=Wait_By.VISIBILITY_OF)
        # reset password title     FORGOT YOUR PASSWORD?
        self.reset_password_title = CreateElement.create(Locator_Type.ID,
                                                         'com.mm.droid.livetv.stb31023418:id/resetpwd_tv_title',
                                                   wait_type=Wait_By.VISIBILITY_OF)
        self.reset_password_doozy_icon = CreateElement.create(Locator_Type.ID,
                                                              'com.mm.droid.livetv.stb31023418:id/resetpwd_iv_title',
                                                   wait_type=Wait_By.VISIBILITY_OF)
        self.reset_password_remind_tips_text = CreateElement.create(Locator_Type.ID,
                                                                    'com.mm.droid.livetv.stb31023418:id/resetpwd_tv_remind',
                                                   wait_type=Wait_By.VISIBILITY_OF)

        # menu
        self.reset_password_method_container = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/resetpwd_lly_switch',
                                                                    wait_type=Wait_By.VISIBILITY_OF)
        self.reset_password_submit_btn = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/resetpwd_tv_submit',
                                                              wait_type=Wait_By.VISIBILITY_OF)
        self.reset_password_send_verify_code_btn = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/tv_verify',
                                                                  wait_type=Wait_By.VISIBILITY_OF)
        self.reset_password_input_verify_code_edit = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/resetpwd_et_verify_code',
                                                                  wait_type=Wait_By.VISIBILITY_OF)
        self.reset_password_input_password_edit = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/et_pwd',
                                                                  wait_type=Wait_By.VISIBILITY_OF)
        self.reset_password__show_password_btn = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/pwd_show_state_iv',
                                                                  wait_type=Wait_By.VISIBILITY_OF)

        # reset password email element
        self.reset_password_email_element = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/tabitem_email',
                                                                  wait_type=Wait_By.VISIBILITY_OF)
        self.reset_password_input_email_edit = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/resetpwd_et_email',
                                                                  wait_type=Wait_By.VISIBILITY_OF)

        # reset password phone element
        self.reset_password_phone_element = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/tabitem_phone',
                                                                  wait_type=Wait_By.VISIBILITY_OF)
        self.reset_password_phone_spinner_phone_code = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/spinner_phonecode',
                                                                  wait_type=Wait_By.VISIBILITY_OF)
        self.reset_password_phone_number_edit = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/et_phonenumber',
                                                                     wait_type=Wait_By.VISIBILITY_OF)

        # tv_notice
        self.login_notice_id = CreateElement.create(Locator_Type.ID,
                                                    'com.mm.droid.livetv.stb31023418:id/loada_tv_notice',
                                                    wait_type=Wait_By.VISIBILITY_OF)

