


from server.lobby import Lobby
from server.clientapi import ClientApi
from server.servereventhandler import ServerEventHandler

##################################################
## Author: Luis Eckert
##################################################

class ServerEventHandler_LobbyBrowse(ServerEventHandler):
    def __init__(self, client: ClientApi) -> None:
        super().__init__(client)
        pass

    def handleEvent(self, eventData):
        if self._handleIvalidateAuthToken(eventData.get('token')): return
        
        lobbyList = []
        lobby: Lobby

        for key, lobby in self._client.lobbies.items():
            if lobby.cantBeJoined: continue
            lobbyList.append({
                'lobbyId':lobby.lobbyId,
                'playerCount':lobby.playerCount,
                'difficulty':'easy'
            })
        
        self._client.connection.emit_availableLobbies(lobbyList)
        pass
    
