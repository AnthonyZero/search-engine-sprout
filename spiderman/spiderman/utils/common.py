#!/usr/bin/env python
# encoding: utf-8
'''
@author: AnthonyZero
@file: common.py
@time: 2019/2/6 23:37
@desc:
'''

import hashlib

def get_md5(url):
    if isinstance(url, str):
        url = url.encode('utf-8')
    obj = hashlib.md5()
    obj.update(url)
    return obj.hexdigest()

if __name__ == '__main__':
    print(get_md5('www.baidu.com'))