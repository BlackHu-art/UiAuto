#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :  
 @time        :    14:16
"""
from page_objects.createElement import CreateElement
from page_objects.doozy_tv.wait_type import Wait_Type as Wait_By
from page_objects.doozy_tv.locator_type import Locator_Type


class PurchasePageElements:
    def __init__(self):
        self.purchase_qr_code_container = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/ll_qr_code',
                                                               wait_type=Wait_By.VISIBILITY_OF)
        self.purchase_code_image = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/iv_qrcode',
                                                           wait_type=Wait_By.VISIBILITY_OF)
        self.purchase_code_refresh_btn = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/qrcode_refresh',
                                                              wait_type=Wait_By.VISIBILITY_OF)
        self.purchase_see_payment_btn = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/qrcode_refresh_check',
                                                             wait_type=Wait_By.VISIBILITY_OF)

        # purchase text
        self.purchase_info_container = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/ll_purchase_txt',
                                                   wait_type=Wait_By.VISIBILITY_OF)
        self.purchase_info_title_text = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/renew_recharge_tip_title',
                                                     wait_type=Wait_By.VISIBILITY_OF)
        self.purchase_info_tips_text = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/renew_recharge_tip',
                                                            wait_type=Wait_By.VISIBILITY_OF)