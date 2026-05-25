#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :  
 @time        :    14:43
"""
from page_objects.createElement import CreateElement
from page_objects.doozy_tv.wait_type import Wait_Type as Wait_By
from page_objects.doozy_tv.locator_type import Locator_Type


class FeedBackPageElements:
    def __init__(self):
        # feedback page
        self.feedback_element = CreateElement.create(Locator_Type.ID,'com.mm.droid.livetv.stb31023418:id/tv_feedback',
                                                     wait_type=Wait_By.VISIBILITY_OF)
        self.feedback_container = CreateElement.create(Locator_Type.ID,'com.mm.droid.livetv.stb31023418:id/feedbackf_ll_question_parent',
                                                     wait_type=Wait_By.VISIBILITY_OF)
        self.feedback_title_text = CreateElement.create(Locator_Type.ID,'com.mm.droid.livetv.stb31023418:id/feedbackf_tv_title',
                                                        wait_type=Wait_By.VISIBILITY_OF)
        self.feedback_question_list_container = CreateElement.create(Locator_Type.ID,'com.mm.droid.livetv.stb31023418:id/feedbackf_plv_feedback',
                                                                     wait_type=Wait_By.VISIBILITY_OF)
        self.feedback_remind_text = CreateElement.create(Locator_Type.ID,'com.mm.droid.livetv.stb31023418:id/feedbackf_tv_remind1',
                                                         wait_type=Wait_By.VISIBILITY_OF)

        # FAQ page
        self.faq_element = CreateElement.create(Locator_Type.ID,'com.mm.droid.livetv.stb31023418:id/tv_faq',
                                                     wait_type=Wait_By.VISIBILITY_OF)
        self.faq_container = CreateElement.create(Locator_Type.ID,'com.mm.droid.livetv.stb31023418:id/vp_content',
                                                  wait_type=Wait_By.VISIBILITY_OF)
        self.faq_list_container = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/lv_question',
                                                       wait_type=Wait_By.VISIBILITY_OF)

        # contact 元素存在乱写，顺序及定义不对
        self.contact_element = CreateElement.create(Locator_Type.ID,'com.mm.droid.livetv.stb31023418:id/tv_contact',
                                                     wait_type=Wait_By.VISIBILITY_OF)
        self.contact_container = CreateElement.create(Locator_Type.ID,'com.mm.droid.livetv.stb31023418:id/vp_content',
                                                      wait_type=Wait_By.VISIBILITY_OF)
        self.contact_title_text = CreateElement.create(Locator_Type.ID,'com.mm.droid.livetv.stb31023418:id/tv_title',
                                                       wait_type=Wait_By.VISIBILITY_OF)
        self.contact_email_container = CreateElement.create(Locator_Type.ID,'com.mm.droid.livetv.stb31023418:id/email_parent',
                                                            wait_type=Wait_By.VISIBILITY_OF)
        self.contact_group_container = CreateElement.create(Locator_Type.ID,'com.mm.droid.livetv.stb31023418:id/group_parent',
                                                            wait_type=Wait_By.VISIBILITY_OF)
        self.contact_official_website_container = CreateElement.create(Locator_Type.ID,'com.mm.droid.livetv.stb31023418:id/official_parent',
                                                            wait_type=Wait_By.VISIBILITY_OF)


        self.contact_remind_text = CreateElement.create(Locator_Type.ID,'com.mm.droid.livetv.stb31023418:id/tv_contact_remind',
                                                        wait_type=Wait_By.VISIBILITY_OF)