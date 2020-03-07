# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class CrawlerPipeline(object):
    def process_item(self, item, spider):
        return item


class diskCachePipeline(object):

    collection_name = 'scrapy_items'

    def __init__(self):
        pass


    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        spider.cache.close()
        spider.cacheAgent.close()
        
    def process_item(self, item, spider):
        return item