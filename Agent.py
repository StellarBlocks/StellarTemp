# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 13:37:20 2020

@author: zijia
"""
from CrawlerManager import CCrawlerManager, CUrlList
from StorageManager import CStorage,CStorageMongoDB
from KnowledgeManager import CKnowledgeClient
from StellarLog.StellarLog import CDirectoryConfig,CLog
import signal
from diskcache import Cache
import json
import yaml
import time

class CConfigByYaml:
    
    def __init__(self,filePath):
        self.content = self._readYaml(filePath)
        
    def _readYaml(self,filePath):
        ans = None
        with open(filePath,'r') as stream:
            try:
                ans = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        return ans
    
    def __getitem__(self,attr):
        return self.content[attr]
    
    def getConfigValues(self,attrs=None):
        if(attrs == None):
            return self.content
        else:
            ans = dict()
            for attr in attrs:
                ans[attr] = self.content[attr]
            return ans

class CAgent:
    
    def __init__(self,name, oDir:CDirectoryConfig, oConfigByYaml:CConfigByYaml):
        self.name = name
        self.crawlerManager:CCrawlerManager = None
        self.storageManager:CStorage = None
        self.knowledgeManagerClient:CKnowledgeClient = None
        self.oDir:CDirectoryConfig = oDir
        self.oConf = oConfigByYaml
        self.oLog = CLog(oDir['Log'],self.name + '_log')
        self.dbWeb = ''
        self.cacheAgent = Cache(oDir['cacheAgentFolder'])
        self.cacheCrawler = Cache(oDir['cacheCrawlerFolder'])
        
        
    def _configStorage(self,mode = 'mongoDB'):
        oSubConfig = self.oConf['Storage']
        self.dbWeb = oSubConfig['dbWeb']
        if(oSubConfig.get('mode') != None):
            mode = oSubConfig['mode']
        path = self.dbWeb
        if(mode == 'mongoDB'):
            self.storageManager = CStorageMongoDB(self.name,path)
    
    def _configCrawler(self):
        self.crawlerManager = CCrawlerManager(self.name,self.oDir['crawlerCWD'],
                                              self.oLog,self.oDir['cacheCrawlerFolder'],
                                              self.oDir['cacheAgentFolder'])
        
    def _configKnowledgeManager(self):
        oSubConfig = self.oConf['KnowledgeManager']
        addressTuple = (oSubConfig['address'],oSubConfig['port'])
        key = oSubConfig['password']
        self.knowledgeManagerClient = CKnowledgeClient(addressTuple,key,self.oLog)
    
    def configAll(self):
        self._configCrawler()
        self.oLog.safeRecordTime('CrawlerManager conf finished')
        self._configKnowledgeManager()
        self.oLog.safeRecordTime('KnowledgeManager conf finished')
        self._configStorage()
        self.oLog.safeRecordTime('StorageManager conf finished')
    
    def startCrawling(self,jobsList:list):
        return self.crawlerManager.engineStart(jobsList)
    
    def fetchResult(self,handler,subProcHandle,timeWaitStep = 1,maxWaitTimes=5): #total continuous waittime will be (timeWaitStep * maxWaitTimes)
        result = ''
        cnt = 0
        while(True):
            _,result = self.cacheAgent.pull()
            if(result != None):
                result = json.loads(result)
                ans = handler(result['type'],result['content'])
#                print(ans)
                for temp in ans:
                    self.storageManager.storeData(temp[0],temp[1],temp[2])
#                break
                cnt = 0 #clear counter
            elif(timeWaitStep * maxWaitTimes > 0):
                if(cnt >= maxWaitTimes):# if continuous wait time equals to maxWaitTimes
                    return False
                elif subProcHandle.poll() != None: #if the subprocess is finished
                    return subProcHandle.poll()
                else:
                    time.sleep(timeWaitStep)
                    cnt+=1 #counter add one
            else:
                raise ValueError("timeWaitStep * maxWaitTimes should be bigger than 0")
    
    def clearCache(self):
        self.cacheAgent.clear()
        self.cacheCrawler.clear()
        
    def closeCache(self):
        self.cacheAgent.close()
        self.cacheCrawler.close()
        self.crawlerManager.closeCache()
        
    def close(self):
        self.closeCache()
        
        
class CJrjHelper:
    
    def __init__(self):
        self.urlRoot = r'http://stock.jrj.com.cn/share/news/company/'
    
    def fetchUrlsForDate(self,year,month,day):
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
            
        logInfo = {"Date":date,"Total":numNews}
        oUrlList = CUrlList(None,logInfo)
        for news in info:
#            print(news)
            url = news[0]['infourl']
            preInfo = news[0]['stockname'].split(',')
            oUrlList.append(url,preInfo)
                    
        return oUrlList
        
        