


import pickle
import socket
from networking.server.clientapi import ClientApi
from networking.socketwrapper import SocketWrapper

from networking.networkevent import NetworkEvent


class ServerEventHandler:

    def handleEvent(self, client:ClientApi, eventData):
        print("handle event")

        client.sendSysMessage('this event is being handled by the eventhandler')
        
        pass
    
