#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :  
 @time        :    20:29
"""
from common.appium.tvRemoteOperator import TvRemoteOperator
from common.logger.logTool import logger


class RemoteControlActions:
    def __init__(self, driver):
        self.driver = driver

    def press_button(self, key_code):
        logger.info(f'Pressing key code: {key_code}')
        self.driver.press_keycode(key_code)

    def press_up(self):
        logger.info('ARROW_UP')
        self.press_button(TvRemoteOperator.UP)

    def press_down(self):
        logger.info('ARROW_DOWN')
        self.press_button(TvRemoteOperator.DOWN)

    def press_left(self):
        logger.info('ARROW_LEFT')
        self.press_button(TvRemoteOperator.LEFT)

    def press_right(self):
        logger.info('ARROW_RIGHT')
        self.press_button(TvRemoteOperator.RIGHT)

    def press_enter(self):
        logger.info('ENTER_BUTTON')
        self.press_button(TvRemoteOperator.ENTER)

    def press_back(self):
        logger.info('BACK_BUTTON')
        self.press_button(TvRemoteOperator.BACK)

    def press_ok(self):
        logger.info('OK_BUTTON')
        self.press_button(TvRemoteOperator.CENTER)

    def press_home(self):
        logger.info('HOME_BUTTON')
        self.press_button(TvRemoteOperator.HOME)

    def press_menu(self):
        logger.info('MENU_BUTTON')
        self.press_button(TvRemoteOperator.MENU)

    def press_volume_up(self):
        logger.info('VOLUME_UP')
        self.press_button(TvRemoteOperator.VOLUME_UP)

    def press_volume_down(self):
        logger.info('VOLUME_DOWN')
        self.press_button(TvRemoteOperator.VOLUME_DOWN)

    def press_mute(self):
        logger.info('MUTE_BUTTON')
        self.press_button(TvRemoteOperator.MUTE)

    def press_power(self):
        logger.info('POWER_BUTTON')
        self.press_button(TvRemoteOperator.POWER)

    def press_channel_up(self):
        logger.info('CHANNEL_UP')
        self.press_button(TvRemoteOperator.CHANNEL_UP)

    def press_channel_down(self):
        logger.info('CHANNEL_DOWN')
        self.press_button(TvRemoteOperator.CHANNEL_DOWN)

    def press_play(self):
        logger.info('PLAY_BUTTON')
        self.press_button(TvRemoteOperator.PLAY)

    def press_pause(self):
        logger.info('PAUSE_BUTTON')
        self.press_button(TvRemoteOperator.PAUSE)

    def press_stop(self):
        logger.info('STOP_BUTTON')
        self.press_button(TvRemoteOperator.STOP)

    def press_rewind(self):
        logger.info('REWIND_BUTTON')
        self.press_button(TvRemoteOperator.REWIND)

    def press_fast_forward(self):
        logger.info('FAST_FORWARD_BUTTON')
        self.press_button(TvRemoteOperator.FAST_FORWARD)

    def press_next(self):
        logger.info('NEXT_BUTTON')
        self.press_button(TvRemoteOperator.NEXT)

    def press_previous(self):
        logger.info('PREVIOUS_BUTTON')
        self.press_button(TvRemoteOperator.PREVIOUS)

    def press_guide(self):
        logger.info('GUIDE_BUTTON')
        self.press_button(TvRemoteOperator.GUIDE)

    def press_info(self):
        logger.info('INFO_BUTTON')
        self.press_button(TvRemoteOperator.INFO)

    def press_settings(self):
        logger.info('SETTINGS_BUTTON')
        self.press_button(TvRemoteOperator.SETTINGS)

    def press_tv_input(self):
        logger.info('TV_INPUT_BUTTON')
        self.press_button(TvRemoteOperator.TV_INPUT)

    def press_dvr(self):
        logger.info('DVR_BUTTON')
        self.press_button(TvRemoteOperator.DVR)

    def press_sap(self):
        logger.info('SAP_BUTTON')
        self.press_button(TvRemoteOperator.SAP)

    def press_captions(self):
        logger.info('CAPTIONS_BUTTON')
        self.press_button(TvRemoteOperator.CAPTIONS)