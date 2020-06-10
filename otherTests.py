# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 21:01:01 2020

@author: jido
"""


from StellarLog.StellarLog import CLog, CDirectoryConfig
from MiddleWare import resultHandler, MINDate
from datetime import datetime,timedelta
from Agent import CJrjHelper,CAgent,CConfigByYaml
import signal,time
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
oAgent = CAgent('testjrjNew',oDir,oConf,True)
oAgent.configAll()
oAgent.knowledgeManagerClient.send('busyMode')
oAgent.knowledgeManagerClient.send('nextDate')
oAgent.knowledgeManagerClient.send('quitBusyMode')
key = oAgent.knowledgeManagerClient.recv(True)
result = oAgent.cacheAgent.get(key)
dateToFetch = None
endDate = None
if(type(result) == str):
    dateToFetch = MINDate
    endDate = datetime.now()
else:
    if type(result) == tuple:
        dateToFetch = MINDate
        endDate = result[0]
    elif(isinstance(result,datetime)):
        dateToFetch = result
        endDate = datetime.now()
print(dateToFetch,endDate)
while dateToFetch <= endDate :
    print(str(dateToFetch) + '; current time  '+str(datetime.now()))
    oJrjUrls = CJrjHelper()
    y = dateToFetch.year
    m = dateToFetch.month
    d = dateToFetch.day
    print('start fetchUrls; current time  ' + str(datetime.now()))
    oUrlList = oJrjUrls.fetchUrlsForDate(y,m,d)
    #oUrlList = oUrlList[0:2]
    jobsList = [oUrlList]
    print('start crawling; current time ' + str(datetime.now()))
    err= oAgent.startCrawling(jobsList)
    print('start fetching; current time  ' + str(datetime.now()))
    oAgent.fetchResult(resultHandler,err,1,10)
    dateToFetch = dateToFetch + oDateDelta
    if(oAgent.flagUserClose):
        break
    print('------------------------------------------------')
oAgent.clearCache()
oAgent.close()

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

#from multiprocessing.connection import Client
#
#address = ('localhost', 6085)
#conn = Client(address, authkey=b'secret password')
#print('connected')
#for idx in range(3):
#    conn.send(str(idx))
#conn.send('close')
#
#msg = conn.recv()
#print(msg)
#
## can also send arbitrary objects:
## conn.send(['a', 2.5, None, int, sum])
#conn.close()

from KnowledgeManager import CKnowledgeClient
address = ('localhost', 6085)
oClient = CKnowledgeClient(address)
oClient.connect()
oClient.send('hi')
oClient.send('close')
msg = oClient.recv()
print(msg)
err = oClient.close()
print(err)
