# -*- coding: utf-8 -*-
import scrapy
import re

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/114536/']

    def parse(self, response):
        title = response.xpath('//div[@class="entry-header"]/h1/text()').extract()[0];
        create_data = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract()[0].replace("·","").strip()
        vote_num = response.xpath('//span[contains(@class,"vote-post-up")]/h10/text()').extract()[0]
        collect_num = response.xpath('//span[contains(@class,"bookmark-btn")]/text()').extract()[0]
        match_re = re.match(".*(\d+).*", collect_num)
        favour_num = 0
        if match_re:
            favour_num = match_re.group(1)
        comments_num = response.xpath('//a[@href="#article-comment"]/span/text()').extract()[0]
        match_re = re.match(".*(\d+).*", comments_num) #正则获取字符串中的数字
        if match_re:
            comments_num = match_re.group(1)

        pass
