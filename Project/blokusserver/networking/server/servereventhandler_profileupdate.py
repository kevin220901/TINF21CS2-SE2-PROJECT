
from server.clientapi import ClientApi
from server.servereventhandler import ServerEventHandler

class ServerEventHandler_ProfileUpdate(ServerEventHandler):
    def __init__(self, client:ClientApi):
        super().__init__(client)
    
    def handleEvent(self, eventData):
        if self._handleIvalidateAuthToken(eventData.get('token')): return

        self._client.updateProfile(eventData['token'], eventData['username'], eventData['email'])