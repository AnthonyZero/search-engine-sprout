#!/usr/bin/env python
# encoding: utf-8
'''
@author: AnthonyZero
@file: config.py
@time: 2019/2/17 22:23
@desc: 读取配置
'''
from configparser import ConfigParser
import os
base_dir = os.path.dirname(os.path.dirname(__file__))
file_path = base_dir + "/config.ini"  # 配置文件绝对路径

class ConfigUtils(object):
    def __init__(self):
        super(ConfigUtils, self).__init__()
        try:
            self.config = ConfigParser()
            self.config.read(file_path)
        except IOError as e:
            print("Error: 没有找到文件或读取文件失败")

    def get_value(self, section, key):
        return self.config.get(section, key)

if __name__ == '__main__':
    co = ConfigUtils()
    print(co.config.sections())
    print(co.config.options('mysql-database'))
    print(co.config.get('mysql-database', 'host'))