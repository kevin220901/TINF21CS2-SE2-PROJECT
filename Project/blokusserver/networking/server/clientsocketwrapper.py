



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


    def notify_SysMessage(self, message):
        eventId = NetworkEvent.SYSMESSAGE
        eventData = {
            'message':message
        }
        self.sendall(eventId, eventData)


    def notify_Message(self, sender:str, message:str):
        eventId = NetworkEvent.MESSAGE
        eventData = {
            'from':sender, 
            'message':message
        }
        self.sendall(eventId, eventData)
        pass

    def notify_Login_success(self, token):
        eventId = NetworkEvent.LOGIN_SUCCESS
        eventData = {
            'token':token
        }
        self.sendall(eventId, eventData)
        pass

    def notify_Login_fail(self):
        self.notify_SysMessage('access denied')
        pass

    def notify_LobbyCreate_success(self, lobbyInfo): #TODO: the data structure for lobbyInfo has yet to be defined
        eventId = NetworkEvent.LOGIN_SUCCESS
        eventData = {
            'lobbyInfo':lobbyInfo
        }
        self.sendall(eventId, eventData)
        pass

    def notify_LobbyCreate_fail(self, message):
        self.notify_SysMessage(message)
        pass

    def notify_LobbyJoin_success(self, lobbyInfo):
        eventId = NetworkEvent.LOBBY_JOIN
        eventData = {
            'lobbyInfo':lobbyInfo
        }
        self.sendall(eventId, eventData)
        pass

    def notify_LobbyJoin_fail(self, message):
        self.notify_SysMessage(message)
        pass