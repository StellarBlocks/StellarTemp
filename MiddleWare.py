# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 15:49:49 2020

@author: Jin Dou
"""
from StorageManager import CDataWrapper
#input:
from datetime import datetime,timedelta
MINDate = datetime(2015,10,1)

oLogWrapper = CDataWrapper(attrSet={'data'})
oResultWrapper = CDataWrapper(currentEmpty=['postInfo'])

def resultHandler(Type,data):
    if(Type == 'logInfo'):
        temp = data['data']
#        print(temp)
        temp['Date'] = dateStrToObject(temp['Date'])
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
            
def dateStrToObject(string):
    from datetime import datetime
    temp = string.split('-')
    temp = [int(i) for i in temp]
    return datetime(*temp)


class CCommandDict:
    
    def __init__(self):
        self.command = dict()
        self.command['nextDate'] = self.calNextStartDate

    def calNextStartDate(self,DBHandle):
        coll = DBHandle['LogInfo']
        numDates = len(coll.distinct("data.Date"))
        maxDate = coll.aggregate([{"$group":{"_id":None,"max":{"$max":"$data.Date"}}}]).next()['max']
        minDate = coll.aggregate([{"$group":{"_id":None,"min":{"$min":"$data.Date"}}}]).next()['min']
        numCalDays = maxDate - minDate 
        numCalDays = numCalDays.days + 1
        step = timedelta(1)
        if(numDates != numCalDays):
            #errorHandle
            print('aaa',numDates,numCalDays)
            pass
        else:
            if(minDate > MINDate):
                return (minDate-step,maxDate+step)
            else:
                return maxDate+step
        
    def __getitem__(self,key):
        return self.command[key]