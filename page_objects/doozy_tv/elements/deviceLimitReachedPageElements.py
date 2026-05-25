#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :  
 @time        :    10:05
"""
from page_objects.createElement import CreateElement
from page_objects.doozy_tv.wait_type import Wait_Type as Wait_By
from page_objects.doozy_tv.locator_type import Locator_Type


class DeviceLimitReachedPageElements:

    def __init__(self):
        self.device_limit_reached_container = CreateElement.create(Locator_Type.XPATH,
                                                                   '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout',
                                                                   wait_type=Wait_By.VISIBILITY_OF)
        self.device_limit_reached_text_container = CreateElement.create(Locator_Type.XPATH,
                                                                        '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[1]',
                                                                        wait_type=Wait_By.VISIBILITY_OF)
        self.device_limit_reached_text = CreateElement.create(Locator_Type.ID,
                                                              'com.mm.droid.livetv.stb31023418:id/forcelogoutdlg_tv_title',
                                                              wait_type=Wait_By.VISIBILITY_OF)
        self.device_limit_reached_button_container = CreateElement.create(Locator_Type.XPATH,
                                                                          '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]',
                                                                          wait_type=Wait_By.VISIBILITY_OF)
        self.device_limit_reached_button_exit = CreateElement.create(Locator_Type.ID,
                                                                     'com.mm.droid.livetv.stb31023418:id/forcelogoutdlg_btn_exit',
                                                                     wait_type=Wait_By.VISIBILITY_OF)
        self.device_limit_reached_button_login = CreateElement.create(Locator_Type.XPATH,
                                                                      'com.mm.droid.livetv.stb31023418:id/forcelogoutdlg_btn_login',
                                                                      wait_type=Wait_By.VISIBILITY_OF)
