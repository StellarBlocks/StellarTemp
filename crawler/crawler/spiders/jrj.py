# -*- coding: utf-8 -*-
import scrapy


class JrjSpider(scrapy.Spider):
    name = 'jrj'
    allowed_domains = ['stock.jrj.com.cn']
    start_urls = ['http://http://stock.jrj.com.cn//']

    def parse(self, response):
        pass
