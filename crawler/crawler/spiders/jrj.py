# -*- coding: utf-8 -*-
import scrapy
import json
from StellarLog.StellarLog import CDirectoryConfig
from diskcache import Cache
from ..items import CrawlerItem

class JrjSpider(scrapy.Spider):
    name = 'jrj'
    allowed_domains = ['stock.jrj.com.cn']
    start_urls = ['http://http://stock.jrj.com.cn//']
    

    def __init__(self,cacheCrawlerPath='',cacheKey='', cacheAgentPath='', *args,**kwargs):
        super().__init__(*args, **kwargs)
        self.cacheKey = cacheKey
        self.cacheCrawlerPath = cacheCrawlerPath
        print('aa',cacheCrawlerPath,'bb',cacheAgentPath,cacheKey)
        self.cache = Cache(cacheCrawlerPath)
        self.cacheAgent = Cache(cacheAgentPath)
#        jsonStr = self.cache[int(cacheKey)]
        _,jsonStr = self.cache.pull()
        print(jsonStr)
        oUrlList = json.loads(jsonStr)
        
        self.start_urls = oUrlList['urlList']
        
    def parse(self, response):
        temp0 = './/div[@class="titmain"]//h1//text()'
        temp = './/div[@class="texttit_m1"]//p//text()'
#        print(response)
        item = CrawlerItem()
        item['link'] = response.url
        ans0 = response.xpath(temp0).getall()
        ans1 = response.xpath(temp).getall()
        item['title'] = ans0
        item['content'] = ans1
        ansFinal = {'link':item['link'],'title':ans0,'content':ans1}
        ansJson = json.dumps(ansFinal)
        self.cacheAgent.push(ansJson)
        self.cache.close()
        self.cacheAgent.close()
        yield item
        
        