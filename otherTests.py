# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 21:01:01 2020

@author: jido
"""


from StellarLog.StellarLog import CLog, CDirectoryConfig
from MiddleWare import resultHandler

#oLog = CLog('./','testLog')
#oLog.safeRecord('aaahhh')
dir_list = ['root','rootCode','sourceListFile','outputRoot','crawlerCWD','jobUrlsFolder',
            'cacheCrawlerFolder','cacheAgentFolder','Log']
oDir = CDirectoryConfig(dir_list,'./conf/filesDirectory.conf')
oDir.checkFolders()
#
#

#oTemp = Cache(oDir['cacheCrawlerFolder'])

from Agent import CJrjHelper,CAgent,CConfigByYaml
oConf = CConfigByYaml('./conf/ConfigAttributes.yml')


oJrjUrls = CJrjHelper()
oUrlList = oJrjUrls.fetchUrlsForDate(2020,3,6)
#oUrlList = oUrlList[0:2]
jobsList = [oUrlList]
oAgent = CAgent('testjrj',oDir,oConf)
oAgent.configAll()
err= oAgent.startCrawling(jobsList)
#err.wait()
import time
#print(len(oAgent.cacheAgent))
#time.sleep(4)
#print(len(oAgent.cacheAgent))
oAgent.fetchResult(resultHandler,err,1,10)
oAgent.clearCache()
oAgent.closeCache()

#
#import subprocess
##r'C:\Users\zijia\.conda\envs\StellarCrawler\python.exe'
#temp = subprocess.Popen([r'C:\Users\zijia\.conda\envs\StellarCrawler\python.exe','otherTests.py'])

#import subprocess
#
#temp = subprocess.Popen([r'C:\Users\Jin Dou\AppData\Local\conda\conda\envs\Spider\python.exe','KnowledgeManager.py',
#                         "--name","test","--dbPath","mongodb://localhost:27017/","--logFlag","True"])

#python KnowledgeManager.py --name test --dbPath mongodb://localhost:27017/ --logFlag True

#import os
#
#pythonPath = r'"C:\Users\Jin Dou\AppData\Local\conda\conda\envs\Spider\python.exe"'
#knowledgeManagerPath = oDir['rootCode'] + 'KnowledgeManager.py'
#params = "--name test --dbPath mongodb://localhost:27017/ --logFlag True"
#startCmd = pythonPath + ' ' + knowledgeManagerPath + ' ' + params
#print(startCmd)
#err= os.system(startCmd)
#print(err)

#from multiprocessing.connection import Client
#
#address = ('localhost', 6085)
#conn = Client(address, authkey=b'secret password')
#print('connected')
#for idx in range(3):
#    conn.send(str(idx))
#conn.send('close')
##for idx in range(3,10**4):
##    conn.send(str(idx))
#    
#
#msg = conn.recv()
#print(msg)
#
## can also send arbitrary objects:
## conn.send(['a', 2.5, None, int, sum])
#conn.close()