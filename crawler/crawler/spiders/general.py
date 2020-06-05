# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import scrapy
import json
from StellarLog.StellarLog import CDirectoryConfig
from diskcache import Cache
from ..items import CrawlerItem
from CrawlerManager import CContentExtract

class GeneralSpider(scrapy.Spider):
    name = 'general'
    allowed_domains = []
    start_urls = ['http://finance.jrj.com.cn/2020/04/24012529362098.shtml']
    

    def __init__(self,cacheCrawlerPath='',cacheKey='', cacheAgentPath='', *args,**kwargs):
        super().__init__(*args, **kwargs)
        self.cacheKey = cacheKey
        self.cacheCrawlerPath = cacheCrawlerPath
        print('aa',cacheCrawlerPath,'bb',cacheAgentPath,cacheKey)
        self.cache = Cache(cacheCrawlerPath)
        self.cacheAgent = Cache(cacheAgentPath)
        self.oContentExtract = CContentExtract('boilerpipe')
#        jsonStr = self.cache[int(cacheKey)]
        _,jsonStr = self.cache.pull()
        print('cc',jsonStr)
        if(jsonStr == None):
            oUrlList = ['http://finance.jrj.com.cn/2020/04/24012529362098.shtml']
            self.start_urls = oUrlList
        else:
            oUrlList = json.loads(jsonStr)
            self.start_urls = oUrlList['urlList']
            self.logInfo = oUrlList['logInfo']
            self.preInfoList:list = oUrlList['preInfo']
            self.preInfoUrlDict = None
            if(len(self.preInfoList) == len(self.start_urls)):
                self.preInfoUrlDict = dict()
                for idx,url in enumerate(self.start_urls):
                    self.preInfoUrlDict[url] = self.preInfoList[idx]
            
            logInfo = {'type':'logInfo','content':{'data':self.logInfo}}
            logInfoStr = json.dumps(logInfo)
            self.cacheAgent.push(logInfoStr)
            
        
    def parse(self, response):
        temp0 = './/div[@class="titmain"]//h1//text()'
        temp = './/div[@class="texttit_m1"]//p//text()'
#        print(response)
        item = CrawlerItem()
        item['link'] = response.url
        html = response.text
#        print(html)
#        ans0 = response.xpath(temp0).getall()
#        ans1 = response.xpath(temp).getall()
        ans0,ans1 = self.oContentExtract.boilerpipe(html)
        item['title'] = ans0
        item['content'] = ans1
        print(ans0,ans1)
        preInfo = None
        if(self.preInfoUrlDict != None):
            preInfo = self.preInfoUrlDict[item['link']]
        elif(len(self.preInfoList) == 1):
            preInfo = self.preInfoList[0]
        ansFinal = {'type':'crawlerResult','content':
            {'data':{'link':item['link'],'title':ans0,'content':ans1},'preInfo':preInfo}}
        ansJson = json.dumps(ansFinal)
        self.cacheAgent.push(ansJson)
#        self.cache.close()
#        self.cacheAgent.close()
        yield item
        
        