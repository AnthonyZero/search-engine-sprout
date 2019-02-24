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
import time

# 运行JS脚本 进行滚动下滑
browser = webdriver.Chrome(executable_path='F:/tmp/chromedriver.exe')
browser.get('https://www.oschina.net/blog')
time.sleep(5)
for i in range(5): # 向下滚动5次
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
    time.sleep(5)

# 微博登陆
# browser = webdriver.Chrome(executable_path='F:/tmp/chromedriver.exe')
# browser.get('https://weibo.com/')
# time.sleep(10)
# browser.find_element_by_css_selector('#loginname').send_keys('username')
# browser.find_element_by_css_selector('.info_list.password input[name="password"]').send_keys('password')
# browser.find_element_by_css_selector(".info_list.login_btn a[node-type='submitBtn']").click()

# 知乎登陆
# browser = webdriver.Chrome(executable_path='F:/tmp/chromedriver.exe')
# browser.get('https://www.zhihu.com/signup?next=%2F')
# print(browser.page_source)
# # 点击登陆tab
# browser.find_element_by_css_selector('.SignContainer-switch span').click()
# browser.find_element_by_css_selector(".SignFlow-accountInput input[name='username']").send_keys('username')
# browser.find_element_by_css_selector(".SignFlow-password input[name='password']").send_keys('password')
# browser.find_element_by_css_selector('.SignFlow-submitButton').click()

# 获取天猫商品促销价
# browser = webdriver.Chrome(executable_path='F:/tmp/chromedriver.exe')
# browser.get('https://detail.tmall.com/item.htm?spm=a230r.1.14.3.yYBVG6&id=538286972599&cm_id=140105335569ed55e27b&abbucket=15&sku_properties=10004:709990523;5919063:6536025')
# time.sleep(10) #get未加载完成 故sleep 10秒
# selector = Selector(text=browser.page_source)
# goods_value = selector.css('.tm-price-panel .tm-price::text').extract_first()
# print("该商品原价为:", goods_value)