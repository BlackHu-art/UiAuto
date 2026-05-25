#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :  
 @time        :    14:05
"""
from page_objects.createElement import CreateElement
from page_objects.doozy_tv.wait_type import Wait_Type as Wait_By
from page_objects.doozy_tv.locator_type import Locator_Type


class BindToPhoneElements:
    def __init__(self):
        # tv_notice
        self.bind_phone_tv_notice_id = CreateElement.create(Locator_Type.ID,
                                                            'com.mm.droid.livetv.stb31023418:id/tv_notice',
                                                            wait_type=Wait_By.VISIBILITY_OF)
        self.bind_phone_tv_notice_xpath = CreateElement.create(Locator_Type.XPATH,
                                                               '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.TextView',
                                                               wait_type=Wait_By.VISIBILITY_OF)
        # bind_phone_back_btn
        self.bind_phone_back_btn = CreateElement.create(Locator_Type.ID,
                                                        'com.mm.droid.livetv.stb31023418:id/resetpwd_tv_return',
                                                        wait_type=Wait_By.VISIBILITY_OF)

        # bind_phone_container
        self.bind_phone_container = CreateElement.create(Locator_Type.XPATH,
                                                         '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout',
                                                         wait_type=Wait_By.VISIBILITY_OF)
        self.bind_phone_title_text = CreateElement.create(Locator_Type.ID,
                                                          'com.mm.droid.livetv.stb31023418:id/bind_title_tv',
                                                          wait_type=Wait_By.VISIBILITY_OF)
        self.bind_phone_icon = CreateElement.create(Locator_Type.ID,
                                                    'com.mm.droid.livetv.stb31023418:id/resetpwd_iv_title',
                                                    wait_type=Wait_By.VISIBILITY_OF)
        self.bind_phone_tips_text = CreateElement.create(Locator_Type.ID,
                                                         'com.mm.droid.livetv.stb31023418:id/bind_action_tip_tv',
                                                         wait_type=Wait_By.VISIBILITY_OF)
        self.bind_phone_phone_code_select_btn = CreateElement.create(Locator_Type.ID,
                                                                     'com.mm.droid.livetv.stb31023418:id/spinner_phonecode',
                                                                     wait_type=Wait_By.VISIBILITY_OF)
        self.bind_phone_phone_number_edit_text = CreateElement.create(Locator_Type.ID,
                                                                      'com.mm.droid.livetv.stb31023418:id/et_phonenumber',
                                                                      wait_type=Wait_By.VISIBILITY_OF)
        self.bind_phone_verify_send_btn = CreateElement.create(Locator_Type.ID,
                                                               'com.mm.droid.livetv.stb31023418:id/tv_verify',
                                                               wait_type=Wait_By.VISIBILITY_OF)
        self.bind_phone_verify_edit_text = CreateElement.create(Locator_Type.ID,
                                                                'com.mm.droid.livetv.stb31023418:id/bind_et_verify_code',
                                                                wait_type=Wait_By.VISIBILITY_OF)
        self.bind_phone_submit_btn = CreateElement.create(Locator_Type.ID,
                                                          'com.mm.droid.livetv.stb31023418:id/bind_tv_submit',
                                                          wait_type=Wait_By.VISIBILITY_OF)
