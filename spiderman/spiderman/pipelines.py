# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
import codecs
import json
from scrapy.exporters import JsonItemExporter
import MySQLdb
import MySQLdb.cursors

class SpidermanPipeline(object):
    def process_item(self, item, spider):
        return item

# 自定义json文件的导出
class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open('article.json','w', encoding='utf-8')
    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)  # item写入json 文件
        return item
    def spider_closed(self, spider):
        self.file.close()

# 利用scrapy提供的json exporter
class JsonExporterPipeline(object):
    def __init__(self):
        self.file = open('articleexport.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

# 利用scrapy.pipelines.images.ImagesPipeline 下载图片之后 获取返回的相对路径
class ArticleImagePipeline(ImagesPipeline):

    def item_completed(self, results, item, info):
        for ok, value in results:
            image_url_path = value['path']
        item['front_image_path'] = image_url_path
        return item

# mysql 同步方式 保存数据到db
class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('url', 'root', 'password',
                    'search-engine-sprout', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        sql = """
            insert into jobbole_article(title,create_date,url,url_object_id,front_image_url,
            front_image_path,praise_nums,comment_nums,fav_nums,tags,content)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        self.cursor.execute(sql, (item['title'], item['create_date'], item['url'], item['url_object_id'], item['front_image_url'], item['front_image_path']
            , item['praise_nums'], item['comment_nums'], item['fav_nums'], item['tags'], item['content']))
        self.conn.commit()
