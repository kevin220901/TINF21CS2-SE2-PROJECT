

from server.clientapi import ClientApi
from server.servereventhandler import ServerEventHandler

##################################################
## Author: Luis Eckert
##################################################

class ServerEventHandler_LobbyJoin(ServerEventHandler):
    
    def handleEvent(self, client:ClientApi, eventData):
        if 'lobbyId' not in eventData:
            client.sendSysMessage('invalid eventData: missing lobby id')
            return

        client.joinLobby(eventData['lobbyId']) 

        pass