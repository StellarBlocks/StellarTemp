# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 18:20:57 2020

@author: jindou
"""
import subprocess
from StellarLog.StellarLog import CLog
from diskcache import Cache

class CUrlList:
    
    def __init__(self,index,logInfo:dict):
        self.index  = index
        self.logInfo:dict = logInfo
        self.preInfoList:list = list()
        self._list:list = list()
        
    def append(self,url:str,preInfo:list):
        self._list.append(url)
        self.preInfoList.append(preInfo)
        
    def replace(self,List:list,preInfoList:list):
        if(type(preInfoList[0])!=list):
            raise ValueError('preInfoList must be list of list')
        self._list = List
        self.preInfoList = preInfoList
        
    def clear(self):
        self._list.clear()
        self.preInfoList.clear()
        
    def exportJson(self):
        import json
        jsonDict = {'index':self.index,
                    'logInfo':self.logInfo,
                    'preInfo':self.preInfoList,
                    'urlList':self._list}
        jsonStr = json.dumps(jsonDict)
        return jsonStr
    
    def __getitem__(self,idx):
        tempDict = self.logInfo.copy()
        tempDict['type'] = 'subList'
        oUrlList = CUrlList(self.index,tempDict)
        oUrlList._list = self._list[idx]
        oUrlList.preInfoList = self.preInfoList[idx]
        return oUrlList
    
    def __len__(self):
        return len(self._list)
        

class CCrawlerManager:
    def __init__(self,name,workDirectory:str, oLog:CLog,cachePath:str, cacheAgentPath:str):
        self.workDirectory = workDirectory
        self.jobsList = None
        self.oLog = oLog
        self.outputFolder = workDirectory
        self.name = name + '_crawler'
        self.jobCnt = 0
        self._cachePathCrawler = cachePath
        self._cachePathAgent = cacheAgentPath
        self.cache = Cache(cachePath)
    
    def _newProcess(self,crawlerName,oUrlCacheKey:str):
        outFilePath = 'file:///' + self.outputFolder + self.name + '.json'
#        print(outFilePath,urlsFilePath)
#        process = subprocess.Popen(['scrapy','crawl',crawlerName,'-o',outFilePath,'-a',
#                                    'cacheCrawlerPath='+ self._cachePathCrawler,'-a',
#                                    'cacheKey='+oUrlCacheKey,'-a',
#                                    'cacheAgentPath=' + self._cachePathAgent],
#                                   shell=True, 
#                                   cwd=self.workDirectory)
#        print('scrapy','crawl',crawlerName,'-o',outFilePath,'-a',
#                                    'cacheCrawlerPath='+ self._cachePathCrawler,'-a',
#                                    'cacheKey='+oUrlCacheKey,'-a',
#                                    'cacheAgentPath=' + self._cachePathAgent)
        process = subprocess.Popen(['scrapy','crawl',crawlerName,'-a',
                                    'cacheCrawlerPath='+ self._cachePathCrawler,'-a',
                                    'cacheKey='+oUrlCacheKey,'-a',
                                    'cacheAgentPath=' + self._cachePathAgent],
                                   shell=True, 
                                   cwd=self.workDirectory)
        print('scrapy','crawl',crawlerName,'-a',
                                    'cacheCrawlerPath='+ self._cachePathCrawler,'-a',
                                    'cacheKey='+oUrlCacheKey,'-a',
                                    'cacheAgentPath=' + self._cachePathAgent)
        
        return process
    
    def engineStart(self,jobsList:list):
        for oUrlList in jobsList:
            oUrlList.index = self.jobCnt
            tempKey = self._prepareJob(oUrlList.exportJson())
            self.oLog.safeRecordTime(str(oUrlList.index)+"start")
            temp = self._newProcess('general',tempKey)
#            temp.wait()
            self.oLog.safeRecordTime(str(oUrlList.index)+"end")
            return temp
    
    def _prepareJob(self,content:str):
#        key = str(self.jobCnt)
#        if(self.cache.get(key)==False):
#            raise ValueError("this key exists in the cache")
#            return None
#        else:
#            self.cache[key] = content
#            self.jobCnt+=1
#            return key
        self.jobCnt+=1
#        print(self.cache.directory)
        key = self.cache.push(content)
        return str(key)
    
    def closeCache(self):
        self.cache.close()

class CContentExtract():
    
    def __init__(self,mode='boilerpipe'):
        if(mode=='boilerpipe'):
            self.Module = self._importBoilerpipe3Extractor()
        else:
            raise ValueError("doesn't have this kind of mode")
    
    def boilerpipe(self,htmlText):
        
        extractor = self.Module(extractor='ArticleExtractor', html=htmlText)
        title = extractor.getTitle()
        content = extractor.getText()
        return title,content
    
    def _importBoilerpipe3Extractor(self):
        from boilerpipe.extract import Extractor
        return Extractor
        
    



        