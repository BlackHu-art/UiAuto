#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :
 @time        :  2024/10/8 11:20
"""
from common.logger.logTool import logger
import platform


def deal_pytest_ini_file():
    """
    当前pytest运行指定的pytest.ini在Windows下编码有bug，故对不同环境进行处理。
    避免使用带BOM的编码来生成pytest.ini文件。
    """
    try:
        # 读取 pytest.conf 文件的内容
        with open('config/pytest.conf', 'r', encoding='utf-8') as pytest_f:
            content = pytest_f.read()

        # 判断操作系统，并根据操作系统写入 pytest.ini
        if platform.system() == 'Windows':
            # 写入时确保不会添加 BOM (不要使用 'utf-8-sig')
            with open('config/pytest.ini', 'w+', encoding='utf-8') as tmp_pytest_f:
                tmp_pytest_f.write(content)
        else:
            with open('config/pytest.ini', 'w+', encoding='utf-8') as tmp_pytest_f:
                tmp_pytest_f.write(content)

        # 检查生成的文件是否包含 BOM，并在需要时删除 BOM
        remove_bom('config/pytest.ini')

    except Exception as e:
        logger.error(f"Error occurred: {e}")


def remove_bom(file_path):
    """
    如果文件以 BOM 开头，移除 BOM。
    :param file_path: 文件路径
    """
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
        # 检查文件是否以 BOM 开头
        if content.startswith(b'\xef\xbb\xbf'):
            logger.warn(f"Removing BOM from {file_path}")
            # 如果存在 BOM，重新写入文件，去除 BOM
            with open(file_path, 'wb') as f:
                f.write(content[3:])
    except Exception as e:
        logger.error(f"Error occurred while removing BOM: {e}")

