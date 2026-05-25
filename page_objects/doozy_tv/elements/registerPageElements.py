#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :  
 @time        :    13:46
"""
from page_objects.createElement import CreateElement
from page_objects.doozy_tv.wait_type import Wait_Type as Wait_By
from page_objects.doozy_tv.locator_type import Locator_Type


class RegisterPageElements:
    def __init__(self):
        # _back_btn
        self.register_back_btn = CreateElement.create(Locator_Type.ID,
                                                   'com.mm.droid.livetv.stb31023418:id/registeremail_tv_button_return',
                                                   wait_type=Wait_By.VISIBILITY_OF)
        # tv_notice
        self.login_notice_id = CreateElement.create(Locator_Type.ID,
                                                    'com.mm.droid.livetv.stb31023418:id/loada_tv_notice',
                                                    wait_type=Wait_By.VISIBILITY_OF)
        # public
        self.register_title = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/registeremail_tv_remind_started',
                                                    wait_type=Wait_By.VISIBILITY_OF)
        self.register_doozy_icon = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/registeremail_iv_title',
                                                     wait_type=Wait_By.VISIBILITY_OF)
        # menu
        self.register_method_container = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/lly_login_switch',
                                                     wait_type=Wait_By.VISIBILITY_OF)
        self.register_remind_tips_text = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/registeremail_ltv_remind',
                                                     wait_type=Wait_By.VISIBILITY_OF)
        self.register_input_verify_code_edit = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/registeremail_et_verify_code',
                                                                  wait_type=Wait_By.VISIBILITY_OF)
        self.register_input_password_edit = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/et_pwd',
                                                                  wait_type=Wait_By.VISIBILITY_OF)
        self.register_show_password_btn = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/pwd_show_state_iv',
                                                                  wait_type=Wait_By.VISIBILITY_OF)
        self.register_submit_btn = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/registeremail_tv_submit',
                                                        wait_type=Wait_By.VISIBILITY_OF)

        # email
        self.register_email_element = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/tabitem_email',
                                                     wait_type=Wait_By.VISIBILITY_OF)
        self.register_email_input_text = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/registeremail_et_email',
                                                     wait_type=Wait_By.VISIBILITY_OF)
        self.register_email_verify_code_btn = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/tv_verify',
                                                                  wait_type=Wait_By.VISIBILITY_OF)

        # phone
        self.register_phone_element = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/tabitem_phone',
                                                     wait_type=Wait_By.VISIBILITY_OF)
        self.register_phone_spinner_phone_code = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/spinner_phonecode',
                                                                  wait_type=Wait_By.VISIBILITY_OF)
        self.register_phone_input_phone_edit = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/et_phonenumber',
                                                                    wait_type=Wait_By.VISIBILITY_OF)
        self.register_phone_verify_code_btn = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/tv_verify_phone',
                                                                  wait_type=Wait_By.VISIBILITY_OF)

        # agreement
        self.register_agreement_show_btn = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/agreement_show',
                                                             wait_type=Wait_By.VISIBILITY_OF)