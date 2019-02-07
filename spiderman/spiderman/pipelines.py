# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
import codecs
import json
from scrapy.exporters import JsonItemExporter

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