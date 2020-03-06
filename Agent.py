# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 13:37:20 2020

@author: zijia
"""
from CrawlerManager import CCrawlerManager, CUrlList
from StorageManager import CStorage,CStorageMongoDB
from KnowledgeManager import CKnowledge
from StellarLog.StellarLog import CDirectoryConfig,CLog

class CAgent:
    
    def __init__(self,name, oDir:CDirectoryConfig):
        self.name = name
        self.crawlerManager:CCrawlerManager = None
        self.storageManager:CStorage = None
        self.knowledgeManager:CKnowledge = None
        self.oDir:CDirectoryConfig = oDir
        self.oLog = CLog(oDir['outputRoot'],self.name + '_log')
        
    def configStorage(self, path ,mode = 'mongoDB'):
        if(mode == 'mongoDB'):
            self.storageManager = CStorageMongoDB(self.name,path)
    
    def configCrawler(self):
        self.crawlerManager = CCrawlerManager(self.name,self.oDir['crawlerCWD'],self.oLog)
        
    def configKnowledge(self):
        self.knowledgeManager = CKnowledge(self.name, self.storageManager)
        
    
        
class CJrjHelper:
    
    def __init__(self):
        self.urlRoot = r'http://stock.jrj.com.cn/share/news/company/'
    
    def fetchUrlsForDate(self,year,month,day):
        import requests,json
        import numpy as np
        cnt = 0
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
        
        jobsList = list()
        
        for news in info:
#            print(news)
            logInfo = {"makeDate":news[0]['makedate'],"Date":date,"Index":cnt,"Total":numNews}
            preInfo = news[0]['stockname'].split(',')
            oUrlList = CUrlList(None,logInfo,preInfo)
            oUrlList.replace([news[0]['infourl']])
            jobsList.append(oUrlList)
            cnt+=1
            
        return jobsList
        
        