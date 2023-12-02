


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
        if 'message' not in eventData: 
            self._client.connection.emit_SysMessage('invalid message')
            return 
        
        self._client.connection.emit_Message(eventData['message'])
        pass

