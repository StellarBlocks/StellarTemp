# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 18:20:57 2020

@author: jindou
"""
import subprocess
from StellarLog.StellarLog import CLog

class CUrlList:
    
    def __init__(self,name,index,logInfo:dict):
        self.name = name
        self.index  = index
        self.info:dict = logInfo
        self._list:list = None
        
    def append(self,List:list):
        self._list.append(List)
        
    def replace(self,List:list):
        self._list = List

class CCrawlerManager:
    def __init__(self,name,workDirectory:str, oLog:CLog, oAgent):
        self.workDirectory = workDirectory
        self.jobsList = None
        self.oLog = oLog
        self.outputFolder = workDirectory
        self.name = name + '_crawler'
    
    def newProcess(self,crawlerName,oUrlList:CUrlList):
        outFilePath = 'file:///' + self.outputFolder + self.name + '.json'
#        print(outFilePath,urlsFilePath)
        process = subprocess.Popen(['scrapy','crawl',crawlerName,'-o',outFilePath,'-a','urlFile='+oUrlList],
                                   shell=True, 
                                   cwd=self.workDirectory)
        return process
    
    def engineStart(self):
        for oJob in self.jobsList:
            print(oJob.name)
            self.oLog.safeRecordTime(oJob.name+"start")
            temp = self.newProcess('pageWorker',oJob.name,oJob.fileName)
            temp.wait()
            self.oLog.safeRecordTime(oJob.name+"end")



        