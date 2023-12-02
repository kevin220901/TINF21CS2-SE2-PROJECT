

from server.clientapi import ClientApi
from server.servereventhandler import ServerEventHandler

##################################################
## Author: Luis Eckert
##################################################

class ServerEventHandler_LobbyJoin(ServerEventHandler):
    def __init__(self, client: ClientApi) -> None:
        super().__init__(client)
        pass
    
    def handleEvent(self, client:ClientApi, eventData):
        if 'lobbyId' not in eventData:
            self._client.connection.emit_SysMessage('invalid eventData: missing lobby id')
            return
        
        self._client.joinLobby(eventData['lobbyId']) 

        pass