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


class BindInfoPageElements:
    def __init__(self):
        # tv_notice
        self.bind_info_tv_notice_id = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/tv_notice',
                                                 wait_type=Wait_By.VISIBILITY_OF)
        self.bind_info_tv_notice_xpath = CreateElement.create(Locator_Type.XPATH,
                                                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.TextView',
                                                    wait_type=Wait_By.VISIBILITY_OF)
        # bind_info_container
        self.bind_info_container = CreateElement.create(Locator_Type.XPATH,
                                                        '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout',
                                                        wait_type=Wait_By.VISIBILITY_OF)
        self.bind_info_big_title = CreateElement.create(Locator_Type.ID,
                                                        'com.mm.droid.livetv.stb31023418:id/loginf_tv_welcome',
                                                        wait_type=Wait_By.VISIBILITY_OF)
        self.bind_info_tips = CreateElement.create(Locator_Type.ID,
                                                   'com.mm.droid.livetv.stb31023418:id/loginf_tv_account_tip',
                                                   wait_type=Wait_By.VISIBILITY_OF)
        # bind_info_email_container
        self.bind_info_email_container = CreateElement.create(Locator_Type.ID,
                                                              'com.mm.droid.livetv.stb31023418:id/bind_email_rl',
                                                              wait_type=Wait_By.VISIBILITY_OF)
        self.bind_info_email_icon = CreateElement.create(Locator_Type.ID,
                                                         'com.mm.droid.livetv.stb31023418:id/bind_email_iv',
                                                         wait_type=Wait_By.VISIBILITY_OF)
        self.bind_info_email_text = CreateElement.create(Locator_Type.ID,
                                                         'com.mm.droid.livetv.stb31023418:id/bind_email_tv',
                                                         wait_type=Wait_By.VISIBILITY_OF)
        self.bind_info_email_acc_text = CreateElement.create(Locator_Type.ID,
                                                             'com.mm.droid.livetv.stb31023418:id/email_info_tv',
                                                             wait_type=Wait_By.VISIBILITY_OF)
        self.bind_info_email_acc_text = CreateElement.create(Locator_Type.ID,
                                                             'com.mm.droid.livetv.stb31023418:id/bind_phone_action_tv',
                                                             wait_type=Wait_By.VISIBILITY_OF)
        # bind_info_phone_container
        self.bind_info_phone_container = CreateElement.create(Locator_Type.ID,
                                                              'com.mm.droid.livetv.stb31023418:id/bind_phone_rl',
                                                              wait_type=Wait_By.VISIBILITY_OF)
        self.bind_info_phone_icon = CreateElement.create(Locator_Type.ID,
                                                         'com.mm.droid.livetv.stb31023418:id/bind_phone_iv',
                                                         wait_type=Wait_By.VISIBILITY_OF)
        self.bind_info_phone_text = CreateElement.create(Locator_Type.ID,
                                                         'com.mm.droid.livetv.stb31023418:id/bind_phone_tv',
                                                         wait_type=Wait_By.VISIBILITY_OF)
        self.bind_info_phone_acc_text = CreateElement.create(Locator_Type.ID,
                                                             'com.mm.droid.livetv.stb31023418:id/phone_info_tv',
                                                             wait_type=Wait_By.VISIBILITY_OF)
        self.bind_info_bind_phone_btn = CreateElement.create(Locator_Type.ID,
                                                             'com.mm.droid.livetv.stb31023418:id/bind_phone_action_tv',
                                                             wait_type=Wait_By.VISIBILITY_OF)
