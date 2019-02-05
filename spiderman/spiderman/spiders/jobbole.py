# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):

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
        # 通常css选择器提取数据
        front_image_url = response.meta.get("front_image_url", "") #文章封面图
        title = response.css('.entry-header h1::text').extract_first()
        create_data = response.css('p.entry-meta-hide-on-mobile::text').extract_first().replace("·","").strip()
        praise_num = response.css('.vote-post-up h10::text').extract_first() #点赞数
        fav_num = response.css('.bookmark-btn::text').extract_first() #收藏数
        match_re = re.match(".*?(\d+).*", fav_num)
        if match_re:
            fav_num = int(match_re.group(1))
        else:
            fav_num = 0
        comments_num = response.css('a[href="#article-comment"] span::text').extract_first() # 评论数
        match_re = re.match(".*?(\d+).*", comments_num)  # 正则获取字符串中的数字
        if match_re:
            comments_num = int(match_re.group(1))
        else:
            comments_num = 0
        content = response.css('div.entry').extract_first() # 正文
        tag_selecter = response.css('p.entry-meta-hide-on-mobile a::text').extract()
        tag_list = [element for element in tag_selecter if not element.strip().endswith('评论')]
        tags = ",".join(tag_list)  # 标签
        pass
