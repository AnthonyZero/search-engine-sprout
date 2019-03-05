# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse
from items import JobboleArticleItem,ArticleItemLoader
from utils.common import get_md5
from datetime import datetime
from scrapy.loader import ItemLoader
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    # def __init__(self):
    #     self.browser = webdriver.Chrome(executable_path="F:/tmp/chromedriver.exe")
    #     super(JobboleSpider,self).__init__()
    #     dispatcher.connect(self.handle_spider_closed, signals.spider_closed) #spider退出时候候的信号
    #
    # # 当爬虫结束的时候 关闭chrome
    # def handle_spider_closed(self):
    #     print("spider closed")
    #     self.browser.quit()

    # 收集伯乐在线所有404的url以及404页面数
    handle_httpstatus_list = [404]
    def __init__(self):
        self.fail_urls = []
        dispatcher.connect(self.handle_spider_closed, signals.spider_closed)  #信号

    def handle_spider_closed(self, spider, reason):
        self.crawler.stats.set_value("failed_urls", ",".join(self.fail_urls))

    def parse(self, response):

        if response.status == 404:
            self.fail_urls.append(response.url)
            self.crawler.stats.inc_value("fail_url_total") # stats收集器

        post_nodes = response.css("#archive .post-thumb a")
        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url}, callback=self.parse_content)

        # 获取下一页
        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_url:
            yield Request(url=next_url, callback=self.parse)

    def parse_content(self, response):
        # 通过css选择器提取数据
        # front_image_url = response.meta.get("front_image_url", "") #文章封面图
        # title = response.css('.entry-header h1::text').extract_first()
        # create_date = response.css('p.entry-meta-hide-on-mobile::text').extract_first().replace("·","").strip()
        # praise_num = response.css('.vote-post-up h10::text').extract_first() #点赞数
        # fav_num = response.css('.bookmark-btn::text').extract_first() #收藏数
        # match_re = re.match(".*?(\d+).*", fav_num)
        # if match_re:
        #     fav_num = int(match_re.group(1))
        # else:
        #     fav_num = 0
        # comments_num = response.css('a[href="#article-comment"] span::text').extract_first() # 评论数
        # match_re = re.match(".*?(\d+).*", comments_num)  # 正则获取字符串中的数字
        # if match_re:
        #     comments_num = int(match_re.group(1))
        # else:
        #     comments_num = 0
        # content = response.css('div.entry').extract_first() # 正文
        # tag_selecter = response.css('p.entry-meta-hide-on-mobile a::text').extract()
        # tag_list = [element for element in tag_selecter if not element.strip().endswith('评论')]
        # tags = ",".join(tag_list)  # 标签
        #
        # article_item = JobboleArticleItem()
        # article_item["title"] = title
        # try:
        #     create_date = datetime.strptime(create_date, '%Y/%m/%d').date()
        # except Exception as e:
        #     create_date = datetime.now().date()
        # article_item["create_date"] = create_date
        # article_item["url"] = response.url
        # article_item["url_object_id"] = get_md5(response.url)
        # article_item["front_image_url"] = [front_image_url]
        # article_item["praise_nums"] = praise_num
        # article_item["comment_nums"] = comments_num
        # article_item["fav_nums"] = fav_num
        # article_item["tags"] = tags
        # article_item["content"] = content

        # 通过item loader加载item  使用自定义的loader：ArticleItemLoader 由list变成str
        front_image_url = response.meta.get("front_image_url", "")  # 文章封面图
        item_loader = ArticleItemLoader(item=JobboleArticleItem(), response = response)
        item_loader.add_css("title", ".entry-header h1::text")
        item_loader.add_css("create_date","p.entry-meta-hide-on-mobile::text")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_value("front_image_url", [front_image_url])
        item_loader.add_css("praise_nums", ".vote-post-up h10::text")
        item_loader.add_css("comment_nums", "a[href='#article-comment'] span::text")
        item_loader.add_css("fav_nums", ".bookmark-btn::text")
        item_loader.add_css("tags", "p.entry-meta-hide-on-mobile a::text")
        item_loader.add_css("content", "div.entry")

        article_item = item_loader.load_item()

        yield article_item

