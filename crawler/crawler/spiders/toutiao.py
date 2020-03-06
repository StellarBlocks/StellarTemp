# -*- coding: utf-8 -*-
import scrapy


class ToutiaoSpider(scrapy.Spider):
    name = 'toutiao'
    allowed_domains = ['']
    start_urls = ['http:///']

    def parse(self, response):
        pass
