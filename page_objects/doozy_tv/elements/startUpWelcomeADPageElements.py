#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :  
 @time        :    13:38
"""
from page_objects.createElement import CreateElement
from page_objects.doozy_tv.wait_type import Wait_Type as Wait_By
from page_objects.doozy_tv.locator_type import Locator_Type


class StartUpWelcomeADPageElements:
    def __init__(self):
        self.start_up_welcome_ad_container = CreateElement.create(Locator_Type.ID,
                                                                  'com.mm.droid.livetv.stb31023418:id/loada_iv_ad',
                                                                  wait_type=Wait_By.VISIBILITY_OF)
        self.start_up_welcome_ad_skip_button = CreateElement.create(Locator_Type.ID,
                                                                    'com.mm.droid.livetv.stb31023418:id/loada_ad_canskip',
                                                                    wait_type=Wait_By.VISIBILITY_OF)
        self.start_up_welcome_ad_skip_count_down_text = CreateElement.create(Locator_Type.ID,
                                                                             'com.mm.droid.livetv.stb31023418:id/loada_ad_system_tv',
                                                                             wait_type=Wait_By.VISIBILITY_OF)
