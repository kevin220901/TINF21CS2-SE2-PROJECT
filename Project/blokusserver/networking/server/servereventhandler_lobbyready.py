


from server.clientapi import ClientApi
from server.servereventhandler import ServerEventHandler

class ServerEventHandler_LobbyReady(ServerEventHandler):

    def handleEvent(self, client:ClientApi, eventData):

        client.toggleReady()
        pass
    
