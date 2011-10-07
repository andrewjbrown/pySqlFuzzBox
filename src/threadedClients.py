'''
Created on Oct 7, 2011

@author: nemo@whipping-post.com
'''

import sys
import thread

class threadedClients(object):
    '''
    threadedClients takes control of how many clients are to run.  
    It will run N clients and return when they have finished.  
    '''
    def __init__(self, arg1):
        '''
        Constructor
        '''
        self.clients = arg1
        
    def clientPayload(self,arg1):
        # TODO: Accept payload as a text file and create a sql statement
        print("Client SQL Statement Happens Here # %d" %arg1)

    
    def createChildren(self):
        # TODO: Create N   number of children  
        for x in range(self.clients):
            thread.start_new_thread(threadedClients.clientPayload, (self,x))
        
        
