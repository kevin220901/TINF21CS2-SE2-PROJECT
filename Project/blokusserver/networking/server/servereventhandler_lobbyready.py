


from networking.server.clientapi import ClientApi
class ServerEventHandler_LobbyReady:

    def handleEvent(self, client:ClientApi, eventData):

        client.toggleReady()
        pass
    
