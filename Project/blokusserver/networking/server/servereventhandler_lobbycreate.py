

from server.clientapi import ClientApi
from server.servereventhandler import ServerEventHandler

#do i need to make the handleEvent a critical section?
#maby use one set of ServerEventHandlers per connected client to prevent thread bleeding?

##################################################
## Author: Luis Eckert
##################################################

class ServerEventHandler_LobbyCreate(ServerEventHandler):
    def __init__(self, client: ClientApi) -> None:
        super().__init__(client)
        pass
    
    def handleEvent(self, eventData):
        if not eventData: 
            self._client.connection.emit_SysMessage('server recieved invalid data')
            return
        
        if self._handleIvalidateAuthToken(eventData.get('token')): return

        if 'lobbyName' not in eventData: 
            self._client.connection.emit_SysMessage('server recieved invalid lobby name')
            return

        self._client.createLobby(eventData['lobbyName'])
        pass