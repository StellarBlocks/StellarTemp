# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 21:01:01 2020

@author: jido
"""


from StellarLog.StellarLog import CLog, CDirectoryConfig
from MiddleWare import resultHandler, MINDate
from datetime import datetime,timedelta
from Agent import CJrjHelper,CAgent,CConfigByYaml
#oLog = CLog('./','testLog')
#oLog.safeRecord('aaahhh')

#
#

#oTemp = Cache(oDir['cacheCrawlerFolder'])

oDateDelta = timedelta(1)

#config agent
dir_list = ['root','rootCode','sourceListFile','outputRoot','crawlerCWD','jobUrlsFolder',
            'cacheCrawlerFolder','cacheAgentFolder','Log']
oDir = CDirectoryConfig(dir_list,'./conf/filesDirectory.conf')
oDir.checkFolders()

oConf = CConfigByYaml('./conf/ConfigAttributes.yml')
oAgent = CAgent('testjrj',oDir,oConf)

dateToFetch =datetime(2016,1,1)
today = datetime.now()
while dateToFetch <= today :
    oJrjUrls = CJrjHelper()
    y = dateToFetch.year
    m = dateToFetch.month
    d = dateToFetch.day
    oUrlList = oJrjUrls.fetchUrlsForDate(y,m,d)
    #oUrlList = oUrlList[0:2]
    jobsList = [oUrlList]
    oAgent.configAll()
    err= oAgent.startCrawling(jobsList)
    oAgent.fetchResult(resultHandler,err,1,10)
    dateToFetch = dateToFetch + oDateDelta
oAgent.clearCache()
oAgent.closeCache()

'''
#to do:
Add the part for handling keyboard interrupt,
Add a semophore to indicate that the agent is writing to database,
make the program didn't exit until all fetched data is written in database

'''
#
#import subprocess
##r'C:\Users\zijia\.conda\envs\StellarCrawler\python.exe'
#temp = subprocess.Popen([r'C:\Users\zijia\.conda\envs\StellarCrawler\python.exe','otherTests.py'])

#import subprocess
#
#temp = subprocess.Popen([r'C:\Users\Jin Dou\AppData\Local\conda\conda\envs\Spider\python.exe','KnowledgeManager.py',
#                         "--name","test","--dbPath","mongodb://localhost:27017/","--logFlag","True"])

#python KnowledgeManager.py --name testjrj --dbPath mongodb://localhost:27017/ --logFlag True

#import os
#
#pythonPath = r'"C:\Users\Jin Dou\AppData\Local\conda\conda\envs\Spider\python.exe"'
#knowledgeManagerPath = oDir['rootCode'] + 'KnowledgeManager.py'
#params = "--name test --dbPath mongodb://localhost:27017/ --logFlag True"
#startCmd = pythonPath + ' ' + knowledgeManagerPath + ' ' + params
#print(startCmd)
#err= os.system(startCmd)
#print(err)

from multiprocessing.connection import Client

address = ('localhost', 6085)
conn = Client(address, authkey=b'secret password')
print('connected')
for idx in range(3):
    conn.send(str(idx))
conn.send('close')
#for idx in range(3,10**4):
#    conn.send(str(idx))
    

msg = conn.recv()
print(msg)

# can also send arbitrary objects:
# conn.send(['a', 2.5, None, int, sum])
conn.close()