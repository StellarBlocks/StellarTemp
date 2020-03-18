# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 21:01:01 2020

@author: jido
"""


from StellarLog.StellarLog import CLog, CDirectoryConfig

oLog = CLog('./','testLog')
oLog.safeRecord('aaahhh')
dir_list = ['root','sourceListFile','outputRoot','crawlerCWD','jobUrlsFolder',
            'cacheCrawlerFolder','cacheAgentFolder']
oDir = CDirectoryConfig(dir_list,'filesDirectory.conf')
oDir.checkFolders()


from diskcache import Cache

#oTemp = Cache(oDir['cacheCrawlerFolder'])

from Agent import CJrjHelper,CAgent

oJrjUrls = CJrjHelper()
jobsList = oJrjUrls.fetchUrlsForDate(2020,3,6)
jobsList = jobsList[0:2]
oAgent = CAgent('jrj',oDir)
oAgent.dbWeb = "mongodb://localhost:27017/"
oAgent.configAll()
oAgent.startCrawling(jobsList)
oAgent.fetchResult()
oAgent.clearCache()
oAgent.closeCache()

#
#import subprocess
##r'C:\Users\zijia\.conda\envs\StellarCrawler\python.exe'
#temp = subprocess.Popen([r'C:\Users\zijia\.conda\envs\StellarCrawler\python.exe','otherTests.py'])

import subprocess

temp = subprocess.Popen([r'C:\Users\zijia\.conda\envs\StellarCrawler\python.exe','KnowledgeManager.py',
                         "--name","test","--dbPath","mongodb://localhost:27017/"])

from multiprocessing.connection import Client

address = ('localhost', 6083)
conn = Client(address, authkey=b'secret password')
conn.send('close')
msg = conn.recv()
print(msg)
# can also send arbitrary objects:
# conn.send(['a', 2.5, None, int, sum])
conn.close()