#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :  
 @time        :    17:06
"""
from page_objects.createElement import CreateElement
from page_objects.doozy_tv.wait_type import Wait_Type as Wait_By
from page_objects.doozy_tv.locator_type import Locator_Type


class UpdateElements:
    def __init__(self):
        self.update_title_new_version = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/tv_new_version',
                                                             wait_type=Wait_By.VISIBILITY_OF)
        self.update_title_current_version = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/tv_current_version',
                                                                 wait_type=Wait_By.VISIBILITY_OF)
        self.update_note_title = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/tv_update_select',
                                                      wait_type=Wait_By.VISIBILITY_OF)
        self.update_note_content = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/upgrade_text',
                                                       wait_type=Wait_By.VISIBILITY_OF)

        self.update_later_btn = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/btn_cancel',
                                                      wait_type=Wait_By.VISIBILITY_OF)
        self.update_update_btn = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/btn_cancel',
                                                 wait_type=Wait_By.VISIBILITY_OF)
