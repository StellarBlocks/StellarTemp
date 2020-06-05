# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 14:13:54 2020

@author: jidou
"""
import pymongo
from diskcache import Cache


#current collections: companiesName, ....., LogInfo
class CDataWrapper:
    
    def __init__(self,attrSet = {'preInfo','data','postInfo'},currentEmpty:list=list()):
        self.attrSet = attrSet
        self.currentEmpty = currentEmpty
        
    def __call__(self,*args,**kwargs):
        return self._getDict(*args,**kwargs)
    
    def _getDict(self,*attrListUser,**attrUser):
        userDict = None
        attrListUser = attrListUser[0]
        if(type(attrListUser) == dict):
            userDict = attrListUser
        elif(attrUser != None):
            userDict = attrUser
        else:
            raise ValueError("the input should be a dict or several atttibutes with keys indicated")
        ans = dict()
        for attr in self.attrSet:
            temp = userDict.get(attr)
            if(temp != None):
                ans[attr] = temp
            elif attr in self.currentEmpty:
                ans[attr] = ''
            else:
                raise ValueError("lose data for the key %s indicated in attributes set" % attr)
            
        return ans

class CStorage:
    
    def __init__(self,name,path):
        self.name = name #+ '_storage'
        self.path = path
    

class CStorageMongoDB(CStorage):
    
    def __init__(self,name,path):
        super().__init__(name,path)
        print(path)
        self.client = pymongo.MongoClient(self.path)
        self.db = self.client[self.name + '_db']
        
    def storeData(self,collectionName,wrapper:CDataWrapper,*args,**kwargs):
        collection = self.db[collectionName]
        document = wrapper(*args,**kwargs)
        return collection.insert_one(document)
        

        

        
        
        
    


