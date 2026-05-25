#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :  
 @time        :    16:27
"""
from page_objects.createElement import CreateElement
from page_objects.doozy_tv.wait_type import Wait_Type as Wait_By
from page_objects.doozy_tv.locator_type import Locator_Type


class LoginPageElements:
    def __init__(self):
        # login_back_btn
        self.login_back_btn = CreateElement.create(Locator_Type.ID,
                                                   'com.mm.droid.livetv.stb31023418:id/loginf_iv_back',
                                                   wait_type=Wait_By.VISIBILITY_OF)
        # login_
        self.login_title = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/loginf_tv_welcome',
                                                    wait_type=Wait_By.VISIBILITY_OF)
        self.login_doozy_icon = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/loginf_iv_title',
                                                     wait_type=Wait_By.VISIBILITY_OF)
        self.login_method_container = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/loginf_ll_switch',
                                                     wait_type=Wait_By.VISIBILITY_OF)
        self.login_remind_tips_text = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/loginf_tv_account_tip',
                                                     wait_type=Wait_By.VISIBILITY_OF)
        self.login_show_password_btn = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/pwd_show_state_iv',
                                                     wait_type=Wait_By.VISIBILITY_OF)
        self.login_user_sel_btn = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/loginf_iv_more_user',
                                                              wait_type=Wait_By.VISIBILITY_OF)
        self.login_remember_pwd_sl = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/remember_pwd_cb',
                                                                  wait_type=Wait_By.VISIBILITY_OF)
        self.login_remember_pwd_text = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/loginf_tv_register',
                                                                   wait_type=Wait_By.VISIBILITY_OF)
        self.login_forget_password_btn = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/loginf_tv_forget_pwd',
                                                              wait_type=Wait_By.VISIBILITY_OF)
        self.login_login_btn = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/loginf_tv_login',
                                                    wait_type=Wait_By.VISIBILITY_OF)
        self.login_agreement_show_btn = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/agreement_show',
                                                             wait_type=Wait_By.VISIBILITY_OF)
        self.login_input_password_edit = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/et_pwd',
                                                     wait_type=Wait_By.VISIBILITY_OF)

        # email_login
        self.login_email_element = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/tabitem_email',
                                                     wait_type=Wait_By.VISIBILITY_OF)
        self.login_email_input_container = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/loginf_ll_email_login',
                                                     wait_type=Wait_By.VISIBILITY_OF)
        self.login_email_input_email_edit = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/loginf_et_username',
                                                     wait_type=Wait_By.VISIBILITY_OF)


        # phone_login
        self.login_phone_element = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/tabitem_phone',
                                                     wait_type=Wait_By.VISIBILITY_OF)
        self.login_phone_spinner_phone_code = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/spinner_phonecode',
                                                                  wait_type=Wait_By.VISIBILITY_OF)
        self.login_phone_input_phone_edit = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/et_phonenumber',
                                                                    wait_type=Wait_By.VISIBILITY_OF)

        # tv_notice
        self.login_notice_id = CreateElement.create(Locator_Type.ID,
                                                    'com.mm.droid.livetv.stb31023418:id/loada_tv_notice',
                                                    wait_type=Wait_By.VISIBILITY_OF)

        # email account select popup
        self.login_select_account_popup_title = CreateElement.create(Locator_Type.ID,
                                                                        'com.mm.droid.livetv.stb31023418:id/loginf_tv_welcome',
                                                                        wait_type=Wait_By.VISIBILITY_OF)
        self.login_select_account_popup_logo = CreateElement.create(Locator_Type.ID,
                                                                        'com.mm.droid.livetv.stb31023418:id/loginf_iv_logo',
                                                                        wait_type=Wait_By.VISIBILITY_OF)
        self.login_select_account_popup_account_container = CreateElement.create(Locator_Type.ID,
                                                                            'com.mm.droid.livetv.stb31023418:id/userlistdlg_rv_userlist',
                                                                            wait_type=Wait_By.VISIBILITY_OF)
        self.login_select_account_popup_first_account_item = CreateElement.create(Locator_Type.XPATH,
                                                                            '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[1]/android.widget.TextView',
                                                                            wait_type=Wait_By.VISIBILITY_OF)