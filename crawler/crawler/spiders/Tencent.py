# -*- coding: utf-8 -*-
import scrapy


class TencentSpider(scrapy.Spider):
    name = 'Tencent'
    allowed_domains = ['news.qq.com']
    start_urls = ['http://news.qq.com/']

    def parse(self, response):
        pass
