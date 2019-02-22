#!/usr/bin/env python
# encoding: utf-8
'''
@author: AnthonyZero
@file: selenium_spider.py
@time: 2019/2/22 23:15
@desc: 通过selenium 爬虫（需要浏览器driver）
'''

# Selenium requires a driver to interface with the chosen browser
from selenium import webdriver

browser = webdriver.Chrome(executable_path='F:/tmp/chromedriver.exe')
browser.get('https://detail.tmall.com/item.htm?spm=a222t.8063993.9145579178.15.5ea84546Lbpfeq&acm=lb-zebra-164656-1021961.1003.4.3780621&id=562099309982&scm=1003.4.lb-zebra-164656-1021961.ITEM_562099309982_3780621&sku_properties=10004:709990523;5919063:6536025;12304035:3222911')

print(browser.page_source)
