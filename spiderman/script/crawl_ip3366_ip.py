#!/usr/bin/env python
# encoding: utf-8
'''
@author: AnthonyZero
@file: crawl_ip3366_ip.py
@time: 2019/2/18 21:01
@desc: 爬取云代理 免费高匿代理
'''

import requests
from scrapy.selector import Selector
import MySQLdb
from utils.config import ConfigUtils

co = ConfigUtils() # 读取配置文件属性
host = co.get_value('mysql-database','host')
user = co.get_value('mysql-database','user')
passwd = co.get_value('mysql-database','password')
db = co.get_value('mysql-database','db')
charset = co.get_value('mysql-database','charset')
conn = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db, charset=charset)
cursor = conn.cursor()

def crawl_ips():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"
    }

    for i in range(1, 7):
        response = requests.get('http://www.ip3366.net/free/?stype=1&page={0}'.format(i), headers = headers)
        response.encoding = 'gb2312'
        selector = Selector(text=response.text)
        all_trs = selector.css('#list tbody tr')
        for tr in all_trs:
            all_text = tr.css("td::text").extract()
            ip = all_text[0]
            port = all_text[1]
            proxy_type = all_text[3]
            speed_str = all_text[5]
            if speed_str:
                speed = float(speed_str.split("秒")[0])

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