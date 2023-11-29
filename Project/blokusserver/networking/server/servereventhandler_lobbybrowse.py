


from networking.server.lobby import Lobby
from networking.server.clientapi import ClientApi


class ServerEventHandler_LobbyBrowse:

    def handleEvent(self, client:ClientApi, eventData):
        #only return joinable lobbies
        #lobbyId
        #lobbyName
        #playerCount
        
        lobbyList = []
        lobby: Lobby

        for key, lobby in client.lobbies.items():
            if lobby.cantBeJoined: continue
            lobbyList.append({
                'lobbyId':lobby.lobbyId,
                'lobbyName':lobby.lobbyName,
                'playerCount':lobby.playerCount
            })
        
        client.sendLobbyBrowsingResult(lobbyList)
        pass
    
