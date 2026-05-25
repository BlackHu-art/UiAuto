#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :  
 @time        :    9:35
"""

import hashlib
import base64
import hmac
import time
import requests


class WebhookSender:
    def __init__(self):
        """
        初始化 WebhookSender 类。

        :param webhook_url: webhook 地址
        :param secret: 秘钥
        """
        self.secret = 'sYVjoLblEp34kKlpJ8x8Jc'
        self.webhook_url = "https://open.larksuite.com/open-apis/bot/v2/hook/5f12ed40-2d4e-4512-9c3b-29ddc80ae094"

    def generate_signature(self, timestamp):
        """
        生成签名字符串。

        :param timestamp: 时间戳
        :return: 签名字符串
        """
        string_to_sign = f'{timestamp}\n{self.secret}'
        hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()
        sign = base64.b64encode(hmac_code).decode('utf-8')
        return sign

    def send_webhook_message(self, content, device_name=None, channel_name=None, path=None):
        """
        发送带有时间戳和签名的消息到指定的 webhook 地址。

        :param content: 消息内容
        :param device_name: 设备名称
        :param channel_name: 通道名称
        :param path: 路径
        :return: 响应状态码和内容
        """

        # 如果 content 为空，则使用默认文本
        if content is None:
            content = "Default message"
        if channel_name is None:
            channel_name = "Default message"
        if path is None:
            path = "Default message"
        if device_name is None:
            device_name = "Default message"

        # 获取当前时间戳
        timestamp = str(int(time.time()))

        # 生成签名字符串
        sign = self.generate_signature(timestamp)

        # 构造请求体
        data = {
            "timestamp": timestamp,
            "sign": sign,
            "msg_type": "interactive",
            "card": {
                "header": {
                    "template": "red",
                    "title": {
                        "content": content,
                        "tag": "plain_text"
                    }
                },
                "elements": [{
                    "tag": "div",
                    "text": {
                        "content": "**device**   : %s \n**channel** : %s \n**path**      : %s" % (
                            device_name, channel_name, path),
                        "tag": "lark_md"
                    }
                }]
            }
        }

        # 设置请求头
        headers = {
            "Content-Type": "application/json",
            "Charset": "UTF-8"
        }

        try:
            # 发送 POST 请求
            response = requests.post(self.webhook_url, json=data, headers=headers, timeout=5)
            # 返回响应状态码和内容
            return response.status_code, response.text
        except requests.exceptions.RequestException as e:
            return None, f"请求失败: {str(e)}"


# 示例用法
if __name__ == "__main__":
    webhook_sender = WebhookSender()

    status_code, response_text = webhook_sender.send_webhook_message("no signal", "B11", "AMC", "//10.0.0.1/Fatfish/Log")
    print(f"Response Status Code: {status_code}")
    print(f"Response Content: {response_text}")

    # 生成从1到210的整数列表
    channel_list = list(range(1, 211))

    # 输出结果
    print(channel_list)

