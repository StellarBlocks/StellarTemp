# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 21:01:01 2020

@author: jido
"""


#from StellarLog.StellarLog import CLog, CDirectoryConfig

oLog = CLog('./','testLog')
oLog.safeRecord('aaahhh')
dir_list = ['root','sourceListFile','outputRoot','crawlerCWD','jobUrlsFolder']
oDir = CDirectoryConfig(dir_list,'filesDirectory.conf')


