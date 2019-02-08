# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose,Join,TakeFirst
from datetime import datetime
import re
from scrapy.loader import ItemLoader


class SpidermanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

# 日期转换
def date_convert(value):
    value = value.replace("·", "").strip()  # 去掉· 左右空格
    try:
        create_date = datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_date = datetime.now().date()
    return create_date

# 正则提取字符串中的数字
def get_nums(value):
    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums

#去掉标签中提取的 有评论的字段
def remove_comment_tags(value):
    if "评论" in value:
        return ""
    else:
        return value

def return_value(value):
    return value

#自定义itemloader
class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst() # 类似extract_first的方法

class JobboleArticleItem(scrapy.Item):
    title = scrapy.Field()
    create_date = scrapy.Field(
        input_processor = MapCompose(date_convert) # MapCompose 依次对list的元素进行处理
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field(
        output_processor=MapCompose(return_value)
    )
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    comment_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    fav_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    tags = scrapy.Field(
        input_processor=MapCompose(remove_comment_tags), # 输入/输出处理器
        output_processor=Join(",")
    )
    content = scrapy.Field()

    def get_insert_sql(self):
        sql = """
            insert into jobbole_article(title,create_date,url,url_object_id,front_image_url,
            front_image_path,praise_nums,comment_nums,fav_nums,tags,content)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE content=VALUES(content)
        """
        params = (self['title'], self['create_date'], self['url'], self['url_object_id'], self['front_image_url'],
              self['front_image_path'], self['praise_nums'], self['comment_nums'], self['fav_nums'], self['tags'], self['content'])
        return sql, params


class LagouJobItemLoader(ItemLoader):
    #自定义itemloader
    default_output_processor = TakeFirst()

class LagouJobItem(scrapy.Item):
    #拉勾网职位信息
    title = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    salary = scrapy.Field()
    job_city = scrapy.Field(

    )
    work_years = scrapy.Field(

    )
    degree_need = scrapy.Field(

    )
    job_type = scrapy.Field()
    publish_time = scrapy.Field()
    job_advantage = scrapy.Field()
    job_desc = scrapy.Field()
    job_addr = scrapy.Field(

    )
    company_name = scrapy.Field()
    company_url = scrapy.Field()
    tags = scrapy.Field(

    )
    crawl_time = scrapy.Field()