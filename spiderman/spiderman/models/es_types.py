#!/usr/bin/env python
# encoding: utf-8
'''
@author: AnthonyZero
@file: es_types.py
@time: 2019/5/9 22:36
@desc: elasticsearch_dsl 版本要跟本地版本要融合
这里elasticsearch_dsl 是5.2.0  这里elasticsearch 是5.5.3 本机安装的es程序是5.1.1

elasticsearch_dsl版本要求

# Elasticsearch 7.x
elasticsearch-dsl>=7.0.0,<8.0.0

# Elasticsearch 6.x
elasticsearch-dsl>=6.0.0,<7.0.0

# Elasticsearch 5.x
elasticsearch-dsl>=5.0.0,<6.0.0
'''

from datetime import datetime
from elasticsearch_dsl import DocType, Date, Nested, Boolean, \
    analyzer, InnerObjectWrapper, Completion, Keyword, Text, Integer

from elasticsearch_dsl.connections import connections
connections.create_connection(hosts=["localhost"]) # 连接本机

class ArticleType(DocType):
    # 伯乐在线文章类型

    title = Text(analyzer="ik_max_word")
    create_date = Date()
    url = Keyword()
    url_object_id = Keyword()
    front_image_url = Keyword()
    front_image_path = Keyword()
    praise_nums = Integer()
    comment_nums = Integer()
    fav_nums = Integer()
    tags = Text(analyzer="ik_max_word")
    content = Text(analyzer="ik_max_word")

    # 定义es中index(数据库) type(表)
    class Meta:
        index = "jobbole"
        doc_type = "article"

if __name__ == '__main__':
    ArticleType.init() # 直接生成es mapping