#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :  
 @time        :    16:52
"""
from common.logger.logTool import logger
from appium.webdriver import Remote


class TvRemoteOperator:
    """封装遥控器按键代码"""
    UP = 19             # KEYCODE_DPAD_UP
    DOWN = 20           # KEYCODE_DPAD_DOWN
    LEFT = 21           # KEYCODE_DPAD_LEFT
    RIGHT = 22          # KEYCODE_DPAD_RIGHT
    CENTER = 23         # KEYCODE_DPAD_CENTER (OK键)
    BACK = 4            # KEYCODE_BACK
    HOME = 3            # KEYCODE_HOME
    MENU = 1            # KEYCODE_MENU
    VOLUME_UP = 24      # KEYCODE_VOLUME_UP
    VOLUME_DOWN = 25    # KEYCODE_VOLUME_DOWN
    MUTE = 164          # KEYCODE_MUTE
    POWER = 26          # KEYCODE_POWER
    ENTER = 66          # KEYCODE_ENTER
    CHANNEL_UP = 166    # KEYCODE_CHANNEL_UP
    CHANNEL_DOWN = 167  # KEYCODE_CHANNEL_DOWN
    PLAY = 126          # KEYCODE_MEDIA_PLAY
    PAUSE = 127         # KEYCODE_MEDIA_PAUSE
    STOP = 86           # KEYCODE_MEDIA_STOP
    REWIND = 89         # KEYCODE_MEDIA_REWIND
    FAST_FORWARD = 90   # KEYCODE_MEDIA_FAST_FORWARD
    NEXT = 87           # KEYCODE_MEDIA_NEXT
    PREVIOUS = 88       # KEYCODE_MEDIA_PREVIOUS
    GUIDE = 172         # KEYCODE_GUIDE
    INFO = 165          # KEYCODE_INFO
    SETTINGS = 176      # KEYCODE_SETTINGS
    PICTURE_IN_PICTURE = 252  # KEYCODE_PICTURE_IN_PICTURE
    TV_INPUT = 178      # KEYCODE_TV_INPUT
    DVR = 173           # KEYCODE_DVR
    CAPTIONS = 175      # KEYCODE_CAPTIONS
    SAP = 174           # KEYCODE_SAP

    # 添加更多根据设备需求的按键...
    @classmethod
    def press_key(cls, driver: Remote, key_name: str):
        """按下指定的按键并打印日志"""
        key_code = getattr(cls, key_name, None)
        if key_code is not None:
            logger.info(f'按下了按键: {key_name} (KeyCode: {key_code})')
            driver.press_keycode(key_code)
        else:
            logger.error(f'无效的按键名称: {key_name}')


# 示例调用代码
# def simulate_remote_control(driver: Remote):
#     # 模拟遥控器的操作
#     TvRemoteOperator.press_key(driver, 'UP')
#     TvRemoteOperator.press_key(driver, 'DOWN')
#     TvRemoteOperator.press_key(driver, 'VOLUME_UP')
#     TvRemoteOperator.press_key(driver, 'POWER')
#     TvRemoteOperator.press_key(driver, 'CENTER')  # OK键