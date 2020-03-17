# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 13:27:23 2020

@author: jido
"""

from StorageManager import CStorage,CStorageMongoDB
from multiprocessing.connection import Listener
from multiprocessing.managers import BaseManager  
import multiprocessing as mp
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

class CServer:
    
    def __init__(self,address:tuple):
        self.address = address
        self.listener = Listener(self.address, authkey=b'secret password')
        self.conn = None
        
    def start(self):
        self.conn = self.listener.accept()
    
    def recv(self):
        return self.conn.recv()
    
    def send(self,content):
        return self.conn.send(content)
    
    def close(self):
        return self.conn.close()
    
class CCrsProcManager(BaseManager):
    pass

CCrsProcManager.register('server', CServer)

def listenReq(oServer:CServer,oCache:mp.Queue):
    msg = oServer.recv()
    oCache.put(msg)
    return 0

def sendRes(oServer:CServer,msg):
    oServer.send(msg+'multiprocess')
    return 0

class CKnowledge:
    
    def __init__(self,name, dbPath:str):
        self.name = name + '_knowledge'
        self._storageManager:CStorage = CStorageMongoDB(name,dbPath)
        self.address = ('localhost', 6082)
        self.oCrsProcManager = CCrsProcManager()
        self.oCrsProcManager.start()
        self.oServer = self.oCrsProcManager.server(self.address)
        self.oCache = mp.Queue()
            
    def startServer(self):
        self.oServer.start()
        while True:
            tempP = mp.Process(target = listenReq, args=[self.oServer,self.oCache])
            tempP.start()
            tempP.join()
            tempP.close()
            
            msg = self.oCache.get()
            
            tempP = mp.Process(target = sendRes, args=[self.oServer,msg])
            tempP.start()
            tempP.join()
            tempP.close()
    
            if msg == 'close':
                self.oServer.close()
                break
            # family is deduced to be 'AF_INET'
        
        

if __name__ == "__main__":
    args = parse_args()
    print("call with arguments:")
    print(args)
    
    oKnowledge = CKnowledge(args.name,args.dbPath)
    oKnowledge.startServer()
    