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


class MyPlansPageElements:
    def __init__(self):
        self.my_plans_page_title = CreateElement.create(Locator_Type.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.TextView',
                                                        wait_type=Wait_By.VISIBILITY_OF)
        self.my_plans_list = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/planlist_lv_plan_list',
                                                          wait_type=Wait_By.VISIBILITY_OF)
        self.my_plans_list_item_product_name = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/planlistf_item_prodct_name',
                                                                    wait_type=Wait_By.VISIBILITY_OF)
        self.my_plans_list_item_prodct_expired_date = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/planlistf_item_prodct_expired_date',
                                                                          wait_type=Wait_By.VISIBILITY_OF)
        # ad banner
        self.my_plans_ad_banner_container = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/ll_banner',
                                                      wait_type=Wait_By.VISIBILITY_OF)
        self.my_plans_ad_banner_item = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/ad_banner',
                                                            wait_type=Wait_By.VISIBILITY_OF)