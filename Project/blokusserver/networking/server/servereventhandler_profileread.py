

from server.clientapi import ClientApi
from server.servereventhandler import ServerEventHandler


class ServerEventHandler_ProfileRead(ServerEventHandler):
    def __init__(self, client:ClientApi):
        super().__init__(client)
    
    def handleEvent(self, eventData):
        if self._handleIvalidateAuthToken(eventData.get('token')): return

        self._client.readProfile(eventData['token'])