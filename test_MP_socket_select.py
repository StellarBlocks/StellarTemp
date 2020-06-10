# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 23:09:15 2020

@author: Jin Dou
"""

import multiprocessing as mp
import socket,select
from multiprocessing.connection import Listener
from multiprocessing.managers import BaseManager
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
    
    def getConnection(self):
        return self.conn
    
class CCrsProcManager(BaseManager):
    pass


def onCallRecvDaemon(address,oServer:CServer,oRecvCache:mp.Queue):
    oSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    oSocket.bind(address)
    oSocket.listen()
    oInnerConn,addr = oSocket.accept()
    oOuterConn = oServer.getConnection()
    
    readList = [oSocket,oOuterConn,oInnerConn]
    otherEndCloseFlag = False
    while True:
        rd,wt,ex = select.select(readList,[],[])
        for r in rd:
            if r is oSocket:
                c,addr = r.accept()
                oInnerConn = c
                readList.append(c)
                print('onCallRecv: connected')
            elif r is oOuterConn:
                if r.poll(3):
                    try:
                        recvMsg = oOuterConn.recv()
                    except:
                        recvMsg = ''
                        print('onCallRecv: the other side is closed')
                        readList.remove(oOuterConn)
                    else:
                        print('onCallRecv_recv_msg: ',recvMsg)
                        oRecvCache.put(recvMsg)
                        oInnerConn.send(b'newMsg')
                        if(recvMsg == 'quitBusyMode'):
                            return
            elif r is oInnerConn:
                data = r.recv(512)
                msg = data.decode()
                print('onCallRecv_recv_instr:',msg)
                if(msg == 'close'):
                    oSocket.close()
                    return
    return
    

def onCallSendDaemon(address,oServer:CServer,oSendCache:mp.Queue):
    oSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    oSocket.bind(address)
    oSocket.listen()
    oInnerConn,addr = oSocket.accept()
    oOuterConn = oServer.getConnection()
    
    readList = [oSocket,oInnerConn]
    while True:
        rd,wt,ex = select.select(readList,[],[])
        for r in rd:
            if r is oSocket:
                c,addr = r.accept()
                oInnerConn = c
                readList.append(c)
                print('onCallSend_connected')
            elif r is oInnerConn:
                data = r.recv(512)
                msg = data.decode()
                print('onCallSend_recv_instr:',msg)
                if('send' in msg): #close and send can be concatenated together
                    while (not oSendCache.empty()):
                        try:
                            sendMsg = oSendCache.get(timeout = 3)
                        except:
                            sendMsg = ''
                        else:
                            oOuterConn.send(sendMsg)
                            print('onCallSend_send_msg: ', sendMsg)
                if('close' in msg):
                    oSocket.close()
                    return

if __name__ == '__main__':

    CCrsProcManager.register('server', CServer)#regested class in Manager can only use the class's method but not attribute
    #https://docs.python.org/3.6/library/multiprocessing.html#multiprocessing.managers.BaseManager.register
    
    
    address = ('localhost', 6085)
    addressSendDaemon = ('localhost',8300)
    addressRecvDaemon = ('localhost',8301)
    
    #prepare connection for outer
    oCrsProcManager = CCrsProcManager()
    oCrsProcManager.start()
    oServer = oCrsProcManager.server(address)
    print('main server is ready for connection')
    oServer.start()
    oConn = oServer.getConnection()
    oRecvCache = mp.Queue()
    oSendCache = mp.Queue()
    
    
    prcRecv = mp.Process(target=onCallRecvDaemon,
                         args=[addressRecvDaemon,oServer,oRecvCache])
    
    prcSend = mp.Process(target=onCallSendDaemon,
                         args=[addressSendDaemon,oServer,oSendCache])
    
    prcRecv.start()
    prcSend.start()
    
    oSockSendDaemon = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    oSockRecvDaemon = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    
    oSockSendDaemon.connect(addressSendDaemon)
    oSockRecvDaemon.connect(addressRecvDaemon)
    readList = [oSockRecvDaemon]
    Flag = True
    timeout = 5
    while Flag:
        rd,wt,ex = select.select(readList,[],[],timeout)
        for r in rd:
            if r is oSockRecvDaemon:
                data = r.recv(512)
                msg = data.decode()
                print('main server recv inner msg:', msg)
                if(msg == 'newMsg'):
                    recvMsg = ''
                    try:
                        recvMsg = oRecvCache.get(timeout=1)
                    except:
                        recvMsg = ''
                #                print(self.oCommandDict.command.keys())
                    print('main server recv msg:', recvMsg)
                    if(recvMsg == 'close'):
                        oSendCache.put('All is closed')
                        oSockSendDaemon.send(b'send')
                        err1 = oSockSendDaemon.send(b'close')
                        err2 = oSockRecvDaemon.send(b'close')
                        prcRecv.join()
                        prcSend.join()
                        oRecvCache.close()
                        oSendCache.close()
                        Flag = False
        print('main server select timeout:',timeout)


