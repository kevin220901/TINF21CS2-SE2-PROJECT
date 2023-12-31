


from server.clientapi import ClientApi
from server.servereventhandler import ServerEventHandler

##################################################
## Author: Luis Eckert
##################################################

class ServerEventHandler_GameStart(ServerEventHandler):
    def __init__(self, client: ClientApi) -> None:
        super().__init__(client)
        pass

    def handleEvent(self, eventData):
        if self._handleIvalidateAuthToken(eventData.get('token')): return
        if self._handleNotInLobby(): return

        self._client.startGame()
        
        pass
    
