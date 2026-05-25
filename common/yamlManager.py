#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :  
 @time        :    19:17
"""
from yamlTool import YamlTool


class YamlManager:
    """
    YamlManager类用来管理多个YAML文件的数据操作，包括对嵌套键值的操作。
    """

    def __init__(self, yaml_file_paths):
        """
        初始化方法，加载多个YAML文件。
        :param yaml_file_paths: YAML文件路径列表
        """
        self.editors = {file_path: YamlTool(file_path) for file_path in yaml_file_paths}

    def add_to_file(self, file_path, key, value):
        """
        向指定的YAML文件中添加键值对。
        :param file_path: YAML文件路径
        :param key: 键
        :param value: 值
        """
        editor = self.editors.get(file_path)
        if editor:
            editor.add(key, value)
        else:
            raise FileNotFoundError(f"{file_path} 文件不存在")

    def update_file(self, file_path, key, value):
        """
        更新指定YAML文件中的键值对。
        :param file_path: YAML文件路径
        :param key: 键
        :param value: 新值
        """
        editor = self.editors.get(file_path)
        if editor:
            editor.update(key, value)
        else:
            raise FileNotFoundError(f"{file_path} 文件不存在")

    def delete_from_file(self, file_path, key):
        """
        从指定YAML文件中删除键值对。
        :param file_path: YAML文件路径
        :param key: 要删除的键
        """
        editor = self.editors.get(file_path)
        if editor:
            editor.delete(key)
        else:
            raise FileNotFoundError(f"{file_path} 文件不存在")

    def get_from_file(self, file_path, key):
        """
        从指定YAML文件中获取键的值。
        :param file_path: YAML文件路径
        :param key: 要获取的键
        :return: 返回键对应的值
        """
        editor = self.editors.get(file_path)
        if editor:
            return editor.get(key)
        else:
            raise FileNotFoundError(f"{file_path} 文件不存在")

    def get_nested_value(self, file_path, parent_key, child_key):
        """
        获取嵌套键中的值。
        :param file_path: YAML文件路径
        :param parent_key: 父键
        :param child_key: 子键
        :return: 返回子键的值
        """
        editor = self.editors.get(file_path)
        if editor:
            return editor.get_nested_value(parent_key, child_key)
        else:
            raise FileNotFoundError(f"{file_path} 文件不存在")

    def update_nested_value(self, file_path, parent_key, child_key, new_value):
        """
        更新嵌套键中的值。
        :param file_path: YAML文件路径
        :param parent_key: 父键
        :param child_key: 子键
        :param new_value: 新值
        """
        editor = self.editors.get(file_path)
        if editor:
            editor.update_nested_value(parent_key, child_key, new_value)
        else:
            raise FileNotFoundError(f"{file_path} 文件不存在")


if __name__ == '__main__':
    yaml_manager = YamlManager(['config/example.yaml', 'config2.yaml'])

    # 获取config2.yaml中desired_caps_mi6的platformVersion值
    yaml_manager.get_nested_value('config/example.yaml', 'desired_caps_mi6', 'platformVersion')

    # 更新config2.yaml中desired_caps_mi6的platformVersion值为10
    yaml_manager.update_nested_value('config/example.yaml', 'desired_caps_mi6', 'platformVersion', 1000)

