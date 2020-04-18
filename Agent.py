# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 13:37:20 2020

@author: zijia
"""
from CrawlerManager import CCrawlerManager, CUrlList
from StorageManager import CStorage,CStorageMongoDB
from KnowledgeManager import CKnowledge
from StellarLog.StellarLog import CDirectoryConfig,CLog
from diskcache import Cache
import json

class CAgent:
    
    def __init__(self,name, oDir:CDirectoryConfig):
        self.name = name
        self.crawlerManager:CCrawlerManager = None
        self.storageManager:CStorage = None
        self.knowledgeManager:CKnowledge = None
        self.oDir:CDirectoryConfig = oDir
        self.oLog = CLog(oDir['outputRoot'],self.name + '_log')
        self.dbWeb = ''
        self.cacheAgent = Cache(oDir['cacheAgentFolder'])
        self.cacheCrawler = Cache(oDir['cacheCrawlerFolder'])
        
        
    def _configStorage(self, mode = 'mongoDB'):
        path = self.dbWeb
        if(mode == 'mongoDB'):
            self.storageManager = CStorageMongoDB(self.name,path)
    
    def _configCrawler(self):
        self.crawlerManager = CCrawlerManager(self.name,self.oDir['crawlerCWD'],
                                              self.oLog,self.oDir['cacheCrawlerFolder'],
                                              self.oDir['cacheAgentFolder'])
        
    def _configKnowledge(self):
#        self.knowledgeManager = CKnowledge(self.name, self.storageManager.path)
        pass
    
    def configAll(self):
        self._configCrawler()
        self._configKnowledge()
        self._configStorage()
    
    def startCrawling(self,jobsList:list):
        self.crawlerManager.engineStart(jobsList)
    
    def fetchResult(self):
        result = ''
        while(result!=None):
            _,result = self.cacheAgent.pull()
            if(result != None):
                result = json.loads(result)
                print(result)
    
    def clearCache(self):
        self.cacheAgent.clear()
        self.cacheCrawler.clear()
        
    def closeCache(self):
        self.cacheAgent.close()
        self.cacheCrawler.close()
        self.crawlerManager.closeCache()
        
class CJrjHelper:
    
    def __init__(self):
        self.urlRoot = r'http://stock.jrj.com.cn/share/news/company/'
    
    def fetchUrlsForDate(self,year,month,day,jobList = None):
        import requests,json
        import numpy as np
        date = str(year) + '-' + str(month).zfill(2) + '-' + str(day).zfill(2)
        randomSeq_len = len('311941729')
        str_list = [str(i) for i in np.random.randint(10,size=randomSeq_len)]
        
        randomSeq = '1583' + ''.join(str_list)
        
        r = requests.get(self.urlRoot + str(year) + '-' + str(month).zfill(2) + '-' + str(day).zfill(2)
                            + r'.js?_=' + randomSeq)
#        print(randomSeq)
        
        strJson = json.loads(r.content[15:-5])
        
        info = strJson['newsinfo']
        numNews = len(info)
        
        if(jobList == None):
            jobsList = list()
            
        logInfo = {"Date":date,"Total":numNews}
        oUrlList = CUrlList(None,logInfo)
        for news in info:
#            print(news)
            url = news[0]['infourl']
            preInfo = news[0]['stockname'].split(',')
            oUrlList.append(url,preInfo)

        jobsList.append(oUrlList)
                    
        return jobsList
        
        