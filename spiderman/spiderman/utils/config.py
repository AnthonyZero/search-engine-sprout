#!/usr/bin/env python
# encoding: utf-8
'''
@author: AnthonyZero
@file: config.py
@time: 2019/2/17 22:23
@desc: 读取配置
'''
from configparser import ConfigParser


class ConfigUtils(object):
    def __init__(self):
        super(ConfigUtils, self).__init__()
        try:
            self.config = ConfigParser()
            self.config.read('config.ini')
        except IOError as e:
            print("Error: 没有找到文件或读取文件失败")

    def get_value(self, section, key):
        return self.config.get(section, key)

if __name__ == '__main__':
    co = ConfigUtils()
    print(co.config.sections())
    print(co.config.options('mysql-database'))
    print(co.config.get('mysql-database', 'host'))