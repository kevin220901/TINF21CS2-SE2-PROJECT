


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
        #only return joinable lobbies
        #lobbyId
        #lobbyName
        #playerCount
        
        lobbyList = []
        lobby: Lobby

        for key, lobby in self._client.lobbies.items():
            if lobby.cantBeJoined: continue
            lobbyList.append({
                'lobbyId':lobby.lobbyId,
                'lobbyName':lobby.lobbyName,
                'playerCount':lobby.playerCount
            })
        
        self._client.sendLobbyBrowsingResult(lobbyList)
        pass
    
