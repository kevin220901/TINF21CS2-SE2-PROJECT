


from server.clientapi import ClientApi
from server.servereventhandler import ServerEventHandler

##################################################
## Author: Luis Eckert
##################################################


class ServerEventHandler_LobbyReady(ServerEventHandler):
    def __init__(self, client: ClientApi) -> None:
        super().__init__(client)
        pass

    def handleEvent(self, eventData):
        self._client.toggleReady()
        pass
    
