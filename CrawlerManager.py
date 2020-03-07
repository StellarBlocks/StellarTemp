# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 18:20:57 2020

@author: jindou
"""
import subprocess
from StellarLog.StellarLog import CLog
from diskcache import Cache

class CUrlList:
    
    def __init__(self,index,logInfo:dict,preInfo:list):
        self.index  = index
        self.logInfo:dict = logInfo
        self.preInfo:list = preInfo
        self._list:list = None
        
    def append(self,List:list):
        self._list.append(List)
        
    def replace(self,List:list):
        self._list = List
        
    def exportJson(self):
        import json
        jsonDict = {'index':self.index,
                    'logInfo':self.logInfo,
                    'preInfo':self.preInfo,
                    'urlList':self._list}
        jsonStr = json.dumps(jsonDict)
        return jsonStr

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
        process = subprocess.Popen(['scrapy','crawl',crawlerName,'-o',outFilePath,'-a',
                                    'cacheCrawlerPath='+ self._cachePathCrawler,'-a',
                                    'cacheKey='+oUrlCacheKey,'-a',
                                    'cacheAgentPath=' + self._cachePathAgent],
                                   shell=True, 
                                   cwd=self.workDirectory)
        return process
    
    def engineStart(self,jobsList:list):
        for oUrlList in jobsList:
            print(oUrlList.preInfo)
            oUrlList.index = self.jobCnt
            tempKey = self._prepareJob(oUrlList.exportJson())
            self.oLog.safeRecordTime(str(oUrlList.index)+"start")
            temp = self._newProcess('jrj',tempKey)
            temp.wait()
            self.oLog.safeRecordTime(str(oUrlList.index)+"end")
    
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
        key = self.cache.push(content)
        return str(key)
    
    def closeCache(self):
        self.cache.close()
            
        
    



        