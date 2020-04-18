# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 14:13:54 2020

@author: jidou
"""
import pymongo
from diskcache import Cache



class CStorage:
    
    def __init__(self,name,path):
        self.name = name + '_storage'
        self.path = path
    

class CStorageMongoDB(CStorage):
    
    def __init__(self,name,path):
        super().__init__(name,path)
        print(path)
        self.client = pymongo.MongoClient(self.path)
        self.db = self.client[self.name + '_db']
        
        

        
        
        
    


