

from server.clientapi import ClientApi
from server.servereventhandler import ServerEventHandler

##################################################
## Author: Luis Eckert
##################################################

class ServerEventHandler_LobbyLeave(ServerEventHandler):
    def __init__(self, client: ClientApi) -> None:
        super().__init__(client)
        pass

    def handleEvent(self, eventData):
        if self._handleIvalidateAuthToken(eventData.get('token')): return
        self._client.leaveLobby()
        pass
    
