#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :  
 @time        :    15:21
"""
from page_objects.createElement import CreateElement
from page_objects.doozy_tv.wait_type import Wait_Type as Wait_By
from page_objects.doozy_tv.locator_type import Locator_Type


class AgreeePageElements:
    def __init__(self):
        # tv_notice
        self.login_notice_id = CreateElement.create(Locator_Type.ID,
                                                    'com.mm.droid.livetv.stb31023418:id/tv_notice',
                                                    wait_type=Wait_By.VISIBILITY_OF)

        # agreement_container
        self.agreement_box_id = CreateElement.create(Locator_Type.ID,
                                                     'com.mm.droid.livetv.stb31023418:id/ll_agreement_box',
                                                     wait_type=Wait_By.VISIBILITY_OF)
        self.agreement_tab_container_id = CreateElement.create(Locator_Type.ID,
                                                               'com.mm.droid.livetv.stb31023418:id/agreement_tab',
                                                               wait_type=Wait_By.VISIBILITY_OF)
        self.privacy_policy_tab_id = CreateElement.create(Locator_Type.XPATH,
                                                          '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.ListView/android.widget.RelativeLayout[1]/android.widget.Button',
                                                          wait_type=Wait_By.VISIBILITY_OF)
        self.privacy_user_agreement_tab_id = CreateElement.create(Locator_Type.XPATH,
                                                                  '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.ListView/android.widget.RelativeLayout[2]/android.widget.Button',
                                                                  wait_type=Wait_By.VISIBILITY_OF)
