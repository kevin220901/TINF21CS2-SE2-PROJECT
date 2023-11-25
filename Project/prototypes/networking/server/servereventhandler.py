


import pickle
import socket
from networking.socketwrapper import SocketWrapper

from networking.networkevent import NetworkEvent


class ServerEventHandler:

    def handleEvent(self, context, eventData):
        print("handle event")
        conn: SocketWrapper = context['conn']

        eventData = {'sysmessage':'this event is being handled by the eventhandler'}
       
        conn.sendall(NetworkEvent.SYSMESSAGE, eventData)
        pass
    
