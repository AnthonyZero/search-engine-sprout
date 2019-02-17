#!/usr/bin/env python
# encoding: utf-8
'''
@author: AnthonyZero
@file: crawl_xici_ip.py
@time: 2019/2/17 21:03
@desc:
'''

import requests
from scrapy.selector import Selector
import MySQLdb

conn = MySQLdb.connect(host="host", user="root", passwd="password", db="search-engine-sprout", charset="utf8")
cursor = conn.cursor()

def crawl_ips():
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"}

    for i in range(3595): # 最大页码为3595
        response = requests.get("https://www.xicidaili.com/nn/{0}".format(i), headers = headers)
        selector = Selector(text=response.text)

        all_trs = selector.css("#ip_list tr") # 获取所有tr
        for tr in all_trs[1:]:
            speed_str = tr.css(".bar::attr(title)").extract_first()
            if speed_str:
                speed = float(speed_str.split("秒")[0])  # 获取代理速度

            all_texts = tr.css("td::text").extract()
            ip = all_texts[0]
            port = all_texts[1]
            proxy_type = all_texts[5]

            if "HTTP" not in proxy_type:
                proxy_type = "HTTP"

            # 插入数据库
            sql = """
                insert into proxy_ip(ip, port, speed, proxy_type)
                VALUES (%s, %s, %s, %s)  ON DUPLICATE KEY UPDATE speed=VALUES(speed)
            """
            params = (ip, port, speed, proxy_type)
            print(params)
            cursor.execute(sql, params)
            conn.commit()

if __name__ == '__main__':
    crawl_ips()