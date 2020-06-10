# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 13:26:35 2020

@author: jido
"""

##not work very well
#import trafilatura
#downloaded = trafilatura.fetch_url('http://finance.jrj.com.cn/2020/04/24012529362098.shtml')
##string = trafilatura.extract(downloaded, include_comments=False, include_tables=False)
#
#from boilerpipe.extract import Extractor
#extractor = Extractor(extractor='ArticleExtractor', html=downloaded)
#title = extractor.getTitle()
#content = extractor.getText()


from StellarLog.StellarLog import CLog, CDirectoryConfig
from MiddleWare import resultHandler, MINDate
from datetime import datetime,timedelta
from Agent import CJrjHelper,CAgent,CConfigByYaml
from KnowledgeManager import oCommandDict

import signal,time
#oLog = CLog('./','testLog')
#oLog.safeRecord('aaahhh')

#
#self.command['nextDate'] = self.calNextStartDate

#oTemp = Cache(oDir['cacheCrawlerFolder'])

oDateDelta = timedelta(1)

#config agent
dir_list = ['root','rootCode','sourceListFile','outputRoot','crawlerCWD','jobUrlsFolder',
            'cacheCrawlerFolder','cacheAgentFolder','Log']
oDir = CDirectoryConfig(dir_list,'./conf/filesDirectory.conf')
oDir.checkFolders()

#register agent needed service with knowledgeManager
oConf = CConfigByYaml('./conf/ConfigAttributes.yml')
oAgent = CAgent('testjrj',oDir,oConf,True)
oAgent.configAll()
#oAgent.test()

oAgent.knowledgeManagerClient.send('busyMode')
oAgent.knowledgeManagerClient.send('quitBusyMode')
oAgent.close()

oAgent.knowledgeManagerClient.send('nextDate')
key = oAgent.knowledgeManagerClient.recv(True)
result = oAgent.cacheAgent.get(key)


#test keyboard interrupt
#print('Press Ctrl+C')
#for x in range(1,100):
#    time.sleep(0.2)
#    print(x) 