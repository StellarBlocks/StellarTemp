# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 14:44:46 2020

@author: Jin Dou
"""

import signal
import sys

    
class CFkeyboardInterrupt:
    
    def __init__(self):
        self._register = set()
    
    def __call__(self,func):
        if(callable(func)):
            self._register.add(func)
        else:
            raise ValueError("input should be a function")
    
    def handler(self,signalInput,frame):
        for func in self._register:
            err,errmsg = func(signalInput,frame)
            if(err == False):
                print(errmsg)
                return
        sys.exit(0)
        
    def test_signal_handler(self,signal,frame):
        print('You pressed Ctrl+C!')
        
fKeyboardInterruptRegistrar = CFkeyboardInterrupt()

signal.signal(signal.SIGINT,fKeyboardInterruptRegistrar.handler)
#print('Press Ctrl+C')
#for x in range(1,100):
#    time.sleep(2)
#    print(x) 

