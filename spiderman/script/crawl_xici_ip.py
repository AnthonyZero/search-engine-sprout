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

class GetIP(object):
    def delete_ip(self, ip):
        # 删除数据库中无效的ip
        delete_sql = """
                   delete from proxy_ip where ip='{0}'
               """.format(ip)
        cursor.execute(delete_sql)
        conn.commit()
        return True

    def judge_ip(self, ip, port):
        # 判断ip是否有效 https://icanhazip.com/
        http_url = "http://icanhazip.com/"
        proxy_url = "http://{0}:{1}".format(ip, port)
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"}
        try:
            proxy_dict = {
                "http": proxy_url,
            }
            response = requests.get(http_url, headers=headers, proxies=proxy_dict, timeout=10)
        except Exception as e:
            print("invalid ip and port")
            self.delete_ip(ip)
            return False
        else:
            code = response.status_code # 根据状态码判断是否有效
            if code >= 200 and code < 300:
                print("effective ip")
                return True
            else:
                print("invalid ip and port")
                self.delete_ip(ip)
                return False

    def get_random_ip(self):
        # 从数据库中随机获取一个可用的ip
        random_sql = """
             SELECT ip,port,proxy_type FROM proxy_ip ORDER BY RAND() LIMIT 1
        """
        result = cursor.execute(random_sql)
        for ip_info in cursor.fetchall():
            ip = ip_info[0]
            port = ip_info[1]
            judge_result = self.judge_ip(ip, port)
            if judge_result:
                return "http://{0}:{1}".format(ip, port)
            else:
                return self.get_random_ip()

if __name__ == '__main__':
    getip = GetIP()
    getip.get_random_ip()