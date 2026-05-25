#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :  
 @time        :    11:24
"""
from page_objects.createElement import CreateElement
from page_objects.doozy_tv.wait_type import Wait_Type as Wait_By
from page_objects.doozy_tv.locator_type import Locator_Type


class ProfilePageElements:
    def __init__(self):
        # 跑马灯消息容器 进入页面光标默认在profile_account_bind
        self.profile_horse_view_container = CreateElement.create(Locator_Type.XPATH,
                                                                 '//android.widget.FrameLayout[@resource-id="com.mm.droid.livetv.stb31023418:id/profile_layout"]/android.widget.LinearLayout/android.widget.RelativeLayout',
                                                                 wait_type=Wait_By.VISIBILITY_OF)
        # account container
        self.profile_account_icon = CreateElement.create(Locator_Type.XPATH,
                                                         '//android.widget.FrameLayout[@resource-id="com.mm.droid.livetv.stb31023418:id/profile_layout"]/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.ImageView',
                                                         wait_type=Wait_By.VISIBILITY_OF)
        self.profile_account_userid = CreateElement.create(Locator_Type.ID,
                                                           'com.mm.droid.livetv.stb31023418:id/myaccountf_tv_account_userid',
                                                           wait_type=Wait_By.VISIBILITY_OF)
        self.profile_account_bind_btn = CreateElement.create(Locator_Type.ID,
                                                             'com.mm.droid.livetv.stb31023418:id/myaccountf_bind_info_bt',
                                                             wait_type=Wait_By.VISIBILITY_OF)
        self.profile_account_login_btn = CreateElement.create(Locator_Type.ID,
                                                              'com.mm.droid.livetv.stb31023418:id/myaccountf_btn_account_logout',
                                                              wait_type=Wait_By.VISIBILITY_OF)

        # list_view_container
        self.profile_list_view_container_id = CreateElement.create(Locator_Type.ID,
                                                                   'com.mm.droid.livetv.stb31023418:id/list_view',
                                                                   wait_type=Wait_By.VISIBILITY_OF)

        # recharge_view_container
        self.profile_recharge_view_container = CreateElement.create(Locator_Type.XPATH,
                                                                    '//android.widget.GridView[@resource-id="com.mm.droid.livetv.stb31023418:id/list_view"]/android.widget.RelativeLayout[1]',
                                                                    wait_type=Wait_By.VISIBILITY_OF)
        self.profile_recharge_icon = CreateElement.create(Locator_Type.XPATH,
                                                          '(//android.widget.ImageView[@resource-id="com.mm.droid.livetv.stb31023418:id/leftmenulistitem_iv_icons"])[1]',
                                                          wait_type=Wait_By.VISIBILITY_OF)
        self.profile_recharge_text = CreateElement.create(Locator_Type.XPATH,
                                                          '//android.widget.TextView[@resource-id="com.mm.droid.livetv.stb31023418:id/leftmenulistitem_mtv_item_name" and @text="Recharge"]',
                                                          wait_type=Wait_By.VISIBILITY_OF)
        # my_paln_view_container
        self.profile_my_plan_view_container = CreateElement.create(Locator_Type.XPATH,
                                                                   '//android.widget.GridView[@resource-id="com.mm.droid.livetv.stb31023418:id/list_view"]/android.widget.RelativeLayout[2]',
                                                                   wait_type=Wait_By.VISIBILITY_OF)
        self.profile_my_plan_icon = CreateElement.create(Locator_Type.XPATH,
                                                         '(//android.widget.ImageView[@resource-id="com.mm.droid.livetv.stb31023418:id/leftmenulistitem_iv_icons"])[2]',
                                                         wait_type=Wait_By.VISIBILITY_OF)
        self.profile_my_plan_text = CreateElement.create(Locator_Type.XPATH,
                                                         '//android.widget.TextView[@resource-id="com.mm.droid.livetv.stb31023418:id/leftmenulistitem_mtv_item_name" and @text="My plans"]',
                                                         wait_type=Wait_By.VISIBILITY_OF)
        # profile_info_view_container
        self.profile_info_view_container = CreateElement.create(Locator_Type.XPATH,
                                                                '//android.widget.GridView[@resource-id="com.mm.droid.livetv.stb31023418:id/list_view"]/android.widget.RelativeLayout[3]',
                                                                wait_type=Wait_By.VISIBILITY_OF)
        self.profile_info_icon = CreateElement.create(Locator_Type.XPATH,
                                                      '(//android.widget.ImageView[@resource-id="com.mm.droid.livetv.stb31023418:id/leftmenulistitem_iv_icons"])[3]',
                                                      wait_type=Wait_By.VISIBILITY_OF)
        self.profile_info_text = CreateElement.create(Locator_Type.XPATH,
                                                      '//android.widget.TextView[@resource-id="com.mm.droid.livetv.stb31023418:id/leftmenulistitem_mtv_item_name" and @text="Info"]',
                                                      wait_type=Wait_By.VISIBILITY_OF)

        # profile_notification_view_container
        self.profile_notification_view_container = CreateElement.create(Locator_Type.XPATH,
                                                                        '//android.widget.GridView[@resource-id="com.mm.droid.livetv.stb31023418:id/list_view"]/android.widget.RelativeLayout[4]',
                                                                        wait_type=Wait_By.VISIBILITY_OF)
        self.profile_notification_icon = CreateElement.create(Locator_Type.XPATH,
                                                              '(//android.widget.ImageView[@resource-id="com.mm.droid.livetv.stb31023418:id/leftmenulistitem_iv_icons"])[4]',
                                                              wait_type=Wait_By.VISIBILITY_OF)
        self.profile_notification_text = CreateElement.create(Locator_Type.XPATH,
                                                              '//android.widget.TextView[@resource-id="com.mm.droid.livetv.stb31023418:id/leftmenulistitem_mtv_item_name" and @text="Notification"]',
                                                              wait_type=Wait_By.VISIBILITY_OF)

        # profile_setting_view_container
        self.profile_setting_view_container = CreateElement.create(Locator_Type.XPATH,
                                                                   '//android.widget.GridView[@resource-id="com.mm.droid.livetv.stb31023418:id/list_view"]/android.widget.RelativeLayout[5]',
                                                                   wait_type=Wait_By.VISIBILITY_OF)
        self.profile_setting_icon = CreateElement.create(Locator_Type.XPATH,
                                                         '(//android.widget.ImageView[@resource-id="com.mm.droid.livetv.stb31023418:id/leftmenulistitem_iv_icons"])[5]',
                                                         wait_type=Wait_By.VISIBILITY_OF)
        self.profile_setting_text = CreateElement.create(Locator_Type.XPATH,
                                                         '//android.widget.TextView[@resource-id="com.mm.droid.livetv.stb31023418:id/leftmenulistitem_mtv_item_name" and @text="Setting"]',
                                                         wait_type=Wait_By.VISIBILITY_OF)
