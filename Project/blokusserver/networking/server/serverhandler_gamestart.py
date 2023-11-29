


from networking.server.clientapi import ClientApi

class ServerEventHandler_GameStart:

    def handleEvent(self, client:ClientApi, eventData):
        
        client.currentLobby.startGame(client)
        
        pass
    
