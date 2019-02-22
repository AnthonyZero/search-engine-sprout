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
from scrapy.selector import Selector

# 获取天猫商品促销价
browser = webdriver.Chrome(executable_path='F:/tmp/chromedriver.exe')
browser.get('https://detail.tmall.com/item.htm?spm=a230r.1.14.3.yYBVG6&id=538286972599&cm_id=140105335569ed55e27b&abbucket=15&sku_properties=10004:709990523;5919063:6536025')
print(browser.page_source)
# selector = Selector(text=browser.page_source)
# goods_value = selector.css('.tm-price-panel .tm-price::text').extract_first()
# print("该商品原价为:", goods_value)