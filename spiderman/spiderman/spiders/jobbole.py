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

        post_urls = response.css("#archive .post-thumb a::attr(href)").extract()
        for post_url in post_urls:
            Request(url=post_url, callback=self.parse_content)

    def parse_content(self, response):
        # title = response.xpath('//div[@class="entry-header"]/h1/text()').extract()[0];
        # create_data = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract()[0].replace("·","").strip()
        # vote_num = response.xpath('//span[contains(@class,"vote-post-up")]/h10/text()').extract()[0]
        # collect_num = response.xpath('//span[contains(@class,"bookmark-btn")]/text()').extract()[0]
        # match_re = re.match(".*?(\d+).*", collect_num)
        # favour_num = 0
        # if match_re:
        #     favour_num = match_re.group(1)
        # comments_num = response.xpath('//a[@href="#article-comment"]/span/text()').extract()[0]
        # match_re = re.match(".*?(\d+).*", comments_num) #正则获取字符串中的数字
        # if match_re:
        #     comments_num = match_re.group(1)
        #
        # content = response.xpath('//div[@class="entry"]').extract()[0]
        # tag_selecter = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()
        # tag_list = [element for element in tag_selecter if not element.strip().endswith('评论')]
        # tags = ",".join(tag_list) #标签

        # 通常css选择器提取数据
        title = response.css('.entry-header h1::text').extract_first()
        create_data = response.css('p.entry-meta-hide-on-mobile::text').extract_first().replace("·","").strip()
        praise_num = response.css('.vote-post-up h10::text').extract_first() #点赞数
        fav_num = response.css('.bookmark-btn::text').extract_first() #收藏数
        match_re = re.match(".*?(\d+).*", fav_num)
        if match_re:
            fav_num = match_re.group(1)
        else:
            fav_num = 0
        comments_num = response.css('a[href="#article-comment"] span::text').extract_first() # 评论数
        match_re = re.match(".*?(\d+).*", comments_num)  # 正则获取字符串中的数字
        if match_re:
            comments_num = match_re.group(1)
        content = response.css('div.entry').extract_first() # 正文
        tag_selecter = response.css('p.entry-meta-hide-on-mobile a::text').extract()
        tag_list = [element for element in tag_selecter if not element.strip().endswith('评论')]
        tags = ",".join(tag_list)  # 标签
        pass
