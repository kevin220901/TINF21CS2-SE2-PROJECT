

from server.clientapi import ClientApi
from server.servereventhandler import ServerEventHandler

##################################################
## Author: Luis Eckert
##################################################

class ServerEventHandler_LobbyRefresh(ServerEventHandler):
    def __init__(self, client: ClientApi) -> None:
        super().__init__(client)
        pass
    
    def handleEvent(self, eventData):
        if self._handleIvalidateAuthToken(eventData.get('token')): return
        if self._handleNotInLobby(): return
        
        self._client.connection.emit_lobby_update(self._client.currentLobby.get_lobby_info())

        pass