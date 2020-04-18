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
    
    def poll(self,timeout=1):
        return self.conn.poll(timeout=timeout)
    
class CCrsProcManager(BaseManager):
    pass

CCrsProcManager.register('server', CServer)

## Multiprocessing Functions

def listenReq(oServer:CServer,oCache:mp.Queue): # old version
    msg = oServer.recv()
    oCache.put(msg)
    return 0

def sendRes(oServer:CServer,msg): # old version
    oServer.send(msg+'multiprocess')
    return 0

def onCallRecvDaemon(oServer:CServer,oInstrCache:mp.Queue,oRecvCache:mp.Queue):
    while True:
        instr = ''
        recvMsg = ''
        otherEndCloseFlag = True
        
        if(oServer.poll(3) != False):# poll will return true when the other end of the pipe is closed
#            print("onCallRecv: Waiting for msg",oServer.poll())
            try:
                recvMsg = oServer.recv()
            except:
                otherEndCloseFlag = True
                recvMsg = ''
            else:
                print(recvMsg)
                oRecvCache.put(recvMsg)
                otherEndCloseFlag = False
        
        if(oServer.poll() == False or otherEndCloseFlag):
            try:
                instr = oInstrCache.get(block = False)
            except:
                instr = ''
            else:
                if (instr == 'close'):
                    print('onCallRecv: recv inst: ' + instr)
                    oInstrCache.put('onCallRecv_Close')
                    break
                else:
                    pass
        
    return 0

def onCallSendDaemon(oServer:CServer,oInstrCache:mp.Queue,oSendCache:mp.Queue):
    while True:
        instr = ''
        sendMsg = ''
        
        try:
            sendMsg = oSendCache.get(block = False)
        except:
            sendMsg = ''
        else:
            oServer.send(sendMsg)
        
        
        if(oSendCache.empty() == True):
            try:
                instr = oInstrCache.get(block = False)
            except:
                instr = ''
            else:
                if (instr == 'close'):
                    print('onCallSend: recv inst: ' + instr)
                    oInstrCache.put('onCallSend_Close')
                    break
                else:
                    pass
        
    return 0

class CKnowledge:
    
    def __init__(self,name, dbPath:str):
        self.name = name + '_knowledge'
        self._storageManager:CStorage = CStorageMongoDB(name,dbPath)
        self.address = ('localhost', 6084)
        self.oCrsProcManager = CCrsProcManager()
        self.oServer = None
        self.oRecvCache = mp.Queue()
        self.oSendCache = mp.Queue()
        self.oInstrRecvCache = mp.Queue()
        self.oInstrSendCache = mp.Queue()
        self.prcRecv = None
        self.prcSend = None
            
    def startServer(self):
        self.oCrsProcManager.start()
        self.oServer = self.oCrsProcManager.server(self.address)
        self.oServer.start()
        print('server start')
        self.prcRecv = mp.Process(target = onCallRecvDaemon, 
                                  args=[self.oServer, self.oInstrRecvCache,self.oRecvCache])
        
        self.prcSend = mp.Process(target = onCallSendDaemon,
                                  args=[self.oServer, self.oInstrSendCache,self.oSendCache])
        self.prcRecv.start()
        self.prcSend.start()
        
        while True:
            recvMsg = ''
            try:
                recvMsg = self.oRecvCache.get(block=False)
            except:
                recvMsg = ''
            else:
                if(recvMsg == 'close'):
                    self.oSendCache.put('close'+'newMultiprocess')
                    self.oInstrRecvCache.put('close')
                    self.oInstrSendCache.put('close')
                    self.prcRecv.join()
                    self.prcSend.join()
                    try:
                        self.prcRecv.close()
                    except:
                        self.prcRecv.terminate()
                    try:
                        self.prcSend.close()
                    except:
                        self.prcSend.terminate()
                    print(self.oInstrRecvCache.get())
                    print(self.oInstrSendCache.get())
                    self.oServer.close()
                    self.oCrsProcManager.shutdown()
                    return 'CKnowledgeServer_close'
                
        return 0
    
    def _close(self):
        try:
            self.prcRecv.close()
        except:
            self.prcRecv.terminate()
        try:
            self.prcSend.close()
        except:
            self.prcSend.terminate()
        self.oServer.close()
        self.oCrsProcManager.shutdown()
#    def startServer(self):
#        self.oServer.start()
#        while True:
#            tempP = mp.Process(target = listenReq, args=[self.oServer,self.oCache])
#            tempP.start()
#            tempP.join()
#            tempP.close()
#            
#            msg = self.oCache.get()
#            
#            tempP = mp.Process(target = sendRes, args=[self.oServer,msg])
#            tempP.start()
#            tempP.join()
#            tempP.close()
#    
#            if msg == 'close':
#                self.oServer.close()
#                break
        
        

if __name__ == "__main__":
    args = parse_args()
    print("call with arguments:")
    print(args)
    
    oKnowledge = CKnowledge(args.name,args.dbPath)
    try:
        err = oKnowledge.startServer()
    except:
        oKnowledge._close()
    print(err)
#    oServer = CServer(('localhost', 6083))
#    oServer.start()
    