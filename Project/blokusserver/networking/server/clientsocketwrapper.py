



import socket
from common.networkevent import NetworkEvent
from common.socketwrapper import SocketWrapper

#TODO: do i need this class or can the funtionality be moved to lobby?


##################################################
## Author: Luis Eckert
##################################################


class ClientSocketWrapper(SocketWrapper):
    def __init__(self, conn: socket.socket) -> None:
        super().__init__(conn)


    def sendSysMessage(self, message):
        eventId = NetworkEvent.SYSMESSAGE
        eventData = {
            'message':message
        }
        self.sendall(eventId, eventData)


    def sendMessage(self, sender:str, message:str):
        eventId = NetworkEvent.MESSAGE
        eventData = {
            'from':sender, 
            'message':message
        }
        self.sendall(eventId, eventData)