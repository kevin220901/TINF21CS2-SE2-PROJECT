

from networking.server.clientapi import ClientApi

class ServerEventHandler_LobbyLeave:

    def handleEvent(self, client:ClientApi, eventData):

        client.leaveLobby()
        pass
    
