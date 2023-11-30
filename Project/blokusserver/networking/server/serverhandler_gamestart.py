


from server.clientapi import ClientApi
from server.servereventhandler import ServerEventHandler

##################################################
## Author: Luis Eckert
##################################################

class ServerEventHandler_GameStart:

    def handleEvent(self, client:ClientApi, eventData):
        
        client.currentLobby.startGame(client)
        
        pass
    
