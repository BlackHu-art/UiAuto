#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :  
 @time        :    14:23
"""
from page_objects.createElement import CreateElement
from page_objects.doozy_tv.wait_type import Wait_Type as Wait_By
from page_objects.doozy_tv.locator_type import Locator_Type


class InfoPageElements:
    def __init__(self):
        self.info_page_title = CreateElement.create(Locator_Type.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.LinearLayout[1]/android.widget.TextView[1]',
                                                    wait_type=Wait_By.VISIBILITY_OF)
        self.info_page_ad_banner = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/ad_banner',
                                                        wait_type=Wait_By.VISIBILITY_OF)
        # check update
        self.info_page_check_update_container = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/reset_virtual_code_rl',
                                                              wait_type=Wait_By.VISIBILITY_OF)
        self.info_page_check_update_btn = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/contactf_btn_info_upgrade',
                                                               wait_type=Wait_By.VISIBILITY_OF)
        self.info_page_check_update_text = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/contactf_tv_check',
                                                                wait_type=Wait_By.VISIBILITY_OF)
        self.info_page_check_update_current_version_text = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/contactf_tv_version',
                                                                wait_type=Wait_By.VISIBILITY_OF)
        # feedback
        self.info_page_feedback_btn = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/contactf_btn_feedback',
                                                                wait_type=Wait_By.VISIBILITY_OF)
        # terms & policy
        self.info_page_terms_policy_btn = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/contactf_btn_agreement',
                                                                wait_type=Wait_By.VISIBILITY_OF)

        # mac text
        self.info_page_mac_text = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/contactf_tv_info_mac',
                                                       wait_type=Wait_By.VISIBILITY_OF)
        # tips
        self.info_page_tips1_text = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/contactf_tv_info_1',
                                                       wait_type=Wait_By.VISIBILITY_OF)
        self.info_page_tips2_text = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/contactf_tv_info_2',
                                                         wait_type=Wait_By.VISIBILITY_OF)
        # security level info
        self.info_page_security_level_text_container = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/security_level_info',
                                                       wait_type=Wait_By.VISIBILITY_OF)
        self.info_page_max_hdcp_level = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/max_hdcp_level',
                                                             wait_type=Wait_By.VISIBILITY_OF)
        self.info_page_current_hdcp_level = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/current_hdcp_level',
                                                                 wait_type=Wait_By.VISIBILITY_OF)
        self.info_page_security_level = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/security_level',
                                                             wait_type=Wait_By.VISIBILITY_OF)

        # 点击升级检测pop，没有升级配置
        self.info_page_check_update_pop_tips = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/upgradesamedlg_tv_tips',
                                                                        wait_type=Wait_By.VISIBILITY_OF)
        self.info_page_check_update_pop_icon = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/upgradesamedlg_iv_icon',
                                                                    wait_type=Wait_By.VISIBILITY_OF)