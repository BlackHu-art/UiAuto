#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :  
 @time        :    10:28
"""
from page_objects.createElement import CreateElement
from page_objects.doozy_tv.wait_type import Wait_Type as Wait_By
from page_objects.doozy_tv.locator_type import Locator_Type


class HomePageElements:
    def __init__(self):
        # 顶部按钮container
        self.home_top_rl_menu_container = CreateElement.create(Locator_Type.ID,
                                                               'com.mm.droid.livetv.stb31023418:id/rl_menu',
                                                               wait_type=Wait_By.VISIBILITY_OF)
        # home页面频道大banner
        self.home_channel_banner_container = CreateElement.create(Locator_Type.ID,'com.mm.droid.livetv.stb31023418:id/rl_home_banner_btns',
                                                                  wait_type=Wait_By.VISIBILITY_OF)
        self.home_channel_banner_name_text = CreateElement.create(Locator_Type.ID,
                                                             'com.mm.droid.livetv.stb31023418:id/tv_details_name',
                                                             wait_type=Wait_By.VISIBILITY_OF)
        self.home_channel_banner_play_btn = CreateElement.create(Locator_Type.ID,'com.mm.droid.livetv.stb31023418:id/play_ll',
                                                                 wait_type=Wait_By.VISIBILITY_OF)
        self.home_channel_banner_play_text = CreateElement.create(Locator_Type.ID,'com.mm.droid.livetv.stb31023418:id/play_icon_tv',
                                                                  wait_type=Wait_By.VISIBILITY_OF)
        # home页面推荐频道列表   CHANNELS FOR YOU
        self.home_recommend_channel_list_name_container = CreateElement.create(Locator_Type.ID,
                                                                    'com.mm.droid.livetv.stb31023418:id/lb_row_container_header_dock',
                                                                    wait_type=Wait_By.VISIBILITY_OF)
        self.home_recommend_channel_list_name_text = CreateElement.create(Locator_Type.ID,'com.mm.droid.livetv.stb31023418:id/row_header',
                                                                          wait_type=Wait_By.VISIBILITY_OF)
        self.home_recommend_channel_list_container = CreateElement.create(Locator_Type.ID,'com.mm.droid.livetv.stb31023418:id/base_row_content',
                                                                          wait_type=Wait_By.VISIBILITY_OF)
        self.home_recommend_channel_list_lock_icon = CreateElement.create(Locator_Type.XPATH,'//android.widget.GridView[@content-desc="CHANNELS FOR YOU"]/android.widget.FrameLayout[1]/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.ImageView',
                                                                               wait_type=Wait_By.VISIBILITY_OF)
        self.home_recommend_channel_list_first_channel = CreateElement.create(Locator_Type.XPATH,'//android.widget.GridView[@content-desc="CHANNELS FOR YOU"]/android.widget.FrameLayout[1]/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.ImageView',
                                                                              wait_type=Wait_By.VISIBILITY_OF)
        self.home_recommend_channel_list_first_channel_name = CreateElement.create(Locator_Type.XPATH,'//android.widget.GridView[@content-desc="CHANNELS FOR YOU"]/android.widget.FrameLayout[1]/android.widget.LinearLayout/android.widget.TextView',
                                                                                   wait_type=Wait_By.VISIBILITY_OF)

        # loading
        self.home_loading_container = CreateElement.create(Locator_Type.ID,
                                                           'com.mm.droid.livetv.stb31023418:id/liveloadf_ll_loading',
                                                           wait_type=Wait_By.VISIBILITY_OF)
        self.home_loading_icon = CreateElement.create(Locator_Type.ID,
                                                      '	com.mm.droid.livetv.stb31023418:id/liveloadf_slv',
                                                      wait_type=Wait_By.VISIBILITY_OF)
        self.home_loading_text = CreateElement.create(Locator_Type.ID,
                                                      'com.mm.droid.live tv.stb31023418:id/liveloadf_tv_loading_text',
                                                      wait_type=Wait_By.VISIBILITY_OF)
