


from server.clientapi import ClientApi
from server.servereventhandler import ServerEventHandler

##################################################
## Author: Luis Eckert
##################################################

class ServerEventHandler_ChatMessage(ServerEventHandler):
    def __init__(self, client: ClientApi) -> None:
        super().__init__(client)
        pass
    
    def handleEvent(self, eventData):
        if self._handleIvalidateAuthToken(eventData.get('token')): return
        if 'message' not in eventData: 
            self._client.connection.emit_SysMessage('invalid message')
            return 
        
        self._client.currentLobby.broadcastMessage(self._client, eventData['message'])
        pass

