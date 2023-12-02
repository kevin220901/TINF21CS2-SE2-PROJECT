
from server.clientapi import ClientApi
from server.servereventhandler import ServerEventHandler

##################################################
## Author: Luis Eckert
##################################################

class ServerEventHandler_Login(ServerEventHandler):

    def __init__(self, client: ClientApi) -> None:
        super().__init__(client)
        pass
    
    def handleEvent(self, eventData):
        if 'username' not in eventData or 'password' not in eventData:
            self._client.connection.emit_SysMessage('invalid eventData: missing credentials')

        if self._client.hasAuthToken:
            self._client.connection.emit_SysMessage('allready logged in')
            return
            
        self._client.login(eventData['username'], eventData['password'])

        pass