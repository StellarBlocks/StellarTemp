# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 15:49:49 2020

@author: Jin Dou
"""
from StorageManager import CDataWrapper
#input:

oLogWrapper = CDataWrapper(attrSet={'data'})
oResultWrapper = CDataWrapper(currentEmpty=['postInfo'])

def resultHandler(Type,data):
    if(Type == 'logInfo'):
        return [('LogInfo',oLogWrapper,data)]
    elif (Type == 'crawlerResult'):
#        ans = list()
#        for info in data['preInfo']:
#            ans.append((info,oResultWrapper,data))
#        return ans
        if len(data['preInfo']) > 1:
            data['keywords'] = "_".join(data['preInfo'])
            return [("multiCompaniesTogether",oResultWrapper,data)]
        else:
            return [(data['preInfo'][0],oResultWrapper,data)]
            
    