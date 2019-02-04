#!/usr/bin/env python
# encoding: utf-8
'''
@author: AnthonyZero
@file: main.py
@time: 2019/2/4 16:24
@desc:
'''

from scrapy.cmdline import execute
import os
import sys

path = os.path.dirname(os.path.abspath(__file__))
print(path)
sys.path.append(path)