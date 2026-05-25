#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :  
 @time        :    15:41
"""
from page_objects.createElement import CreateElement
from page_objects.doozy_tv.wait_type import Wait_Type as Wait_By
from page_objects.doozy_tv.locator_type import Locator_Type


class SettingPageElements:
    def __init__(self):
        self.setting_title = CreateElement.create(Locator_Type.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.TextView',
                                                  wait_type=Wait_By.VISIBILITY_OF)
        self.setting_container = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/system_setting_layout',
                                                    wait_type=Wait_By.VISIBILITY_OF)
        self.setting_language_list_container = CreateElement.create(Locator_Type.ID, 'android:id/list_container',
                                                                    wait_type=Wait_By.VISIBILITY_OF)
        # 需要点击setting_language_list_container下面的item才能显示出来   、xpath
        self.setting_language_list_item_follow = CreateElement.create(Locator_Type.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.TextView[1]',
                                                              wait_type=Wait_By.VISIBILITY_OF)
        self.setting_language_list_item_english = CreateElement.create(Locator_Type.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.TextView[2]',
                                                              wait_type=Wait_By.VISIBILITY_OF)
        self.setting_language_list_item_Portuguese = CreateElement.create(Locator_Type.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.TextView[3]',
                                                              wait_type=Wait_By.VISIBILITY_OF)
        self.setting_language_list_item_Spanish = CreateElement.create(Locator_Type.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.TextView[4]',
                                                              wait_type=Wait_By.VISIBILITY_OF)
        # 网络测速
        self.setting_network_diagnosis_container = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/network_diagnosis_layout',
                                                                    wait_type=Wait_By.VISIBILITY_OF)
        self.setting_network_diagnosis_code = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/network_diagnosis_code',
                                                             wait_type=Wait_By.VISIBILITY_OF)
        # 测速页面 & 测速结果文案获取需要等待2分钟，文案获取通过Xpath
        # 尝试使用network_diagnosis_see_more_btn等待测试结束按钮出现
        self.network_diagnosis_page = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/ndlayout',
                                                                   wait_type=Wait_By.VISIBILITY_OF)
        self.network_diagnosis_internet_connect_text = CreateElement.create(Locator_Type.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.view.ViewGroup/android.view.ViewGroup[1]/android.widget.TextView[2]',
                                                                            wait_type=Wait_By.VISIBILITY_OF)
        self.network_diagnosis_feedback_btn = CreateElement.create(Locator_Type.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.TextView[4]',
                                                                   wait_type=Wait_By.ELEMENT_TO_BE_CLICKABLE)
        self.network_re_diagnosis_btn = CreateElement.create(Locator_Type.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.TextView[5]',
                                                             wait_type=Wait_By.ELEMENT_TO_BE_CLICKABLE)
        self.network_diagnosis_see_more_btn = CreateElement.create(Locator_Type.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.view.ViewGroup/android.view.ViewGroup[4]/android.widget.TextView[3]',
                                                                   wait_type=Wait_By.VISIBILITY_OF)