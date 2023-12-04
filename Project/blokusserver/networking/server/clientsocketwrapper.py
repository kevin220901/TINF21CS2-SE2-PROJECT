



import socket
from common.networkevent import NetworkEvent
from common.socketwrapper import SocketWrapper

##################################################
## Author: Luis Eckert
##################################################


class ClientSocketWrapper(SocketWrapper):
    def __init__(self, conn: socket.socket) -> None:
        super().__init__(conn)


    def emit_SysMessage(self, message):
        eventId = NetworkEvent.SYSMESSAGE
        eventData = {
            'message':message
        }
        self.sendall(eventId, eventData)


    def emit_Message(self, sender:str, message:str):
        eventId = NetworkEvent.MESSAGE
        eventData = {
            'from':sender, 
            'message':message
        }
        self.sendall(eventId, eventData)
        pass

    def emit_Login_success(self, token):
        eventId = NetworkEvent.LOGIN_SUCCESS
        eventData = {
            'token':token
        }
        self.sendall(eventId, eventData)
        pass

    def emit_Login_fail(self):
        self.emit_SysMessage('access denied')
        pass

    def emit_LobbyCreate_success(self, lobbyInfo):
        eventId = NetworkEvent.LOBBY_CREATE
        eventData = lobbyInfo
        self.sendall(eventId, eventData)
        pass

    def emit_LobbyCreate_fail(self, message):
        self.emit_SysMessage(message)
        pass

    def emit_LobbyJoin_success(self, lobbyInfo):
        eventId = NetworkEvent.LOBBY_JOIN
        eventData = {
            'lobbyInfo':lobbyInfo
        }
        self.sendall(eventId, eventData)
        pass

    def emit_LobbyJoin_fail(self, message):
        self.emit_SysMessage(message)
        pass


    def emit_availableLobbies(self, lobbies):
        eventId = NetworkEvent.LOBBIES_GET
        eventData = lobbies
        self.sendall(eventId, eventData)
        pass

    def emit_Registration_success(self):
        eventId = NetworkEvent.REGISTRATION_SUCCESS
        eventData = {}
        self.sendall(eventId, eventData)
        pass
     
    def emit_Profile_read(self, profileData):
        eventId = NetworkEvent.PROFILE_READ
        eventData = profileData
        self.sendall(eventId, eventData)
        pass

    def emit_profile_deleted(self):
        eventId = NetworkEvent.PROFILE_DELETE
        eventData = {}
        self.sendall(eventId, eventData)
        pass

    def emit_profile_updated(self):
        eventId = NetworkEvent.PROFILE_UPDATE
        eventData = {}
        self.sendall(eventId, eventData)
        pass

    def emit_lobby_update(self, lobbyInfo):
        eventId = NetworkEvent.LOBBY_UPDATE
        eventData = lobbyInfo
        self.sendall(eventId, eventData)
        pass