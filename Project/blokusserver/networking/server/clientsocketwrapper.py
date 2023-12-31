



import socket
from common.networkevent import NetworkEvent
from common.socketwrapper import SocketWrapper

##################################################
## Author: Luis Eckert
##################################################


class ClientSocketWrapper(SocketWrapper):
    def __init__(self, conn: socket.socket) -> None:
        super().__init__(conn)


    def emit_SysMessage(self, message)->None:
        eventId = NetworkEvent.SYSMESSAGE
        eventData = {
            'message':message
        }
        self.sendall(eventId, eventData)


    def emit_Message(self, sender:str, message:str)->None:
        eventId = NetworkEvent.MESSAGE
        eventData = {
            'from':sender, 
            'message':message
        }
        self.sendall(eventId, eventData)
        return

    def emit_Login_success(self, token, id, username)->None:
        eventId = NetworkEvent.LOGIN_SUCCESS
        eventData = {
            'token':token,
            'id':id,
            'username':username
        }
        self.sendall(eventId, eventData)
        return

    def emit_Login_fail(self, message='access denied')->None:
        self.emit_SysMessage(message)
        return

    def emit_LobbyCreate_success(self, lobbyInfo)->None:
        eventId = NetworkEvent.LOBBY_CREATE
        eventData = lobbyInfo
        self.sendall(eventId, eventData)
        return

    def emit_LobbyCreate_fail(self, message)->None:
        self.emit_SysMessage(message)
        return

    def emit_LobbyJoin_success(self, lobbyInfo)->None:
        eventId = NetworkEvent.LOBBY_JOIN
        eventData = lobbyInfo
        self.sendall(eventId, eventData)
        return

    def emit_LobbyJoin_fail(self, message)->None:
        self.emit_SysMessage(message)
        return


    def emit_availableLobbies(self, lobbies)->None:
        eventId = NetworkEvent.LOBBIES_GET
        eventData = lobbies
        self.sendall(eventId, eventData)
        return

    def emit_Registration_success(self)->None:
        eventId = NetworkEvent.REGISTRATION_SUCCESS
        eventData = {}
        self.sendall(eventId, eventData)
        return
     
    def emit_Profile_read(self, profileData)->None:
        eventId = NetworkEvent.PROFILE_READ
        eventData = profileData
        self.sendall(eventId, eventData)
        return

    def emit_profile_deleted(self)->None:
        eventId = NetworkEvent.PROFILE_DELETE
        eventData = {}
        self.sendall(eventId, eventData)
        return

    def emit_profile_updated(self)->None:
        eventId = NetworkEvent.PROFILE_UPDATE
        eventData = {}
        self.sendall(eventId, eventData)
        return
    
    def emit_profile_updated_password(self, token, id, username)->None:
        eventId = NetworkEvent.PROFILE_UPDATE_PASSWORD
        eventData = {
            'token':token,
            'id':id,
            'username':username
        }
        self.sendall(eventId, eventData)
        return

    def emit_lobby_update(self, lobbyInfo)->None:
        eventId = NetworkEvent.LOBBY_UPDATE
        eventData = lobbyInfo
        self.sendall(eventId, eventData)
        return

    def emit_game_start(self, gameInfo)->None:
        eventId = NetworkEvent.GAME_START
        eventData = gameInfo
        self.sendall(eventId, eventData)
        return

    def emit_game_update(self, gameInfo)->None:
        eventId = NetworkEvent.GAME_UPDATE
        eventData = gameInfo
        self.sendall(eventId, eventData)
        return
    
    def emit_game_invalidPlacement(self, message)->None:
        eventId = NetworkEvent.GAME_INVALID_PLACEMENT
        eventData = message
        self.sendall(eventId, eventData)
        return
    
    def emit_game_finish(self, winnerInfo)->None:
        eventId = NetworkEvent.GAME_FINISH
        eventData = winnerInfo
        self.sendall(eventId, eventData)
        return