#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :
 @time        :  2024/10/10 11:01
"""
from page_objects.createElement import CreateElement
from page_objects.doozy_tv.wait_type import Wait_Type as Wait_By
from page_objects.doozy_tv.locator_type import Locator_Type


class StartPageElements:
    def __init__(self):

        self.permission_container = CreateElement.create(Locator_Type.ID, 'com.android.permissioncontroller:id/grant_dialog',
                                                    wait_type=Wait_By.VISIBILITY_OF)
        self.permission_allow_button = CreateElement.create(Locator_Type.ID, 'com.android.permissioncontroller:id/permission_allow_button',
                                              wait_type=Wait_By.VISIBILITY_OF)
        self.permission_deny_button = CreateElement.create(Locator_Type.ID, 'com.android.permissioncontroller:id/permission_deny_button',
                                                           wait_type=Wait_By.VISIBILITY_OF)
