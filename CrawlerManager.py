# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 18:20:57 2020

@author: jindou
"""
import subprocess
from StellarLog.StellarLog import CLog

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
        
    def exportJson(self,folder):
        import json
        jsonDict = {'index':self.index,
                    'logInfo':self.logInfo,
                    'preInfo':self.preInfo,
                    'urlList':self._list}
        jsonStr = json.dumps(jsonDict)
        return jsonStr

class CCrawlerManager:
    def __init__(self,name,workDirectory:str, oLog:CLog, oAgent):
        self.workDirectory = workDirectory
        self.jobsList = None
        self.oLog = oLog
        self.outputFolder = workDirectory
        self.name = name + '_crawler'
    
    def newProcess(self,crawlerName,oUrlFile:str):
        outFilePath = 'file:///' + self.outputFolder + self.name + '.json'
#        print(outFilePath,urlsFilePath)
        process = subprocess.Popen(['scrapy','crawl',crawlerName,'-o',outFilePath,'-a','urlFile=',oUrlFile],
                                   shell=True, 
                                   cwd=self.workDirectory)
        return process
    
    def engineStart(self,jobsList):
        for oUrlList in jobsList:
            print(oUrlList.name)
            self.oLog.safeRecordTime(oUrlList.name+"start")
            temp = self.newProcess('pageWorker',oUrlList)
            temp.wait()
            self.oLog.safeRecordTime(oUrlList.name+"end")
            
    



        