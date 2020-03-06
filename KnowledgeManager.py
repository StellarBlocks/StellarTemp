# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 13:27:23 2020

@author: jido
"""

from StorageManager import CStorage

class CKnowledge:
    
    def __init__(self,name, storageManager:CStorage):
        self.name = name + '_knowledge'
        self._storageManager:CStorage = storageManager