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
        print('cc',jsonStr)
        oUrlList = json.loads(jsonStr)
        
        self.start_urls = oUrlList['urlList']
        self.logInfo = oUrlList['logInfo']
        self.preInfoList:list = oUrlList['preInfo']
        self.preInfoUrlDict = None
        if(len(self.preInfoList) == len(self.start_urls)):
            self.preInfoUrlDict = dict()
            for idx,url in enumerate(self.start_urls):
                self.preInfoUrlDict[url] = self.preInfoList[idx]
        
        logInfo = {'type':'logInfo','content':self.logInfo}
        logInfoStr = json.dumps(logInfo)
        self.cacheAgent.push(logInfoStr)
            
        
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
        preInfo = None
        if(self.preInfoUrlDict != None):
            preInfo = self.preInfoUrlDict[item['link']]
        elif(len(self.preInfoList) == 1):
            preInfo = self.preInfoList[0]
        ansFinal = {'type':'crawlerResult','content':
            {'link':item['link'],'title':ans0,'content':ans1,'preInfo':preInfo}}
        ansJson = json.dumps(ansFinal)
        self.cacheAgent.push(ansJson)
#        self.cache.close()
#        self.cacheAgent.close()
        yield item
        
        