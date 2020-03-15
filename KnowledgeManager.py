# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 13:27:23 2020

@author: jido
"""

from StorageManager import CStorage,CStorageMongoDB
from multiprocessing.connection import Listener
import argparse

def parse_args():
  """
  Parse input arguments
  """
  parser = argparse.ArgumentParser(description='Train a Fast R-CNN network')
  parser.add_argument('--name', dest='name',
                      help='name',
                      default='test', type=str)
  parser.add_argument('--dbPath', dest='dbPath',
                    help='database path',
                    default='mongodb://localhost:27017/', type=str)

  args = parser.parse_args()
  return args



class CKnowledge:
    
    def __init__(self,name, dbPath:str):
        self.name = name + '_knowledge'
        self._storageManager:CStorage = CStorageMongoDB(name,dbPath)
        self.address = ('localhost', 6082) 
        self.listener = Listener(self.address, authkey=b'secret password')
        self.readers = list()
        self.readers.append(self.listener)
        
        
    def startServer(self):
        self.conn = self.listener.accept()
        while True:
            msg = self.conn.recv()
            self.conn.send(msg)
            if msg == 'close':
                self.conn.close()
                break
            # family is deduced to be 'AF_INET'
        
        

if __name__ == "__main__":
    args = parse_args()
    print("call with arguments:")
    print(args)
    
    oKnowledge = CKnowledge(args.name,args.dbPath)
    oKnowledge.startServer()
    