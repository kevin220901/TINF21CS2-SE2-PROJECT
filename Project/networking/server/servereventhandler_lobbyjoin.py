

from networking.server.clientapi import ClientApi
from networking import ServerEventHandler

class ServerEventHandler_LobbyJoin(ServerEventHandler):
    
    def handleEvent(self, client:ClientApi, eventData):
        if 'lobbyId' not in eventData:
            client.sendSysMessage('invalid eventData: missing lobby id')
            return

        client.joinLobby(eventData['lobbyId']) 

        pass